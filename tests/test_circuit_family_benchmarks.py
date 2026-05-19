"""Tests for v1.4: circuit-family benchmarks and extended noise models."""

import numpy as np
import pytest
from qem_inverse_theory.benchmarks.circuit_families import (
    ghz_sanity_response, tfim_trotter_response, heisenberg_trotter_response,
    hardware_efficient_vqe_response, qaoa_response, sample_circuit_family,
)
from qem_inverse_theory.benchmarks.noise_models import (
    coherent_overrotation_response, pauli_lindblad_response,
    time_correlated_drift_response, non_markovian_stress_response,
    apply_noise_model,
)
from qem_inverse_theory.benchmarks.suite import run_benchmark_suite


# --- Circuit families ---

@pytest.mark.parametrize("family", ["ghz", "tfim", "heisenberg", "vqe", "qaoa"])
def test_circuit_family_deterministic(family):
    data1, f0_1 = sample_circuit_family(family, seed=42)
    data2, f0_2 = sample_circuit_family(family, seed=42)
    assert f0_1 == f0_2
    np.testing.assert_array_equal(data1.estimates, data2.estimates)


@pytest.mark.parametrize("family", ["ghz", "tfim", "heisenberg", "vqe", "qaoa"])
def test_circuit_family_f0_finite(family):
    _, f0 = sample_circuit_family(family)
    assert np.isfinite(f0)
    assert -1.0 <= f0 <= 1.0


@pytest.mark.parametrize("family", ["ghz", "tfim", "heisenberg", "vqe", "qaoa"])
def test_circuit_family_scales_positive(family):
    data, _ = sample_circuit_family(family)
    assert np.all(data.scales > 0)


# --- Noise models ---

def test_coherent_overrotation_oscillates():
    vals = [coherent_overrotation_response(0.8, s, angle=2.0) for s in [0, 1, 2, 3, 4, 5]]
    # Should not be monotone due to cos
    diffs = np.diff(vals)
    assert not np.all(diffs <= 0), "Coherent noise should oscillate"


def test_pauli_lindblad_decays():
    v1 = pauli_lindblad_response(0.8, 1.0)
    v5 = pauli_lindblad_response(0.8, 5.0)
    assert v5 < v1


def test_time_correlated_decays():
    v1 = time_correlated_drift_response(0.8, 1.0)
    v5 = time_correlated_drift_response(0.8, 5.0)
    assert v5 < v1


def test_non_markovian_has_backflow():
    """Non-Markovian response should show partial recovery at intermediate scales."""
    vals = [non_markovian_stress_response(0.8, s, memory_strength=0.3) for s in np.linspace(0, 5, 20)]
    diffs = np.diff(vals)
    assert np.any(diffs > 0), "Non-Markovian should have some positive slope (backflow)"


def test_apply_noise_model_all():
    scales = np.array([1.0, 2.0, 3.0])
    for model in ["depolarizing", "amplitude_damping", "coherent_overrotation",
                  "pauli_lindblad", "time_correlated", "non_markovian"]:
        result = apply_noise_model(0.8, scales, model)
        assert len(result) == 3
        assert np.all(np.isfinite(result))


# --- Benchmark suite ---

def test_benchmark_suite_returns_metrics():
    r = run_benchmark_suite("tfim", shots_total=100, seed=42)
    assert "true_f0" in r
    assert "raw_error" in r
    assert "bounded_error" in r
    assert "chebyshev_error" in r
    assert r["family"] == "tfim"


def test_benchmark_suite_no_nans():
    for family in ["ghz", "tfim", "vqe"]:
        r = run_benchmark_suite(family, shots_total=500, seed=0)
        assert np.isfinite(r["raw_error"])
        assert np.isfinite(r["bounded_error"])
        assert np.isfinite(r["chebyshev_error"])


def test_benchmark_suite_fast():
    """Suite should run in under 2 seconds for a single instance."""
    import time
    t0 = time.time()
    run_benchmark_suite("qaoa", shots_total=1000, seed=42)
    assert time.time() - t0 < 2.0


# --- Noise model integration tests ---

def test_noise_model_changes_output():
    """Same family + seed but different noise_model must produce different errors."""
    r1 = run_benchmark_suite("tfim", noise_model="depolarizing", seed=42)
    r2 = run_benchmark_suite("tfim", noise_model="coherent_overrotation", seed=42)
    assert r1["chebyshev_error"] != r2["chebyshev_error"], "Different noise models should give different results"


def test_noise_model_deterministic():
    """Same family + noise_model + seed must give identical results."""
    r1 = run_benchmark_suite("vqe", noise_model="pauli_lindblad", seed=99)
    r2 = run_benchmark_suite("vqe", noise_model="pauli_lindblad", seed=99)
    assert r1["chebyshev_error"] == r2["chebyshev_error"]


def test_all_noise_models_run():
    """All 6 noise models should run without error for all families."""
    for family in ["ghz", "tfim", "vqe"]:
        for nm in ["depolarizing", "amplitude_damping", "coherent_overrotation",
                   "pauli_lindblad", "time_correlated", "non_markovian"]:
            r = run_benchmark_suite(family, noise_model=nm, shots_total=100, seed=0)
            assert np.isfinite(r["chebyshev_error"]), f"Failed: {family}/{nm}"
