# Theorem Sketches

These are informal statements to be made rigorous. Not yet proven.

---

## Theorem 1: Stability of Bounded Estimator

**Statement (sketch):**
Let f̂_B(0) be the bounded polynomial estimator of degree d with bounds [a, b].
If the true response f ∈ P_d (polynomials of degree ≤ d) and f(0) ∈ [a, b], then:

    |f̂_B(0) - f(0)| ≤ κ_B · max_i |ε_i|

where κ_B ≤ κ_U (the unconstrained condition number), with strict inequality when the unconstrained estimate violates bounds.

**Proof idea:** The feasible set is a convex polytope. Projection onto a convex set is non-expansive. The bounded estimator is the projection of the unconstrained estimator onto [a, b] intersected with the least-squares manifold.

---

## Theorem 2: Non-Identifiability Without Physical Assumptions

**Statement (sketch):**
For any set of observations {(λ_i, y_i)}_{i=1}^n and any target value t ∈ ℝ, there exists a smooth function g with g(λ_i) = y_i for all i and g(0) = t.

**Proof idea:** Polynomial interpolation with n+1 free parameters (degree n) can match n data points and any prescribed value at 0. Without restricting the function class or imposing bounds, f(0) is completely undetermined.

**Corollary:** Physical bounds [a, b] reduce the ambiguity set to at most [a, b] ∩ {achievable values}, which may be a strict subset.

---

## Theorem 3: Finite-Shot Help/Harm Criterion

**Statement (sketch):**
Let MSE_raw = σ²/N (raw measurement MSE) and MSE_ZNE = κ² · σ²/N + bias²(d, f).
ZNE helps (MSE_ZNE < MSE_raw) if and only if:

    κ² < N · (1 - bias²(d, f) · N / σ²)

For fixed bias, there exists a critical shot count N* below which ZNE always harms.

**Proof idea:** Direct comparison of MSE expressions. The condition number κ amplifies variance while extrapolation reduces bias. The tradeoff depends on N.

---

## Theorem 4: Spectral Projection Validity

**Statement (sketch):**
Let O be a Hermitian observable with eigenvalues in [λ_min, λ_max]. For any quantum state ρ:

    λ_min ≤ Tr[ρO] ≤ λ_max

Therefore, any estimator returning values outside [λ_min, λ_max] is provably wrong, and projection onto these bounds cannot increase error when the true value satisfies the bounds.

**Proof idea:** Tr[ρO] = Σ_i p_i λ_i where p_i ≥ 0, Σ p_i = 1. This is a convex combination of eigenvalues, hence bounded by extremes.

---

## Conjecture 5: Structured Escape Hatch

**Statement (conjecture):**
For circuits with depth D on n qubits with local noise of strength ε, if the observable O has support on k ≪ n qubits, then ZNE achieves MSE ≤ poly(k, D) · ε² / N with polynomial shot cost, evading the exponential lower bounds that apply to global observables.

**Intuition:** Local observables are insensitive to noise on distant qubits. The effective dimension of the inverse problem scales with the observable's support, not the full system size.

**Status:** Unproven. Requires careful analysis of noise propagation through circuit structure.
