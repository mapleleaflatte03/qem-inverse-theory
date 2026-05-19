"""Tests for commutator-based locality envelopes."""

import numpy as np
import pytest
from qem_inverse_theory.theory.commutator_envelopes import (
    pauli_string_weight, pauli_commutes, commutator_support_growth,
    derivative_envelope_proxy,
)
from qem_inverse_theory.estimators.locality_aware import fit_locality_aware_zne
from qem_inverse_theory.types import ZNEData


H_TERMS = ["XXII", "IXXI", "IIXX", "ZIII", "IZII", "IIZI", "IIIZ"]
N_TERMS = ["ZIII", "IZII", "IIZI", "IIIZ"]


def test_pauli_weight():
    assert pauli_string_weight("ZIII") == 1
    assert pauli_string_weight("ZZII") == 2
    assert pauli_string_weight("XYZX") == 4
    assert pauli_string_weight("IIII") == 0


def test_pauli_commutes_same():
    assert pauli_commutes("ZIII", "ZIII")


def test_pauli_commutes_identity():
    assert pauli_commutes("ZIII", "IIII")


def test_pauli_anticommutes():
    # X and Z on same qubit anticommute
    assert not pauli_commutes("XIII", "ZIII")


def test_pauli_commutes_different_sites():
    assert pauli_commutes("XIII", "IZII")


def test_commutator_growth_local():
    growth = commutator_support_growth("ZIII", H_TERMS)
    assert growth >= 1


def test_commutator_growth_increases_with_weight():
    g1 = commutator_support_growth("ZIII", H_TERMS)
    g4 = commutator_support_growth("ZZZZ", H_TERMS)
    assert g4 >= g1


def test_derivative_envelope_finite():
    env = derivative_envelope_proxy("ZZII", H_TERMS, N_TERMS, depth=5, noise_strength=0.04)
    assert np.isfinite(env["derivative_bound_proxy"])
    assert env["derivative_bound_proxy"] > 0


def test_derivative_envelope_local_leq_global():
    env_local = derivative_envelope_proxy("ZIII", H_TERMS, N_TERMS, depth=5, noise_strength=0.04)
    env_global = derivative_envelope_proxy("ZZZZ", H_TERMS, N_TERMS, depth=5, noise_strength=0.04)
    assert env_local["derivative_bound_proxy"] <= env_global["derivative_bound_proxy"]


def test_recommended_reg_finite():
    env = derivative_envelope_proxy("ZZII", H_TERMS, N_TERMS, depth=10, noise_strength=0.05)
    assert np.isfinite(env["recommended_regularization_strength"])
    assert env["recommended_regularization_strength"] > 0


def test_locality_aware_commutator_mode():
    scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    values = 0.8 * np.exp(-0.2 * scales)
    data = ZNEData(scales=scales, estimates=values)
    result = fit_locality_aware_zne(
        data, "ZZII", depth=5, noise_strength=0.04,
        locality_mode="commutator",
        hamiltonian_terms=H_TERMS, noise_terms=N_TERMS,
    )
    assert -1.0 <= result.estimate <= 1.0
    assert result.diagnostics["locality_mode"] == "commutator"
    assert "commutator_envelope" in result.diagnostics
