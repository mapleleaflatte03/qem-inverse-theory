"""Constrained polynomial ZNE estimators using bounded optimization."""

import numpy as np
from scipy.optimize import minimize

from ..types import ZNEData, FitResult
from ..constraints.spectral import spectral_bounds, project_to_spectral_bounds


def _poly_residuals(coeffs: np.ndarray, scales: np.ndarray, values: np.ndarray) -> float:
    """Sum of squared residuals for polynomial fit."""
    predicted = np.polyval(coeffs, scales)
    return float(np.sum((values - predicted) ** 2))


def fit_bounded_polynomial_zne(
    data: ZNEData, degree: int, bounds: tuple[float, float] = (-1.0, 1.0)
) -> FitResult:
    """Polynomial ZNE with constrained optimization enforcing f(0) ∈ bounds.

    Uses L-BFGS-B with the constraint that the constant term (f(0)) lies
    within physical bounds. This is NOT post-hoc clipping.
    """
    n = data.n
    # Initial guess: unconstrained polyfit
    x0 = np.polyfit(data.scales, data.estimates, degree)

    # Bounds: only the last coefficient (constant term = f(0)) is bounded
    param_bounds = [(None, None)] * degree + [bounds]

    result = minimize(
        _poly_residuals,
        x0,
        args=(data.scales, data.estimates),
        method="L-BFGS-B",
        bounds=param_bounds,
    )

    estimate = float(result.x[-1])  # constant term = f(0)
    residuals = data.estimates - np.polyval(result.x, data.scales)

    return FitResult(
        estimate=estimate,
        method=f"bounded_polynomial_deg{degree}",
        diagnostics={
            "coefficients": result.x.tolist(),
            "rss": float(np.sum(residuals**2)),
            "converged": result.success,
        },
        assumptions=[
            f"f(0) ∈ [{bounds[0]}, {bounds[1]}]",
            f"polynomial degree {degree}",
            "L-BFGS-B constrained optimization",
        ],
    )


def fit_spectral_constrained_zne(
    data: ZNEData, degree: int, eigenvalues: np.ndarray
) -> FitResult:
    """Polynomial ZNE with bounds derived from observable eigenvalues."""
    bounds = spectral_bounds(np.asarray(eigenvalues))
    result = fit_bounded_polynomial_zne(data, degree, bounds)
    result.method = f"spectral_constrained_deg{degree}"
    result.assumptions.append(f"spectral bounds from eigenvalues: {bounds}")
    return result
