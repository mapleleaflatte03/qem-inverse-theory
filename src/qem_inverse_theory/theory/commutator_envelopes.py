"""Commutator-based locality envelopes for operator-aware ZNE.

Estimates derivative bounds and regularization recommendations based on
how an observable's support grows under commutation with Hamiltonian/noise terms.

This is a proxy based on Pauli algebra, not a rigorous Lieb-Robinson bound.
"""

import numpy as np


def pauli_string_weight(pauli: str) -> int:
    """Number of non-identity Pauli operators."""
    return sum(1 for c in pauli.upper() if c in "XYZ")


def _pauli_at(pauli: str, i: int) -> str:
    return pauli[i].upper() if i < len(pauli) else "I"


def pauli_commutes(p: str, q: str) -> bool:
    """Check if two Pauli strings commute.

    Two n-qubit Paulis commute iff they anti-commute on an even number of sites.
    """
    n = max(len(p), len(q))
    anticommuting_sites = 0
    for i in range(n):
        a, b = _pauli_at(p, i), _pauli_at(q, i)
        if a != "I" and b != "I" and a != b:
            anticommuting_sites += 1
    return anticommuting_sites % 2 == 0


def commutator_support_growth(observable: str, local_terms: list[str]) -> int:
    """Estimate support growth after one layer of commutation.

    Counts how many new sites are touched by [H_term, observable] for each term.
    """
    obs_sites = {i for i, c in enumerate(observable.upper()) if c != "I"}
    new_sites = set()
    for term in local_terms:
        if not pauli_commutes(observable, term):
            term_sites = {i for i, c in enumerate(term.upper()) if c != "I"}
            new_sites |= term_sites
    return len(obs_sites | new_sites)


def derivative_envelope_proxy(
    observable: str,
    hamiltonian_terms: list[str],
    noise_terms: list[str],
    depth: int,
    noise_strength: float,
) -> dict:
    """Estimate derivative envelope for ZNE response based on commutator growth.

    Models how the observable's effective support grows through circuit layers,
    affecting the smoothness and stability of the noise response f(λ).
    """
    obs_weight = pauli_string_weight(observable)

    # Estimate support growth per layer via commutation
    growth_per_layer = commutator_support_growth(observable, hamiltonian_terms + noise_terms)
    effective_support = min(growth_per_layer + (depth - 1) * max(0, growth_per_layer - obs_weight), 50)

    # Non-commuting noise terms affect derivative magnitude
    non_commuting_noise = sum(1 for t in noise_terms if not pauli_commutes(observable, t))
    noise_coupling = non_commuting_noise * noise_strength

    # Derivative bound proxy: larger effective support + more noise coupling = steeper response
    derivative_bound = noise_coupling * (1 + 0.1 * effective_support) * depth

    # Recommended regularization: scale with derivative bound
    # Calibrated to avoid the over-regularization seen in v0.8
    reg_strength = 1e-4 + 5e-3 * min(derivative_bound, 5.0)

    return {
        "observable_weight": obs_weight,
        "estimated_commutator_growth": growth_per_layer,
        "effective_support_after_depth": effective_support,
        "non_commuting_noise_terms": non_commuting_noise,
        "noise_coupling": float(noise_coupling),
        "derivative_bound_proxy": float(derivative_bound),
        "recommended_regularization_strength": float(reg_strength),
        "caveats": [
            "Proxy based on Pauli commutation counting, not rigorous Lieb-Robinson",
            "Derivative bound is heuristic, not proven",
            "Regularization mapping calibrated empirically, not theoretically optimal",
        ],
    }
