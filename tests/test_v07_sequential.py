"""Tests for v0.7: Bayesian calibration and sequential design."""

import numpy as np
import pytest
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators.bayesian import fit_bayesian_zne_gp, design_next_scale
from qem_inverse_theory import design_next_scale as design_top


def _make_data():
    scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    values = 0.8 * np.exp(-0.25 * scales)
    variances = np.full(5, 0.01)
    return ZNEData(scales=scales, estimates=values, variances=variances)


def test_optimized_gp_nll_improves():
    """Optimized hyperparameters should not worsen NLL."""
    data = _make_data()
    r_fixed = fit_bayesian_zne_gp(data, bounds=(-1, 1), optimize_hyperparameters=False)
    r_opt = fit_bayesian_zne_gp(data, bounds=(-1, 1), optimize_hyperparameters=True)
    assert r_opt.diagnostics["nll_after"] <= r_fixed.diagnostics["nll_after"] + 0.1


def test_optimized_gp_returns_finite():
    data = _make_data()
    r = fit_bayesian_zne_gp(data, bounds=(-1, 1), optimize_hyperparameters=True)
    assert np.isfinite(r.estimate)
    assert np.isfinite(r.variance)
    assert r.diagnostics["optimize_hyperparameters"] is True


def test_design_next_scale_returns_candidate():
    data = _make_data()
    candidates = np.arange(0.5, 6.0, 0.5)
    selected = design_next_scale(data, candidates, bounds=(-1, 1))
    assert selected in candidates


def test_design_next_scale_top_level_import():
    assert design_top is design_next_scale


def test_design_reduces_posterior_variance():
    """Adding the selected point should reduce posterior variance at 0."""
    data = _make_data()
    candidates = np.arange(0.5, 6.0, 0.5)

    r_before = fit_bayesian_zne_gp(data, bounds=(-1, 1))
    var_before = r_before.diagnostics["posterior_var_g0"]

    selected = design_next_scale(data, candidates, bounds=(-1, 1))
    # Add dummy observation at selected scale
    new_scales = np.append(data.scales, selected)
    new_est = np.append(data.estimates, 0.8 * np.exp(-0.25 * selected))
    new_var = np.append(data.variances, 0.01)
    data_aug = ZNEData(scales=new_scales, estimates=new_est, variances=new_var)

    r_after = fit_bayesian_zne_gp(data_aug, bounds=(-1, 1))
    var_after = r_after.diagnostics["posterior_var_g0"]

    assert var_after <= var_before + 1e-6


def test_design_respects_candidate_minimum():
    """If all candidates are ≥1, selected scale must be ≥1."""
    data = _make_data()
    candidates_ge1 = np.arange(1.0, 6.0, 0.5)
    selected = design_next_scale(data, candidates_ge1, bounds=(-1, 1))
    assert selected >= 1.0


def test_design_selects_from_provided_pool():
    """Selected scale must be one of the provided candidates."""
    data = _make_data()
    candidates = np.array([1.5, 2.5, 3.5, 4.5])
    selected = design_next_scale(data, candidates, bounds=(-1, 1))
    assert selected in candidates
