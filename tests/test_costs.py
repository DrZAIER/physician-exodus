import os
import sys

import numpy as np
from dataclasses import replace
from scipy.optimize import brentq

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from model import simulate  # noqa: E402
from analysis import CENTRAL, _scenario_costs, _scen_dict, draw_params  # noqa: E402


def calibrated():
    m = brentq(
        lambda m: simulate(replace(CENTRAL, m_base=m), end_year=2024)["stock"][-1] - 15315,
        0, 6000, xtol=0.05,
    )
    return replace(CENTRAL, m_base=m)


def test_discounting_reduces_present_value():
    p = calibrated()
    b = simulate(p, end_year=2040)
    o = simulate(p, scenario=_scen_dict("REMUN"), end_year=2040)
    f0, r0 = _scenario_costs("REMUN", o, b, 1.0, 0.0)
    f3, r3 = _scenario_costs("REMUN", o, b, 1.0, 0.03)
    f5, r5 = _scenario_costs("REMUN", o, b, 1.0, 0.05)
    assert f0 > f3 > f5 > 0
    assert r0 == r3 == r5 == 0


def test_cost_components_are_separate():
    p = calibrated()
    b = simulate(p, end_year=2040)
    o = simulate(p, scenario=_scen_dict("CAREER"), end_year=2040)
    f, r = _scenario_costs("CAREER", o, b, 1.0, 0.0)
    assert f == 0
    assert r > 0


def test_draw_params_reproducible():
    a = draw_params(np.random.default_rng(12345))
    b = draw_params(np.random.default_rng(12345))
    for field in ("sigma", "phi", "g_scale", "rho", "diaspora_attrition", "initial_stock_2008"):
        assert getattr(a, field) == getattr(b, field)
