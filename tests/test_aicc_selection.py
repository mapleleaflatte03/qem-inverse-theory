"""Tests for AICc model selection."""

import numpy as np
import pytest
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators.model_selection import aicc, aic, bic, select_by_aicc


def test_aicc_infinite_for_overparameterized():
    """AICc should be infinite when n - k - 1 <= 0."""
    n, k = 5, 5  # n - k - 1 = -1
    assert aicc(n, k, rss_val=0.1) == np.inf


def test_aicc_penalizes_more_than_aic():
    """AICc correction should increase penalty for small n."""
    n, k, rss_val = 5, 3, 0.1
    assert aicc(n, k, rss_val) > aic(n, k, rss_val)


def test_aicc_converges_to_aic_large_n():
    """For large n, AICc ≈ AIC."""
    n, k, rss_val = 1000, 3, 0.1
    assert abs(aicc(n, k, rss_val) - aic(n, k, rss_val)) < 0.1


def test_select_by_aicc_avoids_overfitting():
    """With n=5 data points, AICc should not select degree 4."""
    rng = np.random.default_rng(42)
    scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    clean = 0.8 * np.exp(-0.3 * scales)
    noisy = clean + rng.normal(0, 0.02, size=5)
    data = ZNEData(scales=scales, estimates=noisy)

    result = select_by_aicc(data, max_degree=4)
    selected = result.diagnostics["selected_degree"]
    # Should prefer low degree for smooth exponential data
    assert selected <= 3


def test_bic_penalizes_more_for_large_n():
    """BIC penalty grows with log(n), should exceed AIC for large n."""
    n, k, rss_val = 100, 5, 1.0
    assert bic(n, k, rss_val) > aic(n, k, rss_val)
