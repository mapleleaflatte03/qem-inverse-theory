# Formal Definitions

All notation used in theorem statements and proofs.

---

## 1. ZNE Observation Model

Let $O$ be a Hermitian observable on a quantum system, and let $\mathcal{E}_\lambda$ denote a noise channel parameterized by scale factor $\lambda \geq 0$, where $\lambda = 0$ corresponds to the noiseless (ideal) channel.

The **noiseless expectation** is:
$$f(0) = \mathrm{Tr}[\rho_{\mathrm{ideal}} \, O]$$

The **noisy expectation** at scale $\lambda$ is:
$$f(\lambda) = \mathrm{Tr}[\mathcal{E}_\lambda(\rho_{\mathrm{ideal}}) \, O]$$

The **observation model** is:
$$y_i = f(\lambda_i) + \varepsilon_i, \quad i = 1, \ldots, n$$

where $\varepsilon_i$ is measurement noise (shot noise).

---

## 2. Scale Factors as Fixed Design Points

The scale factors $\boldsymbol{\lambda} = (\lambda_1, \lambda_2, \ldots, \lambda_n)$ are **fixed, known, exact design points** satisfying:
$$0 < \lambda_1 < \lambda_2 < \cdots < \lambda_n$$

They are not random variables. They are chosen by the experimenter (e.g., via unitary folding or pulse stretching). The target $\lambda = 0$ is **not observed**; it is the extrapolation target.

**Consequence:** The inverse problem is a fixed-design regression with extrapolation beyond the observed domain.

---

## 3. Function Class $\mathcal{F}$

A **function class** $\mathcal{F}$ is a set of candidate response functions $f: [0, \lambda_n] \to \mathbb{R}$.

Examples used in this work:

| Notation | Definition |
|----------|-----------|
| $\mathcal{P}_d$ | Polynomials of degree $\leq d$ |
| $\mathcal{E}_1$ | Single exponentials: $f(\lambda) = a \cdot e^{-\alpha \lambda} + c$ |
| $\mathcal{E}_2$ | Bi-exponentials: $f(\lambda) = a_1 e^{-\alpha_1 \lambda} + a_2 e^{-\alpha_2 \lambda}$ |
| $\mathcal{F}_{\mathrm{mon}}$ | Monotone non-increasing functions on $[0, \lambda_n]$ |
| $\mathcal{F}_{\mathrm{Lip}(L)}$ | $L$-Lipschitz functions: $|f(x) - f(y)| \leq L|x-y|$ |

The choice of $\mathcal{F}$ is an **assumption**, not a consequence of the data. Different choices lead to different identifiability guarantees.

---

## 4. Physical Constraint Set $\mathcal{C}$

The **physical constraint set** $\mathcal{C} \subseteq \mathbb{R}$ is the set of physically admissible values for $f(0)$.

**Definition:** For observable $O$ with eigenvalues $\{\mu_1, \ldots, \mu_m\}$:
$$\mathcal{C} = [\mu_{\min}, \mu_{\max}] = [\min_j \mu_j, \, \max_j \mu_j]$$

**Justification:** For any quantum state $\rho$,
$$\mathrm{Tr}[\rho O] = \sum_j p_j \mu_j$$
where $p_j \geq 0$, $\sum_j p_j = 1$. This is a convex combination of eigenvalues, hence $\mathrm{Tr}[\rho O] \in [\mu_{\min}, \mu_{\max}]$.

**Special cases:**
- Pauli observable ($O \in \{X, Y, Z\}$): $\mathcal{C} = [-1, 1]$
- Probability ($O = |0\rangle\langle 0|$): $\mathcal{C} = [0, 1]$
- General Hamiltonian: $\mathcal{C} = [\lambda_{\min}(H), \lambda_{\max}(H)]$

---

## 5. Ambiguity Set $\mathcal{A}(\mathbf{y}, \mathcal{F}, \mathcal{C}, \delta)$

Given observations $\mathbf{y} = (y_1, \ldots, y_n)$, function class $\mathcal{F}$, physical constraints $\mathcal{C}$, and tolerance $\delta \geq 0$:

**Definition:**
$$\mathcal{A}(\mathbf{y}, \mathcal{F}, \mathcal{C}, \delta) = \left\{ f(0) \;\middle|\; f \in \mathcal{F}, \; f(0) \in \mathcal{C}, \; \max_{i=1}^n |f(\lambda_i) - y_i| \leq \delta \right\}$$

This is the set of all zero-noise values consistent with:
- the observed data (within tolerance $\delta$),
- the assumed function class,
- the physical constraints.

**Interpretation:**
- $\delta = 0$: exact interpolation (noiseless case)
- $\delta > 0$: approximate interpolation (accounts for shot noise)
- A natural choice: $\delta = z_{\alpha/2} \cdot \max_i \sigma_i$ for confidence level $1-\alpha$

---

## 6. Ambiguity Diameter

**Definition:**
$$\mathrm{diam}(\mathcal{A}) = \sup \mathcal{A} - \inf \mathcal{A}$$

**Interpretation:**
- $\mathrm{diam}(\mathcal{A}) = 0$: $f(0)$ is **identifiable** (uniquely determined)
- $\mathrm{diam}(\mathcal{A}) < \epsilon$: $f(0)$ is **$\epsilon$-identifiable** (determined up to $\epsilon$)
- $\mathrm{diam}(\mathcal{A}) = \mu_{\max} - \mu_{\min}$: constraints provide **no information** beyond physics

**Key question:** How does $\mathrm{diam}(\mathcal{A})$ depend on $n$, $\mathcal{F}$, $\mathcal{C}$, and $\delta$?

---

## 7. ZNE Condition Number $\kappa$

For a linear estimator $\hat{f}(0) = \mathbf{w}^\top \mathbf{y}$ where $\mathbf{w} \in \mathbb{R}^n$ are the extrapolation weights:

**Definition (unconstrained):**
$$\kappa_U = \|\mathbf{w}\|_1 = \sum_{i=1}^n |w_i|$$

This is the **worst-case noise amplification factor**: if $|\varepsilon_i| \leq \sigma$ for all $i$, then $|\hat{f}(0) - f(0)| \leq \kappa_U \cdot \sigma$.

**For polynomial extrapolation of degree $d$:** The weights $\mathbf{w}$ are determined by the Vandermonde system:
$$\mathbf{w} = \mathbf{e}_0^\top V^{-1}$$
where $V_{ij} = \lambda_i^{j-1}$ and $\mathbf{e}_0 = (1, 0, \ldots, 0)^\top$ selects the constant term.

**Definition (constrained):**
$$\kappa_B = \sup_{\|\boldsymbol{\varepsilon}\|_\infty \leq 1} \left| \hat{f}_B(0; \mathbf{y} + \boldsymbol{\varepsilon}) - \hat{f}_B(0; \mathbf{y}) \right|$$

where $\hat{f}_B$ is the bounded estimator. Note: $\kappa_B$ depends on $\mathbf{y}$ (it is a local sensitivity), unlike $\kappa_U$ which is data-independent for linear estimators.

**Key distinction:** $\kappa_U$ is a property of the design $(\boldsymbol{\lambda}, d)$. $\kappa_B$ is a property of the design, the bounds, AND the data.

---

## 8. Raw Baseline Estimator

**Definition:** The **raw baseline** is the measurement at the lowest available scale factor without extrapolation:
$$\hat{f}_{\mathrm{raw}} = y_1 = f(\lambda_1) + \varepsilon_1$$

**MSE of raw baseline:**
$$\mathrm{MSE}_{\mathrm{raw}} = \mathrm{Bias}^2_{\mathrm{raw}} + \mathrm{Var}_{\mathrm{raw}} = [f(\lambda_1) - f(0)]^2 + \sigma_1^2$$

where $\sigma_1^2 = \mathrm{Var}(\varepsilon_1)$.

**Interpretation:** The raw estimator has bias $f(\lambda_1) - f(0)$ (the noise-induced shift at the lowest scale) and variance $\sigma_1^2$ (shot noise at that point).

---

## 9. Help/Harm Criterion

**Definition:** ZNE **helps** if $\mathrm{MSE}_{\mathrm{ZNE}} < \mathrm{MSE}_{\mathrm{raw}}$.

For an unconstrained polynomial estimator of degree $d$:
$$\mathrm{MSE}_{\mathrm{ZNE}} = \mathrm{Bias}^2_{\mathrm{ZNE}}(d, f) + \kappa_U^2 \cdot \bar{\sigma}^2$$

where $\bar{\sigma}^2 = \frac{1}{n}\sum_i \sigma_i^2$ (mean shot noise variance, assuming uniform shot allocation).

**Help condition:**
$$\mathrm{Bias}^2_{\mathrm{ZNE}}(d, f) + \kappa_U^2 \cdot \bar{\sigma}^2 < [f(\lambda_1) - f(0)]^2 + \sigma_1^2$$

**Special case (well-specified model, $\mathrm{Bias}_{\mathrm{ZNE}} = 0$):**
ZNE helps if and only if:
$$\kappa_U^2 \cdot \bar{\sigma}^2 < [f(\lambda_1) - f(0)]^2 + \sigma_1^2$$

i.e., the variance amplification from extrapolation is less than the bias of not extrapolating.

**Critical shot count:** For uniform allocation with $N$ total shots ($\sigma_i^2 \approx v / (N/n)$ where $v$ is single-shot variance):
$$N^* = \frac{n \cdot \kappa_U^2 \cdot v}{[f(\lambda_1) - f(0)]^2}$$

Below $N^*$ shots, ZNE harms (variance dominates). Above $N^*$, ZNE helps (bias reduction dominates).
