"""Shot noise simulation for finite-sample ZNE analysis."""

import numpy as np
from numpy.typing import NDArray


def pauli_variance_from_expectation(expectation: float) -> float:
    """Variance of single-shot Pauli measurement: Var = 1 - <O>²."""
    return 1.0 - expectation**2


def add_gaussian_shot_noise(
    values: NDArray[np.float64],
    shots: int,
    rng: np.random.Generator | None = None,
) -> NDArray[np.float64]:
    """Add Gaussian shot noise to expectation values.

    σ_i = sqrt((1 - v_i²) / shots) for Pauli observables.
    """
    if rng is None:
        rng = np.random.default_rng()
    v = np.asarray(values)
    variances = np.maximum(1.0 - v**2, 0.0) / shots
    noise = rng.normal(0, np.sqrt(variances))
    return v + noise


def allocate_shots_uniform(total_shots: int, n_points: int) -> NDArray[np.int64]:
    """Allocate shots uniformly across measurement points."""
    base = total_shots // n_points
    remainder = total_shots % n_points
    allocation = np.full(n_points, base, dtype=np.int64)
    allocation[:remainder] += 1
    return allocation
