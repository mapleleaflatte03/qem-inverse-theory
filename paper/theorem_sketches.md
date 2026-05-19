# Theorem Sketches

These are informal statements at various stages of rigor. Status labels:
- **Proposition**: Formalizable and provable with standard techniques.
- **Conjecture**: Believed true but proof not yet available.
- **Research direction**: An open question, not a claim.

---

## Proposition 1: Non-Identifiability Without Physical Assumptions

**Status:** Proven. See [proofs.md](proofs.md).

**Statement:**
For any observations $\mathbf{y} = (y_1, \ldots, y_n)$ at scale factors $\boldsymbol{\lambda}$, and any target value $t \in \mathbb{R}$, there exists a polynomial $g$ of degree $n$ such that $g(\lambda_i) = y_i$ for all $i$ and $g(0) = t$.

**Consequence:** Without restricting the function class $\mathcal{F}$ or imposing physical constraints $\mathcal{C}$:
$$\mathcal{A}(\mathbf{y}, \mathcal{P}_n, \mathbb{R}, 0) = \mathbb{R}$$

The ambiguity set is all of $\mathbb{R}$. ZNE is completely undetermined.

**Proof sketch:** The system $g(\lambda_i) = y_i$, $g(0) = t$ gives $n+1$ constraints on a degree-$n$ polynomial with $n+1$ coefficients. The Vandermonde matrix on $\{0, \lambda_1, \ldots, \lambda_n\}$ is invertible (distinct points), so a unique solution exists for any $t$. $\square$

**Corollary:** Physical bounds $\mathcal{C} = [a, b]$ reduce the ambiguity set to:
$$\mathcal{A}(\mathbf{y}, \mathcal{P}_n, [a,b], 0) \subseteq [a, b]$$
which is a strict reduction from $\mathbb{R}$ but may still equal all of $[a,b]$.

---

## Proposition 2: Spectral Projection Validity

**Status:** Proven. See [proofs.md](proofs.md).

**Statement:**
Let $O$ be a Hermitian observable with eigenvalues $\mu_1, \ldots, \mu_m$. For any quantum state $\rho$:
$$\mu_{\min} \leq \mathrm{Tr}[\rho O] \leq \mu_{\max}$$

**Consequence:** Any estimator $\hat{f}(0) \notin [\mu_{\min}, \mu_{\max}]$ is provably incorrect. Projection onto $[\mu_{\min}, \mu_{\max}]$ cannot increase error when the true value satisfies the bounds:
$$|\mathrm{proj}_{[a,b]}(\hat{f}) - f(0)| \leq |\hat{f} - f(0)| \quad \text{for all } f(0) \in [a,b]$$

**Proof sketch:** $\mathrm{Tr}[\rho O] = \sum_j p_j \mu_j$ with $p_j \geq 0$, $\sum p_j = 1$ (Born rule in eigenbasis). Convex combination of $\{\mu_j\}$ lies in $[\mu_{\min}, \mu_{\max}]$. Projection onto a convex set containing the target is non-expansive. $\square$

---

## Conjecture 1: Stability of Bounded Estimator

**Status:** Conjecture (not yet proven; the proof sketch below has gaps).

**Statement (informal):**
Let $\hat{f}_B(0)$ be the bounded polynomial estimator (degree $d$, bounds $[a,b]$) and $\hat{f}_U(0)$ the unconstrained estimator. Then:
$$\kappa_B(\mathbf{y}) \leq \kappa_U$$

where $\kappa_B$ is the local sensitivity of the bounded estimator (see definitions.md §7) and $\kappa_U = \|\mathbf{w}\|_1$ is the unconstrained condition number.

**Why this is not yet proven:**
The bounded estimator is NOT the projection of the unconstrained estimate onto $[a,b]$. It solves a constrained least-squares problem with different KKT conditions. The non-expansiveness of projection applies to projecting a *point* onto a convex set, but the bounded estimator changes the entire fit (all coefficients), not just the intercept.

**What would be needed:**
- Sensitivity analysis of the KKT system for bounded least-squares
- Characterization of when the bound constraint is active vs inactive
- Possibly: the statement holds only when the constraint is active (the interesting case)

**Partial result (provable):**
If the bounded estimator is defined as $\hat{f}_B(0) = \mathrm{proj}_{[a,b]}(\hat{f}_U(0))$ (simple clipping), then $\kappa_B \leq \kappa_U$ trivially. But this is a weaker estimator than constrained optimization.

---

## Theorem 3: Finite-Shot Help/Harm Criterion

**Status:** To be corrected (the original formulation had dimensional issues).

**Corrected statement (see definitions.md §9):**

For a well-specified polynomial model (zero bias) with uniform shot allocation:

ZNE helps if and only if:
$$\kappa_U^2 \cdot \bar{\sigma}^2 < [f(\lambda_1) - f(0)]^2 + \sigma_1^2$$

The critical total shot count below which ZNE harms is:
$$N^* = \frac{n \cdot \kappa_U^2 \cdot v}{[f(\lambda_1) - f(0)]^2}$$

where $v$ is the single-shot variance and $n$ is the number of scale factors.

**Issues remaining:**
- The well-specified assumption ($\mathrm{Bias}_{\mathrm{ZNE}} = 0$) is unrealistic. Real response functions are not exactly polynomial.
- For misspecified models, the bias term depends on the unknown $f$, making the criterion non-computable from data alone.
- A practical version would need an estimable upper bound on bias.

---

## Research Direction 5: Structured Escape Hatches

**Status:** Research direction (open question, not a claim).

**Question:**
Do there exist natural circuit/observable structures under which ZNE achieves polynomial sample cost, despite generic QEM lower bounds (Takagi et al. 2022, Quek et al. 2024) showing exponential cost for worst-case instances?

**Candidate structures:**
- Local observables with support on $k \ll n$ qubits
- Circuits with bounded depth $D$ and local noise
- Observables commuting with a symmetry of the noise channel
- Systems with spectral gap in the noise channel's transfer matrix

**What is NOT claimed:**
- We do not claim to have identified such a structure.
- We do not claim polynomial cost is achievable.
- We do not claim the lower bounds have loopholes.

**What we aim to do:**
- Identify the assumptions in existing lower bound proofs.
- Construct candidate structured instances.
- Test numerically whether these instances exhibit better-than-generic scaling.
- If promising, attempt rigorous proof for specific cases.

---

## Proposition 3: Help/Harm Decision Criterion (Elementary)

**Status:** Proven (stylized bias-variance model). See `paper/main.tex` Proposition 3.

**Statement:**
Under a bias-variance decomposition MSE = B² + V/N, ZNE improves over raw iff ΔB² > ΔV/N, where ΔB² = B_raw² - B_ZNE² and ΔV = V_ZNE - V_raw. Critical shot count: N* = ΔV/ΔB².

**Proof:** Direct subtraction of MSE expressions.

**Assumptions:**
- Bias and variance are separable and known
- Shot noise scales as V/N (uniform allocation)
- No model-selection randomness accounted for

**Limitations:**
- In practice, B and V are unknown and must be estimated
- Does not account for model misspecification uncertainty
- N* depends on the unknown true response
- Does not prove ZNE always helps above any universal threshold

**Empirical validation:** Experiment 08 phase diagram is consistent with this criterion (low-shot harm, high-shot help).

---

## Proposition 4: Two-Point Indistinguishability Lower Bound

**Status:** Proven (standard Le Cam argument applied to ZNE setting).

**Statement:**
Let f+, f- be two admissible response functions with |f+(0) - f-(0)| = Δf(0) and |f+(λ_i) - f-(λ_i)| ≤ Δ_obs for all observed i. Under Gaussian noise with variance σ²/N per point across n observed scales, any estimator satisfies:

    MSE ≥ (Δf(0)/2)² × (1 - TV)

where TV ≤ √(n × Δ_obs² × N / (4σ²)) via Pinsker's inequality.

**Proof:** Standard Le Cam two-point method. The testing error between the two hypotheses is lower bounded by (1 - TV)/2. Any estimator that achieves small MSE must implicitly solve the testing problem, giving the stated bound.

**Connection to ambiguity diameter:**
This formalizes the intuition that large ambiguity diameter implies fundamental estimation difficulty. If many admissible responses agree at observed scales but disagree at zero noise, no estimator can reliably recover f(0).

**Assumptions:**
- Gaussian observation model (approximation of shot noise)
- Two specific admissible responses (not minimax over full class)
- Known noise variance

**Limitations:**
- Two-point bound, not minimax over a function class
- Does not prove a universal QEM lower bound
- Does not apply to all possible noise channels
- Tighter bounds would require Le Cam or Fano over larger hypothesis sets
