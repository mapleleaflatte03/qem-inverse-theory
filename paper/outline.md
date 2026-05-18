# Zero-Noise Extrapolation as a Constrained Quantum Inverse Problem

## Paper Outline

### 1. Introduction
- ZNE is the most deployed QEM technique
- Current practice: ad hoc curve fitting with no formal guarantees
- Our framing: ZNE as constrained inverse inference
- Key question: when is f(0) identifiable from finite noisy observations?

### 2. ZNE as Inverse Inference
- Forward model: noise channel maps ρ → ρ(λ)
- Observation model: y_i = Tr[ρ(λ_i) O] + ε_i
- Inverse problem: recover Tr[ρ_ideal O] from {y_i}
- Ill-posedness: existence, uniqueness, stability (Hadamard)

### 3. Physical Admissibility Constraints
- Spectral bounds from observable eigenvalues
- Probability simplex for state tomography
- Monotonicity from channel contractivity
- Smoothness from analyticity of quantum channels
- How constraints reduce the ambiguity set

### 4. Identifiability and Instability
- Definition: f(0) is identifiable if ambiguity diameter → 0
- Condition number of extrapolation map
- Adversarial examples: same data, different f(0)
- Role of function class in determining identifiability
- Theorem: identifiability under bounded polynomial class

### 5. Constrained Estimators
- Unconstrained polynomial (baseline)
- Bounded optimization (L-BFGS-B with physical constraints)
- Spectral-constrained estimator
- Comparison: clipping vs constrained optimization

### 6. Finite-Shot Help–Harm Phase Diagrams
- When does ZNE reduce MSE vs amplify it?
- Phase boundary as function of (shots, noise, model complexity)
- Bias-variance decomposition under constraints
- Practical criterion: "should I mitigate?"

### 7. Bayesian Uncertainty-Aware ZNE
- GP prior over response functions
- Posterior at λ=0 with physical bounds
- Credible intervals and calibration
- Decision-theoretic framing: mitigate only when confident

### 8. Structured Escape Hatches from Generic Lower Bounds
- Review of QEM lower bounds (Takagi, Quek, Tsubouchi)
- Why generic bounds don't apply to all circuits
- Structured assumptions: locality, symmetry, spectral gap
- Conjecture: polynomial-cost mitigation under structure

### 9. Discussion and Limitations
- What we proved vs what remains conjectural
- Assumptions that may not hold in practice
- Comparison with existing ZNE theory
- Open problems
