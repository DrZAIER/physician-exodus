"""
Annual cohort-component (stock-and-flow) model of the Tunisian physician workforce.

Revision 2.0 (scientific audit)
--------------------------------
The key conceptual correction in this version is the separation of:

1. **Pipeline non-entry**: graduates who do not enter the Tunisian practising
   stock. This includes international emigration, further training, domestic
   non-clinical employment, temporary inactivity and other reasons.
2. **Pre-entry international emigration**: the share ``phi`` of pipeline
   non-entry that is assumed to be international emigration.
3. **Post-entry international emigration**: emigration from the practising stock.

Only international emigration enters the return-eligible diaspora pool. The
model therefore no longer silently equates non-entry with emigration.

The return-eligible pool also has an explicit attrition hazard (death abroad,
onward migration and permanent settlement) and a return-retention probability.
Structural escalation can be applied to post-entry emigration only, or to both
the pre-entry international and post-entry margins.
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
    phi: float = 0.50           # share of pipeline non-entry that is international emigration
    entry_lag: int = 5           # years between doctorate and independent practice
    g_scale: float = 1.0         # multiplier on the graduate series
    grad_path: str = "baseline"  # baseline | continued_growth | constant_1900

    # Emigration (post-entry flow, annual number at 2024 intensity)
    m_base: float = 350.0
    emig_tilt: float = 1.0       # >1 shifts emigration towards older ages

    # Return migration and diaspora accounting
    rho: float = 0.020           # annual return rate from the return-eligible pool
    diaspora_attrition: float = 0.08   # death abroad, onward migration, settlement
    return_retention: float = 0.85     # share of return attempts that remain in practice
    return_recycling: bool = True      # re-emigrants rejoin the return-eligible pool

    # Structural trends in emigration intensity after 2024 (0 = constant)
    emig_growth_post: float = 0.0
    emig_growth_pre: float = 0.0
    # Projection-only shock to emigration intensity (does not affect the
    # 2024 calibration). This is the independent parameter used in PRCC.
    emig_future_mult: float = 1.0

    # Retirement and mortality
    retire_shift: float = 0.0    # years added to (positive) or removed from legal ages
    mortality_mult: float = 1.0  # multiplier on baseline mortality hazards

    # Initial conditions
    initial_stock_2008: float = 12600.0
    initial_diaspora_2008: float = 4000.0
    age_shape: str = "uniform"   # uniform | young | old

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

    Legal ages in Tunisia vary by sector: 60 in the private sector, 62 in the
    public sector under Law 2019-37, and extensions for hospitalo-university
    professors. The hazard is a smooth approximation to actual retirement
    behaviour, not a legal rule; ``shift`` moves the schedule.

    The shift is applied by linear interpolation on the single-year age grid,
    so fractional shifts (for example 1.5 years) are distinct from integer
    shifts. The earlier implementation used a discrete threshold and produced
    identical schedules for +1.5 and +2 years.
    """
    base = np.zeros(N_AGES)
    for i, a in enumerate(AGES):
        if a < 60:
            base[i] = 0.0
        elif a < 62:
            base[i] = 0.20
        elif a < 63:
            base[i] = 0.45
        elif a < 65:
            base[i] = 0.35
        elif a < 70:
            base[i] = 0.45
        else:
            base[i] = 1.0
    if shift == 0.0:
        return base
    return np.interp(AGES - shift, AGES, base, left=0.0, right=1.0)


def mortality_hazard(mult: float = 1.0) -> np.ndarray:
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
    return np.clip(q * mult, 0.0, 1.0)


# Entry age distribution (after a five-year postgraduate pathway)
ENTRY_AGES = {29: 0.15, 30: 0.30, 31: 0.30, 32: 0.15, 33: 0.10}

# Return-migration age distribution
RETURN_AGES = {33: 0.10, 35: 0.20, 38: 0.25, 41: 0.20, 45: 0.15, 50: 0.10}


def initial_distribution(initial_stock: float, shape: str = "uniform") -> np.ndarray:
    """Age distribution of CNOM-registered physicians in 2008, single years.

    Source: CNOM 2007-2008 report, physicians by age group
    (25-30: 2 000; 30-35: 2 109; 35-40: 2 468; 40-45: 1 946; 45-50: 2 041;
     50-55: 1 241; 55-60: 535; 60-65: 144; 65+: 132).
    Scaled to the 2008 practising stock (WHO: 12 996 in 2010; 12 600 for 2008).

    ``shape`` produces alternative reconstructions for sensitivity analysis:
    ``uniform`` spreads each five-year band uniformly; ``young`` and ``old``
    shift the whole distribution by two years to test the influence of the
    reconstructed age structure. These are not observations.
    """
    bands = {
        25: 2000, 30: 2109, 35: 2468, 40: 1946, 45: 2041,
        50: 1241, 55: 535, 60: 144, 65: 100, 70: 32,
    }
    d = np.zeros(N_AGES)
    for start, n in bands.items():
        for a in range(start, min(start + 5, AGE_MAX + 1)):
            d[_idx(a)] += n / 5.0
    d = d / d.sum() * initial_stock

    if shape == "young":
        shifted = np.zeros_like(d)
        shifted[:-2] = d[2:]
        d = shifted
    elif shape == "old":
        shifted = np.zeros_like(d)
        shifted[2:] = d[:-2]
        d = shifted
    elif shape != "uniform":
        raise ValueError("age_shape must be 'uniform', 'young' or 'old'")

    return d / d.sum() * initial_stock


# ----------------------------------------------------------------------------
# Exogenous series
# ----------------------------------------------------------------------------
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
        Continue the 2017-2024 growth rate of 1.7% per year after 2024.
    ``constant_1900``
        Hold output at 1 900. This is an unverified press-reported cohort,
        used only as a stress test in the audit; it is not a ministerial
        statement and is not used in the main analysis.

    ``train_mult`` implements a training-capacity scenario from 2031 (the
    first cohort affected by a 2025 admissions increase graduating around
    2031, then entering practice after the postgraduate lag).
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
    "entry_retention": 0.0,  # proportional reduction of PRE-ENTRY emigration
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
    q = mortality_hazard(params.mortality_mult)
    w = emigration_weights(params.emig_tilt)

    P = initial_distribution(params.initial_stock_2008, params.age_shape)
    D = float(params.initial_diaspora_2008)

    years = np.arange(start_year, end_year + 1)
    keys = [
        "stock", "entries", "emig_post", "emig_pre", "nonentry_total",
        "nonentry_domestic", "returns_gross", "returns_net", "re_emigration",
        "retirements", "deaths", "diaspora", "graduates", "pipe_nonentry_share",
        "pre_emig_share", "m_effective", "emig_hazard_max", "cap_binding",
    ]
    out = {k: np.zeros(len(years)) for k in keys}
    age_store = {}

    for j, t in enumerate(years):
        ramp = _ramp(t, scen) if t >= scen["start_year"] else 0.0

        # --- effective policy parameters -----------------------------------
        emig_mult = 1.0 + ramp * (scen["emig_mult"] - 1.0)
        pre_emig_reduction = ramp * scen["entry_retention"]
        return_mult = 1.0 + ramp * (scen["return_mult"] - 1.0)
        # The training expansion is defined on the graduate cohort, not on the
        # entry year: an admissions increase affects graduates from 2031 and
        # entrants only after the postgraduate lag.
        grad_year = t - params.entry_lag
        train_mult = scen["train_mult"] if grad_year >= 2031 else 1.0

        # --- structural escalation -----------------------------------------
        g_post = (1.0 + params.emig_growth_post) ** max(0, t - 2024)
        g_pre = (1.0 + params.emig_growth_pre) ** max(0, t - 2024)

        # --- pipeline: non-entry, pre-entry emigration and entry -----------
        n = 1.0 - params.sigma
        # The policy reduces pre-entry international emigration by r. Domestic
        # non-entry is unchanged.
        pre_emig_share_raw = params.phi * n * (1.0 - pre_emig_reduction) * g_pre
        domestic_nonentry_share = (1.0 - params.phi) * n
        pipe_nonentry_share = pre_emig_share_raw + domestic_nonentry_share
        if pipe_nonentry_share > 0.95:
            # Keep at least 5% of a cohort entering practice.
            pre_emig_share_raw = max(0.0, 0.95 - domestic_nonentry_share)
            pipe_nonentry_share = pre_emig_share_raw + domestic_nonentry_share
        sigma_entry = 1.0 - pipe_nonentry_share

        g_cohort = graduates(grad_year, params.g_scale,
                             train_mult, params.grad_path)
        entrants = g_cohort * sigma_entry
        pre_emig = g_cohort * pre_emig_share_raw
        domestic_nonentry = g_cohort * domestic_nonentry_share
        nonentry_total = pre_emig + domestic_nonentry

        for age, share in ENTRY_AGES.items():
            P[_idx(age)] += entrants * share

        # Only international emigration enters the return-eligible pool.
        D += pre_emig

        # --- emigration from the practising stock --------------------------
        future_mult = params.emig_future_mult if t > 2024 else 1.0
        m = params.m_base * emigration_trend(t) * emig_mult * g_post * future_mult
        denom = float(np.sum(P * w))
        raw_hazard = m * w / max(denom, 1e-9)
        e = np.minimum(raw_hazard, params.max_emig_hazard)
        emig = float(np.sum(P * e))
        P = P * (1.0 - e)
        D += emig

        # --- return migration ----------------------------------------------
        ret_rate = params.rho * return_mult
        returns_gross = min(D * ret_rate, D)
        returns_net = returns_gross * params.return_retention
        re_emigration = returns_gross - returns_net
        D -= returns_gross
        if params.return_recycling:
            # Re-emigrants are assumed to rejoin the return-eligible pool
            # immediately. The successful-return hazard is theta*rho.
            D += re_emigration
        # If return_recycling is False, the unsuccessful return attempts leave
        # the return-eligible pool permanently; the pool exit hazard is rho and
        # the successful-return hazard is still theta*rho.
        for age, share in RETURN_AGES.items():
            P[_idx(age)] += returns_net * share

        # --- diaspora attrition ---------------------------------------------
        D *= (1.0 - params.diaspora_attrition)

        # --- mortality, then retirement among survivors ---------------------
        survived = P * (1.0 - q)
        deaths = P - survived
        retirees = survived * r
        P = survived - retirees

        # --- ageing ----------------------------------------------------------
        newP = np.zeros(N_AGES)
        newP[1:] = P[:-1]
        newP[-1] += P[-1]          # 75+ absorbs the open-ended group
        P = newP

        out["stock"][j] = P.sum()
        out["entries"][j] = entrants
        out["emig_post"][j] = emig
        out["emig_pre"][j] = pre_emig
        out["nonentry_total"][j] = nonentry_total
        out["nonentry_domestic"][j] = domestic_nonentry
        out["returns_gross"][j] = returns_gross
        out["returns_net"][j] = returns_net
        out["re_emigration"][j] = re_emigration
        out["retirements"][j] = retirees.sum()
        out["deaths"][j] = deaths.sum()
        out["diaspora"][j] = D
        out["graduates"][j] = g_cohort
        out["pipe_nonentry_share"][j] = pipe_nonentry_share
        out["pre_emig_share"][j] = pre_emig_share_raw
        out["m_effective"][j] = m
        out["emig_hazard_max"][j] = float(e.max()) if len(e) else 0.0
        out["cap_binding"][j] = float(np.any(raw_hazard > params.max_emig_hazard))
        if t in (2008, 2017, 2024, 2030, 2035, 2040):
            age_store[t] = P.copy()

    out["years"] = years
    out["age_dist"] = age_store
    return out
