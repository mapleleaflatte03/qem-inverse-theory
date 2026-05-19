# Deep Research Report Implementation Audit

Mapping the original `deep-research-report.md` vision to actual repository state.

---

## Component Status Table

| # | Component (from report) | Status | Evidence files | Gap | Priority |
|---|---|---|---|---|---|
| A | Constrained inverse-problem ZNE | **Implemented** | `estimators/constrained.py`, `theory/inverse_problem.py`, `theory/identifiability.py`, `paper/main.tex §2-3` | Chebyshev basis, Padé, monotone constraints missing | Low (core done) |
| B | Spectral/operator regularization | **Partially implemented** | `constraints/spectral.py`, `constraints/probability_simplex.py`, `constraints/physical_bounds.py` | Operator-aware derivative penalties, commutator envelopes, Sobolev penalties missing | Medium |
| C | Finite-shot help–harm phase diagrams | **Partially implemented** | `theory/phase_diagram.py`, `experiments/03_finite_shot_phase_diagram.py`, `benchmarks/metrics.py` | Only toy grid; no systematic benchmark across circuit families; no theoretical phase boundary derivation | High |
| D | Nonasymptotic risk bounds | **Documentation only** | `theory/risk_bounds.py` (condition number + variance amplification), `paper/theorem_sketches.md` (Theorem 3) | No proven risk bound; no oracle inequality; no minimax result | High |
| E | Bayesian nonparametric ZNE with credible intervals | **Prototype only** | `estimators/bayesian.py` (basic GP), `experiments/04_bayesian_credible_intervals.py` | No bounded transform (tanh), no calibration study, no coverage plots, no hyperparameter optimization | High |
| F | Sequential design (choose next scale) | **Missing** | — | Not implemented at all | Medium |
| G | Operator/locality-aware extrapolation | **Missing** | `theory/lower_bounds_notes.py` (text only) | No commutator envelopes, no locality-aware priors, no support-size experiments | Low (v0.7+) |
| H | Lower bounds / structured escape hatches | **Documentation only** | `theory/lower_bounds_notes.py`, `paper/theorem_sketches.md` (Research Direction 5) | No minimax lower bounds, no structured upper bounds, no taxonomy | Low (v0.7+) |
| I | Benchmark harness (noise models, circuit families) | **Partially implemented** | `benchmarks/synthetic_response.py`, `benchmarks/noise_models.py`, `benchmarks/shot_noise.py`, `benchmarks/metrics.py` | Only 1 exponential response tested; no TFIM/Heisenberg/VQE/QAOA circuits; no time-correlated noise; no grid benchmark | Medium |
| J | Public API: ZNEData, FitResult, Estimator protocol | **Partially implemented** | `types.py` (ZNEData, FitResult) | No `Estimator` protocol; no `fit_constrained_zne` top-level; no `design_next_scale`; no `estimate_commutator_envelope` | Medium |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Implemented | 1 |
| Partially implemented | 5 |
| Prototype only | 1 |
| Documentation only | 2 |
| Missing | 2 |

**Overall coverage: ~60% of the report's vision has some representation in code; ~30% is substantively implemented.**

---

## Top 5 Missing Pieces (by impact)

1. **Finite-shot phase diagram with theoretical boundary** — The report emphasizes this as the key figure. Current experiment 03 is a toy. Need: systematic grid, multiple response functions, theoretical N* overlay.

2. **Bayesian ZNE with calibrated credible intervals** — Current prototype uses raw GP without bounded transform. Need: tanh/logistic transform for physical bounds, coverage calibration study, hyperparameter selection.

3. **Nonasymptotic risk bound (even one)** — The report calls for MSE ≤ bias² + selection_penalty + shot_variance with explicit terms. Currently only sketched in theorem_sketches.md.

4. **Multiple response functions in benchmarks** — All ambiguity experiments use a single exponential. Need: polynomial, mixed, adversarial, and at least one "realistic" (e.g., depolarizing channel on TFIM).

5. **Chebyshev/regularized constrained estimator** — Report specifically calls for Chebyshev basis + Tikhonov penalty. Current constrained estimator uses raw polynomial + L-BFGS-B bounds only.

---

## Recommended v0.6 Scope

Focus: **Return to core research implementation.** No packaging, no arXiv, no release.

| Task | Deliverable | Effort |
|------|-------------|--------|
| Implement bounded Bayesian ZNE with tanh transform | `estimators/bayesian.py` rewrite + coverage test | 1 day |
| Implement Chebyshev-basis constrained estimator | `estimators/constrained.py` addition | 0.5 day |
| Systematic finite-shot phase diagram experiment | `experiments/08_systematic_phase_diagram.py` | 1 day |
| Multiple response functions in ambiguity experiments | Extend experiment 05/06/07 | 0.5 day |
| Formalize help/harm criterion as proposition | `paper/proofs.md` addition | 0.5 day |
| Coverage calibration experiment for Bayesian ZNE | `experiments/09_bayesian_coverage.py` | 0.5 day |
| Add Estimator protocol + top-level API | `types.py` + `__init__.py` | 0.5 day |

**Explicitly deferred to v0.7+:**
- Operator/locality-aware extrapolation
- Lower bounds / escape-hatch taxonomy
- Sequential design
- Circuit-family benchmarks (TFIM, VQE, QAOA)
- Non-Markovian noise models
