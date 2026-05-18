"""Probability simplex projection for quantum state tomography constraints."""

import numpy as np
from numpy.typing import NDArray


def project_to_simplex(vector: NDArray[np.float64]) -> NDArray[np.float64]:
    """Project vector onto the probability simplex (Duchi et al. 2008)."""
    v = np.asarray(vector, dtype=np.float64)
    n = len(v)
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u) - 1.0
    rho = np.nonzero(u * np.arange(1, n + 1) > cssv)[0][-1]
    theta = cssv[rho] / (rho + 1.0)
    return np.maximum(v - theta, 0.0)


def validate_probability_vector(
    vector: NDArray[np.float64], tol: float = 1e-8
) -> bool:
    """Check if vector is a valid probability distribution."""
    v = np.asarray(vector, dtype=np.float64)
    return bool(np.all(v >= -tol) and abs(v.sum() - 1.0) <= tol)
