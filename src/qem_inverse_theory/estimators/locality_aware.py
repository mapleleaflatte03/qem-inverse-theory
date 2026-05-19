"""Locality-aware ZNE estimator wrapper.

Sets regularization strength based on observable support size and circuit depth.
"""

from ..types import ZNEData, FitResult
from ..theory.locality import (
    estimate_observable_support,
    locality_envelope_proxy,
    recommend_regularization_from_locality,
)
from .chebyshev import fit_chebyshev_tikhonov_zne


def fit_locality_aware_zne(
    data: ZNEData,
    pauli_string: str,
    depth: int,
    noise_strength: float,
    base_degree: int = 2,
    bounds: tuple[float, float] = (-1.0, 1.0),
) -> FitResult:
    """Locality-aware ZNE: adapts regularization to observable structure.

    Uses Chebyshev-Tikhonov internally with reg_lambda determined by
    the locality envelope proxy.
    """
    support = estimate_observable_support(pauli_string)
    envelope = locality_envelope_proxy(support, depth, noise_strength)
    reg_lambda = recommend_regularization_from_locality(envelope)

    result = fit_chebyshev_tikhonov_zne(data, degree=base_degree, bounds=bounds, reg_lambda=reg_lambda)

    # Augment diagnostics
    result.method = "locality_aware_chebyshev"
    result.diagnostics["support_size"] = support
    result.diagnostics["pauli_weight"] = support
    result.diagnostics["envelope_proxy"] = envelope
    result.diagnostics["recommended_reg_lambda"] = reg_lambda
    result.assumptions.append(f"Locality-aware: support={support}, depth={depth}")
    result.assumptions.append("Regularization heuristic, not theorem-backed")

    return result
