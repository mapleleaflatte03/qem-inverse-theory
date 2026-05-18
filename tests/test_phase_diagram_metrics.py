"""Tests for phase diagram and metrics."""

import numpy as np
import pytest
from qem_inverse_theory.theory.phase_diagram import (
    compute_help_harm_ratio,
    classify_region,
    build_phase_grid,
)
from qem_inverse_theory.benchmarks.metrics import (
    absolute_error,
    mse,
    bias_variance_decomposition,
    physical_validity_rate,
    interval_coverage,
)
from qem_inverse_theory.estimators import fit_bayesian_zne_gp
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.benchmarks import adversarial_response_with_same_observed_nodes


def test_help_harm_ratio_help():
    assert compute_help_harm_ratio(1.0, 0.5) == 2.0


def test_help_harm_ratio_harm():
    assert compute_help_harm_ratio(0.5, 1.0) == 0.5


def test_classify_help():
    assert classify_region(1.0, 0.5) == "help"


def test_classify_harm():
    assert classify_region(0.5, 1.0) == "harm"


def test_classify_neutral():
    assert classify_region(1.0, 1.0) == "neutral"


def test_mse_zero_for_perfect():
    assert mse(np.array([1.0, 1.0, 1.0]), 1.0) == 0.0


def test_bias_variance_decomposition():
    estimates = np.array([1.1, 0.9, 1.0, 1.1, 0.9])
    result = bias_variance_decomposition(estimates, truth=1.0)
    assert abs(result["mse"] - (result["bias_squared"] + result["variance"])) < 1e-10


def test_physical_validity_rate():
    estimates = np.array([0.5, 1.5, -0.5, 0.8, -1.5])
    rate = physical_validity_rate(estimates, bounds=(-1.0, 1.0))
    assert rate == 0.6  # 3 out of 5 valid


def test_interval_coverage():
    intervals = [(0.0, 1.0), (0.5, 0.9), (0.0, 0.4)]
    assert interval_coverage(intervals, truth=0.7) == pytest.approx(2 / 3)


def test_bayesian_returns_finite():
    """Bayesian GP should return finite mean and variance."""
    scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    values = 0.8 * np.exp(-0.2 * scales)
    data = ZNEData(scales=scales, estimates=values)
    result = fit_bayesian_zne_gp(data)
    assert np.isfinite(result.estimate)
    assert np.isfinite(result.variance)
    assert result.variance >= 0


def test_adversarial_agree_at_nodes():
    """Adversarial responses should approximately agree at observed scales."""
    scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    vals_a, vals_b, f0_a, f0_b = adversarial_response_with_same_observed_nodes(
        scales, f0_a=0.9, f0_b=0.3
    )
    # Should agree at nodes (within offset tolerance)
    assert np.max(np.abs(vals_a - vals_b)) < 0.15
    # But differ at zero
    assert abs(f0_a - f0_b) > 0.1
