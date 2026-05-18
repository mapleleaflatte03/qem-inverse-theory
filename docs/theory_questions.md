# Open Theory Questions

## Q1: Identifiability
Given n noisy observations {(λ_i, y_i)} and physical bounds [a, b], under what conditions on the function class F is f(0) uniquely determined?

Conjecture: For polynomial F of degree d < n with bounds, identifiability holds generically. For d ≥ n-1, it fails.

## Q2: Stability constant
What is the condition number κ of the extrapolation map T: (y_1,...,y_n) → f(0) as a function of the scale factors and model class?

Known: For polynomial extrapolation, κ grows exponentially with degree. Do physical bounds reduce κ?

## Q3: Help–harm threshold
For a given circuit with noise strength ε and shot budget N, what is the critical N*(ε) below which ZNE increases MSE?

## Q4: Bayesian calibration
Under what prior does the posterior credible interval achieve nominal coverage for f(0)?

## Q5: Escape hatches
Generic QEM lower bounds (Takagi et al., Quek et al.) show exponential sample cost. What structured assumptions (locality, symmetry, spectral gap) allow polynomial-cost mitigation?

## Q6: Model selection consistency
Is AICc consistent for ZNE model selection as n → ∞? What happens at fixed small n (the realistic regime)?

## Q7: Adversarial non-identifiability
Can we construct two physically valid response functions that agree at all observed noise levels but differ maximally at zero noise? What is the diameter of the ambiguity set?
