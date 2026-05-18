# Research Notes

## 2026-05-18: Project initialization

Starting point: the observation that ZNE is treated as regression but is actually an inverse problem.

Key insight from quantum-noise-optimizer work:
- Bounded ZNE achieves 0% unphysical rate but doesn't always win on MAE
- The advantage is reliability, not universal accuracy
- This suggests the real question is: when is extrapolation reliable?

## Connections to inverse problem theory

- Hadamard well-posedness: existence, uniqueness, continuous dependence
- ZNE fails uniqueness (many curves through data) and stability (small noise → large error)
- Physical constraints restore partial well-posedness

## Key references to study

- Tikhonov regularization as analogy for constrained ZNE
- Bayesian inverse problems (Stuart 2010) for uncertainty quantification
- Compressed sensing: structured sparsity as escape from underdetermination

## Open questions for next session

1. Can we prove that bounded polynomial ZNE has strictly smaller condition number?
2. What is the minimax rate for ZNE under spectral constraints?
3. Is there a natural prior for Bayesian ZNE that gives calibrated intervals?
