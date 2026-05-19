"""Structured escape-hatch taxonomy for QEM lower bounds.

Classifies circuit/observable structures by their potential to escape
generic QEM lower-bound pessimism. This is a research taxonomy, not a theorem.
"""

from dataclasses import dataclass, field


@dataclass
class StructureDescriptor:
    """Describes the structure of a ZNE instance for escape-hatch classification."""

    circuit_depth: int
    observable_support: int
    estimated_lightcone_size: int | None = None
    symmetry_constraints: list[str] = field(default_factory=list)
    noise_model: str = "local_depolarizing"
    scrambling_indicator: float = 0.0  # 0 = no scrambling, 1 = maximal


def classify_structure(desc: StructureDescriptor) -> str:
    """Classify structure as low-risk, intermediate, or generic hard.

    This is a heuristic taxonomy, not a rigorous classification.
    """
    lightcone = desc.estimated_lightcone_size or min(desc.circuit_depth + desc.observable_support, 50)

    # Low-risk: small effective problem
    if desc.observable_support <= 4 and desc.circuit_depth <= 10 and desc.scrambling_indicator < 0.3:
        return "low-risk structured"

    # Generic hard: large, scrambling, no symmetry
    if (desc.scrambling_indicator > 0.7 and lightcone > 20
            and not desc.symmetry_constraints):
        return "generic hard"

    return "intermediate"


def explain_escape_hatch(desc: StructureDescriptor) -> dict:
    """Explain why a structure might escape generic lower-bound pessimism."""
    classification = classify_structure(desc)
    lightcone = desc.estimated_lightcone_size or min(desc.circuit_depth + desc.observable_support, 50)

    assumptions = []
    why_escape = []
    still_hard = []
    recommended = []

    if desc.observable_support <= 4:
        assumptions.append("Observable has small support (≤4 qubits)")
        why_escape.append("Generic lower bounds scale with system size; local observables may have effective dimension independent of n")
        recommended.append("Test MSE scaling with n at fixed support")

    if desc.circuit_depth <= 10:
        assumptions.append("Circuit is shallow (depth ≤10)")
        why_escape.append("Information propagation is limited; noise response may be simpler")
        recommended.append("Compare ambiguity diameter at different depths")

    if desc.symmetry_constraints:
        assumptions.append(f"Symmetry constraints: {desc.symmetry_constraints}")
        why_escape.append("Symmetry reduces effective Hilbert space dimension")
        recommended.append("Test whether symmetry-projected estimates have lower variance")

    if desc.scrambling_indicator < 0.3:
        assumptions.append("Low scrambling (indicator < 0.3)")
        why_escape.append("Weak scrambling preserves locality; noise response is smoother")
    else:
        still_hard.append("High scrambling makes noise response complex and hard to extrapolate")

    if lightcone > 20:
        still_hard.append("Large effective light cone means many qubits contribute to noise")

    if not assumptions:
        still_hard.append("No identified structural advantage over generic case")

    return {
        "classification": classification,
        "assumptions": assumptions,
        "why_lower_bounds_may_not_directly_apply": why_escape,
        "what_still_remains_hard": still_hard,
        "recommended_experiment": recommended,
        "caveat": "This is a research taxonomy, not a proven escape from lower bounds.",
    }
