# Zero-Noise Extrapolation as a Constrained Quantum Inverse Problem

**Draft — work in progress**

---

## Abstract

Zero-noise extrapolation (ZNE) is one of the most widely used quantum error mitigation techniques, yet its theoretical foundations as an inference problem remain underdeveloped. We formalize ZNE as a constrained inverse problem: recovering an unobserved noiseless expectation value from finite, noisy measurements at amplified noise levels. We show that without function-class restrictions, the zero-noise limit is not identifiable from any finite set of observations (Proposition 1). We establish that spectral bounds from the observable's eigenvalues provide physically valid constraints, and that post-hoc projection of a scalar estimate onto these bounds cannot increase error when the true value lies within the spectral interval (Proposition 2). We introduce the *ambiguity diameter* — the range of zero-noise values consistent with data, function class, and physical constraints — as a quantitative measure of identifiability. Synthetic experiments illustrate that physical bounds reduce ambiguity diameter by up to 6× in a degree-4 polynomial ambiguity experiment at tolerance δ = 0.1, with the reduction becoming more pronounced as measurement tolerance increases. All numerical results in this draft are synthetic and intended to illustrate the identifiability framework. These results do not prove that constrained estimators are universally superior; rather, they formalize the conditions under which extrapolation is well-posed and quantify the role of physical constraints in restoring identifiability.

---

## 1. Introduction

Zero-noise extrapolation mitigates errors on noisy quantum processors by measuring expectation values at multiple amplified noise levels and extrapolating to the zero-noise limit. Since its introduction [Li & Benjamin 2017, Temme et al. 2017], ZNE has become a common error mitigation strategy due to its simplicity: no knowledge of the noise model is required, only the ability to amplify noise controllably.

Despite widespread use, ZNE is typically treated as a curve-fitting exercise: choose a model (linear, polynomial, exponential), fit it to noisy data, and evaluate at zero noise. This framing obscures a fundamental question:

> Under what conditions is the zero-noise limit uniquely determined from finite noisy observations?

We argue that ZNE is more naturally understood as a **constrained inverse problem** in the sense of Hadamard: the noiseless expectation value is never directly observed, and must be inferred from indirect measurements subject to physical constraints. This framing reveals that:

1. Without restricting the function class, ZNE is ill-posed — infinitely many smooth functions pass through the data but disagree at zero noise.
2. Physical constraints (spectral bounds from the observable) provide valid restrictions that reduce the set of admissible solutions.
3. The degree of identifiability depends on the interaction between function class, physical constraints, and measurement uncertainty.

In this paper, we formalize these observations, prove foundational propositions, and introduce the ambiguity diameter as a quantitative tool for studying identifiability. We do not propose a new extrapolation method; we study when extrapolation is physically identifiable.

---

## 2. ZNE as a Constrained Inverse Problem

### 2.1 Observation model

Let $O$ be a Hermitian observable on a quantum system and $\mathcal{E}_\lambda$ a noise channel parameterized by scale factor $\lambda \geq 0$, where $\lambda = 0$ is the noiseless channel. The noiseless expectation is $f(0) = \mathrm{Tr}[\rho_{\mathrm{ideal}} \, O]$, and the noisy expectation at scale $\lambda$ is $f(\lambda) = \mathrm{Tr}[\mathcal{E}_\lambda(\rho_{\mathrm{ideal}}) \, O]$.

We observe:
$$y_i = f(\lambda_i) + \varepsilon_i, \quad i = 1, \ldots, n$$

where $\lambda_1 < \cdots < \lambda_n$ are fixed, known design points (chosen by the experimenter via unitary folding or pulse stretching) and $\varepsilon_i$ is shot noise with variance $\sigma_i^2$.

### 2.2 The inverse problem

ZNE seeks to recover $f(0)$ from $\{(\lambda_i, y_i)\}_{i=1}^n$. This is an extrapolation beyond the observed domain: the target $\lambda = 0$ is never measured directly.

The problem is constrained by:
- **Function class** $\mathcal{F}$: the set of admissible response functions (e.g., polynomials of degree $\leq d$).
- **Physical constraints** $\mathcal{C}$: the set of physically valid values for $f(0)$ (e.g., spectral bounds $[\mu_{\min}, \mu_{\max}]$).
- **Data consistency**: $f$ must be approximately consistent with observations (within tolerance $\delta$ reflecting shot noise).

### 2.3 Well-posedness in the sense of Hadamard

An inverse problem is well-posed if its solution (i) exists, (ii) is unique, and (iii) depends continuously on the data. ZNE generically fails conditions (ii) and (iii):

- **Non-uniqueness**: Multiple functions in $\mathcal{F}$ may pass through the data but give different $f(0)$ (see §3).
- **Instability**: Small perturbations in $\{y_i\}$ can cause large changes in the extrapolated $f(0)$, quantified by the condition number $\kappa$.

Physical constraints and function-class restrictions are the tools available to restore (partial) well-posedness.

---

## 3. Non-Identifiability Without Assumptions

We formalize the observation that ZNE is undetermined without structural assumptions.

### 3.1 The ambiguity set

**Definition.** Given observations $\mathbf{y}$, function class $\mathcal{F}$, physical constraints $\mathcal{C}$, and tolerance $\delta \geq 0$:
$$\mathcal{A}(\mathbf{y}, \mathcal{F}, \mathcal{C}, \delta) = \left\{ f(0) \;\middle|\; f \in \mathcal{F}, \; f(0) \in \mathcal{C}, \; \|f(\boldsymbol{\lambda}) - \mathbf{y}\|_\infty \leq \delta \right\}$$

The **ambiguity diameter** is $\mathrm{diam}(\mathcal{A}) = \sup \mathcal{A} - \inf \mathcal{A}$.

### 3.2 Proposition 1: Non-identifiability

**Proposition 1.** Let $\lambda_1, \ldots, \lambda_n > 0$ be distinct. For any observations $y_1, \ldots, y_n \in \mathbb{R}$ and any target $t \in \mathbb{R}$, there exists a polynomial $p$ of degree at most $n$ such that $p(\lambda_i) = y_i$ for all $i$ and $p(0) = t$.

*Proof.* The $n+1$ points $\{0, \lambda_1, \ldots, \lambda_n\}$ are distinct. By Lagrange interpolation, there exists a unique polynomial of degree $\leq n$ taking prescribed values at $n+1$ distinct points. $\square$

**Consequence.** For $\mathcal{F} = \mathcal{P}_n$ and $\mathcal{C} = \mathbb{R}$: $\mathcal{A}(\mathbf{y}, \mathcal{P}_n, \mathbb{R}, 0) = \mathbb{R}$. The zero-noise limit is completely undetermined.

### 3.3 How restrictions restore identifiability

Two mechanisms reduce the ambiguity set:

1. **Function-class restriction** ($\mathcal{F} = \mathcal{P}_d$ with $d < n$): The interpolation system becomes overdetermined, and generically only a bounded range of $f(0)$ values are achievable.

2. **Physical constraints** ($\mathcal{C} = [a, b]$): The ambiguity set is intersected with $[a, b]$, which provides a finite upper bound on the diameter regardless of $\mathcal{F}$.

These mechanisms are complementary: function-class restriction helps when the model is well-specified; physical constraints help unconditionally.

---

## 4. Physical Admissibility via Spectral Constraints

### 4.1 Proposition 2: Spectral validity

**Proposition 2.** Let $O$ be Hermitian with eigenvalues $\mu_1, \ldots, \mu_m$. For any density operator $\rho$:
$$\mu_{\min} \leq \mathrm{Tr}[\rho O] \leq \mu_{\max}$$

*Proof.* In the eigenbasis of $O$: $\mathrm{Tr}[\rho O] = \sum_j \mu_j \langle e_j | \rho | e_j \rangle = \sum_j \mu_j p_j$ where $p_j \geq 0$ and $\sum_j p_j = 1$. A convex combination of real numbers lies within their range. $\square$

### 4.2 Corollary: Post-hoc projection cannot increase error

For any scalar estimate $\hat{f}$ and true value $f(0) \in [\mu_{\min}, \mu_{\max}]$:
$$|\mathrm{proj}_{[\mu_{\min}, \mu_{\max}]}(\hat{f}) - f(0)| \leq |\hat{f} - f(0)|$$

This follows from non-expansiveness of projection onto a convex set containing the target. Note: this applies to clipping a scalar estimate after computation. It does not imply that constrained *optimization* (which changes all model parameters) always reduces MSE.

### 4.3 Implications for ZNE

- Any ZNE estimate outside $[\mu_{\min}, \mu_{\max}]$ is provably wrong.
- Enforcing spectral bounds via post-hoc projection is a free improvement: it cannot increase pointwise error when the true value lies within bounds.
- For Pauli observables ($\mathcal{C} = [-1, 1]$) and probability estimation ($\mathcal{C} = [0, 1]$), the bounds are known a priori without additional measurement.

### 4.4 What spectral bounds do NOT guarantee

Spectral bounds guarantee physical validity but not accuracy:
- An estimate of $f(0) = 0.5$ when the true value is $f(0) = 0.9$ is physically valid but inaccurate.
- Bounds reduce the ambiguity set but do not eliminate estimation error.
- Whether constrained *optimization* (as opposed to post-hoc projection) further reduces MSE is an open question (see Conjecture 1 in theorem sketches).

---

## 5. Ambiguity Diameter: Quantitative Results

We compute the ambiguity diameter numerically using linear programming to find the extremal values of $f(0)$ over the feasible set of polynomials.

### 5.1 Setup

- Response: $f(\lambda) = 0.8 \cdot e^{-0.25\lambda}$ (exponential decay, true $f(0) = 0.8$)
- Scales: $\lambda \in \{1, 2, 3, 4, 5\}$ ($n = 5$)
- Tolerance: $\delta = 0.01$ (approximate interpolation)
- Constraint sets: no bounds $[-10, 10]$, Pauli $[-1, 1]$, probability $[0, 1]$

### 5.2 Ambiguity vs polynomial degree

| Degree | No bounds | Pauli [-1, 1] | Probability [0, 1] |
|--------|-----------|---------------|---------------------|
| 1      | infeasible | infeasible   | infeasible          |
| 2      | 0.070     | 0.070         | 0.070               |
| 3      | 0.180     | 0.180         | 0.180               |
| 4      | 0.620     | 0.510         | 0.510               |

At degree 1, no linear function passes within $\delta = 0.01$ of the exponential data — the model is misspecified. At degrees 2–3, the overdetermined system constrains $f(0)$ regardless of bounds. At degree 4 (interpolation regime), bounds reduce ambiguity from 0.62 to 0.51 (18% reduction).

### 5.3 Ambiguity vs tolerance (degree 4)

| δ       | No bounds | Pauli [-1, 1] | Probability [0, 1] |
|---------|-----------|---------------|---------------------|
| 0.0     | 0.000     | 0.000         | 0.000               |
| 0.001   | 0.062     | 0.062         | 0.062               |
| 0.01    | 0.620     | 0.510         | 0.510               |
| 0.05    | 3.100     | 1.750         | 1.000               |
| 0.1     | 6.200     | 2.000         | 1.000               |

At $\delta = 0$ (exact data), the degree-4 polynomial is uniquely determined by 5 points, giving zero ambiguity. As $\delta$ increases (simulating shot noise), ambiguity grows linearly without bounds but is capped by physical constraints. At $\delta = 0.1$, probability bounds reduce ambiguity from 6.2 to 1.0 — a 6.2× reduction in this specific synthetic experiment (degree-4 polynomial, exponential response, $n=5$).

### 5.4 Key observations

1. **Physical bounds matter most in the high-uncertainty regime.** When data is precise ($\delta$ small), the function class alone constrains $f(0)$. When data is noisy ($\delta$ large), bounds become the dominant constraint.

2. **Tighter bounds help more.** Probability bounds $[0, 1]$ cap ambiguity at 1.0 regardless of $\delta$, while Pauli bounds $[-1, 1]$ cap at 2.0. The tighter the physical constraint, the stronger the identifiability guarantee.

3. **Model complexity trades off against identifiability.** Higher-degree polynomials fit more data patterns but increase ambiguity. This is the bias-variance tradeoff viewed through the lens of identifiability.

---

## Limitations

- **Synthetic data only.** All results use analytically defined response functions. No quantum hardware or circuit simulation is involved.
- **Polynomial function classes only.** Exponential and mixed models are not yet analyzed in the ambiguity framework.
- **Tolerance chosen manually.** The connection between $\delta$ and actual shot-noise variance is noted but not rigorously derived.
- **No hardware claims.** We make no claims about performance on real quantum processors.
- **No proof that constrained estimators reduce MSE.** Propositions 1–2 establish identifiability and validity, not accuracy. Whether constrained optimization improves MSE over unconstrained estimation remains an open question.
- **Single response function.** The ambiguity diameter results are for one specific exponential response. Generalization to other response classes is future work.
