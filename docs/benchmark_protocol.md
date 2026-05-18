# Benchmark Protocol

## Synthetic benchmarks

All initial experiments use synthetic response functions with known ground truth f(0).

### Response classes
1. **Exponential decay**: f(λ) = f(0) · exp(-αλ)
2. **Polynomial bias**: f(λ) = f(0) + c₁λ + c₂λ² + ...
3. **Mixed**: f(λ) = a·exp(-αλ) + (1-a)·(f(0) + c₁λ)
4. **Adversarial**: Two functions agreeing at observed λ_i but differing at λ=0

### Noise model
- Shot noise: ε_i ~ N(0, (1 - f(λ_i)²) / N_shots)
- Scale factors: λ ∈ {1, 2, 3, 4, 5} (default) or {1, 1.5, 2, 2.5, 3}

### Metrics
- Absolute error |f̂(0) - f(0)|
- MSE over repeated trials
- Bias² + Variance decomposition
- Physical validity rate (fraction inside bounds)
- Interval coverage (for Bayesian methods)
- Help/harm ratio: MSE_raw / MSE_method

### Phase diagram axes
- x: log₁₀(total shots)
- y: noise strength (or scale factor range)
- color: log₁₀(MSE_raw / MSE_method) — positive = help, negative = harm
