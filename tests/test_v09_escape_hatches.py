"""Tests for v0.9: structured escape-hatch taxonomy."""

import pytest
from qem_inverse_theory.theory.structured_escape_hatches import (
    StructureDescriptor,
    classify_structure,
    explain_escape_hatch,
)


def test_low_support_low_depth_is_low_risk():
    desc = StructureDescriptor(circuit_depth=5, observable_support=2, scrambling_indicator=0.1)
    assert classify_structure(desc) == "low-risk structured"


def test_high_scrambling_large_system_is_generic_hard():
    desc = StructureDescriptor(
        circuit_depth=50, observable_support=20,
        estimated_lightcone_size=40, scrambling_indicator=0.9
    )
    assert classify_structure(desc) == "generic hard"


def test_intermediate_classification():
    desc = StructureDescriptor(circuit_depth=15, observable_support=6, scrambling_indicator=0.5)
    assert classify_structure(desc) == "intermediate"


def test_explanation_includes_caveat():
    desc = StructureDescriptor(circuit_depth=5, observable_support=2, scrambling_indicator=0.1)
    explanation = explain_escape_hatch(desc)
    assert "caveat" in explanation
    assert "not a proven escape" in explanation["caveat"].lower() or "not a theorem" in explanation["caveat"].lower()


def test_explanation_has_assumptions():
    desc = StructureDescriptor(
        circuit_depth=5, observable_support=3,
        symmetry_constraints=["Z2"], scrambling_indicator=0.1
    )
    explanation = explain_escape_hatch(desc)
    assert len(explanation["assumptions"]) > 0
    assert any("symmetry" in a.lower() for a in explanation["assumptions"])


def test_no_defeat_lower_bounds_phrase():
    """Explanations must not claim to defeat lower bounds."""
    desc = StructureDescriptor(circuit_depth=5, observable_support=2, scrambling_indicator=0.1)
    explanation = explain_escape_hatch(desc)
    full_text = str(explanation).lower()
    assert "defeat lower bounds" not in full_text
    assert "overcome lower bounds" not in full_text
