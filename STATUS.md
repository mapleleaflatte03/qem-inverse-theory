# Status

**Current phase:** Early research prototype.

## Working

- Synthetic ZNE response generators (exponential, polynomial, mixed, adversarial)
- Spectral bounds and probability simplex projection
- Constrained polynomial ZNE estimators (L-BFGS-B bounded optimization)
- AICc / AIC / BIC / RSS model selection
- Finite-shot phase-diagram utilities (help/harm classification)
- Basic metrics (MSE, bias-variance decomposition, coverage)

## Experimental

- Bayesian ZNE via Gaussian process (minimal prototype)
- Adversarial identifiability examples
- Structured escape-hatch analysis (placeholder)

## Not implemented

- Hardware integration
- Full quantum circuit simulation
- Rigorous theorem proofs (sketches only)
- Peer-reviewed claims
- Regularized estimators (Tikhonov, LASSO)

## Assumption ledger

All current results assume:
- Bounded observables with known spectral bounds
- Known, exact noise scale factors
- Independent Gaussian shot noise (Pauli variance approximation)
- Exact noiseless reference available in synthetic benchmarks
- No systematic calibration error in scale factors

These assumptions will be relaxed in future work.

## Tests

26+ unit tests covering constraints, estimators, model selection, phase diagrams, and Bayesian prototype.
