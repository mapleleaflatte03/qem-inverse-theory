# Project Status: v0.9

## Executive Summary

`qem-inverse-theory` is a theory-first research repository studying zero-noise extrapolation as a constrained quantum inverse problem. As of v0.9, all five research directions from the original deep-research-report have code representation. The repo contains 80 passing tests, 11 experiments, a 5-page LaTeX manuscript skeleton, reproducible figures, and multiple safety layers (asset, citation, claim, reproducibility).

The project is at the stage of a **research lab prototype with honest negative results**, not a finished paper or production tool.

---

## Tag Timeline

| Tag | Focus | Tests |
|-----|-------|-------|
| v0.1 | Research scaffold | 34 |
| v0.2 | Manuscript draft | 41 |
| v0.3 | Reviewer-readable draft | 41 |
| v0.4 | arXiv package tooling | 41 |
| v0.6 | Core research implementation | 57 |
| v0.7 | Bayesian calibration + sequential design | 64 |
| v0.8 | Locality-aware prototype | 74 |
| v0.9 | Structured lower-bound taxonomy | 80 |

---

## Deep-Research-Report Coverage

| # | Direction | Report vision | Repo status | Key files |
|---|-----------|--------------|-------------|-----------|
| 1 | Constrained inverse-problem ZNE | Core line | **Implemented** | `estimators/constrained.py`, `estimators/chebyshev.py`, `theory/identifiability.py` |
| 2 | Risk bounds / phase diagrams | Theorem line | **Phase diagrams done; risk bound elementary** | `theory/phase_diagram.py`, `experiments/08_*` |
| 3 | Bayesian ZNE / UQ / sequential | Uncertainty line | **Implemented + calibration + design** | `estimators/bayesian.py`, `experiments/09_*`, `experiments/10_*` |
| 4 | Operator/locality-aware | Physics line | **Prototype (negative result)** | `theory/locality.py`, `estimators/locality_aware.py`, `experiments/11_*` |
| 5 | Lower bounds / escape hatches | Frontier line | **Structured taxonomy** | `theory/structured_escape_hatches.py`, `docs/structured_lower_bound_taxonomy.md` |

---

## What Is Implemented as Code

- Constrained polynomial ZNE (L-BFGS-B bounded optimization)
- Chebyshev-basis ZNE with Tikhonov regularization
- AICc / AIC / BIC / RSS model selection + model averaging
- Bounded Bayesian GP ZNE with tanh output transform
- Marginal likelihood hyperparameter optimization
- Sequential design via posterior variance minimization at λ=0
- Finite-shot help/harm phase diagram (3 responses × 4 noise × 5 shots × 5 methods)
- Ambiguity diameter computation via linear programming
- Spectral bounds, probability simplex projection
- Locality-aware regularization wrapper
- Structured escape-hatch classifier
- Public API: ZNEData, FitResult, Estimator protocol, 7 top-level functions

---

## What Is Prototype Only

- Locality-aware regularization (heuristic mapping, not calibrated)
- Sequential design (greedy one-step, not globally optimal)
- Escape-hatch taxonomy (classification heuristic, not theorem)
- Bayesian coverage (well-calibrated at low noise only)

---

## Negative Results and Limitations

| Finding | Implication |
|---------|-------------|
| Bayesian GP under-covers at high noise (70% empirical for 90% nominal) | Fixed hyperparameters insufficient; optimization helps but not fully validated |
| Locality-aware proxy over-regularizes (-1% to -11% vs baseline) | Simple support-size → reg_lambda mapping is too aggressive |
| Sequential design λ<1 gives 66% improvement but is not standard ZNE | Must restrict candidates to λ≥1 for ZNE-relevant claims (24% improvement) |
| Ambiguity diameter experiments use single exponential response | Generalization to other response classes not yet tested |
| All results are synthetic | No hardware validation whatsoever |

---

## What Is NOT Claimed

- No hardware validation or improvement
- No proof that constrained/bounded ZNE is universally superior
- No defeat or circumvention of QEM lower bounds
- No rigorous commutator-derived envelope bound
- No full circuit-family benchmark suite
- No peer-reviewed results
- No claim of optimality for any estimator or model selection criterion

---

## Remaining v1.0+ Research Debt

| Category | What's missing | Difficulty |
|----------|---------------|------------|
| Theory | Nonasymptotic risk bound / oracle inequality | Hard |
| Theory | Minimax rate for bounded smooth ZNE class | Hard |
| Theory | Condition number theorem (κ_B ≤ κ_U or counterexample) | Medium |
| Benchmarks | TFIM / Heisenberg / VQE / QAOA circuit families | Medium |
| Benchmarks | Non-Markovian / time-correlated noise models | Medium |
| Locality | Commutator-derived envelope (not heuristic) | Hard |
| Locality | Calibrated locality → regularization mapping | Medium |
| Bayesian | Full hyperparameter optimization with coverage guarantee | Medium |
| Sequential | Multi-step lookahead / globally optimal design | Hard |
| Lower bounds | Rigorous structured upper/lower bound pair | Very hard |

---

## Suggested Next Milestone Options

### Option A: v1.0 Benchmark Suite
Add TFIM/VQE/QAOA synthetic circuit-family benchmarks. Validate whether taxonomy predictions (low support helps, high scrambling hurts) hold across circuit families.

### Option B: v1.0 Theorem Hardening
Prove one additional theorem beyond Props 1-2: either the help/harm criterion formally, or a stability bound for Chebyshev-Tikhonov, or a counterexample for κ_B ≤ κ_U.

### Option C: v1.0 Paper Integration
Update the LaTeX manuscript to reflect v0.6–v0.9 results: Chebyshev estimator, Bayesian coverage, sequential design, phase diagram, locality negative result, escape-hatch taxonomy. This would make the paper a 8-10 page draft covering the full research program.

**Recommended:** Option C first (paper reflects current state), then Option A or B based on reviewer feedback direction.
