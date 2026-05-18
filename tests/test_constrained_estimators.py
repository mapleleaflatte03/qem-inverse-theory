"""Tests for constrained ZNE estimators."""

import numpy as np
import pytest
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators import (
    fit_polynomial_zne,
    fit_bounded_polynomial_zne,
    fit_spectral_constrained_zne,
)


def _make_data(f0=0.95, decay=0.1, seed=42):
    """Create synthetic ZNE data close to upper bound."""
    rng = np.random.default_rng(seed)
    scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    clean = f0 * np.exp(-decay * scales)
    noisy = clean + rng.normal(0, 0.05, size=len(scales))
    return ZNEData(scales=scales, estimates=noisy)


def test_bounded_estimator_inside_bounds():
    data = _make_data(f0=0.99, decay=0.05)
    for deg in [1, 2, 3]:
        result = fit_bounded_polynomial_zne(data, deg, bounds=(-1.0, 1.0))
        assert -1.0 <= result.estimate <= 1.0, f"degree {deg}: {result.estimate}"


def test_bounded_vs_unconstrained_near_boundary():
    """When true value is near bound, bounded should not exceed it."""
    data = _make_data(f0=0.99, decay=0.02, seed=7)
    unc = fit_polynomial_zne(data, degree=3)
    con = fit_bounded_polynomial_zne(data, degree=3, bounds=(-1.0, 1.0))
    # Constrained must be in bounds
    assert -1.0 <= con.estimate <= 1.0
    # If unconstrained exceeds, constrained should be closer to truth
    if unc.estimate > 1.0:
        assert abs(con.estimate - 0.99) < abs(unc.estimate - 0.99)


def test_spectral_constrained():
    data = _make_data(f0=0.5, decay=0.2)
    eigenvalues = np.array([-0.5, 0.0, 0.5, 1.0])
    result = fit_spectral_constrained_zne(data, degree=2, eigenvalues=eigenvalues)
    bounds = (-0.5, 1.0)
    assert bounds[0] <= result.estimate <= bounds[1]


def test_bounded_returns_fit_result():
    data = _make_data()
    result = fit_bounded_polynomial_zne(data, degree=2)
    assert result.method == "bounded_polynomial_deg2"
    assert "rss" in result.diagnostics
    assert "converged" in result.diagnostics
