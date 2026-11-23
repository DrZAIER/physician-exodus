"""
Analysis pipeline for the Tunisian physician workforce model.

Outputs
-------
- retrospective calibration and hindcast diagnostics
- identifiability / flow-reconciliation analysis with an explicit consistency
  threshold and a destination-stock check
- policy scenario projections (central and alternative effect sizes)
- Monte Carlo uncertainty analysis with exact calibration
- true partial rank correlations (PRCC) and one-at-a-time sensitivity
- structural escalation on the post-entry margin only and on both margins
- break-even analysis between retention and training
- diaspora and graduate-output sensitivity
- illustrative cost per additional physician-year
- publication figures and tables
- a JSON and markdown summary of all numbers cited in the manuscript
"""

from __future__ import annotations

import json
import os
import platform
import sys
from dataclasses import replace

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import beta as beta_dist
from scipy.stats import pearsonr, rankdata, spearmanr

sys.path.insert(0, os.path.dirname(__file__))
from model import (  # noqa: E402
    AGES, BASE_SCENARIO, Params, graduates, mortality_hazard,
    retirement_hazard, simulate,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "processed")
OUT = os.path.join(ROOT, "outputs")
FIG = os.path.join(OUT, "figures")
TAB = os.path.join(OUT, "tables")
for d in (OUT, FIG, TAB):
    os.makedirs(d, exist_ok=True)

SEED = 20261121

# ---------------------------------------------------------------------------
# Observed data
# ---------------------------------------------------------------------------
stock = pd.read_csv(os.path.join(DATA, "tunisia_physician_workforce.csv"))
pop = pd.read_csv(os.path.join(DATA, "population_tunisia.csv"))
OBS = {int(y): int(v) for y, v in zip(stock.year, stock.physicians_total)}
OBS_2017_2024 = {y: OBS[y] for y in range(2017, 2025)}
POP = {int(y): int(v) for y, v in zip(pop.year, pop.population)}
CAL_YEARS = list(range(2017, 2025))
TARGET_2024 = OBS[2024]

# Data used only for the destination-stock consistency check
DESTINATION_STOCKS = {
    "France (2023)": 1591,
    "Germany (2022)": 881,
    "OECD country-of-birth lower bound (2015/16)": 4000,
}
OECD_LOWER_BOUND = 4000

# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------
# Central effect sizes. `emig_mult` scales post-entry emigration;
# `entry_retention` is the proportional reduction of PRE-ENTRY INTERNATIONAL
# emigration (phi times pipeline non-entry), not of all pipeline non-entry;
# `return_mult` scales the annual return rate; `train_mult` scales graduates
# from 2031.
SCENARIOS = {
    "BAU": dict(label="Business as usual", emig_mult=1.0, entry_retention=0.0,
                return_mult=1.0, train_mult=1.0),
    "REMUN": dict(label="Remuneration and working conditions",
                  emig_mult=0.70, entry_retention=0.30, return_mult=1.0,
                  train_mult=1.0),
    "CAREER": dict(label="Professional development and career pathways",
                   emig_mult=0.85, entry_retention=0.15, return_mult=1.0,
                   train_mult=1.0),
    "RETURN": dict(label="Return migration and diaspora reintegration",
                   emig_mult=1.0, entry_retention=0.0, return_mult=1.75,
                   train_mult=1.0),
    "TRAINING": dict(label="Expanded domestic training capacity",
                     emig_mult=1.0, entry_retention=0.0, return_mult=1.0,
                     train_mult=1.30),
    "COMBINED": dict(label="Combined retention and return strategy",
                     emig_mult=0.65, entry_retention=0.35, return_mult=1.75,
                     train_mult=1.0),
}

# Alternative effect sizes (low / high) for scenario uncertainty.
EFFECT_RANGE = {
    "BAU": [(1.0, 0.0, 1.0, 1.0), (1.0, 0.0, 1.0, 1.0)],
    "REMUN": [(0.85, 0.15, 1.0, 1.0), (0.55, 0.45, 1.0, 1.0)],
    "CAREER": [(0.92, 0.08, 1.0, 1.0), (0.75, 0.25, 1.0, 1.0)],
    "RETURN": [(1.0, 0.0, 1.35, 1.0), (1.0, 0.0, 2.50, 1.0)],
    "TRAINING": [(1.0, 0.0, 1.0, 1.15), (1.0, 0.0, 1.0, 1.50)],
    "COMBINED": [(0.78, 0.22, 1.35, 1.0), (0.55, 0.45, 2.50, 1.0)],
}

CENTRAL = Params(
    sigma=0.55, phi=0.50, g_scale=1.0, initial_stock_2008=12600,
    retire_shift=0.0, emig_tilt=1.0, rho=0.02, diaspora_attrition=0.08,
    return_retention=0.85, age_shape="uniform", mortality_mult=1.0,
)

# ---------------------------------------------------------------------------
# Illustrative cost assumptions (2025 Tunisian dinars, undiscounted)
# ---------------------------------------------------------------------------
COSTS = {
    "public_share": 6113 / 15315,
    "avg_public_compensation_tnd": 72_000,
    "remuneration_increment": 0.30,
    "career_cost_per_physician_year_tnd": 3_000,
    "training_cost_per_graduate_tnd": 250_000,
    "return_cost_per_migrant_tnd": 40_000,
    "unit_cost_low": 0.50,
    "unit_cost_high": 2.00,
}

COL = {
    "BAU": "#4D4D4D", "REMUN": "#1B7837", "CAREER": "#762A83",
    "RETURN": "#E08214", "TRAINING": "#2166AC", "COMBINED": "#B2182B",
}
LABELS = {
    "BAU": "Business as usual", "REMUN": "Remuneration / conditions",
    "CAREER": "Career development", "RETURN": "Return migration",
    "TRAINING": "Training expansion", "COMBINED": "Combined strategy",
}


def _scen_dict(key: str, effect=None) -> dict:
    s = SCENARIOS[key]
    if effect is None:
        return dict(emig_mult=s["emig_mult"],
                    entry_retention=s["entry_retention"],
                    return_mult=s["return_mult"],
                    train_mult=s["train_mult"], name=s["label"])
    e = effect
    return dict(emig_mult=e[0], entry_retention=e[1], return_mult=e[2],
                train_mult=e[3], name=s["label"])


# ---------------------------------------------------------------------------
# Calibration and fit
# ---------------------------------------------------------------------------
def calibrate_m(p: Params, target: float = TARGET_2024,
                m_max: float = 6000.0, xtol: float = 0.05) -> float:
    """Solve the post-entry emigration flow that reproduces the 2024 stock.

    Returns ``nan`` when the parameter combination cannot reach the target
    even with zero post-entry emigration. This is an informative exclusion,
    not a numerical failure.
    """
    def f(m):
        o = simulate(replace(p, m_base=m), end_year=2024)
        return o["stock"][-1] - target

    if f(0.0) < 0:
        return float("nan")
    if f(m_max) > 0:
        return float(m_max)
    return float(brentq(f, 0.0, m_max, xtol=xtol))


def history_fit(p: Params, o: dict) -> dict:
    years = list(o["years"])
    pred = np.array([o["stock"][years.index(y)] for y in CAL_YEARS])
    obs = np.array([OBS_2017_2024[y] for y in CAL_YEARS])
    mask = np.array([y not in (2020, 2021) for y in CAL_YEARS])
    early = np.array([y in (2017, 2018, 2019) for y in CAL_YEARS])
    late = np.array([y in (2022, 2023, 2024) for y in CAL_YEARS])
    return {
        "rmse": float(np.sqrt(np.mean((pred - obs) ** 2))),
        "rmse_excl_2020_21": float(np.sqrt(np.mean((pred[mask] - obs[mask]) ** 2))),
        "rmse_2017_2019": float(np.sqrt(np.mean((pred[early] - obs[early]) ** 2))),
        "rmse_2022_2024": float(np.sqrt(np.mean((pred[late] - obs[late]) ** 2))),
        "mape": float(np.mean(np.abs(pred - obs) / obs) * 100),
        "calibration_error": float(o["stock"][years.index(2024)] - TARGET_2024),
        "pred": dict(zip(CAL_YEARS, pred.round(0).astype(int).tolist())),
        "obs": OBS_2017_2024,
    }


def run_scenario(key: str, p: Params, effect=None, end_year: int = 2040) -> dict:
    return simulate(p, scenario=_scen_dict(key, effect), end_year=end_year)


def summarise(o: dict, base: dict | None = None, start: int = 2026,
              end: int = 2040) -> dict:
    years = list(o["years"])
    i = lambda y: years.index(y)  # noqa: E731
    mask = np.array([(y >= start) and (y <= end) for y in years])
    res = {
        "stock_2024": float(o["stock"][i(2024)]),
        "stock_2030": float(o["stock"][i(2030)]),
        "stock_2035": float(o["stock"][i(2035)]),
        "stock_2040": float(o["stock"][i(2040)]),
        "density_2024": float(o["stock"][i(2024)] / POP[2024] * 1000),
        "density_2040": float(o["stock"][i(2040)] / POP[2040] * 1000),
        "cum_emigration": float(np.sum((o["emig_pre"] + o["emig_post"])[mask])),
        "cum_emig_pre": float(np.sum(o["emig_pre"][mask])),
        "cum_emig_post": float(np.sum(o["emig_post"][mask])),
        "cum_nonentry": float(np.sum(o["nonentry_total"][mask])),
        "cum_nonentry_domestic": float(np.sum(o["nonentry_domestic"][mask])),
        "cum_returns": float(np.sum(o["returns_net"][mask])),
        "cum_retirements": float(np.sum(o["retirements"][mask])),
        "emigration_2024": float((o["emig_pre"] + o["emig_post"])[i(2024)]),
        "emig_pre_2024": float(o["emig_pre"][i(2024)]),
        "emig_post_2024": float(o["emig_post"][i(2024)]),
        "nonentry_2024": float(o["nonentry_total"][i(2024)]),
        "nonentry_domestic_2024": float(o["nonentry_domestic"][i(2024)]),
        "returns_2024": float(o["returns_net"][i(2024)]),
        "diaspora_2024": float(o["diaspora"][i(2024)]),
        "diaspora_2040": float(o["diaspora"][i(2040)]),
        "cap_binding_any": bool(np.any(o["cap_binding"] > 0)),
        "max_emig_hazard": float(np.max(o["emig_hazard_max"])),
        "pipe_nonentry_share_2024": float(o["pipe_nonentry_share"][i(2024)]),
        "pre_emig_share_2024": float(o["pre_emig_share"][i(2024)]),
    }
    if base is not None:
        diff = (o["stock"] - base["stock"])[mask]
        res["physician_years"] = float(np.sum(diff))
        res["stock_diff_2040"] = float(o["stock"][i(2040)] - base["stock"][i(2040)])
    return res


# ---------------------------------------------------------------------------
# 1. Central calibration
# ---------------------------------------------------------------------------
def run_central() -> dict:
    m = calibrate_m(CENTRAL)
    if np.isnan(m):
        raise RuntimeError("Central parameters cannot reproduce the 2024 stock.")
    p = replace(CENTRAL, m_base=m)
    hist = simulate(p, end_year=2024)
    base = simulate(p, end_year=2040)

    out = {
        "params_central": {
            "sigma": p.sigma, "phi": p.phi, "g_scale": p.g_scale, "m_base": m,
            "rho": p.rho, "retire_shift": p.retire_shift,
            "initial_stock_2008": p.initial_stock_2008,
            "diaspora_attrition": p.diaspora_attrition,
            "return_retention": p.return_retention,
            "age_shape": p.age_shape, "mortality_mult": p.mortality_mult,
        },
        "fit": history_fit(p, hist),
        "bau": summarise(base),
        "scenarios": {},
    }

    for k in SCENARIOS:
        o = run_scenario(k, p)
        out["scenarios"][k] = summarise(o, base)

        lo, hi = EFFECT_RANGE[k]
        out["scenarios"][k]["stock_2040_low"] = summarise(
            run_scenario(k, p, lo), base)["stock_2040"]
        out["scenarios"][k]["stock_2040_high"] = summarise(
            run_scenario(k, p, hi), base)["stock_2040"]
        out["scenarios"][k]["py_low"] = summarise(
            run_scenario(k, p, lo), base)["physician_years"]
        out["scenarios"][k]["py_high"] = summarise(
            run_scenario(k, p, hi), base)["physician_years"]

        # Same scenario with escalation on the post-entry margin only and
        # on both margins. These are distinct structural assumptions.
        for mode, kw in (
            ("post", dict(emig_growth_post=0.03, emig_growth_pre=0.0)),
            ("both", dict(emig_growth_post=0.03, emig_growth_pre=0.03)),
        ):
            pe = replace(p, **kw)
            oe = run_scenario(k, pe)
            base_e = simulate(pe, end_year=2040)
            out["scenarios"][k][f"stock_2040_escalating_{mode}"] = summarise(oe)["stock_2040"]
            out["scenarios"][k][f"py_escalating_{mode}"] = summarise(oe, base_e)["physician_years"]

    # Trajectories
    traj = {"years": base["years"].tolist(), "BAU": base["stock"].tolist()}
    for k in SCENARIOS:
        if k == "BAU":
            continue
        traj[k] = run_scenario(k, p)["stock"].tolist()
    out["trajectories"] = traj

    # Age structure
    bins = [(25, 34), (35, 44), (45, 54), (55, 64), (65, 75)]
    def _shares(d):
        return {f"{a}-{b}": float(d[(AGES >= a) & (AGES <= b)].sum() / d.sum() * 100)
                for a, b in bins}
    hist24 = simulate(p, end_year=2024)
    c40 = run_scenario("COMBINED", p)
    out["age_structure"] = {
        "2024": _shares(hist24["age_dist"][2024]),
        "2040_BAU": _shares(base["age_dist"][2040]),
        "2040_COMBINED": _shares(c40["age_dist"][2040]),
    }
    out["observed"] = {int(k): int(v) for k, v in OBS.items()}
    out["population"] = {int(k): int(v) for k, v in POP.items()}
    return out


# ---------------------------------------------------------------------------
# 2. Identifiability and destination-stock consistency
# ---------------------------------------------------------------------------
def run_identifiability() -> dict:
    sigmas = np.round(np.arange(0.20, 0.801, 0.025), 3)
    gscales = np.round(np.arange(0.80, 1.601, 0.025), 3)
    rows = []
    for gs in gscales:
        for s in sigmas:
            p = replace(CENTRAL, sigma=float(s), g_scale=float(gs))
            m = calibrate_m(p)
            if np.isnan(m):
                rows.append({
                    "sigma": float(s), "g_scale": float(gs), "m_base": np.nan,
                    "rmse": np.nan, "emig_post_2024": np.nan,
                    "emig_pre_2024": np.nan, "emig_total_2024": np.nan,
                    "nonentry_2024": np.nan, "emig_total_phi1_2024": np.nan,
                    "entry_2024": np.nan, "diaspora_2024": np.nan,
                    "diaspora_2040": np.nan, "feasible": False,
                })
                continue
            pp = replace(p, m_base=m)
            o = simulate(pp, end_year=2040)
            fit = history_fit(pp, simulate(pp, end_year=2024))
            i24 = list(o["years"]).index(2024)
            rows.append({
                "sigma": float(s), "g_scale": float(gs), "m_base": float(m),
                "rmse": fit["rmse"],
                "emig_post_2024": float(o["emig_post"][i24]),
                "emig_pre_2024": float(o["emig_pre"][i24]),
                "emig_total_2024": float(o["emig_post"][i24] + o["emig_pre"][i24]),
                "nonentry_2024": float(o["nonentry_total"][i24]),
                "emig_total_phi1_2024": float(o["emig_post"][i24]
                                              + o["nonentry_total"][i24]),
                "entry_2024": float(o["entries"][i24]),
                "diaspora_2024": float(o["diaspora"][i24]),
                "diaspora_2040": float(o["diaspora"][-1]),
                "feasible": True,
            })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(TAB, "identifiability_grid.csv"), index=False)

    feas = df[df.feasible].copy()
    best = feas.loc[feas.rmse.idxmin()]
    # Two thresholds are reported. The strict threshold is within 10% of the
    # best RMSE. The acceptable threshold is an RMSE of 2% of the mean observed
    # stock (about 300 physicians), which is the fit quality the historical
    # comparison can support. The central calibration is inside the acceptable
    # set but outside the strict set; both are reported.
    strict_threshold = 1.10 * best.rmse
    acceptable_threshold = 0.02 * float(np.mean(list(OBS_2017_2024.values())))
    consistent = feas[feas.rmse <= acceptable_threshold].copy()
    strict = feas[feas.rmse <= strict_threshold].copy()
    dest_ok = feasible_destination_check(consistent)

    summary = {
        "best": {
            "sigma": float(best.sigma), "g_scale": float(best.g_scale),
            "m_base": float(best.m_base), "rmse": float(best.rmse),
            "emig_total_2024": float(best.emig_total_2024),
            "emig_total_phi1_2024": float(best.emig_total_phi1_2024),
            "nonentry_2024": float(best.nonentry_2024),
            "diaspora_2024": float(best.diaspora_2024),
        },
        "phi": float(CENTRAL.phi),
        "threshold_rmse": float(acceptable_threshold),
        "strict_threshold_rmse": float(strict_threshold),
        "strict_n": int(len(strict)),
        "strict_emig_range": [float(strict.emig_total_2024.min()),
                              float(strict.emig_total_2024.max())],
        "strict_emig_phi1_range": [float(strict.emig_total_phi1_2024.min()),
                                   float(strict.emig_total_phi1_2024.max())],
        "strict_sigma_range": [float(strict.sigma.min()), float(strict.sigma.max())],
        "strict_g_range": [float(strict.g_scale.min()), float(strict.g_scale.max())],
        "consistent_n": int(len(consistent)),
        "consistent_emig_range": [float(consistent.emig_total_2024.min()),
                                  float(consistent.emig_total_2024.max())],
        "consistent_emig_phi1_range": [float(consistent.emig_total_phi1_2024.min()),
                                       float(consistent.emig_total_phi1_2024.max())],
        "consistent_nonentry_range": [float(consistent.nonentry_2024.min()),
                                      float(consistent.nonentry_2024.max())],
        "consistent_sigma_range": [float(consistent.sigma.min()),
                                   float(consistent.sigma.max())],
        "consistent_g_range": [float(consistent.g_scale.min()),
                               float(consistent.g_scale.max())],
        "consistent_diaspora_range": [float(consistent.diaspora_2024.min()),
                                      float(consistent.diaspora_2024.max())],
        "all_emig_range": [float(feas.emig_total_2024.min()),
                           float(feas.emig_total_2024.max())],
        "all_emig_phi1_range": [float(feas.emig_total_phi1_2024.min()),
                                float(feas.emig_total_phi1_2024.max())],
        "all_rmse_range": [float(feas.rmse.min()), float(feas.rmse.max())],
        "destination_consistent_n": int(len(dest_ok)),
        "destination_consistent_emig_range": [
            float(dest_ok.emig_total_2024.min()),
            float(dest_ok.emig_total_2024.max())] if len(dest_ok) else None,
        "destination_consistent_emig_phi1_range": [
            float(dest_ok.emig_total_phi1_2024.min()),
            float(dest_ok.emig_total_phi1_2024.max())] if len(dest_ok) else None,
        "destination_consistent_diaspora_range": [
            float(dest_ok.diaspora_2024.min()),
            float(dest_ok.diaspora_2024.max())] if len(dest_ok) else None,
        "destination_stocks": DESTINATION_STOCKS,
        "oecd_lower_bound": OECD_LOWER_BOUND,
    }
    return summary


def feasible_destination_check(df: pd.DataFrame,
                               low: float = 4000.0,
                               high: float = 10000.0) -> pd.DataFrame:
    """Rows whose 2024 return-eligible pool falls in a plausible band.

    The band runs from the OECD country-of-birth lower bound to 2.5 times that
    bound, allowing for non-OECD destinations and unregistered physicians. It
    is a consistency screen, not an estimate.
    """
    return df[(df.diaspora_2024 >= low) & (df.diaspora_2024 <= high)]


# ---------------------------------------------------------------------------
# 3. Monte Carlo uncertainty
# ---------------------------------------------------------------------------
def _truncated_beta(rng, mean, sd, lo, hi):
    k = mean * (1 - mean) / sd ** 2 - 1
    for _ in range(1000):
        v = float(beta_dist.rvs(mean * k, (1 - mean) * k, random_state=rng))
        if lo <= v <= hi:
            return v
    return float(np.clip(mean, lo, hi))


def _truncated_lognormal(rng, log_sd, lo, hi, median=1.0):
    for _ in range(1000):
        v = float(median * np.exp(rng.normal(0, log_sd)))
        if lo <= v <= hi:
            return v
    return float(np.clip(median, lo, hi))


def draw_params(rng: np.random.Generator) -> Params:
    """Draw structural parameters from priors that cover the identified range."""
    sigma = _truncated_beta(rng, 0.55, 0.12, 0.30, 0.80)
    gs = _truncated_lognormal(rng, 0.20, 0.85, 1.50)
    phi = float(rng.uniform(0.25, 0.75))
    tilt = _truncated_lognormal(rng, 0.15, 0.60, 1.60)
    shift = float(rng.uniform(-1.5, 1.5))
    rho = _truncated_beta(rng, 0.020, 0.010, 0.005, 0.050)
    delta = float(rng.uniform(0.04, 0.12))
    retention = float(rng.uniform(0.75, 0.95))
    init = float(np.clip(rng.normal(12600, 400), 11300, 13900))
    init_d = float(np.clip(4000 * np.exp(rng.normal(0, 0.30)), 2000, 8000))
    future = _truncated_lognormal(rng, 0.10, 0.70, 1.40)
    mort = float(rng.uniform(0.8, 1.2))
    return Params(
        sigma=sigma, phi=phi, g_scale=gs, emig_tilt=tilt, retire_shift=shift,
        rho=rho, diaspora_attrition=delta, return_retention=retention,
        initial_stock_2008=init, initial_diaspora_2008=init_d,
        emig_future_mult=future, mortality_mult=mort,
    )


def run_mc(n: int = 2000, seed: int = SEED) -> tuple[pd.DataFrame, dict]:
    rng = np.random.default_rng(seed)
    draws = []
    traj = []
    calibration_errors = []
    attempts = 0
    while len(draws) < n:
        attempts += 1
        if attempts > n * 20:
            raise RuntimeError("Too many infeasible parameter draws.")
        p0 = draw_params(rng)
        m = calibrate_m(p0)
        if np.isnan(m):
            continue
        p = replace(p0, m_base=m)
        base = simulate(p, end_year=2040)
        calibration_errors.append(base["stock"][list(base["years"]).index(2024)]
                                  - TARGET_2024)
        traj.append(base["stock"])
        rec = {"draw": len(draws), "sigma": p.sigma, "phi": p.phi,
               "g_scale": p.g_scale, "m_base": p.m_base, "rho": p.rho,
               "retire_shift": p.retire_shift, "emig_tilt": p.emig_tilt,
               "initial_stock_2008": p.initial_stock_2008,
               "initial_diaspora_2008": p.initial_diaspora_2008,
               "diaspora_attrition": p.diaspora_attrition,
               "return_retention": p.return_retention,
               "mortality_mult": p.mortality_mult,
               "emig_future_mult": p.emig_future_mult,
               "calibration_error": calibration_errors[-1]}
        rec.update({f"bau_{k}": v for k, v in summarise(base).items()})
        rec["emig_total_2024"] = rec["bau_emigration_2024"]
        for key in SCENARIOS:
            if key == "BAU":
                continue
            o = run_scenario(key, p)
            s = summarise(o, base)
            rec[f"{key}_stock_2040"] = s["stock_2040"]
            rec[f"{key}_py"] = s["physician_years"]
            rec[f"{key}_cum_emig"] = s["cum_emigration"]
            rec[f"{key}_cum_ret"] = s["cum_returns"]
        draws.append(rec)

    df = pd.DataFrame(draws)
    df.to_csv(os.path.join(OUT, "mc_draws.csv"), index=False)
    traj = np.asarray(traj)
    traj_q = {
        "years": base["years"].tolist(),
        "q05": np.quantile(traj, 0.05, axis=0).tolist(),
        "q50": np.quantile(traj, 0.50, axis=0).tolist(),
        "q95": np.quantile(traj, 0.95, axis=0).tolist(),
    }
    diagnostics = {
        "attempts": attempts,
        "accepted": len(df),
        "max_abs_calibration_error": float(np.max(np.abs(calibration_errors))),
        "trajectory_quantiles": traj_q,
    }
    return df, diagnostics


def summarise_mc(df: pd.DataFrame, diagnostics: dict) -> dict:
    def q(s):
        return {"median": float(s.median()), "lo": float(s.quantile(0.05)),
                "hi": float(s.quantile(0.95)), "p25": float(s.quantile(0.25)),
                "p75": float(s.quantile(0.75))}

    out = {"n": int(len(df)), "diagnostics": diagnostics}
    for c in ["bau_stock_2024", "bau_stock_2030", "bau_stock_2035", "bau_stock_2040",
              "bau_density_2040", "bau_cum_emigration", "bau_cum_returns",
              "bau_diaspora_2024", "bau_diaspora_2040", "bau_nonentry_2024",
              "bau_emig_pre_2024", "bau_emig_post_2024", "emig_total_2024",
              "m_base", "phi", "initial_diaspora_2008"]:
        out[c] = q(df[c])
    for key in SCENARIOS:
        if key == "BAU":
            continue
        out[f"{key}_stock_2040"] = q(df[f"{key}_stock_2040"])
        out[f"{key}_py"] = q(df[f"{key}_py"])
    out["prob_bau_below_2024"] = float((df["bau_stock_2040"] < df["bau_stock_2024"]).mean())
    out["prob_bau_above_2024"] = 1.0 - out["prob_bau_below_2024"]
    cols = ["REMUN_stock_2040", "CAREER_stock_2040", "RETURN_stock_2040",
            "TRAINING_stock_2040", "COMBINED_stock_2040"]
    X = df[cols].values
    out["rank_combined_first"] = float((X.argmax(axis=1) == 4).mean())
    out["rank_training_last"] = float((X.argmin(axis=1) == 3).mean())
    out["rank_return_last"] = float((X.argmin(axis=1) == 2).mean())
    out["prob_combined_above_bau"] = float((df["COMBINED_stock_2040"] > df["bau_stock_2040"]).mean())
    out["prob_training_above_bau"] = float((df["TRAINING_stock_2040"] > df["bau_stock_2040"]).mean())
    out["prob_return_above_training"] = float((df["RETURN_stock_2040"] > df["TRAINING_stock_2040"]).mean())
    out["prob_career_above_training"] = float((df["CAREER_stock_2040"] > df["TRAINING_stock_2040"]).mean())
    out["prob_remun_above_training"] = float((df["REMUN_stock_2040"] > df["TRAINING_stock_2040"]).mean())

    # Full rank distribution: rank 1 = highest 2040 workforce.
    ranking = (-X).argsort(axis=1).argsort(axis=1) + 1
    rank_names = ["REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"]
    out["rank_distribution"] = {
        name: [float((ranking[:, i] == r).mean()) for r in range(1, 6)]
        for i, name in enumerate(rank_names)
    }
    return out


# ---------------------------------------------------------------------------
# 4. Sensitivity: true PRCC, marginal Spearman, one-at-a-time tornado
# ---------------------------------------------------------------------------
SENS_PARAMS = ["sigma", "phi", "g_scale", "emig_future_mult", "rho",
               "retire_shift", "emig_tilt", "initial_stock_2008",
               "initial_diaspora_2008", "diaspora_attrition",
               "return_retention", "mortality_mult"]


def _rank_residual(x: np.ndarray, controls: list[np.ndarray]) -> np.ndarray:
    rx = rankdata(x)
    if not controls:
        return rx - rx.mean()
    R = np.column_stack([np.ones(len(rx))] + [rankdata(c) for c in controls])
    beta, *_ = np.linalg.lstsq(R, rx, rcond=None)
    return rx - R @ beta


def partial_rank_correlation(x, y, controls):
    rx = _rank_residual(np.asarray(x), [np.asarray(c) for c in controls])
    ry = _rank_residual(np.asarray(y), [np.asarray(c) for c in controls])
    r, p = pearsonr(rx, ry)
    return float(r), float(p)


def run_sensitivity(df: pd.DataFrame) -> dict:
    y = df["bau_stock_2040"].values
    prcc, prcc_p, marginal = {}, {}, {}
    for p in SENS_PARAMS:
        ctrl = [df[c].values for c in SENS_PARAMS if c != p]
        prcc[p], prcc_p[p] = partial_rank_correlation(df[p].values, y, ctrl)
        marginal[p] = float(spearmanr(df[p].values, y).statistic)

    # OAT tornado around the central calibration. For m_base, the calibrated
    # flow is varied directly (structural) rather than recalibrated, because
    # recalibration would mechanically remove its effect.
    m0 = calibrate_m(CENTRAL)
    p0 = replace(CENTRAL, m_base=m0)
    base = simulate(p0, end_year=2040)["stock"][-1]
    tornado = {}
    for p in SENS_PARAMS + ["m_base"]:
        if p == "m_base":
            lo, hi = df[p].quantile(0.10), df[p].quantile(0.90)
            res = {"low": float(simulate(replace(p0, m_base=float(lo)),
                                         end_year=2040)["stock"][-1] - base),
                   "high": float(simulate(replace(p0, m_base=float(hi)),
                                          end_year=2040)["stock"][-1] - base),
                   "low_value": float(lo), "high_value": float(hi),
                   "recalibrated": False}
        else:
            lo, hi = df[p].quantile(0.10), df[p].quantile(0.90)
            res = {"low": None, "high": None, "low_value": float(lo),
                   "high_value": float(hi), "recalibrated": True}
            for lab, v in (("low", lo), ("high", hi)):
                pp = replace(p0, **{p: float(v)})
                mm = calibrate_m(pp)
                if np.isnan(mm):
                    res[lab] = np.nan
                else:
                    res[lab] = float(simulate(replace(pp, m_base=mm),
                                              end_year=2040)["stock"][-1] - base)
        tornado[p] = res
    return {"prcc": prcc, "prcc_p": prcc_p, "marginal_spearman": marginal,
            "tornado": tornado, "base_2040": float(base)}


# ---------------------------------------------------------------------------
# 5. Structural escalation: post-entry only vs both margins
# ---------------------------------------------------------------------------
def run_structural(central: dict) -> dict:
    p = replace(CENTRAL, m_base=central["params_central"]["m_base"])
    out = {}
    for mode in ("post", "both"):
        for g in (0.0, 0.03, 0.05, 0.07):
            pp = replace(
                p,
                emig_growth_post=g if mode in ("post", "both") else 0.0,
                emig_growth_pre=g if mode in ("both",) else 0.0,
            )
            b = simulate(pp, end_year=2040)
            s = summarise(b)
            s["trajectory"] = b["stock"].tolist()
            s["years"] = b["years"].tolist()
            s["scenario_2040"] = {}
            s["scenario_py"] = {}
            for k in ("REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"):
                o = run_scenario(k, pp)
                s["scenario_2040"][k] = summarise(o)["stock_2040"]
                s["scenario_py"][k] = summarise(o, b)["physician_years"]
            out[f"{mode}_{g:.2f}"] = s

    rows = []
    for key, s in out.items():
        mode, g = key.split("_")
        rows.append([mode, float(g), s["stock_2030"], s["stock_2040"],
                     s["density_2040"], s["cum_emigration"]]
                    + [s["scenario_2040"][k] for k in
                       ("REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED")])
    pd.DataFrame(rows, columns=[
        "Margin", "Annual growth", "Workforce 2030", "Workforce 2040",
        "Density 2040", "Cumulative emigration",
        "Remuneration 2040", "Career 2040", "Return 2040", "Training 2040",
        "Combined 2040"]).to_csv(
        os.path.join(TAB, "structural_escalation.csv"), index=False)
    return out


# ---------------------------------------------------------------------------
# 6. Break-even analysis: retention vs training
# ---------------------------------------------------------------------------
def run_breakeven(central: dict) -> dict:
    p = replace(CENTRAL, m_base=central["params_central"]["m_base"])
    rs = np.round(np.arange(0.0, 0.501, 0.01), 2)
    ts = np.round(np.arange(0.0, 1.001, 0.01), 2)
    grid = np.zeros((len(ts), len(rs)))
    for i, t in enumerate(ts):
        for j, r in enumerate(rs):
            o = simulate(p, scenario=dict(
                emig_mult=1.0 - r, entry_retention=r, return_mult=1.0,
                train_mult=1.0 + t), end_year=2040)
            grid[i, j] = o["stock"][-1]
    pd.DataFrame(grid, index=[f"{t:.2f}" for t in ts],
                 columns=[f"{r:.2f}" for r in rs]).to_csv(
        os.path.join(TAB, "breakeven_grid.csv"))

    # Retention-only row (training = 0) and training-only column
    # (retention = 0). The break-even is the retention effect whose 2040
    # workforce equals the 30%-training-only workforce, and vice versa.
    i0, i30 = int(np.argmin(np.abs(ts - 0.0))), int(np.argmin(np.abs(ts - 0.30)))
    j0, j30 = int(np.argmin(np.abs(rs - 0.0))), int(np.argmin(np.abs(rs - 0.30)))
    retention_only = grid[i0, :]
    training_only = grid[:, j0]
    stock_training_30 = float(grid[i30, j0])   # r = 0, t = 0.30
    stock_retention_30 = float(grid[i0, j30])  # r = 0.30, t = 0
    r_match = float(np.interp(stock_training_30, retention_only, rs))
    t_match = float(np.interp(stock_retention_30, training_only, ts))

    return {
        "retention_match_30pct_training": r_match,
        "training_match_30pct_retention": t_match,
        "stock_training_30": stock_training_30,
        "stock_retention_30": stock_retention_30,
        "bau_2040": float(grid[0, 0]),
        "grid_rows": len(ts), "grid_cols": len(rs),
    }


# ---------------------------------------------------------------------------
# 7. Diaspora sensitivity
# ---------------------------------------------------------------------------
def run_diaspora_sensitivity(central: dict) -> dict:
    rows = []
    for delta in (0.02, 0.04, 0.06, 0.08, 0.10, 0.15):
        for d0 in (2000, 4000, 6000, 8000):
            for rho in (0.005, 0.010, 0.020, 0.030, 0.040):
                p0 = replace(CENTRAL, diaspora_attrition=delta,
                             initial_diaspora_2008=d0, rho=rho)
                m = calibrate_m(p0)
                if np.isnan(m):
                    continue
                p = replace(p0, m_base=m)
                b = simulate(p, end_year=2040)
                r = simulate(p, scenario=_scen_dict("RETURN"), end_year=2040)
                rows.append({
                    "diaspora_attrition": delta,
                    "initial_diaspora_2008": d0,
                    "rho": rho,
                    "m_base": m,
                    "diaspora_2024": b["diaspora"][list(b["years"]).index(2024)],
                    "bau_2040": b["stock"][-1],
                    "return_2040": r["stock"][-1],
                    "return_diff_2040": r["stock"][-1] - b["stock"][-1],
                    "eventual_return_prob": rho / (rho + delta),
                })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(TAB, "diaspora_sensitivity.csv"), index=False)
    central_row = df[(df.diaspora_attrition == 0.08)
                     & (df.initial_diaspora_2008 == 4000)
                     & (df.rho == 0.020)].iloc[0]
    return {
        "central": central_row.to_dict(),
        "return_diff_range": [float(df.return_diff_2040.min()),
                              float(df.return_diff_2040.max())],
        "diaspora_2024_range": [float(df.diaspora_2024.min()),
                                float(df.diaspora_2024.max())],
        "eventual_return_range": [float(df.eventual_return_prob.min()),
                                  float(df.eventual_return_prob.max())],
    }


# ---------------------------------------------------------------------------
# 8. Alternative graduate-output baselines
# ---------------------------------------------------------------------------
def run_graduate_baselines(central: dict) -> dict:
    m = central["params_central"]["m_base"]
    rows = []
    out = {}
    for path in ("baseline", "continued_growth", "constant_1900"):
        p = replace(CENTRAL, m_base=m, grad_path=path)
        b = simulate(p, end_year=2040)
        r = simulate(p, scenario=_scen_dict("REMUN"), end_year=2040)
        t = simulate(p, scenario=_scen_dict("TRAINING"), end_year=2040)
        c = simulate(p, scenario=_scen_dict("COMBINED"), end_year=2040)
        out[path] = {
            "bau_2040": summarise(b)["stock_2040"],
            "remun_2040": summarise(r)["stock_2040"],
            "training_2040": summarise(t)["stock_2040"],
            "combined_2040": summarise(c)["stock_2040"],
            "training_py": summarise(t, b)["physician_years"],
            "combined_py": summarise(c, b)["physician_years"],
            "graduates_2040": float(graduates(2040, path=path)),
        }
        rows.append([path, out[path]["graduates_2040"],
                     out[path]["bau_2040"], out[path]["training_2040"],
                     out[path]["combined_2040"], out[path]["training_py"],
                     out[path]["combined_py"]])
    pd.DataFrame(rows, columns=[
        "Graduate path", "Graduates 2040", "BAU 2040", "Training 2040",
        "Combined 2040", "Training physician-years", "Combined physician-years"
    ]).to_csv(os.path.join(TAB, "graduate_baselines.csv"), index=False)
    return out


# ---------------------------------------------------------------------------
# 8b. Structural sensitivity: phi, lag, age shape, retirement/mortality
# ---------------------------------------------------------------------------
def retention_match_for_training(p: Params, train_mult: float = 1.30) -> float:
    """Retention reduction that matches a training expansion in 2040."""
    target = simulate(
        p, scenario=dict(emig_mult=1.0, entry_retention=0.0,
                         return_mult=1.0, train_mult=train_mult),
        end_year=2040)["stock"][-1]

    def f(r):
        o = simulate(p, scenario=dict(
            emig_mult=1.0 - r, entry_retention=r, return_mult=1.0,
            train_mult=1.0), end_year=2040)
        return o["stock"][-1] - target

    if f(0.0) >= 0:
        return 0.0
    if f(0.50) <= 0:
        return float("nan")
    return float(brentq(f, 0.0, 0.50, xtol=1e-4))


def _recalibrate(p: Params) -> Params | None:
    m = calibrate_m(p)
    if np.isnan(m):
        return None
    return replace(p, m_base=m)


def run_phi_sensitivity(central: dict) -> dict:
    rows = []
    out = {}
    for phi in (0.0, 0.25, 0.50, 0.75, 1.0):
        p = _recalibrate(replace(CENTRAL, phi=phi))
        if p is None:
            continue
        b = simulate(p, end_year=2040)
        sb = summarise(b)
        scen = {}
        for k in ("REMUN", "RETURN", "TRAINING", "COMBINED"):
            scen[k] = summarise(run_scenario(k, p), b)
        rm = retention_match_for_training(p)
        out[str(phi)] = {
            "phi": phi, "m_base": p.m_base, "bau": sb,
            "scenarios": scen, "retention_match": rm,
        }
        rows.append([
            phi, p.m_base, sb["emigration_2024"], sb["nonentry_2024"],
            sb["diaspora_2024"], sb["stock_2040"],
            scen["REMUN"]["stock_2040"], scen["RETURN"]["stock_2040"],
            scen["TRAINING"]["stock_2040"], scen["COMBINED"]["stock_2040"],
            scen["COMBINED"]["physician_years"], rm,
        ])
    pd.DataFrame(rows, columns=[
        "phi", "Calibrated post-entry flow", "International emigration 2024",
        "Pipeline non-entry 2024", "Return-eligible pool 2024", "BAU 2040",
        "Remuneration 2040", "Return 2040", "Training 2040", "Combined 2040",
        "Combined physician-years", "Retention match for 30% training"
    ]).to_csv(os.path.join(TAB, "phi_sensitivity.csv"), index=False)
    return out


def run_lag_sensitivity(central: dict) -> dict:
    rows = []
    out = {}
    for lag in (3, 4, 5, 6, 7):
        p = _recalibrate(replace(CENTRAL, entry_lag=lag))
        if p is None:
            continue
        b = simulate(p, end_year=2040)
        t = run_scenario("TRAINING", p)
        c = run_scenario("COMBINED", p)
        out[str(lag)] = {
            "lag": lag, "m_base": p.m_base,
            "bau_2040": summarise(b)["stock_2040"],
            "training_2040": summarise(t)["stock_2040"],
            "combined_2040": summarise(c)["stock_2040"],
            "training_py": summarise(t, b)["physician_years"],
            "combined_py": summarise(c, b)["physician_years"],
            "retention_match": retention_match_for_training(p),
        }
        rows.append([lag, p.m_base, out[str(lag)]["bau_2040"],
                     out[str(lag)]["training_2040"],
                     out[str(lag)]["combined_2040"],
                     out[str(lag)]["training_py"], out[str(lag)]["combined_py"],
                     out[str(lag)]["retention_match"]])
    pd.DataFrame(rows, columns=[
        "Postgraduate lag (years)", "Calibrated post-entry flow", "BAU 2040",
        "Training 2040", "Combined 2040", "Training physician-years",
        "Combined physician-years", "Retention match for 30% training"
    ]).to_csv(os.path.join(TAB, "lag_sensitivity.csv"), index=False)
    return out


def run_age_shape_sensitivity(central: dict) -> dict:
    rows = []
    out = {}
    for shape in ("uniform", "young", "old"):
        p = _recalibrate(replace(CENTRAL, age_shape=shape))
        if p is None:
            continue
        b = simulate(p, end_year=2040)
        t = run_scenario("TRAINING", p)
        c = run_scenario("COMBINED", p)
        out[shape] = {
            "shape": shape, "m_base": p.m_base,
            "bau_2040": summarise(b)["stock_2040"],
            "training_2040": summarise(t)["stock_2040"],
            "combined_2040": summarise(c)["stock_2040"],
            "training_py": summarise(t, b)["physician_years"],
            "combined_py": summarise(c, b)["physician_years"],
            "retention_match": retention_match_for_training(p),
        }
        rows.append([shape, p.m_base, out[shape]["bau_2040"],
                     out[shape]["training_2040"], out[shape]["combined_2040"],
                     out[shape]["training_py"], out[shape]["combined_py"],
                     out[shape]["retention_match"]])
    pd.DataFrame(rows, columns=[
        "Initial age shape", "Calibrated post-entry flow", "BAU 2040",
        "Training 2040", "Combined 2040", "Training physician-years",
        "Combined physician-years", "Retention match for 30% training"
    ]).to_csv(os.path.join(TAB, "age_shape_sensitivity.csv"), index=False)
    return out


def run_retirement_sensitivity(central: dict) -> dict:
    rows = []
    out = {}
    for shift in (-2.0, -1.5, 0.0, 1.5, 2.0):
        for mort in (0.5, 1.0, 1.5):
            p = _recalibrate(replace(CENTRAL, retire_shift=shift,
                                     mortality_mult=mort))
            if p is None:
                continue
            b = simulate(p, end_year=2040)
            c = run_scenario("COMBINED", p)
            out[f"{shift:.1f}_{mort:.1f}"] = {
                "retire_shift": shift, "mortality_mult": mort,
                "m_base": p.m_base,
                "bau_2040": summarise(b)["stock_2040"],
                "combined_2040": summarise(c)["stock_2040"],
                "combined_py": summarise(c, b)["physician_years"],
            }
            rows.append([shift, mort, p.m_base, out[f"{shift:.1f}_{mort:.1f}"]["bau_2040"],
                         out[f"{shift:.1f}_{mort:.1f}"]["combined_2040"],
                         out[f"{shift:.1f}_{mort:.1f}"]["combined_py"]])
    pd.DataFrame(rows, columns=[
        "Retirement shift (years)", "Mortality multiplier",
        "Calibrated post-entry flow", "BAU 2040", "Combined 2040",
        "Combined physician-years"
    ]).to_csv(os.path.join(TAB, "retirement_sensitivity.csv"), index=False)
    return out


# ---------------------------------------------------------------------------
# 9. Illustrative cost per additional physician-year
# ---------------------------------------------------------------------------
def _scenario_costs(key: str, o: dict, base: dict,
                    mult: float = 1.0) -> tuple[float, float]:
    """Return (fiscal transfer, real resource cost) for a scenario.

    Fiscal transfers are payments (primarily public-sector pay increments) that
    redistribute resources but are not a resource cost to the economy. Real
    resource costs are training, career-development and return-programme costs.
    Both are illustrative and undiscounted.
    """
    years = list(o["years"])
    mask = np.array([(y >= 2026) and (y <= 2040) for y in years])
    stock_years = np.sum(o["stock"][mask])
    public_stock_years = stock_years * COSTS["public_share"]

    if key == "BAU":
        return 0.0, 0.0
    if key == "REMUN":
        fiscal = (public_stock_years * COSTS["avg_public_compensation_tnd"]
                  * COSTS["remuneration_increment"] * mult)
        return fiscal, 0.0
    if key == "CAREER":
        return 0.0, (stock_years
                     * COSTS["career_cost_per_physician_year_tnd"] * mult)
    if key == "RETURN":
        extra_returns = max(0.0, np.sum(o["returns_net"][mask])
                            - np.sum(base["returns_net"][mask]))
        return 0.0, extra_returns * COSTS["return_cost_per_migrant_tnd"] * mult
    if key == "TRAINING":
        path = CENTRAL.grad_path
        extra_grads = sum(
            graduates(y, train_mult=1.30, path=path)
            - graduates(y, train_mult=1.0, path=path)
            for y in range(2031, 2041))
        return 0.0, extra_grads * COSTS["training_cost_per_graduate_tnd"] * mult
    if key == "COMBINED":
        fiscal = (public_stock_years * COSTS["avg_public_compensation_tnd"]
                  * 0.35 * mult)
        extra_returns = max(0.0, np.sum(o["returns_net"][mask])
                            - np.sum(base["returns_net"][mask]))
        resource = extra_returns * COSTS["return_cost_per_migrant_tnd"] * mult
        return fiscal, resource
    return 0.0, 0.0


def run_costs(central: dict) -> dict:
    p = replace(CENTRAL, m_base=central["params_central"]["m_base"])
    base = simulate(p, end_year=2040)
    rows = []
    out = {}
    for k in ("BAU", "REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"):
        o = simulate(p, scenario=_scen_dict(k), end_year=2040)
        s = summarise(o, base)
        fiscal, resource = _scenario_costs(k, o, base, 1.0)
        fiscal_lo, resource_lo = _scenario_costs(k, o, base, COSTS["unit_cost_low"])
        fiscal_hi, resource_hi = _scenario_costs(k, o, base, COSTS["unit_cost_high"])
        total = fiscal + resource
        total_lo = fiscal_lo + resource_lo
        total_hi = fiscal_hi + resource_hi
        py = max(s["physician_years"], 1.0)
        add = max(s["stock_diff_2040"], 1.0)
        out[k] = {
            "fiscal_transfer_tnd": fiscal,
            "resource_cost_tnd": resource,
            "total_cost_tnd": total,
            "total_cost_low": total_lo, "total_cost_high": total_hi,
            "cost_per_py_total": total / py,
            "cost_per_py_total_low": total_lo / py,
            "cost_per_py_total_high": total_hi / py,
            "cost_per_py_fiscal": fiscal / py,
            "cost_per_py_resource": resource / py,
            "cost_per_additional_physician": total / add,
            "physician_years": s["physician_years"],
            "stock_diff_2040": s["stock_diff_2040"],
        }
        rows.append([k, fiscal, resource, total, total / py,
                     total_lo / py, total_hi / py, fiscal / py, resource / py,
                     total / add, s["physician_years"], s["stock_diff_2040"]])
    pd.DataFrame(rows, columns=[
        "Scenario", "Fiscal transfer (TND)", "Real resource cost (TND)",
        "Total cost (TND)", "Cost per physician-year, total",
        "Cost per physician-year, low unit costs",
        "Cost per physician-year, high unit costs",
        "Cost per physician-year, fiscal", "Cost per physician-year, resource",
        "Cost per additional physician in 2040", "Physician-years vs BAU",
        "Additional physicians in 2040"]).to_csv(
        os.path.join(TAB, "costs.csv"), index=False)
    return out


# ---------------------------------------------------------------------------
# 10. Figures
# ---------------------------------------------------------------------------
def setup_mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 0.8, "figure.dpi": 150,
        "savefig.dpi": 300, "savefig.bbox": "tight",
    })
    return plt


def _save(fig, name):
    fig.savefig(os.path.join(FIG, f"{name}.png"))
    fig.savefig(os.path.join(FIG, f"{name}.pdf"))
    import matplotlib.pyplot as plt
    plt.close(fig)


def fig_fit(plt, central, mc):
    years = np.array(central["trajectories"]["years"])
    bau = np.array(central["trajectories"]["BAU"])
    obs = central["observed"]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    oy = sorted(obs)
    ax.scatter([y for y in oy if y >= 2017], [obs[y] for y in oy if y >= 2017],
               s=20, color="black", zorder=5,
               label="Observed, INS / Ministry of Health")
    ax.scatter([2010], [obs[2010]], s=20, facecolor="white", edgecolor="black",
               zorder=5, label="WHO estimate, 2010 (initial-condition anchor)")
    mask = years <= 2024
    ax.plot(years[mask], bau[mask], color="#2166AC", lw=1.8,
            label="Model, retrospective fit")
    ax.plot(years[~mask], bau[~mask], color="#2166AC", lw=1.8, ls="--",
            label="Baseline projection")
    q = mc["diagnostics"]["trajectory_quantiles"]
    qy = np.array(q["years"])
    m = qy >= 2024
    ax.fill_between(qy[m], np.array(q["q05"])[m], np.array(q["q95"])[m],
                    color="#2166AC", alpha=0.14, lw=0,
                    label="90% simulation interval")
    ax.axvline(2024, color="grey", lw=0.7, ls=":")
    ax.set_ylabel("Physicians in practice")
    ax.set_xlabel("Year")
    ax.set_xlim(2009, 2040)
    ax.legend(frameon=False, fontsize=7.2, loc="upper left")
    _save(fig, "fig1_historical_fit_and_baseline")


def fig_identifiability(plt, ident):
    df = pd.read_csv(os.path.join(TAB, "identifiability_grid.csv"))
    df = df[df.feasible]
    fig, axes = plt.subplots(2, 2, figsize=(9.4, 6.6))
    axes = axes.ravel()

    piv = df.pivot(index="g_scale", columns="sigma", values="rmse")
    im = axes[0].pcolormesh(piv.columns, piv.index, piv.values,
                            shading="auto", cmap="viridis_r")
    axes[0].contour(piv.columns, piv.index, piv.values,
                    levels=[ident["threshold_rmse"]], colors="white",
                    linewidths=1.2, linestyles="--")
    axes[0].scatter([ident["best"]["sigma"]], [ident["best"]["g_scale"]],
                    marker="*", s=90, color="white", edgecolor="black", zorder=5,
                    label="Best fit")
    axes[0].scatter([0.55], [1.0], marker="o", s=35, color="#B2182B",
                    edgecolor="white", zorder=5, label="Central")
    axes[0].set_xlabel("Pipeline retention, σ")
    axes[0].set_ylabel("Training-output multiplier")
    axes[0].set_title("A. Retrospective fit (RMSE)", loc="left", fontsize=9)
    cb = fig.colorbar(im, ax=axes[0], fraction=0.046, pad=0.02)
    cb.set_label("RMSE (physicians)", fontsize=7.5)
    axes[0].legend(frameon=False, fontsize=6.5, loc="upper right")

    piv2 = df.pivot(index="g_scale", columns="sigma", values="emig_total_2024")
    cs = axes[1].pcolormesh(piv2.columns, piv2.index, piv2.values,
                            shading="auto", cmap="YlOrRd")
    axes[1].contour(piv2.columns, piv2.index, piv2.values,
                    levels=[ident["consistent_emig_range"][0],
                            ident["consistent_emig_range"][1]],
                    colors="black", linewidths=0.6, linestyles=":")
    axes[1].set_xlabel("Pipeline retention, σ")
    axes[1].set_ylabel("Training-output multiplier")
    axes[1].set_title("B. International emigration, 2024 (φ=0.5)",
                      loc="left", fontsize=9)
    cb2 = fig.colorbar(cs, ax=axes[1], fraction=0.046, pad=0.02)
    cb2.set_label("Physicians per year", fontsize=7.5)

    piv3 = df.pivot(index="g_scale", columns="sigma", values="emig_total_phi1_2024")
    cs3 = axes[2].pcolormesh(piv3.columns, piv3.index, piv3.values,
                             shading="auto", cmap="YlOrRd")
    axes[2].contour(piv3.columns, piv3.index, piv3.values,
                    levels=[ident["consistent_emig_phi1_range"][0],
                            ident["consistent_emig_phi1_range"][1]],
                    colors="black", linewidths=0.6, linestyles=":")
    axes[2].set_xlabel("Pipeline retention, σ")
    axes[2].set_ylabel("Training-output multiplier")
    axes[2].set_title("C. Upper bound if all non-entry were emigration (φ=1)",
                      loc="left", fontsize=8.5)
    cb3 = fig.colorbar(cs3, ax=axes[2], fraction=0.046, pad=0.02)
    cb3.set_label("Physicians per year", fontsize=7.5)

    piv4 = df.pivot(index="g_scale", columns="sigma", values="diaspora_2024")
    cs4 = axes[3].pcolormesh(piv4.columns, piv4.index, piv4.values,
                             shading="auto", cmap="Blues")
    axes[3].contour(piv4.columns, piv4.index, piv4.values,
                    levels=[OECD_LOWER_BOUND, 10000], colors="black",
                    linewidths=0.7, linestyles="--")
    axes[3].set_xlabel("Pipeline retention, σ")
    axes[3].set_ylabel("Training-output multiplier")
    axes[3].set_title("D. Return-eligible pool, 2024", loc="left", fontsize=9)
    cb4 = fig.colorbar(cs4, ax=axes[3], fraction=0.046, pad=0.02)
    cb4.set_label("Physicians abroad", fontsize=7.5)

    fig.tight_layout()
    _save(fig, "fig2_identifiability")


def fig_scenarios(plt, central, mc):
    years = np.array(central["trajectories"]["years"])
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.5), sharey=True)
    mask = years >= 2024
    base = np.array(central["trajectories"]["BAU"])
    q = mc["diagnostics"]["trajectory_quantiles"]
    qy = np.array(q["years"])
    qm = qy >= 2024

    axes[0].fill_between(qy[qm], np.array(q["q05"])[qm], np.array(q["q95"])[qm],
                         color="#4D4D4D", alpha=0.12, lw=0,
                         label="Baseline 90% interval")
    for k, lab in [("BAU", "Business as usual"),
                   ("REMUN", "Remuneration / conditions"),
                   ("CAREER", "Career development"),
                   ("RETURN", "Return migration"),
                   ("TRAINING", "Training expansion"),
                   ("COMBINED", "Combined strategy")]:
        axes[0].plot(years[mask], np.array(central["trajectories"][k])[mask],
                     color=COL[k], lw=2.0 if k != "BAU" else 1.8,
                     ls="--" if k == "BAU" else "-", label=lab)
    axes[0].set_title("A. Constant emigration intensity", loc="left", fontsize=9)

    # Re-simulate scenario trajectories under the two escalation modes.
    p = replace(CENTRAL, m_base=central["params_central"]["m_base"])
    for ax, mode, title in (
        (axes[1], "post", "B. Post-entry emigration +3%/year"),
        (axes[2], "both", "C. Both margins +3%/year"),
    ):
        kw = dict(emig_growth_post=0.03,
                  emig_growth_pre=0.03 if mode == "both" else 0.0)
        pp = replace(p, **kw)
        b = simulate(pp, end_year=2040)
        ax.plot(b["years"][b["years"] >= 2024], b["stock"][b["years"] >= 2024],
                color=COL["BAU"], lw=1.8, ls="--")
        for k in ("REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"):
            o = run_scenario(k, pp)
            ax.plot(o["years"][o["years"] >= 2024], o["stock"][o["years"] >= 2024],
                    color=COL[k], lw=1.6)
        ax.set_title(title, loc="left", fontsize=9)

    for ax in axes:
        ax.set_xlabel("Year")
        ax.set_xlim(2024, 2040)
    axes[0].set_ylabel("Physicians in practice")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, fontsize=7, ncol=4,
               loc="lower center", bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    _save(fig, "fig3_scenarios")


def fig_outcomes(plt, central, costs):
    keys = ["REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"]
    labels = ["Remuneration", "Career", "Return", "Training", "Combined"]
    fig, axes = plt.subplots(1, 4, figsize=(11.6, 3.2))
    x = np.arange(len(keys))

    bau = central["bau"]["stock_2040"]
    med = [central["scenarios"][k]["stock_2040"] - bau for k in keys]
    lo = [central["scenarios"][k]["stock_2040_low"] - bau for k in keys]
    hi = [central["scenarios"][k]["stock_2040_high"] - bau for k in keys]
    axes[0].bar(x, med, color=[COL[k] for k in keys], alpha=0.85, width=0.65)
    axes[0].errorbar(x, med, yerr=[np.array(med) - lo, np.array(hi) - med],
                     fmt="none", ecolor="black", capsize=2, lw=0.8)
    axes[0].axhline(0, color="black", ls="--", lw=0.9)
    axes[0].set_xticks(x, labels, fontsize=7, rotation=20)
    axes[0].set_ylabel("Difference from BAU in 2040")
    axes[0].set_title("A. Workforce difference", loc="left", fontsize=9)

    med = [central["scenarios"][k]["cum_emigration"] for k in keys]
    axes[1].bar(x, med, color=[COL[k] for k in keys], alpha=0.85, width=0.65)
    axes[1].axhline(central["bau"]["cum_emigration"], color="black", ls="--", lw=0.9)
    axes[1].set_xticks(x, labels, fontsize=7, rotation=20)
    axes[1].set_ylabel("Cumulative emigrants, 2026–2040")
    axes[1].set_title("B. Emigration", loc="left", fontsize=9)

    med = [central["scenarios"][k]["physician_years"] for k in keys]
    lo = [central["scenarios"][k]["py_low"] for k in keys]
    hi = [central["scenarios"][k]["py_high"] for k in keys]
    axes[2].bar(x, med, color=[COL[k] for k in keys], alpha=0.85, width=0.65)
    axes[2].errorbar(x, med, yerr=[np.array(med) - lo, np.array(hi) - med],
                     fmt="none", ecolor="black", capsize=2, lw=0.8)
    axes[2].axhline(0, color="black", lw=0.8)
    axes[2].set_xticks(x, labels, fontsize=7, rotation=20)
    axes[2].set_ylabel("Physician-years vs BAU")
    axes[2].set_title("C. Retention benefit", loc="left", fontsize=9)

    fiscal = [costs[k]["cost_per_py_fiscal"] for k in keys]
    resource = [costs[k]["cost_per_py_resource"] for k in keys]
    total = [costs[k]["cost_per_py_total"] for k in keys]
    lo = [costs[k]["cost_per_py_total_low"] for k in keys]
    hi = [costs[k]["cost_per_py_total_high"] for k in keys]
    axes[3].bar(x, fiscal, color="#9E9E9E", alpha=0.9, width=0.65,
                label="Fiscal transfer")
    axes[3].bar(x, resource, bottom=fiscal, color="#1B7837",
                alpha=0.85, width=0.65, label="Real resource cost")
    axes[3].errorbar(x, total, yerr=[np.array(total) - lo, np.array(hi) - total],
                     fmt="none", ecolor="black", capsize=2, lw=0.8)
    axes[3].set_xticks(x, labels, fontsize=7, rotation=20)
    axes[3].set_ylabel("TND per physician-year")
    axes[3].set_title("D. Illustrative cost (stacked)", loc="left", fontsize=9)
    axes[3].legend(frameon=False, fontsize=6.5, loc="upper left")
    fig.tight_layout()
    _save(fig, "fig4_policy_outcomes")


def fig_density(plt, central):
    years = np.array(central["trajectories"]["years"])
    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    for k, lab in [("BAU", "Business as usual"), ("COMBINED", "Combined strategy")]:
        mask = years >= 2010
        dens = (np.array(central["trajectories"][k])[mask]
                / np.array([POP[int(y)] for y in years[mask]]) * 1000)
        ax.plot(years[mask], dens, color=COL[k], lw=2,
                ls="--" if k == "BAU" else "-", label=lab)
    obs = central["observed"]
    oy = [y for y in sorted(obs) if y >= 2017]
    ax.scatter(oy, [obs[y] / POP[y] * 1000 for y in oy], s=14, color="black",
               zorder=5, label="Observed")
    ax.axvline(2026, color="grey", ls=":", lw=0.8)
    ax.set_xlim(2015, 2040)
    ax.set_ylabel("Physicians per 1 000 population")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, fontsize=7.5)
    _save(fig, "fig5_density")


def fig_sensitivity(plt, sens):
    t = sens["tornado"]
    labels = {
        "sigma": "Pipeline retention (σ)", "g_scale": "Training output",
        "emig_future_mult": "Future emigration intensity",
        "m_base": "Emigration flow (structural)", "rho": "Return rate",
        "retire_shift": "Retirement age",
        "emig_tilt": "Age profile of emigration",
        "initial_stock_2008": "Initial stock (2008)",
        "diaspora_attrition": "Diaspora attrition",
        "return_retention": "Return retention",
    }
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.6),
                             gridspec_kw={"width_ratios": [1.1, 1.0]})

    items = sorted([(k, v) for k, v in t.items() if k != "m_base"],
                   key=lambda kv: abs(kv[1]["high"] - kv[1]["low"]))
    for i, (k, v) in enumerate(items):
        axes[0].barh(i - 0.18, v["low"], color="#2166AC", alpha=0.85, height=0.35)
        axes[0].barh(i + 0.18, v["high"], color="#B2182B", alpha=0.85, height=0.35)
    axes[0].set_yticks(range(len(items)),
                       [labels.get(k, k) for k, _ in items], fontsize=7.2)
    axes[0].axvline(0, color="black", lw=0.8)
    axes[0].set_xlabel("Change in 2040 workforce vs central calibration")
    axes[0].set_title("A. One-at-a-time sensitivity", loc="left", fontsize=9)
    # The calibrated emigration flow is shown in Table 7 rather than in the
    # tornado, because its structural effect (+3 960 / -7 594) would compress
    # every other bar.
    from matplotlib.patches import Patch
    axes[0].legend(handles=[
        Patch(color="#2166AC", alpha=0.85, label="10th percentile"),
        Patch(color="#B2182B", alpha=0.85, label="90th percentile")],
        frameon=False, fontsize=7, loc="lower right")

    order = sorted(sens["prcc"], key=lambda k: abs(sens["prcc"][k]))
    ypos = np.arange(len(order))
    axes[1].barh(ypos - 0.18, [sens["prcc"][k] for k in order],
                 color="#4D4D4D", alpha=0.9, height=0.35, label="Partial rank correlation")
    axes[1].barh(ypos + 0.18, [sens["marginal_spearman"][k] for k in order],
                 color="#E08214", alpha=0.75, height=0.35, label="Marginal Spearman")
    axes[1].set_yticks(ypos, [labels.get(k, k) for k in order], fontsize=7.2)
    axes[1].axvline(0, color="black", lw=0.8)
    axes[1].set_xlabel("Correlation with 2040 workforce")
    axes[1].set_title("B. Conditional vs marginal association", loc="left", fontsize=9)
    axes[1].legend(frameon=False, fontsize=6.8, loc="lower right")
    fig.tight_layout()
    _save(fig, "fig6_sensitivity")


def fig_age(plt, central):
    from model import AGES
    m = central["params_central"]["m_base"]
    p = replace(CENTRAL, m_base=m)
    o24 = simulate(p, end_year=2024)
    b = simulate(p, end_year=2040)
    c = run_scenario("COMBINED", p)
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    bins = [(25, 34), (35, 44), (45, 54), (55, 64), (65, 75)]
    labels = ["25–34", "35–44", "45–54", "55–64", "65+"]
    def shares(d):
        return [d[(AGES >= a) & (AGES <= b)].sum() / d.sum() * 100 for a, b in bins]
    x = np.arange(len(bins))
    ax.bar(x - 0.22, shares(o24["age_dist"][2024]), width=0.22,
           color="#4D4D4D", label="2024")
    ax.bar(x, shares(b["age_dist"][2040]), width=0.22, color="#2166AC",
           label="2040, BAU")
    ax.bar(x + 0.22, shares(c["age_dist"][2040]), width=0.22, color="#B2182B",
           label="2040, combined")
    ax.set_xticks(x, labels)
    ax.set_ylabel("% of practising physicians")
    ax.set_xlabel("Age group (years)")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    _save(fig, "fig7_age_structure")


def fig_structural(plt, central):
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.5), sharey=True)
    for ax, mode, title in (
        (axes[0], "post", "A. Post-entry emigration only"),
        (axes[1], "both", "B. Both pre- and post-entry margins"),
    ):
        for g, ls in ((0.0, "-"), (0.03, "--"), (0.05, "-."), (0.07, ":")):
            s = central["structural"][f"{mode}_{g:.2f}"]
            y = np.array(s["years"])
            ax.plot(y[y >= 2024], np.array(s["trajectory"])[y >= 2024],
                    color={0.0: "#4D4D4D", 0.03: "#E08214", 0.05: "#B2182B",
                           0.07: "#67001F"}[g], lw=2, ls=ls,
                    label="Constant" if g == 0 else f"+{int(g*100)}%/year")
        ax.axhline(TARGET_2024, color="grey", ls=":", lw=0.8)
        ax.set_xlim(2024, 2040)
        ax.set_xlabel("Year")
        ax.set_title(title, loc="left", fontsize=9)
    axes[0].set_ylabel("Physicians in practice")
    axes[0].legend(frameon=False, fontsize=7, loc="lower left")
    fig.tight_layout()
    _save(fig, "fig8_structural_emigration")


def fig_breakeven(plt, be):
    grid = pd.read_csv(os.path.join(TAB, "breakeven_grid.csv"), index_col=0)
    rs = np.array([float(c) for c in grid.columns])
    ts = np.array([float(i) for i in grid.index])
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    cs = ax.contourf(rs * 100, ts * 100, grid.values, levels=16, cmap="RdYlBu")
    lines = ax.contour(rs * 100, ts * 100, grid.values,
                       levels=[16000, 18000, 20000, 22000, 24000],
                       colors="black", linewidths=0.6)
    ax.clabel(lines, fmt="%d", fontsize=6, inline=True)
    ax.plot([0], [30], marker="o", color="#2166AC", ms=6,
            label="Training +30% only")
    ax.plot([30], [0], marker="o", color="#B2182B", ms=6,
            label="Retention −30% only")
    ax.plot([0], [be["training_match_30pct_retention"] * 100], marker="s",
            color="#2166AC", ms=6,
            label=f"Training to match −30% retention ({be['training_match_30pct_retention']*100:.0f}%)")
    ax.axhline(30, color="grey", lw=0.5, ls=":")
    ax.axvline(be["retention_match_30pct_training"] * 100, color="#B2182B",
               lw=0.9, ls="--")
    ax.text(be["retention_match_30pct_training"] * 100 + 2, 62,
            f"break-even\n{be['retention_match_30pct_training']*100:.1f}%\nemigration reduction",
            fontsize=7, color="#B2182B")
    ax.set_xlabel("Reduction in emigration (%)")
    ax.set_ylabel("Training expansion (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Workforce in 2040 under combined retention and training",
                 loc="left", fontsize=9)
    cb = fig.colorbar(cs, ax=ax, fraction=0.046, pad=0.02)
    cb.set_label("Physicians in 2040", fontsize=7.5)
    ax.legend(frameon=False, fontsize=6.5, loc="upper right")
    fig.tight_layout()
    _save(fig, "fig9_breakeven")


# ---------------------------------------------------------------------------
# 11. Tables
# ---------------------------------------------------------------------------
def write_tables(central, mc, sens, ident, struct, be, costs, diaspora, grads):
    # Table 1. Data sources
    data_rows = [
        ["Physicians in active practice", "INS / Ministry of Health; carte sanitaire", "2017–2024",
         "Public-sector physicians plus private practitioners; excludes most residents; 2020 public count affected by a reporting or reclassification change"],
        ["Physicians in active practice, 2010", "WHO Global Health Workforce Statistics", "2010",
         "Used only as an initial-condition anchor; different definition from the 2017–2024 series"],
        ["Physicians registered with the CNOM", "CNOM", "2009–2026",
         "All inscriptions, including inactive, retired, administrative and deceased physicians; not a practising count"],
        ["Medical graduates", "Zehnati 2024; ministerial statements", "2013–2025",
         "Medicine graduates only; 2013 and 2021 anchored, 2024 reconstructed, post-2024 assumptions tested"],
        ["Emigration proxies", "CNOM via ITES; press", "2011–2024",
         "Certificates of good conduct, removal requests, departure files and union/CNOM estimates; not comparable"],
        ["Tunisian physicians in France", "CNOM France", "2010–2023",
         "Registered with the French Order; the 266 (2010) and 1 591 (2023) figures are not guaranteed to use the same counting method"],
        ["Tunisian physicians in Germany", "German medical statistics via ITES", "2022",
         "Country-of-training/nationality definition; 881"],
        ["Tunisian-born physicians in OECD countries", "OECD DIOC; ITES", "2010/11, 2015/16",
         "Country-of-birth estimate; about 4 000 in 2015/16; lower bound"],
        ["Population", "INS 2024 census; UN WPP 2024", "2010–2040",
         "2024 census 11 972 169; WPP rescaled to the census"],
    ]
    pd.DataFrame(data_rows, columns=["Quantity", "Source", "Period",
                                     "Definition and limitations"]).to_csv(
        os.path.join(TAB, "table1_data_sources.csv"), index=False)

    # Table 2. Parameters
    r = central["scenarios"]["BAU"]
    pre_share = r["emig_pre_2024"] / r["emigration_2024"] if r["emigration_2024"] else np.nan
    rows = [
        ["Practising physicians, 2024", "15 315", "—", "Observed", "INS / Ministry of Health"],
        ["Practising physicians, 2017–2024", "14 892–15 426", "—", "Observed", "INS / Ministry of Health"],
        ["Medical graduates, 2013 / 2021 / 2024", "987 / 1 128 / 1 305", "987–1 900", "Observed / reconstructed", "Zehnati 2024; ministerial statements"],
        ["Pipeline retention, σ", "0.55", "0.30–0.80", "Estimated (calibrated, weakly identified)", "Model calibration; flow reconciliation"],
        ["Post-entry emigration, 2024, m", f"{central['params_central']['m_base']:.0f}", "calibrated per draw", "Estimated (calibrated, weakly identified)", "Model calibration"],
        ["Total emigration, 2024", f"{r['emigration_2024']:.0f}", f"{ident['consistent_emig_range'][0]:.0f}–{ident['consistent_emig_range'][1]:.0f} (consistent set)", "Estimated (model-consistent)", "Derived; conditional on other parameters"],
        ["Pipeline non-entry share, 1−σ", "0.45", "0.20–0.70", "Assumption (implied by σ)", "Model structure"],
        ["Pre-entry share of total emigration, 2024", f"{pre_share:.2f}", "varies with σ and training output", "Derived", "Model output"],
        ["Return rate from return-eligible pool, ρ", "0.020", "0.005–0.050", "Assumption", "No Tunisian data; informed by Varga 2017"],
        ["Diaspora attrition (death, onward migration, settlement)", "0.08", "0.02–0.15", "Assumption", "Calibrated to keep pool near destination stocks"],
        ["Return retention (share of returns remaining in practice)", "0.85", "0.75–0.95", "Assumption", "Re-emigration and non-practice of return migrants"],
        ["Retirement age", "60–70", "±1.5 years", "Observed (legal) + assumption", "Law 2019-37; CNRPS/CNSS"],
        ["Initial practising stock, 2008", "12 600", "Normal (SD 400)", "Indirect estimate", "WHO 2010; CNOM 2008"],
        ["Initial return-eligible pool, 2008", "4 000", "2 000–8 000", "Indirect estimate", "OECD 2018; CNOM France; German statistics"],
        ["Population, 2024", "11 972 169", "—", "Observed", "INS 2024 census"],
        ["Population growth, 2024–2040", "0.33%/yr", "UN WPP medium variant", "Projected", "UN WPP 2024"],
    ]
    pd.DataFrame(rows, columns=["Parameter", "Central value", "Range / distribution",
                                "Status", "Source"]).to_csv(
        os.path.join(TAB, "table2_parameters.csv"), index=False)

    # Table 3. Scenarios
    rows = []
    for k, s in SCENARIOS.items():
        lo, hi = EFFECT_RANGE[k]
        rows.append([k, s["label"], s["emig_mult"], s["entry_retention"],
                     s["return_mult"], s["train_mult"],
                     f"{lo[0]:.2f}/{lo[1]:.2f}/{lo[2]:.2f}/{lo[3]:.2f}",
                     f"{hi[0]:.2f}/{hi[1]:.2f}/{hi[2]:.2f}/{hi[3]:.2f}"])
    pd.DataFrame(rows, columns=["Code", "Scenario", "Post-entry emigration multiplier",
                                "Pre-entry emigration reduction",
                                "Return-rate multiplier", "Training multiplier",
                                "Low effect", "High effect"]).to_csv(
        os.path.join(TAB, "table3_scenarios.csv"), index=False)

    # Table 4. Flow decomposition
    m0 = central["params_central"]["m_base"]
    p0 = replace(CENTRAL, m_base=m0)
    o = simulate(p0, end_year=2040)
    rows = []
    for y in [2017, 2020, 2024, 2030, 2035, 2040]:
        i = list(o["years"]).index(y)
        rows.append([y, round(o["stock"][i]), round(o["entries"][i]),
                     round(o["nonentry_total"][i]), round(o["emig_pre"][i]),
                     round(o["nonentry_domestic"][i]), round(o["emig_post"][i]),
                     round(o["returns_net"][i]), round(o["retirements"][i]),
                     round(o["deaths"][i]),
                     round(o["stock"][i] - o["stock"][i - 1]),
                     round(o["stock"][i] / POP[y] * 1000, 2),
                     round(o["diaspora"][i])])
    pd.DataFrame(rows, columns=["Year", "Stock", "Entries", "Pipeline non-entry",
                                "Pre-entry emigration", "Domestic non-entry",
                                "Post-entry emigration", "Returns", "Retirements",
                                "Deaths", "Net change", "Density (/1000)",
                                "Return-eligible pool"]).to_csv(
        os.path.join(TAB, "table4_flow_decomposition.csv"), index=False)

    # Table 5. Results
    rows = []
    for k in ["BAU", "REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"]:
        r = central["scenarios"].get(k, central["bau"])
        rows.append([
            k, r["stock_2030"], r["stock_2040"], r["density_2040"],
            r["cum_emigration"], r["cum_returns"],
            r.get("physician_years", 0),
            r.get("stock_2040_low", np.nan), r.get("stock_2040_high", np.nan),
            r.get("stock_2040_escalating_post", np.nan),
            r.get("stock_2040_escalating_both", np.nan),
            costs[k]["cost_per_py_total"],
        ])
    df = pd.DataFrame(rows, columns=[
        "Scenario", "Workforce 2030", "Workforce 2040", "Density 2040 (/1000)",
        "Cumulative emigration 2026–2040", "Cumulative returns 2026–2040",
        "Physician-years vs BAU", "Workforce 2040, low effect",
        "Workforce 2040, high effect", "Workforce 2040, post-entry +3%/yr",
        "Workforce 2040, both margins +3%/yr", "Cost per physician-year (TND)"])
    df["Density 2040 (/1000)"] = df["Density 2040 (/1000)"].round(2)
    num_cols = [c for c in df.columns if c not in ("Scenario", "Density 2040 (/1000)")]
    df[num_cols] = df[num_cols].round(1)
    df.to_csv(os.path.join(TAB, "table5_results.csv"), index=False)

    # Table 6. MC uncertainty
    rows = []
    for k in ["BAU", "REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"]:
        key = "bau_stock_2040" if k == "BAU" else f"{k}_stock_2040"
        q = mc[key]
        py = "—" if k == "BAU" else (
            f"{mc[f'{k}_py']['median']:.0f} "
            f"({mc[f'{k}_py']['lo']:.0f} to {mc[f'{k}_py']['hi']:.0f})")
        rows.append([k, f"{q['median']:.0f} ({q['lo']:.0f}–{q['hi']:.0f})", py])
    pd.DataFrame(rows, columns=["Scenario", "Workforce 2040, median (90% interval)",
                                "Physician-years vs BAU, median (90% interval)"]).to_csv(
        os.path.join(TAB, "table6_uncertainty.csv"), index=False)

    # Table 7. Sensitivity
    rows = []
    for k, v in sens["tornado"].items():
        rows.append([k, v["low_value"], v["high_value"], v["low"], v["high"],
                     sens["prcc"].get(k, np.nan),
                     sens["marginal_spearman"].get(k, np.nan),
                     sens["prcc_p"].get(k, np.nan)])
    pd.DataFrame(rows, columns=["Parameter", "10th percentile", "90th percentile",
                                "Change at 10th", "Change at 90th",
                                "Partial rank correlation", "Marginal Spearman",
                                "PRCC p-value"]).to_csv(
        os.path.join(TAB, "table7_sensitivity.csv"), index=False)

    # Table 8. Identifiability summary
    b = central["scenarios"]["BAU"]
    rows = [
        ["Best fit", ident["best"]["sigma"], ident["best"]["g_scale"],
         ident["best"]["rmse"], ident["best"]["nonentry_2024"],
         ident["best"]["emig_total_2024"], ident["best"]["emig_total_phi1_2024"],
         ident["best"]["diaspora_2024"]],
        ["Central", 0.55, 1.0, central["fit"]["rmse"],
         b["nonentry_2024"], b["emigration_2024"],
         b["nonentry_2024"] + b["emig_post_2024"], b["diaspora_2024"]],
        ["Acceptable set (RMSE ≤ 2% of mean stock)",
         f"{ident['consistent_sigma_range'][0]:.2f}–{ident['consistent_sigma_range'][1]:.2f}",
         f"{ident['consistent_g_range'][0]:.2f}–{ident['consistent_g_range'][1]:.2f}",
         f"≤ {ident['threshold_rmse']:.0f}",
         f"{ident['consistent_nonentry_range'][0]:.0f}–{ident['consistent_nonentry_range'][1]:.0f}",
         f"{ident['consistent_emig_range'][0]:.0f}–{ident['consistent_emig_range'][1]:.0f}",
         f"{ident['consistent_emig_phi1_range'][0]:.0f}–{ident['consistent_emig_phi1_range'][1]:.0f}",
         f"{ident['consistent_diaspora_range'][0]:.0f}–{ident['consistent_diaspora_range'][1]:.0f}"],
        ["Strict set (RMSE ≤ 1.10 × best)",
         f"{ident['strict_sigma_range'][0]:.2f}–{ident['strict_sigma_range'][1]:.2f}",
         f"{ident['strict_g_range'][0]:.2f}–{ident['strict_g_range'][1]:.2f}",
         f"≤ {ident['strict_threshold_rmse']:.0f}",
         "—",
         f"{ident['strict_emig_range'][0]:.0f}–{ident['strict_emig_range'][1]:.0f}",
         f"{ident['strict_emig_phi1_range'][0]:.0f}–{ident['strict_emig_phi1_range'][1]:.0f}",
         "—"],
    ]
    pd.DataFrame(rows, columns=["Case", "Pipeline retention", "Training multiplier",
                                "RMSE", "Pipeline non-entry 2024",
                                "International emigration 2024 (φ=0.5)",
                                "Upper bound if all non-entry emigrated (φ=1)",
                                "Return-eligible pool 2024"]).to_csv(
        os.path.join(TAB, "table8_identifiability.csv"), index=False)

    # Table 9. Costs
    rows = []
    for k in ["REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"]:
        c = costs[k]
        rows.append([k, c["fiscal_transfer_tnd"], c["resource_cost_tnd"],
                     c["total_cost_tnd"], c["cost_per_py_total"],
                     c["cost_per_py_total_low"], c["cost_per_py_total_high"],
                     c["cost_per_py_fiscal"], c["cost_per_py_resource"],
                     c["cost_per_additional_physician"],
                     c["physician_years"], c["stock_diff_2040"]])
    pd.DataFrame(rows, columns=[
        "Scenario", "Fiscal transfer (TND)", "Real resource cost (TND)",
        "Total cost (TND)", "Cost per physician-year, total",
        "Cost per physician-year, low unit costs",
        "Cost per physician-year, high unit costs",
        "Cost per physician-year, fiscal", "Cost per physician-year, resource",
        "Cost per additional physician in 2040", "Physician-years vs BAU",
        "Additional physicians in 2040"]).to_csv(
        os.path.join(TAB, "table9_costs.csv"), index=False)

    # Table 11. Age structure
    m0 = central["params_central"]["m_base"]
    p_age = replace(CENTRAL, m_base=m0)
    o24 = simulate(p_age, end_year=2024)
    b40 = simulate(p_age, end_year=2040)
    c40 = run_scenario("COMBINED", p_age)
    bins = [(25, 34), (35, 44), (45, 54), (55, 64), (65, 75)]
    labels_age = ["25–34", "35–44", "45–54", "55–64", "65+"]
    def _shares(d):
        return [float(d[(AGES >= a) & (AGES <= b)].sum() / d.sum() * 100)
                for a, b in bins]
    age_rows = []
    for lab, d in (("2024", o24["age_dist"][2024]),
                   ("2040, BAU", b40["age_dist"][2040]),
                   ("2040, combined", c40["age_dist"][2040])):
        age_rows.append([lab] + [round(v, 1) for v in _shares(d)])
    pd.DataFrame(age_rows, columns=["Year / scenario"] + labels_age).to_csv(
        os.path.join(TAB, "table11_age_structure.csv"), index=False)

    # Table 12. Scenario flows in 2040
    rows = []
    for k in ("BAU", "REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"):
        o = simulate(p_age, scenario=_scen_dict(k), end_year=2040)
        i = list(o["years"]).index(2040)
        rows.append([k, round(o["stock"][i]), round(o["entries"][i]),
                     round(o["nonentry_total"][i]), round(o["emig_pre"][i]),
                     round(o["nonentry_domestic"][i]), round(o["emig_post"][i]),
                     round(o["returns_net"][i]), round(o["retirements"][i]),
                     round(o["deaths"][i]), round(o["diaspora"][i]),
                     round(o["pre_emig_share"][i], 3)])
    pd.DataFrame(rows, columns=["Scenario", "Stock 2040", "Entries",
                                "Pipeline non-entry", "Pre-entry emigration",
                                "Domestic non-entry", "Post-entry emigration",
                                "Returns", "Retirements", "Deaths",
                                "Return-eligible pool", "Pre-entry emigration share"]
                 ).to_csv(os.path.join(TAB, "table12_scenario_flows_2040.csv"),
                          index=False)

    # Table 13. Robustness: graduate baselines and escalation
    rows = []
    for path, v in grads.items():
        rows.append(["Graduate path: " + path, v["bau_2040"], v["training_2040"],
                     v["combined_2040"], v["training_py"], v["combined_py"]])
    for mode in ("post", "both"):
        for g in (0.03, 0.05, 0.07):
            s = struct[f"{mode}_{g:.2f}"]
            rows.append([f"Escalation: {mode} +{int(g*100)}%/yr", s["stock_2040"],
                         s["scenario_2040"]["TRAINING"],
                         s["scenario_2040"]["COMBINED"],
                         s["scenario_py"]["TRAINING"],
                         s["scenario_py"]["COMBINED"]])
    pd.DataFrame(rows, columns=["Robustness scenario", "BAU 2040",
                                "Training 2040", "Combined 2040",
                                "Training physician-years", "Combined physician-years"]).to_csv(
        os.path.join(TAB, "table13_robustness.csv"), index=False)


# ---------------------------------------------------------------------------
# 12. Key numbers for the manuscript
# ---------------------------------------------------------------------------
def write_key_numbers(central, mc, sens, ident, struct, be, costs, diaspora,
                      grads, phi_sens, lag_sens, age_sens, ret_sens):
    def f(x, nd=0):
        return f"{x:,.{nd}f}".replace(",", " ")

    def rng(v, nd=0):
        return f"{f(v[0], nd)}–{f(v[1], nd)}"

    c = central
    s = c["scenarios"]
    lines = []
    lines.append("# Key numbers\n")
    lines.append("Generated by `src/analysis.py`. Use these values in the manuscript.\n")
    lines.append("## Calibration and fit\n")
    lines.append(f"- phi (share of pipeline non-entry assumed to be emigration): {c['params_central']['phi']:.2f}")
    lines.append(f"- m_base: {f(c['params_central']['m_base'], 1)}")
    lines.append(f"- Calibration error (2024): {f(c['fit']['calibration_error'], 3)}")
    lines.append(f"- RMSE 2017–2024: {f(c['fit']['rmse'], 1)} ({c['fit']['mape']:.2f}% MAPE)")
    lines.append(f"- RMSE excluding 2020–2021: {f(c['fit']['rmse_excl_2020_21'], 1)}")
    lines.append(f"- RMSE 2017–2019: {f(c['fit']['rmse_2017_2019'], 1)}; 2022–2024: {f(c['fit']['rmse_2022_2024'], 1)}")
    lines.append("\n## Baseline\n")
    for k in ("stock_2024", "stock_2030", "stock_2035", "stock_2040",
              "density_2024", "density_2040", "cum_emigration", "cum_returns",
              "diaspora_2024", "diaspora_2040", "emigration_2024",
              "emig_pre_2024", "emig_post_2024", "nonentry_2024",
              "nonentry_domestic_2024", "returns_2024"):
        lines.append(f"- {k}: {f(c['bau'][k], 2)}")
    lines.append(f"- cap_binding_any: {c['bau']['cap_binding_any']}")
    lines.append(f"- max_emig_hazard: {c['bau']['max_emig_hazard']:.3f}")
    lines.append(f"- MC 2040: {f(mc['bau_stock_2040']['median'])} ({f(mc['bau_stock_2040']['lo'])}–{f(mc['bau_stock_2040']['hi'])})")
    lines.append(f"- MC density 2040: {mc['bau_density_2040']['median']:.2f} ({mc['bau_density_2040']['lo']:.2f}–{mc['bau_density_2040']['hi']:.2f})")
    lines.append(f"- MC probability BAU 2040 > 2024: {mc['prob_bau_above_2024']:.3f}")
    lines.append(f"- MC probability combined first: {mc['rank_combined_first']:.3f}")
    lines.append(f"- MC probability training last: {mc['rank_training_last']:.3f}")
    lines.append(f"- MC probability return last: {mc['rank_return_last']:.3f}")
    for name, probs in mc["rank_distribution"].items():
        lines.append(f"- Rank distribution {name}: " + ", ".join(
            f"{i+1}:{p:.3f}" for i, p in enumerate(probs)))
    lines.append(f"- MC max calibration error: {mc['diagnostics']['max_abs_calibration_error']:.4f}")

    lines.append("\n## Scenarios (deterministic)\n")
    for k in ("REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"):
        r = s[k]
        lines.append(f"- {k}: 2040 {f(r['stock_2040'])} (diff {f(r['stock_diff_2040'])}), "
                     f"PY {f(r['physician_years'])}, cum emig {f(r['cum_emigration'])}, "
                     f"cum returns {f(r['cum_returns'])}, density {r['density_2040']:.2f}")
        lines.append(f"  - low/high 2040: {f(r['stock_2040_low'])} / {f(r['stock_2040_high'])}; "
                     f"post-only +3%: {f(r['stock_2040_escalating_post'])}; "
                     f"both +3%: {f(r['stock_2040_escalating_both'])}")
        lines.append(f"  - cost/PY total: {f(costs[k]['cost_per_py_total'])} "
                     f"({f(costs[k]['cost_per_py_total_low'])}–{f(costs[k]['cost_per_py_total_high'])}); "
                     f"fiscal {f(costs[k]['cost_per_py_fiscal'])}; "
                     f"resource {f(costs[k]['cost_per_py_resource'])}; "
                     f"cost/additional physician: {f(costs[k]['cost_per_additional_physician'])}")
    lines.append(f"- BAU 2040: {f(c['bau']['stock_2040'])}; density {c['bau']['density_2040']:.2f}")

    lines.append("\n## Age structure (% of practising physicians)\n")
    for lab, vals in c["age_structure"].items():
        lines.append(f"- {lab}: " + ", ".join(f"{k} {v:.1f}" for k, v in vals.items()))

    lines.append("\n## Identifiability\n")
    lines.append(f"- Best fit: sigma {ident['best']['sigma']:.2f}, training {ident['best']['g_scale']:.2f}, RMSE {ident['best']['rmse']:.0f}, non-entry {ident['best']['nonentry_2024']:.0f}, emigration (phi=0.5) {ident['best']['emig_total_2024']:.0f}, upper bound (phi=1) {ident['best']['emig_total_phi1_2024']:.0f}, pool {ident['best']['diaspora_2024']:.0f}")
    lines.append(f"- Acceptable set (RMSE ≤ 2% of mean stock, {ident['threshold_rmse']:.0f}): sigma {rng(ident['consistent_sigma_range'], 2)}; training {rng(ident['consistent_g_range'], 2)}; non-entry {rng(ident['consistent_nonentry_range'])}; emigration phi=0.5 {rng(ident['consistent_emig_range'])}; upper bound phi=1 {rng(ident['consistent_emig_phi1_range'])}; pool {rng(ident['consistent_diaspora_range'])}")
    lines.append(f"- Strict set (RMSE ≤ 1.10 × best, {ident['strict_threshold_rmse']:.0f}): n={ident['strict_n']}; emigration phi=0.5 {rng(ident['strict_emig_range'])}; upper bound phi=1 {rng(ident['strict_emig_phi1_range'])}")
    lines.append(f"- All feasible grid: emigration phi=0.5 {rng(ident['all_emig_range'])}; upper bound phi=1 {rng(ident['all_emig_phi1_range'])}; RMSE {rng(ident['all_rmse_range'])}")
    lines.append(f"- Destination-consistent subset: n={ident['destination_consistent_n']}, emigration phi=0.5 {rng(ident['destination_consistent_emig_range'])}, upper bound phi=1 {rng(ident['destination_consistent_emig_phi1_range'])}, pool {rng(ident['destination_consistent_diaspora_range'])}")

    lines.append("\n## Sensitivity\n")
    for k in SENS_PARAMS:
        lines.append(f"- {k}: PRCC {sens['prcc'][k]:.2f} (p={sens['prcc_p'][k]:.3f}), marginal {sens['marginal_spearman'][k]:.2f}, OAT low/high {sens['tornado'][k]['low']:.0f}/{sens['tornado'][k]['high']:.0f}")
    mb = sens["tornado"]["m_base"]
    lines.append(f"- m_base (structural, not recalibrated): OAT low/high {mb['low']:.0f}/{mb['high']:.0f}")

    lines.append("\n## Structural escalation\n")
    for key, v in struct.items():
        lines.append(f"- {key}: BAU 2040 {f(v['stock_2040'])}, density {v['density_2040']:.2f}, cum emig {f(v['cum_emigration'])}; combined {f(v['scenario_2040']['COMBINED'])}, remuneration {f(v['scenario_2040']['REMUN'])}, return {f(v['scenario_2040']['RETURN'])}, training {f(v['scenario_2040']['TRAINING'])}")

    lines.append("\n## Break-even\n")
    lines.append(f"- Retention reduction matching 30% training: {be['retention_match_30pct_training']*100:.1f}%")
    lines.append(f"- Training expansion matching 30% retention: {be['training_match_30pct_retention']*100:.1f}%")
    lines.append(f"- 2040 stock, training +30%: {f(be['stock_training_30'])}; retention −30%: {f(be['stock_retention_30'])}; BAU: {f(be['bau_2040'])}")

    lines.append("\n## Diaspora sensitivity\n")
    dc = diaspora["central"]
    lines.append(f"- Central: attrition {dc['diaspora_attrition']:.2f}, initial pool {f(dc['initial_diaspora_2008'])}, rho {dc['rho']:.3f}, pool 2024 {f(dc['diaspora_2024'])}, BAU 2040 {f(dc['bau_2040'])}, return 2040 {f(dc['return_2040'])}, return difference {f(dc['return_diff_2040'])}, eventual return probability {dc['eventual_return_prob']:.2f}")
    lines.append(f"- Return difference range across sensitivity: {rng(diaspora['return_diff_range'])}")
    lines.append(f"- Pool range across sensitivity: {rng(diaspora['diaspora_2024_range'])}")
    lines.append(f"- Eventual return probability range: {diaspora['eventual_return_range'][0]:.2f}–{diaspora['eventual_return_range'][1]:.2f}")

    lines.append("\n## Graduate baselines\n")
    for k, v in grads.items():
        lines.append(f"- {k}: graduates 2040 {v['graduates_2040']:.0f}; BAU {f(v['bau_2040'])}; training {f(v['training_2040'])}; combined {f(v['combined_2040'])}; training PY {f(v['training_py'])}; combined PY {f(v['combined_py'])}")

    lines.append("\n## Phi sensitivity (share of pipeline non-entry assumed to be emigration)\n")
    for k, v in phi_sens.items():
        b = v["bau"]
        lines.append(f"- phi={v['phi']:.2f}: m={f(v['m_base'],1)}; emigration 2024={f(b['emigration_2024'])}; non-entry 2024={f(b['nonentry_2024'])}; pool 2024={f(b['diaspora_2024'])}; BAU 2040={f(b['stock_2040'])}; remuneration={f(v['scenarios']['REMUN']['stock_2040'])}; return={f(v['scenarios']['RETURN']['stock_2040'])}; training={f(v['scenarios']['TRAINING']['stock_2040'])}; combined={f(v['scenarios']['COMBINED']['stock_2040'])}; combined PY={f(v['scenarios']['COMBINED']['physician_years'])}; retention match={v['retention_match']*100:.1f}%")

    lines.append("\n## Postgraduate lag sensitivity\n")
    for k, v in lag_sens.items():
        lines.append(f"- lag={v['lag']}: m={f(v['m_base'],1)}; BAU 2040={f(v['bau_2040'])}; training={f(v['training_2040'])}; combined={f(v['combined_2040'])}; training PY={f(v['training_py'])}; combined PY={f(v['combined_py'])}; retention match={v['retention_match']*100:.1f}%")

    lines.append("\n## Initial age-shape sensitivity\n")
    for k, v in age_sens.items():
        lines.append(f"- {k}: m={f(v['m_base'],1)}; BAU 2040={f(v['bau_2040'])}; training={f(v['training_2040'])}; combined={f(v['combined_2040'])}; training PY={f(v['training_py'])}; combined PY={f(v['combined_py'])}; retention match={v['retention_match']*100:.1f}%")

    lines.append("\n## Retirement and mortality sensitivity\n")
    for k, v in ret_sens.items():
        lines.append(f"- shift={v['retire_shift']:.1f}, mortality x{v['mortality_mult']:.1f}: m={f(v['m_base'],1)}; BAU 2040={f(v['bau_2040'])}; combined 2040={f(v['combined_2040'])}; combined PY={f(v['combined_py'])}")

    with open(os.path.join(OUT, "key_numbers.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 13. Validation
# ---------------------------------------------------------------------------
def validate(central, mc, ident, sens):
    checks = []
    p = replace(CENTRAL, m_base=central["params_central"]["m_base"])
    base = simulate(p, end_year=2040)

    checks.append(("2024 calibration exact",
                   abs(central["fit"]["calibration_error"]) < 0.5,
                   f"{central['fit']['calibration_error']:.3f}"))
    checks.append(("Monte Carlo calibration exact",
                   mc["diagnostics"]["max_abs_calibration_error"] < 0.5,
                   f"{mc['diagnostics']['max_abs_calibration_error']:.3f}"))
    checks.append(("Combined ranks first in deterministic 2040",
                   all(central["scenarios"]["COMBINED"]["stock_2040"]
                       >= central["scenarios"][k]["stock_2040"]
                       for k in ("REMUN", "CAREER", "RETURN", "TRAINING", "BAU")),
                   ""))
    checks.append(("Identifiability range is non-empty",
                   ident["consistent_emig_range"][1] > ident["consistent_emig_range"][0],
                   str(ident["consistent_emig_range"])))
    checks.append(("True PRCC for future emigration is negative",
                   sens["prcc"]["emig_future_mult"] < 0,
                   f"{sens['prcc']['emig_future_mult']:.3f}"))
    checks.append(("All scenarios positive",
                   all(central["scenarios"][k]["stock_2040"] > 0 for k in SCENARIOS),
                   ""))
    checks.append(("PRCCs within [-1, 1]",
                   all(-1.0001 <= v <= 1.0001 for v in sens["prcc"].values()), ""))

    # Flow identity for every scenario.
    flow_ok = True
    pipeline_ok = True
    nonneg_ok = True
    density_ok = True
    py_ok = True
    for key in SCENARIOS:
        o = simulate(p, scenario=_scen_dict(key), end_year=2040)
        for j in range(1, len(o["years"])):
            lhs = o["stock"][j] - o["stock"][j - 1]
            rhs = (o["entries"][j] - o["emig_post"][j]
                   + o["returns_net"][j] - o["retirements"][j]
                   - o["deaths"][j])
            if abs(lhs - rhs) > 1e-6:
                flow_ok = False
                break
        for j, y in enumerate(o["years"]):
            if abs(o["entries"][j] + o["nonentry_total"][j]
                   - o["graduates"][j]) > 1e-6:
                pipeline_ok = False
                break
        if any((d < -1e-9).any() for d in o["age_dist"].values()):
            nonneg_ok = False
        s = summarise(o)
        if abs(s["density_2040"] - o["stock"][-1] / POP[2040] * 1000) > 1e-9:
            density_ok = False
        if key != "BAU":
            py = summarise(o, base)["physician_years"]
            mask = np.array([y >= 2026 for y in o["years"]])
            if abs(py - float(np.sum((o["stock"] - base["stock"])[mask]))) > 1e-6:
                py_ok = False

    checks.append(("Workforce flow identity holds for all scenarios", flow_ok, ""))
    checks.append(("Graduate pipeline identity holds for all scenarios", pipeline_ok, ""))
    checks.append(("Age distributions non-negative", nonneg_ok, ""))
    checks.append(("Density calculation consistent", density_ok, ""))
    checks.append(("Physician-year calculation consistent", py_ok, ""))
    checks.append(("Emigration hazard cap does not bind centrally",
                   not central["bau"]["cap_binding_any"],
                   f"max hazard {central['bau']['max_emig_hazard']:.3f}"))
    checks.append(("Hazards in [0, 1]",
                   (retirement_hazard(0.0).max() <= 1.0
                    and retirement_hazard(0.0).min() >= 0.0
                    and mortality_hazard(1.0).max() <= 1.0), ""))
    checks.append(("MC intervals ordered",
                   all(mc[k]["lo"] <= mc[k]["median"] <= mc[k]["hi"]
                       for k in ("bau_stock_2040", "bau_stock_2030",
                                 "bau_stock_2035", "emig_total_2024")), ""))

    ok = all(c[1] for c in checks)
    lines = ["# Validation report\n", f"Overall: {'PASS' if ok else 'FAIL'}\n"]
    for name, passed, detail in checks:
        lines.append(f"- [{'x' if passed else ' '}] {name}" + (f" ({detail})" if detail else ""))
    with open(os.path.join(OUT, "validation_report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    if not ok:
        print("\n".join(lines))
    return ok


def write_environment():
    import matplotlib
    lines = [
        f"Python: {platform.python_version()}",
        f"Platform: {platform.platform()}",
        f"numpy: {np.__version__}",
        f"pandas: {pd.__version__}",
        f"scipy: {__import__('scipy').__version__}",
        f"matplotlib: {matplotlib.__version__}",
        f"Seed: {SEED}",
    ]
    with open(os.path.join(OUT, "environment.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Central calibration ...")
    central = run_central()
    print("  m_base =", round(central["params_central"]["m_base"], 1))
    print("  RMSE   =", round(central["fit"]["rmse"], 1))
    print("  BAU 2040 =", round(central["bau"]["stock_2040"]))

    print("Identifiability grid ...")
    ident = run_identifiability()

    print("Monte Carlo ...")
    df, diagnostics = run_mc(n=4000)
    mc = summarise_mc(df, diagnostics)

    print("Sensitivity ...")
    sens = run_sensitivity(df)

    print("Structural escalation ...")
    struct = run_structural(central)
    central["structural"] = struct

    print("Break-even ...")
    be = run_breakeven(central)

    print("Diaspora sensitivity ...")
    diaspora = run_diaspora_sensitivity(central)

    print("Graduate baselines ...")
    grads = run_graduate_baselines(central)

    print("Phi sensitivity ...")
    phi_sens = run_phi_sensitivity(central)
    print("Postgraduate lag sensitivity ...")
    lag_sens = run_lag_sensitivity(central)
    print("Initial age-shape sensitivity ...")
    age_sens = run_age_shape_sensitivity(central)
    print("Retirement and mortality sensitivity ...")
    ret_sens = run_retirement_sensitivity(central)

    print("Costs ...")
    costs = run_costs(central)

    print("Figures ...")
    plt = setup_mpl()
    fig_fit(plt, central, mc)
    fig_identifiability(plt, ident)
    fig_scenarios(plt, central, mc)
    fig_outcomes(plt, central, costs)
    fig_density(plt, central)
    fig_sensitivity(plt, sens)
    fig_age(plt, central)
    fig_structural(plt, central)
    fig_breakeven(plt, be)

    print("Tables ...")
    write_tables(central, mc, sens, ident, struct, be, costs, diaspora, grads)

    summary = {
        "central": central, "mc": mc, "sensitivity": sens,
        "identifiability": ident, "structural": struct, "breakeven": be,
        "costs": costs, "diaspora": diaspora, "graduate_baselines": grads,
        "phi_sensitivity": phi_sens, "lag_sensitivity": lag_sens,
        "age_shape_sensitivity": age_sens,
        "retirement_sensitivity": ret_sens,
    }
    with open(os.path.join(OUT, "results_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2,
                  default=lambda o: float(o) if isinstance(o, np.floating)
                  else (int(o) if isinstance(o, np.integer) else str(o)))

    write_key_numbers(central, mc, sens, ident, struct, be, costs,
                      diaspora, grads, phi_sens, lag_sens, age_sens, ret_sens)
    write_environment()
    ok = validate(central, mc, ident, sens)
    print("Validation:", "PASS" if ok else "FAIL")
    print("Key numbers written to outputs/key_numbers.md")
    print("Done. Outputs in", OUT)


if __name__ == "__main__":
    main()
