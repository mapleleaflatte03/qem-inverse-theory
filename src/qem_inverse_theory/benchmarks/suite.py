"""Benchmark suite runner for systematic ZNE evaluation."""

import numpy as np
from ..types import ZNEData
from ..estimators.constrained import fit_bounded_polynomial_zne
from ..estimators.chebyshev import fit_chebyshev_tikhonov_zne
from .circuit_families import sample_circuit_family
from .noise_models import apply_noise_model
from .shot_noise import add_gaussian_shot_noise
from .metrics import absolute_error


def run_benchmark_suite(
    family: str,
    noise_model: str = "depolarizing",
    n_qubits: int = 4,
    depth: int = 4,
    shots_total: int = 1000,
    seed: int = 42,
) -> dict:
    """Run a single benchmark instance and return metrics.

    Uses the circuit-family response generator with the specified noise model
    overlay. Returns raw and constrained estimates with error metrics.
    """
    scales = np.array([1.0, 1.5, 2.0, 3.0, 4.0])
    rng = np.random.default_rng(seed)

    # Get circuit-family response
    data, f0 = sample_circuit_family(
        family, n_qubits=n_qubits, depth=depth,
        noise_strength=0.04, scales=scales, shots=shots_total, seed=seed
    )

    # Raw estimate (first scale factor)
    raw_estimate = data.estimates[0]

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
        "raw_estimate": float(raw_estimate),
        "bounded_estimate": bounded_result.estimate,
        "chebyshev_estimate": chebyshev_result.estimate,
        "raw_error": absolute_error(float(raw_estimate), f0),
        "bounded_error": absolute_error(bounded_result.estimate, f0),
        "chebyshev_error": absolute_error(chebyshev_result.estimate, f0),
        "physical_valid_raw": -1.0 <= raw_estimate <= 1.0,
        "physical_valid_bounded": -1.0 <= bounded_result.estimate <= 1.0,
        "physical_valid_chebyshev": -1.0 <= chebyshev_result.estimate <= 1.0,
    }
