"""Locality-aware ZNE estimator wrapper.

Sets regularization strength based on observable structure.
Two modes: 'support' (simple weight heuristic) or 'commutator' (derivative envelope proxy).
"""

from ..types import ZNEData, FitResult
from ..theory.locality import (
    estimate_observable_support,
    locality_envelope_proxy,
    recommend_regularization_from_locality,
)
from ..theory.commutator_envelopes import derivative_envelope_proxy
from .chebyshev import fit_chebyshev_tikhonov_zne


def fit_locality_aware_zne(
    data: ZNEData,
    pauli_string: str,
    depth: int,
    noise_strength: float,
    base_degree: int = 2,
    bounds: tuple[float, float] = (-1.0, 1.0),
    locality_mode: str = "support",
    hamiltonian_terms: list[str] | None = None,
    noise_terms: list[str] | None = None,
) -> FitResult:
    """Locality-aware ZNE: adapts regularization to observable structure.

    locality_mode:
        "support" — uses simple support-size heuristic (v0.8 behavior)
        "commutator" — uses commutator-based derivative envelope proxy (v1.5)
    """
    support = estimate_observable_support(pauli_string)

    if locality_mode == "commutator" and hamiltonian_terms and noise_terms:
        envelope = derivative_envelope_proxy(
            pauli_string, hamiltonian_terms, noise_terms, depth, noise_strength
        )
        reg_lambda = envelope["recommended_regularization_strength"]
        mode_diagnostics = {"commutator_envelope": envelope}
    else:
        envelope = locality_envelope_proxy(support, depth, noise_strength)
        reg_lambda = recommend_regularization_from_locality(envelope)
        mode_diagnostics = {"support_envelope": envelope}

    result = fit_chebyshev_tikhonov_zne(data, degree=base_degree, bounds=bounds, reg_lambda=reg_lambda)

    result.method = f"locality_aware_{locality_mode}"
    result.diagnostics["support_size"] = support
    result.diagnostics["pauli_weight"] = support
    result.diagnostics["envelope_proxy"] = envelope
    result.diagnostics["recommended_reg_lambda"] = reg_lambda
    result.diagnostics["locality_mode"] = locality_mode
    result.diagnostics.update(mode_diagnostics)
    result.assumptions.append(f"Locality-aware ({locality_mode}): support={support}, depth={depth}")
    result.assumptions.append("Regularization heuristic, not theorem-backed")

    return result
