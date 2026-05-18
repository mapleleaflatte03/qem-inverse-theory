"""Identifiability analysis for ZNE inverse problem."""

import numpy as np


def ambiguity_diameter(
    scales: np.ndarray,
    values: np.ndarray,
    bounds: tuple[float, float],
    degree: int,
    tol: float = 1e-6,
) -> float:
    """Compute diameter of the ambiguity set for f(0).

    Given observed data and physical bounds, find the range of f(0) values
    consistent with polynomials of given degree that pass near the data.

    Returns max(f(0)) - min(f(0)) over all feasible polynomials.
    """
    from scipy.optimize import linprog

    n = len(scales)
    V = np.vander(scales, degree + 1)

    # Minimize/maximize the constant term (last coefficient = f(0))
    # subject to: |V @ c - values| <= tol (approximate interpolation)
    #             bounds[0] <= c[-1] <= bounds[1]

    # Reformulate: V @ c - values <= tol, values - V @ c <= tol
    # c[-1] >= bounds[0], c[-1] <= bounds[1]
    A_ub = np.vstack([V, -V])
    b_ub = np.concatenate([values + tol, -values + tol])

    # Bounds on coefficients
    c_bounds = [(None, None)] * degree + [bounds]

    # Minimize f(0) = c[-1]
    c_obj_min = np.zeros(degree + 1)
    c_obj_min[-1] = 1.0

    res_min = linprog(c_obj_min, A_ub=A_ub, b_ub=b_ub, bounds=c_bounds, method="highs")

    # Maximize f(0) = -minimize(-c[-1])
    c_obj_max = np.zeros(degree + 1)
    c_obj_max[-1] = -1.0

    res_max = linprog(c_obj_max, A_ub=A_ub, b_ub=b_ub, bounds=c_bounds, method="highs")

    if res_min.success and res_max.success:
        f0_min = res_min.x[-1]
        f0_max = res_max.x[-1]
        return float(f0_max - f0_min)
    else:
        return float("inf")


def is_identifiable(
    scales: np.ndarray,
    values: np.ndarray,
    bounds: tuple[float, float],
    degree: int,
    tol: float = 1e-4,
) -> bool:
    """Check if f(0) is approximately identifiable (ambiguity < tol)."""
    diam = ambiguity_diameter(scales, values, bounds, degree, tol=0.01)
    return diam < tol
