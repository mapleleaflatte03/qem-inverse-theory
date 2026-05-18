"""ZNE formulated as a constrained inverse problem."""


def zne_as_inverse_problem() -> dict:
    """Structured description of ZNE as an inverse problem.

    Returns a dictionary describing the mathematical structure.
    """
    return {
        "observed": (
            "Noisy expectations y_i = f(λ_i) + ε_i at scale factors λ_1 < ... < λ_n, "
            "where ε_i ~ N(0, σ_i²) is shot noise."
        ),
        "unknown": (
            "The noiseless expectation f(0) = Tr[ρ_ideal · O], "
            "which is never directly observed."
        ),
        "ill_posedness": (
            "Without constraints on the function class F, infinitely many smooth "
            "functions interpolate the observed data but disagree at λ=0. "
            "The problem is ill-posed in the sense of Hadamard: "
            "the solution does not depend continuously on the data."
        ),
        "physical_constraints": [
            "Spectral bounds: f(0) ∈ [λ_min(O), λ_max(O)]",
            "Monotonicity (for depolarizing noise): f is non-increasing in λ",
            "Smoothness: f ∈ C^k for some k (physical noise channels are analytic)",
            "Probability simplex: for state tomography, probabilities sum to 1",
        ],
        "assumptions_required": [
            "Function class F must be specified (polynomial, exponential, etc.)",
            "Scale factors must be known exactly (no calibration error)",
            "Shot noise must be characterized (variance known or estimable)",
            "Physical bounds must be known a priori from the observable",
        ],
        "key_insight": (
            "Physical constraints reduce the ambiguity set. The question is: "
            "do they reduce it to a singleton (identifiability) or merely to a "
            "bounded interval (partial identifiability)?"
        ),
    }
