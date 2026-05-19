"""Benchmark suite runner for systematic ZNE evaluation."""

import numpy as np
from ..types import ZNEData
from ..estimators.constrained import fit_bounded_polynomial_zne
from ..estimators.chebyshev import fit_chebyshev_tikhonov_zne
from .circuit_families import ghz_sanity_response, tfim_trotter_response, heisenberg_trotter_response, hardware_efficient_vqe_response, qaoa_response
from .noise_models import apply_noise_model
from .shot_noise import add_gaussian_shot_noise
from .metrics import absolute_error

_FAMILY_F0 = {
    "ghz": lambda nq, d, ns: ghz_sanity_response(nq, ns)[1],
    "tfim": lambda nq, d, ns: tfim_trotter_response(nq, d, ns)[1],
    "heisenberg": lambda nq, d, ns: heisenberg_trotter_response(nq, d, ns)[1],
    "vqe": lambda nq, d, ns: hardware_efficient_vqe_response(nq, d, ns)[1],
    "qaoa": lambda nq, d, ns: qaoa_response(nq, d, ns)[1],
}


def run_benchmark_suite(
    family: str,
    noise_model: str = "depolarizing",
    n_qubits: int = 4,
    depth: int = 4,
    shots_total: int = 1000,
    seed: int = 42,
) -> dict:
    """Run a single benchmark instance and return metrics.

    The family determines f(0) (the noiseless reference value).
    The noise_model determines the noisy response f(λ) for λ > 0.
    Shot noise is added on top.
    """
    scales = np.array([1.0, 1.5, 2.0, 3.0, 4.0])
    rng = np.random.default_rng(seed)

    if family not in _FAMILY_F0:
        raise ValueError(f"Unknown family: {family}. Available: {list(_FAMILY_F0.keys())}")

    # Get true f(0) from circuit family
    noise_strength = 0.04
    f0 = _FAMILY_F0[family](n_qubits, depth, noise_strength)

    # Generate noisy response using the specified noise model
    clean = apply_noise_model(f0, scales, noise_model, n_qubits=n_qubits)

    # Add shot noise
    noisy = add_gaussian_shot_noise(clean, shots=shots_total, rng=rng)
    variances = np.maximum(1.0 - noisy**2, 0.01) / shots_total

    data = ZNEData(scales=scales, estimates=noisy, variances=variances,
                   metadata={"family": family, "noise_model": noise_model,
                             "n_qubits": n_qubits, "depth": depth, "seed": seed})

    # Raw estimate (first scale factor)
    raw_estimate = float(noisy[0])

    # Constrained estimates
    bounded_result = fit_bounded_polynomial_zne(data, degree=2, bounds=(-1.0, 1.0))
    chebyshev_result = fit_chebyshev_tikhonov_zne(data, degree=2, bounds=(-1.0, 1.0))

    return {
        "family": family,
        "noise_model": noise_model,
        "n_qubits": n_qubits,
        "depth": depth,
        "shots_total": shots_total,
        "seed": seed,
        "true_f0": f0,
        "raw_estimate": raw_estimate,
        "bounded_estimate": bounded_result.estimate,
        "chebyshev_estimate": chebyshev_result.estimate,
        "raw_error": absolute_error(raw_estimate, f0),
        "bounded_error": absolute_error(bounded_result.estimate, f0),
        "chebyshev_error": absolute_error(chebyshev_result.estimate, f0),
        "physical_valid_raw": -1.0 <= raw_estimate <= 1.0,
        "physical_valid_bounded": -1.0 <= bounded_result.estimate <= 1.0,
        "physical_valid_chebyshev": -1.0 <= chebyshev_result.estimate <= 1.0,
    }
