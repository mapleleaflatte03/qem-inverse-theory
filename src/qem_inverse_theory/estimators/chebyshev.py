"""Chebyshev-basis constrained ZNE with Tikhonov regularization."""

import numpy as np
from scipy.optimize import minimize

from ..types import ZNEData, FitResult


def _chebyshev_design(x: np.ndarray, degree: int) -> np.ndarray:
    """Chebyshev polynomial design matrix mapped to [x_min, x_max] → [-1, 1]."""
    x_min, x_max = x.min(), x.max()
    z = 2.0 * (x - x_min) / max(1e-12, x_max - x_min) - 1.0
    T = [np.ones_like(z)]
    if degree >= 1:
        T.append(z)
    for k in range(2, degree + 1):
        T.append(2.0 * z * T[-1] - T[-2])
    return np.column_stack(T)


def _chebyshev_eval_at_zero(scales: np.ndarray, degree: int) -> np.ndarray:
    """Chebyshev basis evaluated at λ=0 (mapped to z-space)."""
    x_min, x_max = scales.min(), scales.max()
    z0 = 2.0 * (0.0 - x_min) / max(1e-12, x_max - x_min) - 1.0
    T = [1.0]
    if degree >= 1:
        T.append(z0)
    for k in range(2, degree + 1):
        T.append(2.0 * z0 * T[-1] - T[-2])
    return np.array(T)


def fit_chebyshev_tikhonov_zne(
    data: ZNEData,
    degree: int = 2,
    bounds: tuple[float, float] = (-1.0, 1.0),
    reg_lambda: float = 1e-3,
) -> FitResult:
    """Chebyshev-basis ZNE with Tikhonov regularization and physical bounds.

    Minimizes weighted RSS + λ·‖coeffs‖² subject to f(0) ∈ bounds.
    """
    x = data.scales
    y = data.estimates
    n = data.n
    Phi = _chebyshev_design(x, degree)
    e0 = _chebyshev_eval_at_zero(x, degree)

    # Variance weights
    if data.variances is not None:
        w = 1.0 / np.maximum(data.variances, 1e-12)
    else:
        w = np.ones(n)

    def objective(coeffs):
        residuals = y - Phi @ coeffs
        wls = np.sum(w * residuals**2)
        reg = reg_lambda * np.sum(coeffs[1:]**2)  # don't penalize intercept
        return wls + reg

    # Constraint: bounds[0] <= e0 @ coeffs <= bounds[1]
    constraints = [
        {"type": "ineq", "fun": lambda c: e0 @ c - bounds[0]},
        {"type": "ineq", "fun": lambda c: bounds[1] - e0 @ c},
    ]

    c0 = np.linalg.lstsq(Phi, y, rcond=None)[0]
    result = minimize(objective, c0, method="SLSQP", constraints=constraints)

    estimate = float(e0 @ result.x)
    residuals = y - Phi @ result.x
    rss = float(np.sum(residuals**2))

    return FitResult(
        estimate=estimate,
        method="chebyshev_tikhonov",
        diagnostics={
            "coefficients": result.x.tolist(),
            "rss": rss,
            "reg_lambda": reg_lambda,
            "degree": degree,
            "success": result.success,
            "coeff_norm": float(np.linalg.norm(result.x)),
        },
        assumptions=[
            f"Chebyshev basis degree {degree}",
            f"Tikhonov reg λ={reg_lambda}",
            f"f(0) ∈ [{bounds[0]}, {bounds[1]}]",
        ],
    )
