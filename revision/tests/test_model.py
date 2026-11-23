"""Tests for the revised cohort-component model."""

import os
import sys

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from model import (  # noqa: E402
    AGES, Params, graduates, mortality_hazard, retirement_hazard, simulate,
)


def central_params():
    return Params(
        sigma=0.55, phi=0.50, g_scale=1.0, initial_stock_2008=12600,
        retire_shift=0.0, emig_tilt=1.0, rho=0.02,
        diaspora_attrition=0.08, return_retention=0.85,
        initial_diaspora_2008=4000, age_shape="uniform",
    )


def calibrated_params():
    p = central_params()
    m = brentq(
        lambda m: simulate(Params(**{**p.__dict__, "m_base": m}),
                           end_year=2024)["stock"][-1] - 15315,
        0, 6000, xtol=0.05,
    )
    return Params(**{**p.__dict__, "m_base": m})


def test_calibration_exact():
    p = calibrated_params()
    o = simulate(p, end_year=2024)
    assert abs(o["stock"][-1] - 15315) < 0.5


def test_flow_and_pipeline_identity():
    p = calibrated_params()
    o = simulate(p, end_year=2040)
    for j in range(1, len(o["years"])):
        lhs = o["stock"][j] - o["stock"][j - 1]
        rhs = (o["entries"][j] - o["emig_post"][j] + o["returns_net"][j]
               - o["retirements"][j] - o["deaths"][j])
        assert abs(lhs - rhs) < 1e-6, (o["years"][j], lhs, rhs)
    for j in range(len(o["years"])):
        assert abs(o["entries"][j] + o["nonentry_total"][j]
                   - o["graduates"][j]) < 1e-6


def test_graduate_anchors_and_training_timing():
    assert abs(graduates(2013) - 987) < 1e-6
    assert abs(graduates(2021) - 1128) < 1e-6
    assert abs(graduates(2024) - 1305) < 1e-6
    assert abs(graduates(2040, path="continued_growth") - 1709) < 2
    assert abs(graduates(2040, path="constant_1900") - 1900) < 1e-6
    assert abs(graduates(2031, train_mult=1.30) / graduates(2031) - 1.30) < 1e-6


def test_hazards_and_continuous_retirement_shift():
    r = retirement_hazard(0.0)
    assert r[AGES < 60].max() == 0
    assert r[AGES >= 70].min() == 1.0
    assert not np.allclose(retirement_hazard(1.5), retirement_hazard(2.0))
    q = mortality_hazard()
    assert (q >= 0).all()
    assert (q <= 0.05).all()


def test_phi_separates_nonentry_from_emigration():
    p = calibrated_params()
    o = simulate(p, end_year=2024)
    i = list(o["years"]).index(2024)
    assert abs(o["nonentry_total"][i]
               - o["emig_pre"][i] - o["nonentry_domestic"][i]) < 1e-6
    assert abs(o["emig_pre"][i] / o["nonentry_total"][i] - 0.50) < 1e-9
    # Only international emigration enters the return-eligible pool.
    p0 = Params(**{**p.__dict__, "phi": 0.0})
    o0 = simulate(p0, end_year=2024)
    assert o0["diaspora"][i] < o["diaspora"][i]


def test_training_enters_after_lag():
    p = calibrated_params()
    b = simulate(p, end_year=2040)
    t = simulate(p, scenario=dict(emig_mult=1.0, entry_retention=0.0,
                                  return_mult=1.0, train_mult=1.30),
                 end_year=2040)
    for y in (2030, 2035):
        i = list(b["years"]).index(y)
        assert abs(t["entries"][i] - b["entries"][i]) < 1e-6
    i = list(b["years"]).index(2036)
    assert t["entries"][i] > b["entries"][i]


def test_stock_positive_and_baseline_plateau():
    p = calibrated_params()
    o = simulate(p, end_year=2040)
    assert (o["stock"] > 0).all()
    assert 15000 < o["stock"][-1] < 17000
    assert not bool(o["cap_binding"].any())


def test_combined_exceeds_bau():
    p = calibrated_params()
    b = simulate(p, end_year=2040)
    c = simulate(p, scenario=dict(emig_mult=0.65, entry_retention=0.35,
                                  return_mult=1.75, train_mult=1.0),
                 end_year=2040)
    assert c["stock"][-1] > b["stock"][-1]


def test_pre_entry_growth_margin():
    p = calibrated_params()
    base = simulate(p, end_year=2040)
    both = simulate(Params(**{**p.__dict__, "emig_growth_post": 0.03,
                              "emig_growth_pre": 0.03}), end_year=2040)
    post = simulate(Params(**{**p.__dict__, "emig_growth_post": 0.03,
                              "emig_growth_pre": 0.0}), end_year=2040)
    assert both["stock"][-1] < post["stock"][-1] < base["stock"][-1]
    assert both["pre_emig_share"][-1] > base["pre_emig_share"][-1]


def test_return_pool_accounting():
    p = calibrated_params()
    o = simulate(p, end_year=2040)
    assert o["diaspora"][-1] < 20000
    assert (o["returns_net"] >= 0).all()
    assert (o["returns_gross"] >= o["returns_net"]).all()


def test_age_shape_variants():
    p = calibrated_params()
    base = simulate(p, end_year=2040)
    results = {}
    for shape in ("young", "old"):
        q = Params(**{**p.__dict__, "age_shape": shape})
        m = brentq(
            lambda m: simulate(Params(**{**q.__dict__, "m_base": m}),
                               end_year=2024)["stock"][-1] - 15315,
            0, 6000, xtol=0.05,
        )
        results[shape] = simulate(Params(**{**q.__dict__, "m_base": m}),
                                  end_year=2040)["stock"][-1]
    assert results["young"] < base["stock"][-1] < results["old"]
