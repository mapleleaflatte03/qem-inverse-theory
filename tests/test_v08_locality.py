"""Tests for v0.8: locality-aware ZNE prototype."""

import numpy as np
import pytest
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.theory.locality import (
    estimate_observable_support,
    pauli_weight,
    locality_envelope_proxy,
    recommend_regularization_from_locality,
)
from qem_inverse_theory.estimators.locality_aware import fit_locality_aware_zne
from qem_inverse_theory import (
    fit_locality_aware_zne as fit_loc_top,
    estimate_observable_support as eos_top,
    locality_envelope_proxy as lep_top,
)


def test_pauli_weight_basic():
    assert pauli_weight("ZIII") == 1
    assert pauli_weight("ZZII") == 2
    assert pauli_weight("XYZX") == 4
    assert pauli_weight("IIII") == 0


def test_support_ignores_identity():
    assert estimate_observable_support("ZIIZ") == 2
    assert estimate_observable_support("III") == 0


def test_envelope_increases_with_support():
    e1 = locality_envelope_proxy(1, depth=5, noise_strength=0.1)
    e4 = locality_envelope_proxy(4, depth=5, noise_strength=0.1)
    assert e4["instability_proxy"] > e1["instability_proxy"]


def test_envelope_increases_with_depth():
    e_shallow = locality_envelope_proxy(2, depth=2, noise_strength=0.1)
    e_deep = locality_envelope_proxy(2, depth=20, noise_strength=0.1)
    assert e_deep["instability_proxy"] > e_shallow["instability_proxy"]


def test_envelope_increases_with_noise():
    e_low = locality_envelope_proxy(2, depth=5, noise_strength=0.01)
    e_high = locality_envelope_proxy(2, depth=5, noise_strength=0.1)
    assert e_high["instability_proxy"] > e_low["instability_proxy"]


def test_recommended_reg_increases_with_envelope():
    e_small = locality_envelope_proxy(1, depth=2, noise_strength=0.01)
    e_large = locality_envelope_proxy(4, depth=20, noise_strength=0.1)
    r_small = recommend_regularization_from_locality(e_small)
    r_large = recommend_regularization_from_locality(e_large)
    assert r_large > r_small


def test_locality_aware_estimator_bounded():
    scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    values = 0.8 * np.exp(-0.2 * scales)
    data = ZNEData(scales=scales, estimates=values)
    result = fit_locality_aware_zne(data, "ZZII", depth=10, noise_strength=0.05)
    assert -1.0 <= result.estimate <= 1.0


def test_locality_aware_diagnostics():
    scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    values = 0.8 * np.exp(-0.2 * scales)
    data = ZNEData(scales=scales, estimates=values)
    result = fit_locality_aware_zne(data, "ZZZZ", depth=5, noise_strength=0.1)
    assert "support_size" in result.diagnostics
    assert "envelope_proxy" in result.diagnostics
    assert "recommended_reg_lambda" in result.diagnostics
    assert result.diagnostics["support_size"] == 4


def test_top_level_exports():
    assert fit_loc_top is fit_locality_aware_zne
    assert eos_top is estimate_observable_support
    assert lep_top is locality_envelope_proxy


def test_locality_results_contain_heuristic_caveat():
    """Results file must contain honest labeling."""
    from pathlib import Path
    results_path = Path(__file__).resolve().parent.parent / "results" / "locality_aware_proxy.md"
    if results_path.exists():
        text = results_path.read_text().lower()
        assert "heuristic" in text
        assert "not a rigorous theorem" in text or "not a rigorous" in text
