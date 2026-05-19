"""Tests for v0.6 estimators: Chebyshev-Tikhonov and bounded Bayesian GP."""

import numpy as np
import pytest
from qem_inverse_theory.types import ZNEData, FitResult, Estimator
from qem_inverse_theory.estimators.chebyshev import fit_chebyshev_tikhonov_zne
from qem_inverse_theory.estimators.bayesian import fit_bayesian_zne_gp
from qem_inverse_theory import (
    ZNEData as ZNEData_top,
    FitResult as FitResult_top,
    Estimator as Estimator_top,
    fit_constrained_zne,
    fit_chebyshev_tikhonov_zne as fit_cheb_top,
    select_model_aicc,
    fit_bayesian_zne,
)


def _make_data(f0=0.8, decay=0.25, n=5):
    scales = np.linspace(1.0, float(n), n)
    values = f0 * np.exp(-decay * scales)
    return ZNEData(scales=scales, estimates=values)


# --- Top-level API tests ---

def test_top_level_imports():
    assert ZNEData_top is ZNEData
    assert FitResult_top is FitResult
    assert Estimator_top is Estimator


def test_fit_constrained_zne_callable():
    data = _make_data()
    result = fit_constrained_zne(data, degree=2)
    assert isinstance(result, FitResult)
    assert -1.0 <= result.estimate <= 1.0


def test_select_model_aicc_callable():
    data = _make_data()
    result = select_model_aicc(data)
    assert isinstance(result, FitResult)


# --- Chebyshev-Tikhonov tests ---

def test_chebyshev_bounded_output():
    data = _make_data(f0=0.99)
    result = fit_chebyshev_tikhonov_zne(data, degree=3, bounds=(-1, 1))
    assert -1.0 <= result.estimate <= 1.0


def test_chebyshev_low_degree_recovery():
    """Quadratic data should be recovered well by degree-2 Chebyshev."""
    scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    values = 0.5 - 0.1 * scales + 0.01 * scales**2  # true f(0) = 0.5
    data = ZNEData(scales=scales, estimates=values)
    result = fit_chebyshev_tikhonov_zne(data, degree=2, bounds=(-1, 1), reg_lambda=0.0)
    assert abs(result.estimate - 0.5) < 0.05


def test_chebyshev_regularization_reduces_norm():
    data = _make_data()
    r_noreg = fit_chebyshev_tikhonov_zne(data, degree=4, bounds=(-1, 1), reg_lambda=0.0)
    r_reg = fit_chebyshev_tikhonov_zne(data, degree=4, bounds=(-1, 1), reg_lambda=1.0)
    assert r_reg.diagnostics["coeff_norm"] <= r_noreg.diagnostics["coeff_norm"] + 0.01


def test_chebyshev_stable_under_perturbation():
    data1 = _make_data()
    data2 = ZNEData(scales=data1.scales, estimates=data1.estimates + 0.001)
    r1 = fit_chebyshev_tikhonov_zne(data1, degree=2, bounds=(-1, 1))
    r2 = fit_chebyshev_tikhonov_zne(data2, degree=2, bounds=(-1, 1))
    assert abs(r1.estimate - r2.estimate) < 0.05


# --- Bounded Bayesian GP tests ---

def test_bayesian_bounded_output():
    data = _make_data(f0=0.95)
    result = fit_bayesian_zne_gp(data, bounds=(-1, 1))
    assert -1.0 <= result.estimate <= 1.0


def test_bayesian_variance_nonnegative():
    data = _make_data()
    result = fit_bayesian_zne_gp(data, bounds=(-1, 1))
    assert result.variance >= 0


def test_bayesian_ci_contains_mean():
    data = _make_data()
    result = fit_bayesian_zne_gp(data, bounds=(-1, 1))
    ci95 = result.diagnostics["ci95"]
    assert ci95[0] <= result.estimate <= ci95[1]


def test_bayesian_tiny_variance_no_crash():
    scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    values = 0.8 * np.exp(-0.2 * scales)
    variances = np.full(5, 1e-10)
    data = ZNEData(scales=scales, estimates=values, variances=variances)
    result = fit_bayesian_zne_gp(data, bounds=(-1, 1))
    assert np.isfinite(result.estimate)
    assert np.isfinite(result.variance)


def test_bayesian_matern_kernel():
    data = _make_data()
    result = fit_bayesian_zne_gp(data, bounds=(-1, 1), kernel="matern32")
    assert -1.0 <= result.estimate <= 1.0
    assert result.diagnostics["kernel"] == "matern32"
