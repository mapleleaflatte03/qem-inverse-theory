"""Synthetic ground-truth response functions for ZNE benchmarking."""

import numpy as np
from numpy.typing import NDArray


def exponential_decay_response(
    scales: NDArray[np.float64], f0: float = 0.8, decay_rate: float = 0.3
) -> NDArray[np.float64]:
    """f(λ) = f0 · exp(-α·λ). Models depolarizing-like noise."""
    return f0 * np.exp(-decay_rate * np.asarray(scales))


def polynomial_bias_response(
    scales: NDArray[np.float64], f0: float = 0.8, coeffs: tuple = (0.1, -0.02)
) -> NDArray[np.float64]:
    """f(λ) = f0 + c1·λ + c2·λ² + ... Models polynomial noise bias."""
    s = np.asarray(scales)
    result = np.full_like(s, f0)
    for i, c in enumerate(coeffs):
        result = result + c * s ** (i + 1)
    return result


def mixed_response(
    scales: NDArray[np.float64],
    f0: float = 0.8,
    decay_rate: float = 0.2,
    linear_coeff: float = 0.05,
    mix: float = 0.7,
) -> NDArray[np.float64]:
    """Mixture of exponential and polynomial response."""
    s = np.asarray(scales)
    exp_part = f0 * np.exp(-decay_rate * s)
    poly_part = f0 + linear_coeff * s
    return mix * exp_part + (1 - mix) * poly_part


def adversarial_response_with_same_observed_nodes(
    scales: NDArray[np.float64],
    f0_a: float = 0.8,
    f0_b: float = 0.3,
    decay_a: float = 0.2,
    decay_b: float = 0.5,
) -> tuple[NDArray[np.float64], NDArray[np.float64], float, float]:
    """Two response functions that agree at observed scales but differ at λ=0.

    Demonstrates non-identifiability: without constraints, the data cannot
    distinguish between the two underlying functions.

    Returns (values_a, values_b, true_f0_a, true_f0_b).
    Both are shifted to agree at the observed nodes.
    """
    s = np.asarray(scales)
    raw_a = f0_a * np.exp(-decay_a * s)
    raw_b = f0_b * np.exp(-decay_b * s)

    # Shift b to match a at observed nodes (least-squares offset)
    offset = np.mean(raw_a - raw_b)
    adjusted_b = raw_b + offset

    # True f(0) values differ
    true_f0_a = f0_a
    true_f0_b = f0_b + offset

    return raw_a, adjusted_b, true_f0_a, true_f0_b
