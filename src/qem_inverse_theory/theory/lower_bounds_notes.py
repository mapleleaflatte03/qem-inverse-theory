"""Notes on QEM lower bounds and structured escape hatches.

This module documents the theoretical landscape rather than implementing
rigorous proofs. It serves as a research notebook.
"""


def lower_bound_landscape() -> dict:
    """Summary of known QEM lower bounds and potential escape hatches."""
    return {
        "generic_lower_bounds": [
            "Takagi et al. (2022): Exponential sampling overhead for generic QEM",
            "Quek et al. (2024): Tighter bounds, Ω(2^n) for worst-case circuits",
            "Tsubouchi et al. (2023): Universal cost bounds",
        ],
        "why_they_dont_kill_zne": (
            "Lower bounds apply to worst-case circuits and generic noise. "
            "Practical circuits have structure (locality, symmetry, bounded depth) "
            "that may allow polynomial-cost mitigation."
        ),
        "potential_escape_hatches": [
            "Bounded observables: spectral constraints reduce ambiguity set",
            "Local noise: noise acts on few qubits → low effective dimension",
            "Symmetry: conserved quantities constrain the noise channel",
            "Low scrambling: shallow circuits don't fully mix information",
            "Spectral gap: gap in noise channel eigenvalues aids extrapolation",
            "Known noise structure: if noise model is partially known, fewer samples needed",
        ],
        "research_direction": (
            "We search for structured regimes where mitigation remains identifiable "
            "despite generic lower bounds. The goal is not to violate lower bounds "
            "but to identify their assumptions and find natural problems outside them."
        ),
    }
