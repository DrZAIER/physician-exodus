"""
Analysis pipeline for the Tunisian physician workforce model.

Produces:
  - retrospective calibration and hindcast diagnostics
  - identifiability / flow-reconciliation analysis
  - policy scenario projections (central and alternative effect sizes)
  - Monte Carlo uncertainty analysis
  - deterministic and probabilistic sensitivity analysis
  - publication figures and tables
  - a JSON summary of all numbers cited in the manuscript
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import replace

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import beta as beta_dist
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(__file__))
from model import BASE_SCENARIO, Params, simulate  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "processed")
OUT = os.path.join(ROOT, "outputs")
FIG = os.path.join(OUT, "figures")
TAB = os.path.join(OUT, "tables")
for d in (OUT, FIG, TAB):
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------------------
# Observed data
# ---------------------------------------------------------------------------
stock = pd.read_csv(os.path.join(DATA, "tunisia_physician_workforce.csv"))
pop = pd.read_csv(os.path.join(DATA, "population_tunisia.csv"))
OBS = dict(zip(stock.year, stock.physicians_total))
OBS_2017_2024 = {y: OBS[y] for y in range(2017, 2025)}
POP = dict(zip(pop.year, pop.population))

CAL_YEARS = list(range(2017, 2025))
TARGET_2024 = OBS[2024]

# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------
# Central effect sizes. `emig_mult` scales post-entry emigration; `entry_retention`
# is the proportional reduction of pre-entry emigration (so it raises sigma);
# `return_mult` scales the annual return rate; `train_mult` scales graduates.
SCENARIOS = {
    "BAU": dict(label="Business as usual", **{k: BASE_SCENARIO[k] for k in
               ("emig_mult", "entry_retention", "return_mult", "train_mult")}),
    "REMUN": dict(label="Remuneration and working conditions",
                  emig_mult=0.70, entry_retention=0.30, return_mult=1.0, train_mult=1.0),
    "CAREER": dict(label="Professional development and career pathways",
                   emig_mult=0.85, entry_retention=0.15, return_mult=1.0, train_mult=1.0),
    "RETURN": dict(label="Return migration and diaspora reintegration",
                   emig_mult=1.0, entry_retention=0.0, return_mult=1.75, train_mult=1.0),
    "TRAINING": dict(label="Expanded domestic training capacity",
                     emig_mult=1.0, entry_retention=0.0, return_mult=1.0, train_mult=1.30),
    "COMBINED": dict(label="Combined retention and return strategy",
                     emig_mult=0.65, entry_retention=0.35, return_mult=1.75, train_mult=1.0),
}

# Alternative effect sizes (low / high) for scenario uncertainty
EFFECT_RANGE = {
    "BAU": [(1.0, 0.0, 1.0, 1.0), (1.0, 0.0, 1.0, 1.0)],
    "REMUN": [(0.85, 0.15, 1.0, 1.0), (0.55, 0.45, 1.0, 1.0)],
    "CAREER": [(0.92, 0.08, 1.0, 1.0), (0.75, 0.25, 1.0, 1.0)],
    "RETURN": [(1.0, 0.0, 1.35, 1.0), (1.0, 0.0, 2.50, 1.0)],
    "TRAINING": [(1.0, 0.0, 1.0, 1.15), (1.0, 0.0, 1.0, 1.50)],
    "COMBINED": [(0.78, 0.22, 1.35, 1.0), (0.55, 0.45, 2.50, 1.0)],
}

CENTRAL = Params(sigma=0.55, g_scale=1.0, initial_stock_2008=12600,
                 retire_shift=0.0, emig_tilt=1.0, rho=0.02)


def _scen_dict(key: str, effect=None) -> dict:
    s = SCENARIOS[key]
    if effect is None:
        return dict(emig_mult=s["emig_mult"], entry_retention=s["entry_retention"],
                    return_mult=s["return_mult"], train_mult=s["train_mult"],
                    name=s["label"])
    e = effect
    return dict(emig_mult=e[0], entry_retention=e[1], return_mult=e[2],
                train_mult=e[3], name=s["label"])


def calibrate_m(p: Params, target: float = TARGET_2024) -> float:
    """Solve the post-entry emigration flow that reproduces the 2024 stock."""
    def f(m):
        o = simulate(replace(p, m_base=m), end_year=2024)
        return o["stock"][-1] - target
    lo, hi = 0.0, 6000.0
    if f(lo) < 0:
        return 0.0
    if f(hi) > 0:
        return hi
    return brentq(f, lo, hi, xtol=0.5)


def history_fit(p: Params, o: dict) -> dict:
    years = list(o["years"])
    pred = np.array([o["stock"][years.index(y)] for y in CAL_YEARS])
    obs = np.array([OBS_2017_2024[y] for y in CAL_YEARS])
    mask = np.array([y not in (2020, 2021) for y in CAL_YEARS])
    return {
        "rmse": float(np.sqrt(np.mean((pred - obs) ** 2))),
        "rmse_excl_2020_21": float(np.sqrt(np.mean((pred[mask] - obs[mask]) ** 2))),
        "mape": float(np.mean(np.abs(pred - obs) / obs) * 100),
        "pred": dict(zip(CAL_YEARS, pred.round(0).astype(int).tolist())),
        "obs": OBS_2017_2024,
    }


def run_scenario(key: str, p: Params, effect=None, end_year: int = 2040) -> dict:
    return simulate(p, scenario=_scen_dict(key, effect), end_year=end_year)


def summarise(o: dict, base: dict | None = None, start: int = 2026) -> dict:
    years = list(o["years"])
    i = lambda y: years.index(y)  # noqa: E731
    mask = np.array([(y >= start) and (y <= 2040) for y in years])
    res = {
        "stock_2024": float(o["stock"][i(2024)]),
        "stock_2030": float(o["stock"][i(2030)]),
        "stock_2035": float(o["stock"][i(2035)]),
        "stock_2040": float(o["stock"][i(2040)]),
        "density_2024": float(o["stock"][i(2024)] / POP[2024] * 1000),
        "density_2040": float(o["stock"][i(2040)] / POP[2040] * 1000),
        "cum_emigration": float(np.sum((o["emig_pre"] + o["emig_post"])[mask])),
        "cum_returns": float(np.sum(o["returns"][mask])),
        "cum_retirements": float(np.sum(o["retirements"][mask])),
        "emigration_2024": float((o["emig_pre"] + o["emig_post"])[i(2024)]),
        "returns_2024": float(o["returns"][i(2024)]),
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
    p = replace(CENTRAL, m_base=m)
    hist = simulate(p, end_year=2024)
    base = simulate(p, end_year=2040)

    out = {
        "params_central": {
            "sigma": p.sigma, "g_scale": p.g_scale, "m_base": m,
            "rho": p.rho, "retire_shift": p.retire_shift,
            "initial_stock_2008": p.initial_stock_2008,
        },
        "fit": history_fit(p, hist),
        "bau": summarise(base),
        "scenarios": {},
    }
    for k in SCENARIOS:
        o = run_scenario(k, p)
        out["scenarios"][k] = summarise(o, base)
        # alternative effect sizes
        lo, hi = EFFECT_RANGE[k]
        out["scenarios"][k]["stock_2040_low"] = summarise(
            run_scenario(k, p, lo), base)["stock_2040"]
        out["scenarios"][k]["stock_2040_high"] = summarise(
            run_scenario(k, p, hi), base)["stock_2040"]
        out["scenarios"][k]["py_low"] = summarise(run_scenario(k, p, lo), base)["physician_years"]
        out["scenarios"][k]["py_high"] = summarise(run_scenario(k, p, hi), base)["physician_years"]

        # same scenario under escalating emigration intensity (+3%/yr)
        pe = replace(p, emig_growth=0.03)
        oe = run_scenario(k, pe)
        base_e = simulate(pe, end_year=2040)
        out["scenarios"][k]["stock_2040_escalating"] = summarise(oe)["stock_2040"]
        out["scenarios"][k]["py_escalating"] = summarise(oe, base_e)["physician_years"]

    # store trajectories
    traj = {"years": base["years"].tolist(), "BAU": base["stock"].tolist()}
    for k in SCENARIOS:
        if k == "BAU":
            continue
        traj[k] = run_scenario(k, p)["stock"].tolist()
    out["trajectories"] = traj

    # store observed
    out["observed"] = {int(k): int(v) for k, v in OBS.items()}
    out["population"] = {int(k): int(v) for k, v in POP.items()}
    return out


# ---------------------------------------------------------------------------
# 2. Identifiability / flow reconciliation
# ---------------------------------------------------------------------------
def run_identifiability() -> dict:
    sigmas = np.round(np.arange(0.30, 0.81, 0.05), 2)
    gscales = np.round(np.arange(0.85, 1.51, 0.05), 2)
    rows = []
    for gs in gscales:
        for s in sigmas:
            p = replace(CENTRAL, sigma=float(s), g_scale=float(gs))
            m = calibrate_m(p)
            o = simulate(replace(p, m_base=m), end_year=2024)
            fit = history_fit(p, o)
            i24 = list(o["years"]).index(2024)
            rows.append({
                "sigma": float(s), "g_scale": float(gs), "m_base": float(m),
                "rmse": fit["rmse"],
                "emig_post_2024": float(o["emig_post"][i24]),
                "emig_pre_2024": float(o["emig_pre"][i24]),
                "emig_total_2024": float(o["emig_post"][i24] + o["emig_pre"][i24]),
                "entry_2024": float(o["entries"][i24]),
            })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(TAB, "identifiability_grid.csv"), index=False)
    return rows


# ---------------------------------------------------------------------------
# 3. Monte Carlo uncertainty
# ---------------------------------------------------------------------------
def draw_params(rng: np.random.Generator) -> Params:
    # sigma ~ Beta with mean .55, sd .07
    mean, sd = 0.55, 0.07
    k = mean * (1 - mean) / sd**2 - 1
    sigma = float(beta_dist.rvs(mean * k, (1 - mean) * k, random_state=rng))
    gs = float(np.exp(rng.normal(0, 0.12)))
    tilt = float(np.exp(rng.normal(0, 0.15)))
    shift = float(rng.uniform(-1.5, 1.5))
    rho_mean, rho_sd = 0.020, 0.008
    kr = rho_mean * (1 - rho_mean) / rho_sd**2 - 1
    rho = float(beta_dist.rvs(rho_mean * kr, (1 - rho_mean) * kr, random_state=rng))
    init = float(rng.normal(12600, 300))
    return Params(sigma=sigma, g_scale=gs, emig_tilt=tilt, retire_shift=shift,
                  rho=rho, initial_stock_2008=init)


def run_mc(n: int = 2000, seed: int = 20261121) -> dict:
    rng = np.random.default_rng(seed)
    draws = []
    for j in range(n):
        p0 = draw_params(rng)
        m = calibrate_m(p0)
        p = replace(p0, m_base=m)
        m_resid = float(np.exp(rng.normal(0, 0.06)))
        p = replace(p, m_base=m * m_resid)
        base = simulate(p, end_year=2040)
        rec = {"draw": j, "sigma": p.sigma, "g_scale": p.g_scale,
               "m_base": p.m_base, "rho": p.rho, "retire_shift": p.retire_shift,
               "emig_tilt": p.emig_tilt, "initial_stock_2008": p.initial_stock_2008}
        rec.update({f"bau_{k}": v for k, v in summarise(base).items()})
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
    return df


def summarise_mc(df: pd.DataFrame) -> dict:
    def q(s):
        return {"median": float(s.median()), "lo": float(s.quantile(0.05)),
                "hi": float(s.quantile(0.95)), "p25": float(s.quantile(0.25)),
                "p75": float(s.quantile(0.75))}

    out = {"n": int(len(df))}
    for c in ["bau_stock_2024", "bau_stock_2030", "bau_stock_2035", "bau_stock_2040",
              "bau_density_2040", "bau_cum_emigration", "bau_cum_returns"]:
        out[c] = q(df[c])
    for key in SCENARIOS:
        if key == "BAU":
            continue
        out[f"{key}_stock_2040"] = q(df[f"{key}_stock_2040"])
        out[f"{key}_py"] = q(df[f"{key}_py"])
    out["prob_bau_below_2024"] = float((df["bau_stock_2040"] < df["bau_stock_2024"]).mean())
    cols = ["REMUN_stock_2040", "CAREER_stock_2040", "RETURN_stock_2040",
            "TRAINING_stock_2040", "COMBINED_stock_2040"]
    X = df[cols].values
    out["rank_combined_first"] = float((X.argmax(axis=1) == 4).mean())
    out["rank_training_last"] = float((X.argmin(axis=1) == 3).mean())
    return out


# ---------------------------------------------------------------------------
# 3b. Structural sensitivity: escalation of emigration after 2024
# ---------------------------------------------------------------------------
def run_structural(central: dict) -> dict:
    p = replace(CENTRAL, m_base=central["params_central"]["m_base"])
    out = {}
    for g in [0.0, 0.03, 0.05, 0.07]:
        o = simulate(replace(p, emig_growth=g), end_year=2040)
        s = summarise(o)
        s["trajectory"] = o["stock"].tolist()
        s["years"] = o["years"].tolist()
        out[f"{g:.2f}"] = s
    with open(os.path.join(TAB, "structural_emigration_scenarios.csv"), "w") as f:
        f.write("annual_growth_in_emigration,stock_2030,stock_2040,cum_emigration\n")
        for g, s in out.items():
            f.write(f"{g},{s['stock_2030']:.0f},{s['stock_2040']:.0f},{s['cum_emigration']:.0f}\n")
    return out


# ---------------------------------------------------------------------------
# 4. Sensitivity
# ---------------------------------------------------------------------------
def run_sensitivity(df: pd.DataFrame) -> dict:
    params = ["sigma", "g_scale", "m_base", "rho", "retire_shift", "emig_tilt",
              "initial_stock_2008"]
    y = df["bau_stock_2040"].values
    prcc = {}
    for p in params:
        rho_s, _ = spearmanr(df[p].values, y)
        prcc[p] = float(rho_s)
    # OAT tornado around the central calibration
    m0 = calibrate_m(CENTRAL)
    p0 = replace(CENTRAL, m_base=m0)
    base = simulate(p0, end_year=2040)["stock"][-1]
    tornado = {}
    for p in params:
        if p == "m_base":
            continue
        vals = df[p]
        lo, hi = vals.quantile(0.10), vals.quantile(0.90)
        res = {}
        for lab, v in (("low", lo), ("high", hi)):
            pp = replace(p0, **{p: float(v)})
            pp = replace(pp, m_base=calibrate_m(pp))
            res[lab] = float(simulate(pp, end_year=2040)["stock"][-1] - base)
        tornado[p] = res
    return {"prcc": prcc, "tornado": tornado, "base_2040": float(base)}


# ---------------------------------------------------------------------------
# 5. Figures
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


COL = {"BAU": "#4D4D4D", "REMUN": "#1B7837", "CAREER": "#762A83",
       "RETURN": "#E08214", "TRAINING": "#2166AC", "COMBINED": "#B2182B"}


def fig_fit(plt, central, mc_summary):
    years = np.array(central["trajectories"]["years"])
    bau = np.array(central["trajectories"]["BAU"])
    obs = central["observed"]
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    oy = sorted(obs)
    ax.scatter(oy, [obs[y] for y in oy], s=16, color="black", zorder=5,
               label="Observed (INS / Ministry of Health)")
    mask = years <= 2024
    ax.plot(years[mask], bau[mask], color="#2166AC", lw=1.8,
            label="Model, retrospective fit")
    ax.plot(years[~mask], bau[~mask], color="#2166AC", lw=1.8, ls="--",
            label="Baseline projection")
    lo = mc_summary["bau_stock_2040"]["lo"]
    hi = mc_summary["bau_stock_2040"]["hi"]
    ax.fill_between([2024, 2040], [bau[mask][-1], lo], [bau[mask][-1], hi],
                    color="#2166AC", alpha=0.12, lw=0, label="90% uncertainty interval")
    ax.axvline(2024, color="grey", lw=0.7, ls=":")
    ax.set_ylabel("Physicians in practice")
    ax.set_xlabel("Year")
    ax.set_xlim(2010, 2040)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.savefig(os.path.join(FIG, "fig1_historical_fit_and_baseline.png"))
    fig.savefig(os.path.join(FIG, "fig1_historical_fit_and_baseline.pdf"))
    plt.close(fig)


def fig_identifiability(plt):
    df = pd.read_csv(os.path.join(TAB, "identifiability_grid.csv"))
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2))
    # panel A: RMSE surface
    piv = df.pivot(index="g_scale", columns="sigma", values="rmse")
    im = axes[0].imshow(piv.values, origin="lower", aspect="auto",
                        extent=[piv.columns.min(), piv.columns.max(),
                                piv.index.min(), piv.index.max()],
                        cmap="viridis_r")
    axes[0].set_xlabel("Pipeline retention, σ (share of graduates entering practice)")
    axes[0].set_ylabel("Training-output multiplier")
    axes[0].set_title("A. Retrospective fit (RMSE)", loc="left", fontsize=9)
    cb = fig.colorbar(im, ax=axes[0], fraction=0.046, pad=0.02)
    cb.set_label("RMSE (physicians)", fontsize=7.5)

    # panel B: implied total emigration
    piv2 = df.pivot(index="g_scale", columns="sigma", values="emig_total_2024")
    cs = axes[1].contourf(piv2.columns, piv2.index, piv2.values, levels=12, cmap="YlOrRd")
    axes[1].set_xlabel("Pipeline retention, σ")
    axes[1].set_ylabel("Training-output multiplier")
    axes[1].set_title("B. Implied total emigration in 2024", loc="left", fontsize=9)
    cb2 = fig.colorbar(cs, ax=axes[1], fraction=0.046, pad=0.02)
    cb2.set_label("Physicians per year", fontsize=7.5)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig2_identifiability.png"))
    fig.savefig(os.path.join(FIG, "fig2_identifiability.pdf"))
    plt.close(fig)


def fig_scenarios(plt, central, mc_summary):
    years = np.array(central["trajectories"]["years"])
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.7), sharey=True)
    mask = years >= 2024

    base = np.array(central["trajectories"]["BAU"])
    fan_lo = np.linspace(base[years == 2024][0], mc_summary["bau_stock_2040"]["lo"], mask.sum())
    fan_hi = np.linspace(base[years == 2024][0], mc_summary["bau_stock_2040"]["hi"], mask.sum())
    axes[0].fill_between(years[mask], fan_lo, fan_hi, color="#4D4D4D", alpha=0.12,
                         lw=0, label="Baseline 90% interval")
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
    axes[0].set_xlim(2024, 2040)

    # Panel B: escalating emigration (+3%/yr), deterministic scenario comparison
    from model import simulate
    from dataclasses import replace
    p = replace(CENTRAL, m_base=central["params_central"]["m_base"], emig_growth=0.03)
    base_e = simulate(p, end_year=2040)
    axes[1].plot(years[mask], base_e["stock"][mask], color=COL["BAU"], lw=1.8, ls="--",
                 label="Business as usual")
    for k in ["REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"]:
        o = run_scenario(k, p)
        axes[1].plot(years[mask], o["stock"][mask], color=COL[k], lw=1.8,
                     label=SCENARIOS[k]["label"])
    axes[1].set_title("B. Emigration intensity rising 3%/year", loc="left", fontsize=9)
    axes[1].set_xlim(2024, 2040)

    for ax in axes:
        ax.set_xlabel("Year")
    axes[0].set_ylabel("Physicians in practice")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, fontsize=7, ncol=4,
               loc="lower center", bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    fig.savefig(os.path.join(FIG, "fig3_scenarios.png"))
    fig.savefig(os.path.join(FIG, "fig3_scenarios.pdf"))
    plt.close(fig)


def fig_outcomes(plt, central, mc_summary):
    keys = ["REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"]
    labels = ["Remuneration", "Career", "Return", "Training", "Combined"]
    fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.2))
    x = np.arange(len(keys))

    # A. stock in 2040
    med = [central["scenarios"][k]["stock_2040"] for k in keys]
    lo = [central["scenarios"][k]["stock_2040_low"] for k in keys]
    hi = [central["scenarios"][k]["stock_2040_high"] for k in keys]
    axes[0].bar(x, med, color=[COL[k] for k in keys], alpha=0.85, width=0.65)
    axes[0].errorbar(x, med, yerr=[np.array(med) - lo, np.array(hi) - med],
                     fmt="none", ecolor="black", capsize=2, lw=0.8)
    axes[0].axhline(central["bau"]["stock_2040"], color="black", ls="--", lw=0.9)
    axes[0].set_xticks(x, labels, fontsize=7, rotation=20)
    axes[0].set_ylabel("Physicians in 2040")
    axes[0].set_title("A. Workforce size", loc="left", fontsize=9)

    # B. cumulative emigration
    med = [central["scenarios"][k]["cum_emigration"] for k in keys]
    axes[1].bar(x, med, color=[COL[k] for k in keys], alpha=0.85, width=0.65)
    axes[1].axhline(central["bau"]["cum_emigration"], color="black", ls="--", lw=0.9)
    axes[1].set_xticks(x, labels, fontsize=7, rotation=20)
    axes[1].set_ylabel("Cumulative emigrants, 2026–2040")
    axes[1].set_title("B. Emigration", loc="left", fontsize=9)

    # C. physician-years retained
    med = [central["scenarios"][k]["physician_years"] for k in keys]
    lo = [central["scenarios"][k]["py_low"] for k in keys]
    hi = [central["scenarios"][k]["py_high"] for k in keys]
    axes[2].bar(x, med, color=[COL[k] for k in keys], alpha=0.85, width=0.65)
    axes[2].errorbar(x, med, yerr=[np.array(med) - lo, np.array(hi) - med],
                     fmt="none", ecolor="black", capsize=2, lw=0.8)
    axes[2].axhline(0, color="black", lw=0.8)
    axes[2].set_xticks(x, labels, fontsize=7, rotation=20)
    axes[2].set_ylabel("Physician-years retained vs BAU")
    axes[2].set_title("C. Cumulative retention benefit", loc="left", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig4_policy_outcomes.png"))
    fig.savefig(os.path.join(FIG, "fig4_policy_outcomes.pdf"))
    plt.close(fig)


def fig_density(plt, central):
    years = np.array(central["trajectories"]["years"])
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    for k, lab in [("BAU", "Business as usual"), ("COMBINED", "Combined strategy")]:
        mask = years >= 2010
        dens = (np.array(central["trajectories"][k])[mask]
                / np.array([POP[int(y)] for y in years[mask]]) * 1000)
        ax.plot(years[mask], dens, color=COL[k], lw=2, ls="--" if k == "BAU" else "-", label=lab)
    ax.set_xlim(2015, 2040)
    ax.set_ylabel("Physicians per 1,000 population")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, fontsize=7.5)
    fig.savefig(os.path.join(FIG, "fig5_density.png"))
    fig.savefig(os.path.join(FIG, "fig5_density.pdf"))
    plt.close(fig)


def fig_sensitivity(plt, sens):
    t = sens["tornado"]
    labels = {
        "sigma": "Pipeline retention (σ)", "g_scale": "Training output",
        "rho": "Return rate", "retire_shift": "Retirement age",
        "emig_tilt": "Age profile of emigration",
        "initial_stock_2008": "Initial stock (2008)",
    }
    items = sorted(t.items(), key=lambda kv: abs(kv[1]["high"] - kv[1]["low"]))
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    for i, (k, v) in enumerate(items):
        ax.barh(i, v["low"], color="#2166AC", alpha=0.8, height=0.6)
        ax.barh(i, v["high"], color="#B2182B", alpha=0.8, height=0.6)
    ax.set_yticks(range(len(items)), [labels.get(k, k) for k, _ in items], fontsize=7.5)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("Change in 2040 workforce vs central calibration")
    from matplotlib.patches import Patch
    handles = [Patch(color="#2166AC", alpha=0.8, label="Parameter at 10th percentile"),
               Patch(color="#B2182B", alpha=0.8, label="Parameter at 90th percentile")]
    ax.legend(handles=handles, frameon=False, fontsize=7, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig6_sensitivity.png"))
    fig.savefig(os.path.join(FIG, "fig6_sensitivity.pdf"))
    plt.close(fig)


def fig_age(plt, central):
    # Age structure in 2024 and 2040 under BAU and combined strategy
    from model import AGES
    m = central["params_central"]["m_base"]
    p = replace(CENTRAL, m_base=m)
    o24 = simulate(p, end_year=2024)
    b = simulate(p, end_year=2040)
    c = run_scenario("COMBINED", p)
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    bins = [(25, 34), (35, 44), (45, 54), (55, 64), (65, 75)]
    labels = ["25–34", "35–44", "45–54", "55–64", "65+"]
    def shares(d):
        return [d[(AGES >= a) & (AGES <= b)].sum() / d.sum() * 100 for a, b in bins]
    x = np.arange(len(bins))
    ax.bar(x - 0.2, shares(o24["age_dist"][2024]), width=0.4, color="#4D4D4D", label="2024")
    ax.bar(x, shares(b["age_dist"][2040]), width=0.4, color="#2166AC", label="2040, BAU")
    ax.bar(x + 0.2, shares(c["age_dist"][2040]), width=0.4, color="#B2182B", label="2040, combined")
    ax.set_xticks(x, labels)
    ax.set_ylabel("% of practising physicians")
    ax.set_xlabel("Age group (years)")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig7_age_structure.png"))
    fig.savefig(os.path.join(FIG, "fig7_age_structure.pdf"))
    plt.close(fig)


def fig_structural(plt, struct):
    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    cols = {"0.00": "#4D4D4D", "0.03": "#E08214", "0.05": "#B2182B", "0.07": "#67001F"}
    labs = {"0.00": "Constant emigration intensity (baseline)",
            "0.03": "Emigration intensity +3%/year",
            "0.05": "Emigration intensity +5%/year",
            "0.07": "Emigration intensity +7%/year"}
    for g, s in struct.items():
        y = np.array(s["years"])
        ax.plot(y[y >= 2024], np.array(s["trajectory"])[y >= 2024],
                color=cols[g], lw=2, label=labs[g])
    ax.axhline(15315, color="grey", ls=":", lw=0.8)
    ax.set_xlim(2024, 2040)
    ax.set_ylabel("Physicians in practice")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig8_structural_emigration.png"))
    fig.savefig(os.path.join(FIG, "fig8_structural_emigration.pdf"))
    plt.close(fig)


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------
def write_tables(central, mc_summary, sens):
    # Data sources table
    data_rows = [
        ["Physicians in active practice", "INS / Ministry of Health; carte sanitaire", "2017–2024", "Public-sector physicians plus private practitioners; excludes most residents; 2020 public count affected by reporting change"],
        ["Physicians registered with the CNOM", "CNOM", "2009–2026", "All inscriptions, including inactive, retired, administrative and deceased physicians; not a practising count"],
        ["Medical graduates", "Zehnati 2024; ministerial statements", "2013–2025", "Medicine graduates only; series reconstructed; recent values uncertain"],
        ["Emigration proxies", "CNOM via ITES; press", "2011–2024", "Certificates of good conduct, removal requests, departure files and union/CNOM estimates; not comparable"],
        ["Tunisian physicians in France", "CNOM France", "2010–2023", "Registered with the French Order; excludes unregistered physicians"],
        ["Tunisian physicians in Germany", "German medical statistics via ITES", "2022", "Country-of-training/nationality definition"],
        ["Tunisian-born physicians in OECD countries", "OECD", "2010/11, 2015/16", "Country-of-birth estimate; lower bound"],
        ["Population", "INS 2024 census; UN WPP 2024", "2010–2040", "2024 census 11,972,169; WPP rescaled"],
    ]
    pd.DataFrame(data_rows, columns=["Quantity", "Source", "Period", "Definition and limitations"]).to_csv(
        os.path.join(TAB, "table1_data_sources.csv"), index=False)

    # Parameters table
    rows = [
        ["Physicians in practice, 2024", "15,315", "—", "Observed", "INS / Ministry of Health"],
        ["Physicians in practice, 2017–2024", "14,892–15,315", "—", "Observed", "INS / Ministry of Health"],
        ["Annual medical graduates, 2021", "1,128", "987 (2013) – 1,900 (2025, ministerial statement)", "Observed / reconstructed", "Zehnati 2024; press"],
        ["Share of graduates entering the Tunisian practising stock (σ)", "0.55", "0.30–0.80", "Estimated (calibrated, weakly identified)", "Model calibration; flow reconciliation"],
        ["Post-entry emigration flow, 2024 (m)", f"{central['params_central']['m_base']:.0f}", "calibrated per draw", "Estimated (calibrated, weakly identified)", "Model calibration"],
        ["Total emigration, 2024", f"{central['bau']['emigration_2024']:.0f}", "600–1,500", "Estimated (model-consistent)", "Derived; compare CNOM/press 1,300–1,450"],
        ["Pre-entry share of emigration", "0.45", "0.20–0.70", "Assumption (implied by σ)", "Model structure"],
        ["Retirement age", "60–62 (public); 60 (private); 65–70 (academic)", "±1.5 years", "Observed (legal) + assumption", "Law 2019-37; CNRPS/CNSS"],
        ["Return rate from diaspora (ρ)", "0.020", "0.005–0.040", "Assumption", "No Tunisian data; informed by Varga 2017"],
        ["Initial diaspora stock, 2008", "4,000", "3,200–6,000", "Indirect estimate", "OECD 2018; CNOM France; German statistics"],
        ["Population, 2024", "11.89 million", "—", "Observed", "INS 2024 census"],
        ["Population growth, 2024–2040", "0.33%/yr", "UN WPP medium variant", "Projected", "UN WPP 2024"],
    ]
    pd.DataFrame(rows, columns=["Parameter", "Central value", "Range / alternative",
                                "Status", "Source"]).to_csv(
        os.path.join(TAB, "table2_parameters.csv"), index=False)

    # Scenario table
    rows = []
    for k, s in SCENARIOS.items():
        lo, hi = EFFECT_RANGE[k]
        rows.append([k, s["label"], s["emig_mult"], s["entry_retention"],
                     s["return_mult"], s["train_mult"],
                     f"{lo[0]:.2f}/{lo[1]:.2f}/{lo[2]:.2f}/{lo[3]:.2f}",
                     f"{hi[0]:.2f}/{hi[1]:.2f}/{hi[2]:.2f}/{hi[3]:.2f}"])
    pd.DataFrame(rows, columns=["Code", "Scenario", "Emigration multiplier",
                                "Pre-entry emigration reduction", "Return-rate multiplier",
                                "Training multiplier", "Low effect", "High effect"]).to_csv(
        os.path.join(TAB, "table3_scenarios.csv"), index=False)

    # Results table
    rows = []
    for k in ["BAU", "REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"]:
        r = central["scenarios"].get(k, central["bau"])
        rows.append([k, r["stock_2030"], r["stock_2040"], r["density_2040"],
                     r["cum_emigration"], r["cum_returns"],
                     r.get("physician_years", 0),
                     r.get("stock_2040_low", np.nan), r.get("stock_2040_high", np.nan),
                     r.get("stock_2040_escalating", np.nan),
                     r.get("py_escalating", np.nan)])
    df = pd.DataFrame(rows, columns=["Scenario", "Workforce 2030", "Workforce 2040",
                                "Density 2040 (/1000)", "Cumulative emigration 2026–2040",
                                "Cumulative returns 2026–2040", "Physician-years vs BAU",
                                "Workforce 2040, low effect", "Workforce 2040, high effect",
                                "Workforce 2040, escalating emigration",
                                "Physician-years vs BAU, escalating"])
    df["Density 2040 (/1000)"] = df["Density 2040 (/1000)"].round(2)
    num_cols = [c for c in df.columns if c not in ("Scenario", "Density 2040 (/1000)")]
    df[num_cols] = df[num_cols].round(1)
    df.to_csv(os.path.join(TAB, "table4_results.csv"), index=False)

    # MC summary table
    rows = []
    for k in ["BAU", "REMUN", "CAREER", "RETURN", "TRAINING", "COMBINED"]:
        key = "bau_stock_2040" if k == "BAU" else f"{k}_stock_2040"
        q = mc_summary[key]
        py = "—" if k == "BAU" else (
            f"{mc_summary[f'{k}_py']['median']:.0f} "
            f"({mc_summary[f'{k}_py']['lo']:.0f} to {mc_summary[f'{k}_py']['hi']:.0f})")
        rows.append([k, f"{q['median']:.0f} ({q['lo']:.0f}–{q['hi']:.0f})", py])
    pd.DataFrame(rows, columns=["Scenario", "Workforce 2040, median (90% interval)",
                                "Physician-years vs BAU, median (90% interval)"]).to_csv(
        os.path.join(TAB, "table5_uncertainty.csv"), index=False)

    # Flow decomposition table
    m0 = central["params_central"]["m_base"]
    p0 = replace(CENTRAL, m_base=m0)
    o = simulate(p0, end_year=2040)
    rows = []
    for y in [2017, 2020, 2024, 2030, 2035, 2040]:
        i = list(o["years"]).index(y)
        rows.append([y, round(o["stock"][i]), round(o["entries"][i]),
                     round(o["emig_pre"][i]), round(o["emig_post"][i]),
                     round(o["returns"][i]), round(o["retirements"][i]),
                     round(o["deaths"][i]),
                     round(o["stock"][i] - o["stock"][i - 1]),
                     round(o["stock"][i] / POP[y] * 1000, 2)])
    pd.DataFrame(rows, columns=["Year", "Stock", "Entries", "Pre-entry emigration",
                                "Post-entry emigration", "Returns", "Retirements",
                                "Deaths", "Net change", "Density (/1000)"]).to_csv(
        os.path.join(TAB, "table7_flow_decomposition.csv"), index=False)

    # Sensitivity table
    rows = [[k, v["low"], v["high"], sens["prcc"].get(k, np.nan)]
            for k, v in sens["tornado"].items()]
    pd.DataFrame(rows, columns=["Parameter", "Change low", "Change high", "PRCC"]).to_csv(
        os.path.join(TAB, "table6_sensitivity.csv"), index=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Central calibration ...")
    central = run_central()
    print("  m_base =", central["params_central"]["m_base"])
    print("  RMSE   =", central["fit"]["rmse"])
    print("  BAU 2040 =", round(central["bau"]["stock_2040"]))

    print("Identifiability grid ...")
    run_identifiability()

    print("Monte Carlo ...")
    df = run_mc(n=2000)
    mc = summarise_mc(df)

    print("Sensitivity ...")
    sens = run_sensitivity(df)
    print("Structural emigration scenarios ...")
    struct = run_structural(central)

    print("Figures ...")
    plt = setup_mpl()
    fig_fit(plt, central, mc)
    fig_identifiability(plt)
    fig_scenarios(plt, central, mc)
    fig_outcomes(plt, central, mc)
    fig_density(plt, central)
    fig_sensitivity(plt, sens)
    fig_age(plt, central)
    fig_structural(plt, struct)

    write_tables(central, mc, sens)

    summary = {"central": central, "mc": mc, "sensitivity": sens, "structural": struct}
    with open(os.path.join(OUT, "results_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=lambda o: float(o) if isinstance(o, np.floating) else str(o))
    print("Done. Outputs in", OUT)


if __name__ == "__main__":
    main()
