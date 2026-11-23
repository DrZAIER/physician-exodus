"""
Annual cohort-component (stock-and-flow) model of the Tunisian physician workforce.

Structure and nomenclature follow the supply side of the JRC SANDEM framework
(Bernini et al., 2024): an age-structured stock of practising physicians is
updated each year by entries (graduates surviving postgraduate training),
emigration, return migration, retirement and mortality.

The model is deliberately parsimonious: emigration is represented as a total
annual flow allocated across ages by an assumed age profile, not as a set of
separately estimated age-specific rates. This reflects the fact that Tunisian
age-specific emigration flows are not observed.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, Optional

import numpy as np

# ----------------------------------------------------------------------------
# Age grid
# ----------------------------------------------------------------------------
AGE_MIN = 25
AGE_MAX = 75  # 75 means "75 and over"
AGES = np.arange(AGE_MIN, AGE_MAX + 1)
N_AGES = len(AGES)


def _idx(age: int) -> int:
    return int(np.clip(age - AGE_MIN, 0, N_AGES - 1))


# ----------------------------------------------------------------------------
# Parameters
# ----------------------------------------------------------------------------
@dataclass
class Params:
    # Pipeline
    sigma: float = 0.55          # share of graduates who enter the Tunisian practising stock
    entry_lag: int = 5           # years between doctorate and independent practice
    g_scale: float = 1.0         # multiplier on the graduate series (training output)

    # Emigration (post-entry flow, annual number at 2024 intensity)
    m_base: float = 350.0
    emig_tilt: float = 1.0       # >1 shifts emigration towards older ages

    # Return migration
    rho: float = 0.020           # annual return rate from the diaspora stock

    # Structural trend in emigration intensity after 2024 (0 = constant)
    emig_growth: float = 0.0

    # Retirement
    retire_shift: float = 0.0    # years added to (positive) or removed from legal ages

    # Initial conditions
    initial_stock_2008: float = 12300.0
    initial_diaspora_2008: float = 4000.0

    # Numerical
    max_emig_hazard: float = 0.35


# Age-specific emigration weights (relative risk by age)
def emigration_weights(tilt: float = 1.0) -> np.ndarray:
    base = {
        25: 0.85, 30: 1.00, 35: 0.60, 40: 0.35, 45: 0.20,
        50: 0.10, 55: 0.04, 60: 0.02, 65: 0.01, 70: 0.005, 75: 0.002,
    }
    w = np.array([base[min((a // 5) * 5, 75)] for a in AGES], dtype=float)
    # tilt > 1 gives relatively more weight to older physicians
    w = w * np.power(tilt, (AGES - 30) / 10.0)
    return w / w.sum()


# Retirement hazard by single year of age (legal ages 60-62 in Tunisia,
# academics may stay to 65-70)
def retirement_hazard(shift: float = 0.0) -> np.ndarray:
    r = np.zeros(N_AGES)
    for i, a in enumerate(AGES):
        x = a - shift
        if x < 60:
            r[i] = 0.0
        elif x < 62:
            r[i] = 0.20
        elif x < 63:
            r[i] = 0.45
        elif x < 65:
            r[i] = 0.35
        elif x < 70:
            r[i] = 0.45
        else:
            r[i] = 1.0
    return r


def mortality_hazard() -> np.ndarray:
    q = np.zeros(N_AGES)
    for i, a in enumerate(AGES):
        if a < 55:
            q[i] = 0.0010
        elif a < 65:
            q[i] = 0.0040
        elif a < 75:
            q[i] = 0.0150
        else:
            q[i] = 0.0500
    return q


# Entry age distribution (after a 5-year postgraduate pathway)
ENTRY_AGES = {29: 0.15, 30: 0.30, 31: 0.30, 32: 0.15, 33: 0.10}

# Return-migration age distribution
RETURN_AGES = {33: 0.10, 35: 0.20, 38: 0.25, 41: 0.20, 45: 0.15, 50: 0.10}


def initial_distribution(initial_stock: float) -> np.ndarray:
    """Age distribution of CNOM-registered physicians in 2008, spread to single years.

    Source: CNOM 2007-2008 report, table of physicians by age group
    (25-30: 2000; 30-35: 2109; 35-40: 2468; 40-45: 1946; 45-50: 2041;
     50-55: 1241; 55-60: 535; 60-65: 144; 65+: 132).
    The distribution is scaled to the 2008 practising stock (WHO: 12,996 in 2010;
    12,300 used for 2008).
    """
    bands = {
        25: 2000, 30: 2109, 35: 2468, 40: 1946, 45: 2041,
        50: 1241, 55: 535, 60: 144, 65: 100, 70: 32,
    }
    d = np.zeros(N_AGES)
    for start, n in bands.items():
        for a in range(start, min(start + 5, AGE_MAX + 1)):
            d[_idx(a)] += n / 5.0
    return d / d.sum() * initial_stock


# ----------------------------------------------------------------------------
# Exogenous series
# ----------------------------------------------------------------------------
def graduates(year: int, g_scale: float = 1.0, train_mult: float = 1.0) -> float:
    """Annual medical graduates (doctorate), Tunisia.

    Anchors: ~600/yr in the early 2000s (press), 987 in 2013 and 1,128 in 2021
    (Zehnati 2024, Belgeo), with a reported acceleration towards ~1,300 by 2024.
    Growth of 1.7%/yr is applied outside the anchored period. `train_mult`
    implements a training-capacity scenario (applied from 2031, i.e. six years
    after an admissions increase).
    """
    if year <= 2021:
        g = 987.0 * (1.017 ** (year - 2013))
    elif year <= 2024:
        g = 1128.0 * (1.05 ** (year - 2021))
    else:
        # Training capacity is held constant in the baseline: continued
        # expansion is a policy scenario, not a trend extrapolation.
        g = 1305.0
    if year >= 2031:
        g *= train_mult
    return g * g_scale


def emigration_trend(year: int) -> float:
    """Relative intensity of post-entry emigration, normalised to 1 in 2024."""
    if year <= 2017:
        return 0.60
    if year <= 2024:
        return 0.60 + 0.40 * (year - 2017) / 7.0
    return 1.0


# ----------------------------------------------------------------------------
# Scenario handling
# ----------------------------------------------------------------------------
BASE_SCENARIO = {
    "name": "Business as usual",
    "emig_mult": 1.0,        # multiplier on post-entry emigration
    "entry_retention": 0.0,  # proportional reduction of PRE-entry emigration
    "return_mult": 1.0,      # multiplier on the return rate
    "train_mult": 1.0,       # multiplier on graduates from 2031
    "start_year": 2026,
    "ramp_years": 3,
}


def _ramp(year: int, scen: Dict) -> float:
    """Linear phase-in of a policy effect between start_year and start+ramp."""
    s = scen.get("start_year", 2026)
    r = max(1, scen.get("ramp_years", 3))
    if year < s:
        return 0.0
    return min(1.0, (year - s + 1) / r)


# ----------------------------------------------------------------------------
# Simulation
# ----------------------------------------------------------------------------
def simulate(
    params: Params,
    scenario: Optional[Dict] = None,
    start_year: int = 2008,
    end_year: int = 2040,
) -> Dict[str, np.ndarray]:
    scen = dict(BASE_SCENARIO)
    if scenario:
        scen.update(scenario)

    r = retirement_hazard(params.retire_shift)
    q = mortality_hazard()
    w = emigration_weights(params.emig_tilt)

    P = initial_distribution(params.initial_stock_2008)
    D = float(params.initial_diaspora_2008)

    years = np.arange(start_year, end_year + 1)
    out = {k: np.zeros(len(years)) for k in [
        "stock", "entries", "emig_post", "emig_pre", "returns", "retirements",
        "deaths", "diaspora", "graduates",
    ]}
    age_store = {}

    for j, t in enumerate(years):
        ramp = _ramp(t, scen) if t >= scen["start_year"] else 0.0

        # --- effective policy parameters -----------------------------------
        emig_mult = 1.0 + ramp * (scen["emig_mult"] - 1.0)
        pre_emig_reduction = ramp * scen["entry_retention"]
        sigma_eff = 1.0 - (1.0 - params.sigma) * (1.0 - pre_emig_reduction)
        return_mult = 1.0 + ramp * (scen["return_mult"] - 1.0)
        train_mult = scen["train_mult"] if t >= 2031 else 1.0

        # Structural escalation of emigration intensity after 2024
        growth = (1.0 + params.emig_growth) ** max(0, t - 2024)
        pre_share = min(0.90, (1.0 - sigma_eff) * growth)
        sigma_entry = 1.0 - pre_share

        # --- 1. entry of graduates ----------------------------------------
        g_cohort = graduates(t - params.entry_lag, params.g_scale, train_mult)
        entrants = g_cohort * sigma_entry
        for age, share in ENTRY_AGES.items():
            P[_idx(age)] += entrants * share

        # --- 2. pre-entry emigration (during / immediately after training) -
        pre_emig = g_cohort * pre_share
        D += pre_emig

        # --- 3. emigration from the practising stock -----------------------
        m = params.m_base * emigration_trend(t) * emig_mult * growth
        denom = float(np.sum(P * w))
        e = np.minimum(m * w / max(denom, 1e-9), params.max_emig_hazard)
        emig = float(np.sum(P * e))
        P = P * (1.0 - e)
        D += emig

        # --- 4. return migration ------------------------------------------
        ret_rate = params.rho * return_mult
        returns = min(D * ret_rate, D)
        D -= returns
        for age, share in RETURN_AGES.items():
            P[_idx(age)] += returns * share

        # --- 5. retirement and mortality ----------------------------------
        retirees = P * r
        dead = (P - retirees) * q
        P = P - retirees - dead

        # --- 6. ageing -----------------------------------------------------
        newP = np.zeros(N_AGES)
        newP[1:] = P[:-1]
        newP[-1] += P[-1]          # 75+ absorbs the open-ended group
        P = newP

        out["stock"][j] = P.sum()
        out["entries"][j] = entrants
        out["emig_post"][j] = emig
        out["emig_pre"][j] = pre_emig
        out["returns"][j] = returns
        out["retirements"][j] = retirees.sum()
        out["deaths"][j] = dead.sum()
        out["diaspora"][j] = D
        out["graduates"][j] = graduates(t, params.g_scale, train_mult)
        if t in (2008, 2017, 2024, 2030, 2035, 2040):
            age_store[t] = P.copy()

    out["years"] = years
    out["age_dist"] = age_store
    return out
