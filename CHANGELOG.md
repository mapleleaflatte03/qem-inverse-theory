# Changelog

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
