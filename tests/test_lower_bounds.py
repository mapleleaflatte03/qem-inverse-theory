"""Tests for two-point Le Cam lower bounds."""

import numpy as np
import pytest
from qem_inverse_theory.theory.lower_bounds import (
    two_point_total_variation_bound,
    lecam_mse_lower_bound,
    zne_two_point_lower_bound,
)


def test_tv_bound_nonnegative():
    tv = two_point_total_variation_bound(0.01, 1.0, 5)
    assert tv >= 0


def test_tv_bound_at_most_one():
    tv = two_point_total_variation_bound(10.0, 0.01, 1000)
    assert tv <= 1.0


def test_mse_lb_nonnegative():
    lb = lecam_mse_lower_bound(0.5, 0.3)
    assert lb >= 0


def test_mse_lb_increases_with_delta_f0():
    lb1 = lecam_mse_lower_bound(0.1, 0.3)
    lb2 = lecam_mse_lower_bound(0.5, 0.3)
    assert lb2 > lb1


def test_mse_lb_decreases_with_tv():
    lb1 = lecam_mse_lower_bound(0.5, 0.2)
    lb2 = lecam_mse_lower_bound(0.5, 0.8)
    assert lb1 > lb2


def test_zne_lb_decreases_with_shots():
    r1 = zne_two_point_lower_bound(0.3, 0.01, 1.0, 5, 100)
    r2 = zne_two_point_lower_bound(0.3, 0.01, 1.0, 5, 10000)
    assert r1["mse_lower_bound"] >= r2["mse_lower_bound"]


def test_zne_lb_increases_with_delta_f0():
    r1 = zne_two_point_lower_bound(0.1, 0.01, 1.0, 5, 1000)
    r2 = zne_two_point_lower_bound(0.5, 0.01, 1.0, 5, 1000)
    assert r2["mse_lower_bound"] > r1["mse_lower_bound"]


def test_zne_lb_increases_with_small_delta_obs():
    """Smaller delta_obs = harder to distinguish = higher lower bound."""
    r1 = zne_two_point_lower_bound(0.3, 0.001, 1.0, 5, 1000)
    r2 = zne_two_point_lower_bound(0.3, 0.1, 1.0, 5, 1000)
    assert r1["mse_lower_bound"] >= r2["mse_lower_bound"]


def test_zne_lb_no_nans():
    r = zne_two_point_lower_bound(0.3, 0.01, 1.0, 5, 500)
    assert np.isfinite(r["mse_lower_bound"])
    assert np.isfinite(r["tv_bound"])


def test_zne_lb_deterministic():
    r1 = zne_two_point_lower_bound(0.3, 0.01, 1.0, 5, 500)
    r2 = zne_two_point_lower_bound(0.3, 0.01, 1.0, 5, 500)
    assert r1["mse_lower_bound"] == r2["mse_lower_bound"]


def test_zne_lb_has_assumptions():
    r = zne_two_point_lower_bound(0.3, 0.01, 1.0, 5, 500)
    assert "assumptions" in r
    assert len(r["assumptions"]) > 0
