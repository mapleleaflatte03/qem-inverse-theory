# Changelog

## v1.1-reviewer-rebalanced-manuscript

- Rebalanced manuscript around ambiguity diameter as the central contribution
- Added ambiguity diameter figure (Fig. 1) and bias-ambiguity tradeoff figure (Fig. 2)
- Added formal definitions of function class, tolerance, and admissible set in §2
- Expanded related work: distinguished bounded-ZNE estimators from identifiability analysis
- Added representative method-comparison table (Table 1) and sequential design table (Table 2)
- Compressed locality and structured taxonomy into limitations/future directions
- Softened 5 over-strong claims identified by reviewer audit
- Confirmed no unsafe wording remains (automated grep + claim safety test)
- Explicit paper scope: "framework paper with supporting synthetic experiments"
- Tests remain 80 passing; LaTeX builds cleanly (4 pages two-column)
- Known limitation: workshop-ready draft, not yet public-arXiv-ready (VERIFY citations, single response dominance)

## v1.0-paper-integration-draft

- Integrated v0.6–v0.9 research results into `paper/main.tex`
- Expanded manuscript to 11 sections (4 pages two-column ≈ 8 single-column)
- Added: Chebyshev-Tikhonov estimator, finite-shot phase diagram, Bayesian calibration, sequential design, locality negative result, escape-hatch taxonomy
- Added 10 claim-ledger entries for new manuscript content
- Added Claim Safety Checklist (9 pre-submission verification items)
- Softened "hardware validation" → "eventual hardware evaluation"
- LaTeX builds cleanly (pdflatex + bibtex)
- Tests remain 80 passing
- Known limitation: integration draft, not submission-ready peer-reviewed work

## v0.9-structured-lower-bound-taxonomy

- Added structured lower-bound / escape-hatch taxonomy
- Added `StructureDescriptor` dataclass and classification utilities
- Added `classify_structure()` and `explain_escape_hatch()`
- Added `docs/structured_lower_bound_taxonomy.md` (6 candidate structure classes)
- Added `paper/structured_escape_hatches.md` (paper-ready table)
- Six candidate escape-hatch classes: low support, low depth, symmetry, weak scrambling, bounded smooth response, Bayesian abstention
- Added tests ensuring no "defeat/overcome lower bounds" language in outputs
- Tests increased from 74 to 80
- Known limitation: taxonomy only, not a proven lower-bound theorem; all entries are research directions

## v0.8-locality-aware-prototype

- Added locality-aware ZNE prototype (`theory/locality.py`, `estimators/locality_aware.py`)
- Added Pauli support / Pauli weight utilities
- Added heuristic locality envelope proxy
- Added locality-aware Chebyshev regularization wrapper
- Added experiment 11: support-size proxy comparison
- Added top-level API exports: `fit_locality_aware_zne`, `estimate_observable_support`, `locality_envelope_proxy`
- Negative result documented: current support-size proxy over-regularizes (-1% to -11% vs baseline)
- Tests increased from 64 to 74
- Known limitations: heuristic only, no commutator-derived bound, no theorem, synthetic only

## v0.7-bayesian-sequential-prototype

- Added Bayesian GP hyperparameter optimization via marginal likelihood
- Added NLL diagnostics (nll_before, nll_after) for calibration tracking
- Added `design_next_scale()` greedy sequential design prototype
- Added sequential design experiment with two candidate regimes:
  - λ≥1 ZNE-relevant: 24.3% MSE improvement (synthetic exponential)
  - λ≥0.5 synthetic near-zero: 66.2% MSE improvement (clearly labeled non-standard ZNE)
- Updated deep research implementation audit (Bayesian → calibration partial, sequential → prototype)
- Tests increased from 57 to 64
- Known limitations: greedy one-step design, single response function, synthetic only, no global optimality

## v0.6-core-research-implementation

- Added Chebyshev-basis constrained ZNE with Tikhonov regularization
- Added bounded Bayesian GP ZNE with tanh output transform
- Added Estimator protocol and top-level public API exports
- Added systematic finite-shot phase diagram experiment (3 responses × 4 noise × 5 shots × 5 methods)
- Added Bayesian coverage calibration experiment (3 responses × 2 noise × 3 shots, 200 trials)
- Added help/harm proposition note (elementary MSE decomposition)
- Added estimator diagnostics:
  - Chebyshev: condition_number_proxy, z0_extrapolation
  - Bayesian: clipped_observation_count, latent_noise_variance_min/max
- Added aggregate help/harm summaries by method
- Added aggregate Bayesian coverage summaries by noise level
- Tests increased from 41 to 57
- Known limitation: Bayesian GP with fixed hyperparameters under-covers at high noise (calibration issue, not fundamental)

## v0.4-arxiv-package-ready

- Added arXiv source package builder (`scripts/build_arxiv_package.sh`)
- Added arXiv package integrity checker (`scripts/check_arxiv_package.py`)
- Package includes: main.tex, refs.bib, main.bbl, and 4 PDF figures
- Package excludes: aux/log/out/blg/png files
- Smoke check no longer dirties tracked figures
- arXiv source zip builds at `dist/qem-inverse-theory-arxiv-source.zip`

## v0.3-reviewer-readable-draft

- Polished abstract into problem/results/scope structure
- Converted contributions into numbered list
- Strengthened related-work positioning against physically bounded ZNE
- Clarified that this is identifiability/ambiguity analysis, not a new estimator
- Added conservative figure captions stating what each result does and does not prove
- Added anticipated reviewer concerns to paper/README.md
- Smoke check and LaTeX build pass

## v0.2-manuscript-draft

Expanded LaTeX manuscript to a readable 5-page draft.

### Manuscript
- Full Introduction with inverse-problem motivation and 5 stated contributions
- Related-work paragraph positioning against ZNE literature and QEM lower bounds
- Complete Section 2 with all formal definitions (observation model, function class, ambiguity set, condition number)
- Full proofs for Propositions 1 and 2 with interpretation caveats
- Expanded experiments section with 4 subsections and all numeric results
- Discussion section with 4 key insights
- Limitations section (8 items) with reproducibility note
- 6 verified citations + 1 arXiv preprint (Miranskyy2026, marked not peer-reviewed)

### Infrastructure
- Strengthened manuscript audit (`scripts/check_manuscript_length.py`)
- Claim safety checker allows negated forbidden phrases
- Smoke check includes manuscript metrics
- 41 tests passing

### Limitations (unchanged)
- Synthetic data only
- Polynomial function classes only
- No hardware validation
- No peer review
- No proof that constrained optimization improves MSE

## v0.1-research-scaffold

Initial research scaffold for studying ZNE as a constrained quantum inverse problem.

### Theoretical foundations
- Formal definitions: observation model, function class, ambiguity set, condition number, help/harm criterion
- Proposition 1 (proven): non-identifiability without function-class restrictions
- Proposition 2 (proven): spectral validity of expectation values
- Conjecture 1 (open): bounded estimator condition number ≤ unconstrained
- Research Direction 5 (open): structured escape hatches from QEM lower bounds

### Experiments and results
- Ambiguity diameter vs polynomial degree
- Ambiguity diameter vs tolerance δ (shot-noise proxy)
- Ambiguity diameter vs number of scale factors n (interpolation vs fixed-degree)
- Bias–ambiguity tradeoff for misspecified polynomial models

### Paper
- LaTeX skeleton (`paper/main.tex`): 7 sections, 2 propositions with proofs, 4 figures
- `refs.bib` with verified DOIs for key citations
- Prose draft (`paper/draft.md`)
- Claim ledger controlling allowed claim strength

### Infrastructure
- 41 tests passing
- 4 safety layers: asset, citation, claim, reproducibility
- `scripts/smoke_check.sh` for one-command verification
- Reproducible figures via `experiments/generate_figures.py`

### Limitations
- Synthetic data only — no quantum hardware involved
- Polynomial function classes only
- No hardware validation
- No peer review
- No proof that constrained optimization improves MSE
- Single exponential response function in most experiments
