"""Simple noise models for synthetic ZNE experiments."""

import numpy as np


def depolarizing_expectation(f0: float, scale: float, n_qubits: int = 1) -> float:
    """Expected value under global depolarizing noise at given scale.

    E[O] = f0 · (1 - p)^scale where p = noise rate per layer.
    Simplified: f(λ) = f0 · exp(-γ·λ) for small p.
    """
    gamma = 0.1 * n_qubits  # effective decay rate
    return f0 * np.exp(-gamma * scale)


def amplitude_damping_expectation(f0: float, scale: float, gamma: float = 0.05) -> float:
    """Expected Z-measurement under amplitude damping."""
    damping = 1 - np.exp(-gamma * scale)
    return f0 * (1 - damping) + damping  # relaxes toward |0>
