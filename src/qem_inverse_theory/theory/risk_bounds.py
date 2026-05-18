"""Risk bounds and condition numbers for ZNE extrapolation."""

import numpy as np


def polynomial_condition_number(scales: np.ndarray, degree: int) -> float:
    """Condition number of the Vandermonde extrapolation at λ=0.

    Measures how much noise in observations is amplified in the estimate.
    """
    V = np.vander(scales, degree + 1)
    # Extrapolation vector: evaluate polynomial at 0
    e0 = np.zeros(degree + 1)
    e0[-1] = 1.0  # constant term
    # Condition: ||V^{-1} e0|| relative to data norm
    try:
        coeffs_sensitivity = np.linalg.lstsq(V, np.eye(len(scales)), rcond=None)[0]
        extrap_weights = coeffs_sensitivity[-1, :]  # weights for f(0)
        return float(np.linalg.norm(extrap_weights, 1))
    except np.linalg.LinAlgError:
        return np.inf


def extrapolation_variance_amplification(
    scales: np.ndarray, degree: int, noise_variances: np.ndarray
) -> float:
    """Variance of f(0) estimate due to shot noise propagation."""
    V = np.vander(scales, degree + 1)
    try:
        VtV_inv = np.linalg.inv(V.T @ V)
        # Variance of constant term (f(0))
        e0 = np.zeros(degree + 1)
        e0[-1] = 1.0
        # Weighted least squares variance
        W = np.diag(1.0 / noise_variances)
        VtWV_inv = np.linalg.inv(V.T @ W @ V)
        return float(e0 @ VtWV_inv @ e0)
    except np.linalg.LinAlgError:
        return np.inf
