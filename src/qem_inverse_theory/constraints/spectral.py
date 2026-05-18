"""Spectral bounds from observable eigenvalues."""

import numpy as np
from numpy.typing import NDArray


def spectral_bounds(eigenvalues: NDArray[np.float64]) -> tuple[float, float]:
    """Return (min, max) eigenvalues as physical bounds for expectation value."""
    eigs = np.asarray(eigenvalues, dtype=np.float64)
    return float(eigs.min()), float(eigs.max())


def validate_expectation(value: float, bounds: tuple[float, float]) -> bool:
    """Check if value lies within spectral bounds."""
    return bounds[0] <= value <= bounds[1]


def project_to_spectral_bounds(value: float, bounds: tuple[float, float]) -> float:
    """Project value onto spectral bounds [lb, ub]."""
    return float(np.clip(value, bounds[0], bounds[1]))
