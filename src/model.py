"""
Annual cohort-component (stock-and-flow) model of the Tunisian physician workforce.

The model follows the supply side of the JRC SANDEM framework (Bernini et al.,
2024): an age-structured stock of practising physicians is updated each year by
entries (graduates surviving postgraduate training), emigration, return
migration, retirement and mortality.

Design notes
------------
* The unit of analysis is a physician in **active practice in Tunisia**, not a
  physician registered with the Ordre (CNOM). Registered, practising and
  emigrated physicians are different quantities.
* Emigration is represented as a total annual flow allocated across ages by an
  assumed relative age profile. Tunisian age-specific emigration rates are not
  observed, so the model does not pretend to estimate them.
* The diaspora state ``D`` is a **return-eligible pool**, not a diaspora stock.
  It is depleted by return migration and by an explicit attrition hazard
  (death abroad, onward migration and permanent settlement). This keeps the
  pool within the range implied by destination-country stocks and avoids
  treating every past emigrant as a permanent candidate for return.
* Structural escalation can be applied to the post-entry margin only, to the
  pre-entry margin only, or to both. These are distinct assumptions and are
  reported separately.
"""

from __future__ import annotations

from dataclasses import dataclass
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
    sigma: float = 0.55          # share of graduates entering the practising stock
    entry_lag: int = 5           # years between doctorate and independent practice
    g_scale: float = 1.0         # multiplier on the graduate series
    grad_path: str = "baseline"  # baseline | continued_growth | constant_1900

    # Emigration (post-entry flow, annual number at 2024 intensity)
    m_base: float = 350.0
    emig_tilt: float = 1.0       # >1 shifts emigration towards older ages

    # Return migration and diaspora accounting
    rho: float = 0.020           # annual return rate from the return-eligible pool
    diaspora_attrition: float = 0.10   # death abroad, onward migration, settlement
    return_retention: float = 0.85     # share of returns that remain in practice

    # Structural trends in emigration intensity after 2024 (0 = constant)
    emig_growth_post: float = 0.0
    emig_growth_pre: float = 0.0
    # Projection-only shock to emigration intensity (does not affect the
    # 2024 calibration). This is the independent parameter used in PRCC.
    emig_future_mult: float = 1.0

    # Retirement
    retire_shift: float = 0.0    # years added to (positive) or removed from legal ages

    # Initial conditions
    initial_stock_2008: float = 12600.0
    initial_diaspora_2008: float = 4000.0

    # Numerical
    max_emig_hazard: float = 0.35


# ----------------------------------------------------------------------------
# Hazards and profiles
# ----------------------------------------------------------------------------
def emigration_weights(tilt: float = 1.0) -> np.ndarray:
    """Relative age profile of emigration (normalised to sum to one)."""
    base = {
        25: 0.85, 30: 1.00, 35: 0.60, 40: 0.35, 45: 0.20,
        50: 0.10, 55: 0.04, 60: 0.02, 65: 0.01, 70: 0.005, 75: 0.002,
    }
    w = np.array([base[min((a // 5) * 5, 75)] for a in AGES], dtype=float)
    # tilt > 1 gives relatively more weight to older physicians
    w = w * np.power(tilt, (AGES - 30) / 10.0)
    return w / w.sum()


def retirement_hazard(shift: float = 0.0) -> np.ndarray:
    """Annual retirement hazard by age.

    Legal ages in Tunisia: 60 in the private sector, 62 in the public sector
    (Law 2019-37), and 65-70 for hospitalo-university professors. The hazard
    is a smooth approximation; ``shift`` moves the whole schedule.
    """
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
    """Annual mortality hazard by age (all causes, both sexes, working ages)."""
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


# Entry age distribution (after a five-year postgraduate pathway)
ENTRY_AGES = {29: 0.15, 30: 0.30, 31: 0.30, 32: 0.15, 33: 0.10}

# Return-migration age distribution
RETURN_AGES = {33: 0.10, 35: 0.20, 38: 0.25, 41: 0.20, 45: 0.15, 50: 0.10}


def initial_distribution(initial_stock: float) -> np.ndarray:
    """Age distribution of CNOM-registered physicians in 2008, single years.

    Source: CNOM 2007-2008 report, physicians by age group
    (25-30: 2 000; 30-35: 2 109; 35-40: 2 468; 40-45: 1 946; 45-50: 2 041;
     50-55: 1 241; 55-60: 535; 60-65: 144; 65+: 132).
    Scaled to the 2008 practising stock (WHO: 12 996 in 2010; 12 600 for 2008).
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
# Anchors: 987 graduates in 2013 and 1 128 in 2021 (Zehnati 2024), and 1 305
# in 2024. The 2021-2024 segment is a geometric interpolation; the implied
# growth is 5.0% per year, not the 1.7% observed over 2013-2021. The series is
# therefore explicitly piecewise and the acceleration is tested as a scenario.
GRAD_2013 = 987.0
GRAD_2021 = 1128.0
GRAD_2024 = 1305.0
# Exact geometric growth between the two published anchors (about 1.68% per
# year). The earlier text described this as 1.7%; the exact rate is used so
# that both anchors are reproduced without a residual.
GRAD_GROWTH_2013_2021 = (GRAD_2021 / GRAD_2013) ** (1.0 / 8.0) - 1.0
GRAD_GROWTH_POST_2024 = 0.017


def graduates(
    year: int,
    g_scale: float = 1.0,
    train_mult: float = 1.0,
    path: str = "baseline",
) -> float:
    """Annual medical graduates (doctorate), Tunisia.

    ``path`` controls the post-2024 baseline:

    ``baseline``
        Constant at 1 305 after 2024 (the central assumption).
    ``continued_growth``
        Continue the 2013-2021 growth rate of 1.7% per year after 2024.
    ``constant_1900``
        Hold output at 1 900, an upper-bound figure reported in ministerial
        statements; this is a stress test, not a baseline.

    ``train_mult`` implements a training-capacity scenario from 2031 (the
    first cohort affected by a 2025 admissions increase graduating around
    2031, then entering practice after the five-year postgraduate lag).
    """
    if year <= 2021:
        g = GRAD_2013 * (1.0 + GRAD_GROWTH_2013_2021) ** (year - 2013)
    elif year <= 2024:
        g = GRAD_2021 * (GRAD_2024 / GRAD_2021) ** ((year - 2021) / 3.0)
    else:
        if path == "continued_growth":
            g = GRAD_2024 * (1.0 + GRAD_GROWTH_POST_2024) ** (year - 2024)
        elif path == "constant_1900":
            g = 1900.0
        else:
            g = GRAD_2024
    if year >= 2031:
        g *= train_mult
    return g * g_scale


def emigration_trend(year: int) -> float:
    """Relative intensity of post-entry emigration, normalised to 1 in 2024.

    The historical rise from 60% of the 2024 level in 2017 is an assumption
    informed by the reported acceleration of departures after 2017. It is not
    estimated from data and is discussed as a limitation.
    """
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
) -> Dict[str, object]:
    """Run the model and return annual flows and stocks.

    The returned ``stock[t]`` is the end-of-year practising stock. ``age_dist``
    stores selected end-of-year age distributions.
    """
    scen = dict(BASE_SCENARIO)
    if scenario:
        scen.update(scenario)

    r = retirement_hazard(params.retire_shift)
    q = mortality_hazard()
    w = emigration_weights(params.emig_tilt)

    P = initial_distribution(params.initial_stock_2008)
    D = float(params.initial_diaspora_2008)

    years = np.arange(start_year, end_year + 1)
    keys = [
        "stock", "entries", "emig_post", "emig_pre", "returns_gross",
        "returns_net", "re_emigration", "retirements", "deaths", "diaspora",
        "graduates", "pre_share", "m_effective",
    ]
    out = {k: np.zeros(len(years)) for k in keys}
    age_store = {}

    for j, t in enumerate(years):
        ramp = _ramp(t, scen) if t >= scen["start_year"] else 0.0

        # --- effective policy parameters -----------------------------------
        emig_mult = 1.0 + ramp * (scen["emig_mult"] - 1.0)
        pre_emig_reduction = ramp * scen["entry_retention"]
        sigma_eff = 1.0 - (1.0 - params.sigma) * (1.0 - pre_emig_reduction)
        return_mult = 1.0 + ramp * (scen["return_mult"] - 1.0)
        train_mult = scen["train_mult"] if t >= 2031 else 1.0

        # --- structural escalation -----------------------------------------
        # Separate margins so that a post-entry-only trend can be reported
        # without implicitly raising pre-entry emigration.
        g_post = (1.0 + params.emig_growth_post) ** max(0, t - 2024)
        g_pre = (1.0 + params.emig_growth_pre) ** max(0, t - 2024)
        pre_share = min(0.95, (1.0 - sigma_eff) * g_pre)
        sigma_entry = 1.0 - pre_share

        # --- 1. entry of graduates -----------------------------------------
        g_cohort = graduates(t - params.entry_lag, params.g_scale,
                             train_mult, params.grad_path)
        entrants = g_cohort * sigma_entry
        for age, share in ENTRY_AGES.items():
            P[_idx(age)] += entrants * share

        # --- 2. pre-entry emigration (during / immediately after training) --
        pre_emig = g_cohort * pre_share
        D += pre_emig

        # --- 3. emigration from the practising stock ------------------------
        future_mult = params.emig_future_mult if t > 2024 else 1.0
        m = params.m_base * emigration_trend(t) * emig_mult * g_post * future_mult
        denom = float(np.sum(P * w))
        e = np.minimum(m * w / max(denom, 1e-9), params.max_emig_hazard)
        emig = float(np.sum(P * e))
        P = P * (1.0 - e)
        D += emig

        # --- 4. return migration --------------------------------------------
        ret_rate = params.rho * return_mult
        returns_gross = min(D * ret_rate, D)
        returns_net = returns_gross * params.return_retention
        re_emigration = returns_gross - returns_net
        D -= returns_gross
        D += re_emigration  # return migrants who leave again rejoin the pool
        for age, share in RETURN_AGES.items():
            P[_idx(age)] += returns_net * share

        # --- 5. diaspora attrition ------------------------------------------
        # Deaths abroad, onward migration and permanent settlement. This is
        # what keeps the return-eligible pool from accumulating every emigrant
        # since 2008.
        D *= (1.0 - params.diaspora_attrition)

        # --- 6. mortality, then retirement among survivors -------------------
        # Competing risks are applied sequentially: q first, then r among
        # survivors. This keeps the survival factor non-negative at all ages.
        survived = P * (1.0 - q)
        deaths = P - survived
        retirees = survived * r
        P = survived - retirees

        # --- 7. ageing -------------------------------------------------------
        newP = np.zeros(N_AGES)
        newP[1:] = P[:-1]
        newP[-1] += P[-1]          # 75+ absorbs the open-ended group
        P = newP

        out["stock"][j] = P.sum()
        out["entries"][j] = entrants
        out["emig_post"][j] = emig
        out["emig_pre"][j] = pre_emig
        out["returns_gross"][j] = returns_gross
        out["returns_net"][j] = returns_net
        out["re_emigration"][j] = re_emigration
        out["retirements"][j] = retirees.sum()
        out["deaths"][j] = deaths.sum()
        out["diaspora"][j] = D
        out["graduates"][j] = graduates(t, params.g_scale, train_mult,
                                        params.grad_path)
        out["pre_share"][j] = pre_share
        out["m_effective"][j] = m
        if t in (2008, 2017, 2024, 2030, 2035, 2040):
            age_store[t] = P.copy()

    out["years"] = years
    out["age_dist"] = age_store
    return out
