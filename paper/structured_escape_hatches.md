# Structured Escape Hatches: Paper-Ready Note

Generic QEM lower bounds (Takagi et al. 2022, Quek et al. 2024) establish exponential sampling overhead for worst-case instances. We do not claim to circumvent these results. Instead, we identify candidate structural assumptions that may place specific problem instances outside the pessimistic generic regime.

## Taxonomy Table

| Structure | Assumption added | Possible benefit | Current evidence | Missing proof |
|-----------|-----------------|------------------|------------------|---------------|
| Low support | Observable on k ≪ n qubits | Effective dimension ~ k | Experiment 11 (synthetic) | Risk bound parameterized by k |
| Low depth | D = O(1) or O(log n) | Smoother noise response | Ambiguity experiments | Stability bound with depth |
| Symmetry | Observable in symmetry sector | Reduced Hilbert space | Classification utility | Dimension reduction theorem |
| Weak scrambling | Low scrambling indicator | Structured extrapolation | Phase diagram (synthetic) | Condition number vs scrambling |
| Smooth response | f ∈ bounded analytic class | Constrained ambiguity | Ambiguity diameter results | Minimax rate theorem |
| Bayesian abstention | Calibrated posterior | Avoid harmful mitigation | Coverage calibration | Regret bound |

## Conservative framing

These are research directions, not results. Each row represents a conjecture that specific structure allows better-than-generic ZNE performance. None are proven. The taxonomy serves to organize future theoretical work and identify which experiments would be most informative.

We explicitly do not claim:
- That any structure defeats lower bounds
- That structured ZNE achieves polynomial cost in general
- That the taxonomy is complete
- That synthetic evidence generalizes to hardware
