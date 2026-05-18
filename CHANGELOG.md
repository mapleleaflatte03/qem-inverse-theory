# Changelog

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
