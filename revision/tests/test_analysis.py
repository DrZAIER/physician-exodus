"""Tests for the analysis helpers."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from analysis import partial_rank_correlation  # noqa: E402


def test_partial_rank_correlation_negative_after_control():
    rng = np.random.default_rng(1)
    z = rng.normal(size=500)
    x = z + rng.normal(scale=0.5, size=500)
    y = z + rng.normal(scale=0.5, size=500)  # y is positively associated with x via z
    r, p = partial_rank_correlation(x, y, [z])
    assert abs(r) < 0.25
    assert 0 <= p <= 1


def test_partial_rank_correlation_positive():
    rng = np.random.default_rng(2)
    x = rng.normal(size=500)
    y = 2 * x + rng.normal(scale=0.2, size=500)
    z = rng.normal(size=500)
    r, p = partial_rank_correlation(x, y, [z])
    assert r > 0.8
    assert p < 0.001
