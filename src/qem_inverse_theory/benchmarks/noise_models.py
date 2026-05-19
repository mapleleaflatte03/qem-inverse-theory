"""Noise response models for synthetic ZNE experiments.

These model how expectation values change under different noise channels
at amplified scale factors. Synthetic/analytical — no hardware claims.
"""

import numpy as np


def depolarizing_expectation(f0: float, scale: float, n_qubits: int = 1) -> float:
    """Expected value under global depolarizing noise at given scale."""
    gamma = 0.1 * n_qubits
    return f0 * np.exp(-gamma * scale)


def amplitude_damping_expectation(f0: float, scale: float, gamma: float = 0.05) -> float:
    """Expected Z-measurement under amplitude damping."""
    damping = 1 - np.exp(-gamma * scale)
    return f0 * (1 - damping) + damping


def coherent_overrotation_response(f0: float, scale: float, angle: float = 0.05) -> float:
    """Response under coherent over-rotation noise.

    Coherent errors produce oscillatory behavior rather than pure decay.
    """
    return f0 * np.cos(angle * scale) * np.exp(-0.01 * scale)


def pauli_lindblad_response(f0: float, scale: float, rates: tuple = (0.03, 0.03, 0.04)) -> float:
    """Response under Pauli-Lindblad noise (X, Y, Z rates).

    Models independent Pauli noise channels with different rates.
    Total decay is sum of rates.
    """
    total_rate = sum(rates)
    return f0 * np.exp(-total_rate * scale)


def time_correlated_drift_response(f0: float, scale: float, drift_rate: float = 0.02, correlation_time: float = 3.0) -> float:
    """Response with time-correlated noise drift.

    Models slow drift in noise parameters (e.g., fluctuating qubit frequency).
    At short scales, behaves like standard noise; at long scales, drift accumulates.
    """
    base_decay = 0.05 * scale
    drift = drift_rate * scale * (1 - np.exp(-scale / correlation_time))
    return f0 * np.exp(-(base_decay + drift))


def non_markovian_stress_response(f0: float, scale: float, memory_strength: float = 0.1) -> float:
    """Non-Markovian stress test: partial information backflow.

    At intermediate scales, the expectation value partially recovers
    before continuing to decay. This violates the monotone decay assumption.
    """
    decay = 0.08 * scale
    backflow = memory_strength * np.exp(-0.5 * (scale - 2.5)**2)
    return f0 * (np.exp(-decay) + backflow)


def apply_noise_model(
    f0: float,
    scales: np.ndarray,
    noise_model: str = "depolarizing",
    **kwargs,
) -> np.ndarray:
    """Apply a named noise model to generate response at given scales."""
    models = {
        "depolarizing": lambda s: depolarizing_expectation(f0, s, kwargs.get("n_qubits", 1)),
        "amplitude_damping": lambda s: amplitude_damping_expectation(f0, s, kwargs.get("gamma", 0.05)),
        "coherent_overrotation": lambda s: coherent_overrotation_response(f0, s, kwargs.get("angle", 0.05)),
        "pauli_lindblad": lambda s: pauli_lindblad_response(f0, s, kwargs.get("rates", (0.03, 0.03, 0.04))),
        "time_correlated": lambda s: time_correlated_drift_response(f0, s, kwargs.get("drift_rate", 0.02)),
        "non_markovian": lambda s: non_markovian_stress_response(f0, s, kwargs.get("memory_strength", 0.1)),
    }
    if noise_model not in models:
        raise ValueError(f"Unknown noise model: {noise_model}. Available: {list(models.keys())}")
    return np.array([models[noise_model](s) for s in scales])
