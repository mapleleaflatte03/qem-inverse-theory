"""Unconstrained polynomial ZNE estimators."""

import numpy as np

from ..types import ZNEData, FitResult


def predict_zero_noise_poly(
    scales: np.ndarray, values: np.ndarray, degree: int
) -> float:
    """Fit polynomial of given degree and evaluate at zero noise."""
    coeffs = np.polyfit(scales, values, degree)
    return float(np.polyval(coeffs, 0.0))


def fit_polynomial_zne(data: ZNEData, degree: int) -> FitResult:
    """Unconstrained polynomial ZNE fit."""
    estimate = predict_zero_noise_poly(data.scales, data.estimates, degree)
    coeffs = np.polyfit(data.scales, data.estimates, degree)
    residuals = data.estimates - np.polyval(coeffs, data.scales)
    return FitResult(
        estimate=estimate,
        method=f"polynomial_deg{degree}",
        diagnostics={"coefficients": coeffs.tolist(), "rss": float(np.sum(residuals**2))},
        assumptions=["no physical bounds enforced", f"polynomial degree {degree}"],
    )
