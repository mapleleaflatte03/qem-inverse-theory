"""Operator locality heuristics for ZNE regularization.

Provides support-size estimation, Pauli weight, and a locality-based
envelope proxy for recommending regularization strength.
"""

import numpy as np


def estimate_observable_support(pauli_string: str) -> int:
    """Count non-identity qubits in a Pauli string."""
    return sum(1 for c in pauli_string.upper() if c in "XYZ")


def pauli_weight(pauli_string: str) -> int:
    """Pauli weight = number of non-identity operators."""
    return estimate_observable_support(pauli_string)


def locality_envelope_proxy(
    support_size: int,
    depth: int,
    noise_strength: float,
    locality_radius: int = 1,
) -> dict:
    """Heuristic envelope proxy for noise sensitivity of a local observable.

    Estimates how much the observable's expectation value is affected by
    noise propagation through the circuit. Larger values suggest more
    extrapolation instability and need for stronger regularization.

    This is a heuristic proxy, not a rigorous bound.
    """
    # Effective light cone: support grows with depth up to locality_radius per layer
    effective_support = min(support_size + depth * locality_radius, 50)
    # Noise sensitivity scales with effective support and noise strength
    sensitivity = effective_support * noise_strength
    # Extrapolation instability proxy
    instability = sensitivity * (1 + 0.1 * depth)

    return {
        "support_size": support_size,
        "effective_support": effective_support,
        "noise_sensitivity": float(sensitivity),
        "instability_proxy": float(instability),
    }


def recommend_regularization_from_locality(envelope: dict) -> float:
    """Recommend Tikhonov regularization strength from locality envelope.

    Higher instability → stronger regularization to prevent overfitting.
    """
    instability = envelope["instability_proxy"]
    # Map instability to reg_lambda: sigmoid-like scaling
    reg_lambda = 1e-4 + 0.1 * (1.0 - np.exp(-instability))
    return float(reg_lambda)
