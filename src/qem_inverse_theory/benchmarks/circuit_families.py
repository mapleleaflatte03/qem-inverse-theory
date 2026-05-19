"""Synthetic circuit-family response generators for ZNE benchmarking.

These model the noise response f(λ) for different circuit families WITHOUT
requiring quantum hardware or circuit simulation. Each generator returns a
callable that maps scale factors to expectation values, plus the exact f(0).

These are physics-inspired synthetic models, not exact circuit simulations.
They capture qualitative features (decay rates, oscillations, saturation)
observed in different circuit classes under noise amplification.
"""

import numpy as np
from ..types import ZNEData
from .shot_noise import add_gaussian_shot_noise


def ghz_sanity_response(n_qubits: int = 4, noise_strength: float = 0.05):
    """GHZ state: fast exponential decay, f(0) near ±1.

    GHZ states are maximally sensitive to dephasing — decay rate scales
    linearly with n_qubits.
    """
    f0 = (-1.0) ** (n_qubits % 2) * 0.95
    decay = noise_strength * n_qubits

    def response(scales):
        return f0 * np.exp(-decay * np.asarray(scales))

    return response, f0


def tfim_trotter_response(n_qubits: int = 6, depth: int = 4, noise_strength: float = 0.03):
    """1D TFIM Trotter circuit: moderate decay with slight oscillation.

    Transverse-field Ising model Trotterization produces structured circuits
    with local entanglement. Noise response has moderate decay plus small
    oscillatory component from Trotter error interaction with noise.
    """
    f0 = 0.7 + 0.1 * np.exp(-0.1 * n_qubits)
    decay = noise_strength * depth * 0.5
    osc_amp = 0.02 * depth / n_qubits

    def response(scales):
        s = np.asarray(scales)
        return f0 * np.exp(-decay * s) * (1 + osc_amp * np.sin(2 * s))

    return response, f0


def heisenberg_trotter_response(n_qubits: int = 6, depth: int = 6, noise_strength: float = 0.03):
    """Heisenberg chain Trotter: slower decay than TFIM, more structured.

    Heisenberg model has SU(2) symmetry which partially protects against
    certain noise channels. Decay is slower but response is more nonlinear.
    """
    f0 = 0.65 + 0.05 * np.exp(-0.05 * n_qubits)
    decay = noise_strength * depth * 0.35
    nonlin = 0.01 * noise_strength * depth

    def response(scales):
        s = np.asarray(scales)
        return f0 * np.exp(-decay * s) - nonlin * s**2

    return response, f0


def hardware_efficient_vqe_response(n_qubits: int = 4, depth: int = 3, noise_strength: float = 0.04):
    """Hardware-efficient VQE ansatz: moderate decay, parameter-dependent.

    VQE circuits have variable structure depending on parameters.
    Response is exponential with a polynomial correction modeling
    parameter-noise interaction.
    """
    f0 = -0.5 - 0.1 * n_qubits  # energy-like observable (negative)
    f0 = max(f0, -0.95)  # keep within reasonable bounds
    decay = noise_strength * depth * n_qubits * 0.1
    poly_corr = 0.005 * depth

    def response(scales):
        s = np.asarray(scales)
        base = f0 * np.exp(-decay * s)
        correction = poly_corr * s * (1 - np.exp(-s))
        return base + correction

    return response, f0


def qaoa_response(n_qubits: int = 8, p: int = 2, noise_strength: float = 0.04):
    """QAOA p-layer: fast initial decay then plateau.

    QAOA circuits alternate problem and mixer unitaries. Under noise,
    the expectation value decays quickly for the first few scale factors
    then saturates toward the maximally mixed value.
    """
    f0 = 0.6 + 0.05 * p
    f0 = min(f0, 0.85)
    decay = noise_strength * p * n_qubits * 0.08
    saturation = 0.0  # maximally mixed value for the observable

    def response(scales):
        s = np.asarray(scales)
        return saturation + (f0 - saturation) * np.exp(-decay * s)

    return response, f0


def sample_circuit_family(
    family: str,
    n_qubits: int = 4,
    depth: int = 4,
    noise_strength: float = 0.04,
    scales: np.ndarray | None = None,
    shots: int = 1000,
    seed: int = 42,
) -> tuple[ZNEData, float]:
    """Sample noisy ZNE data from a circuit-family response model.

    Returns (ZNEData, true_f0).
    """
    if scales is None:
        scales = np.array([1.0, 1.5, 2.0, 3.0, 4.0])

    generators = {
        "ghz": lambda: ghz_sanity_response(n_qubits, noise_strength),
        "tfim": lambda: tfim_trotter_response(n_qubits, depth, noise_strength),
        "heisenberg": lambda: heisenberg_trotter_response(n_qubits, depth, noise_strength),
        "vqe": lambda: hardware_efficient_vqe_response(n_qubits, depth, noise_strength),
        "qaoa": lambda: qaoa_response(n_qubits, depth, noise_strength),
    }

    if family not in generators:
        raise ValueError(f"Unknown family: {family}. Available: {list(generators.keys())}")

    response_fn, f0 = generators[family]()
    clean = response_fn(scales)
    rng = np.random.default_rng(seed)
    noisy = add_gaussian_shot_noise(clean, shots=shots, rng=rng)
    variances = np.maximum(1.0 - noisy**2, 0.01) / shots

    data = ZNEData(scales=scales, estimates=noisy, variances=variances,
                   metadata={"family": family, "n_qubits": n_qubits, "depth": depth,
                             "noise_strength": noise_strength, "seed": seed})
    return data, f0
