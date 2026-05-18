# Proofs

---

## Proposition 1: Non-Identifiability Without Function-Class Restrictions

**Statement.**
Let $\lambda_1, \ldots, \lambda_n > 0$ be distinct and let $y_1, \ldots, y_n \in \mathbb{R}$. For any $t \in \mathbb{R}$, there exists a polynomial $p$ of degree at most $n$ such that:
$$p(\lambda_i) = y_i \quad \text{for } i = 1, \ldots, n, \qquad p(0) = t.$$

**Proof.**
Consider the $n+1$ distinct points $x_0 = 0, x_1 = \lambda_1, \ldots, x_n = \lambda_n$. Since all $\lambda_i > 0$ and are distinct, the $n+1$ points $\{0, \lambda_1, \ldots, \lambda_n\}$ are distinct.

Define the interpolation conditions:
$$p(x_0) = t, \quad p(x_i) = y_i \text{ for } i = 1, \ldots, n.$$

By the uniqueness theorem for polynomial interpolation (Lagrange), there exists a unique polynomial of degree at most $n$ passing through any $n+1$ distinct points with prescribed values. Explicitly:
$$p(x) = t \cdot L_0(x) + \sum_{i=1}^n y_i \cdot L_i(x)$$

where the Lagrange basis polynomials are:
$$L_j(x) = \prod_{\substack{k=0 \\ k \neq j}}^{n} \frac{x - x_k}{x_j - x_k}$$

Each $L_j$ has degree exactly $n$, so $p$ has degree at most $n$. By construction, $p(x_j) = y_j$ for $j = 0, \ldots, n$ (with $y_0 := t$). $\square$

**Corollary 1.1.**
If the function class is $\mathcal{F} = \mathcal{P}_n$ (polynomials of degree $\leq n$) and no physical constraints are imposed ($\mathcal{C} = \mathbb{R}$), then:
$$\mathcal{A}(\mathbf{y}, \mathcal{P}_n, \mathbb{R}, 0) = \mathbb{R}$$

The ambiguity diameter is infinite. ZNE is completely undetermined.

**Corollary 1.2.**
For the restricted class $\mathcal{F} = \mathcal{P}_d$ with $d < n$ (fewer parameters than data points), the interpolation system is overdetermined and generically has no solution for arbitrary $t$. In this case, $\mathcal{A}$ may be a proper subset of $\mathbb{R}$, and identifiability becomes possible.

**Corollary 1.3.**
Physical constraints $\mathcal{C} = [a, b]$ reduce the ambiguity set to at most $[a, b]$:
$$\mathcal{A}(\mathbf{y}, \mathcal{P}_n, [a,b], 0) \subseteq [a, b]$$

This is a finite reduction from $\mathbb{R}$, but may still equal all of $[a, b]$ if for every $t \in [a,b]$ the interpolating polynomial exists (which it does, by the proposition above).

---

## Proposition 2: Spectral Validity of Expectation Values

**Statement.**
Let $O$ be a Hermitian operator on a finite-dimensional Hilbert space $\mathcal{H}$ with eigenvalues $\mu_1, \ldots, \mu_m$ (counted with multiplicity). Let $\rho$ be any density operator on $\mathcal{H}$ (i.e., $\rho \geq 0$, $\mathrm{Tr}[\rho] = 1$). Then:
$$\mu_{\min} \leq \mathrm{Tr}[\rho O] \leq \mu_{\max}$$

where $\mu_{\min} = \min_j \mu_j$ and $\mu_{\max} = \max_j \mu_j$.

**Proof.**
Since $O$ is Hermitian, it admits a spectral decomposition:
$$O = \sum_{j=1}^m \mu_j \, |e_j\rangle\langle e_j|$$

where $\{|e_j\rangle\}$ is an orthonormal eigenbasis. Then:
$$\mathrm{Tr}[\rho O] = \sum_{j=1}^m \mu_j \, \mathrm{Tr}[\rho \, |e_j\rangle\langle e_j|] = \sum_{j=1}^m \mu_j \, p_j$$

where $p_j = \langle e_j | \rho | e_j \rangle$.

Since $\rho \geq 0$: $p_j = \langle e_j | \rho | e_j \rangle \geq 0$ for all $j$.

Since $\mathrm{Tr}[\rho] = 1$: $\sum_{j=1}^m p_j = \sum_j \langle e_j | \rho | e_j \rangle = \mathrm{Tr}[\rho] = 1$.

Therefore $(p_1, \ldots, p_m)$ is a probability distribution, and $\mathrm{Tr}[\rho O] = \sum_j \mu_j p_j$ is a convex combination of the eigenvalues. A convex combination of real numbers lies within their range:
$$\mu_{\min} = \min_j \mu_j \leq \sum_j \mu_j p_j \leq \max_j \mu_j = \mu_{\max}$$

$\square$

**Corollary 2.1 (Projection reduces error).**
Let $f(0) \in [\mu_{\min}, \mu_{\max}]$ be the true expectation value and let $\hat{f}$ be any estimate. Define:
$$\hat{f}_{\mathrm{proj}} = \mathrm{proj}_{[\mu_{\min}, \mu_{\max}]}(\hat{f}) = \mathrm{clip}(\hat{f}, \mu_{\min}, \mu_{\max})$$

Then $|\hat{f}_{\mathrm{proj}} - f(0)| \leq |\hat{f} - f(0)|$.

**Proof of Corollary 2.1.**
Projection onto a closed convex set $C$ is non-expansive: for any $x$ and any $y \in C$,
$$|\mathrm{proj}_C(x) - y| \leq |x - y|$$

Since $f(0) \in [\mu_{\min}, \mu_{\max}]$ (by Proposition 2), taking $C = [\mu_{\min}, \mu_{\max}]$, $x = \hat{f}$, and $y = f(0)$ gives the result. $\square$

---

## What These Propositions Do NOT Prove

These two results establish foundational facts but have clear limits:

1. **They do not prove bounded ZNE is more accurate.** Proposition 2 shows projection cannot *increase* error, but a constrained optimization estimator (which changes all coefficients, not just clips the output) may or may not reduce MSE compared to unconstrained estimation. That is a separate, harder question (see Conjecture 1).

2. **They do not prove constrained estimators always reduce MSE.** Constraints reduce the ambiguity set (Corollary 1.3) and projection reduces pointwise error (Corollary 2.1), but the MSE of a constrained *optimization* procedure depends on the bias-variance tradeoff, which is data- and model-dependent.

3. **They do not prove hardware usefulness.** All statements are about mathematical properties of estimators applied to an abstract observation model. Whether these translate to improved results on real quantum hardware depends on whether the assumptions (known scale factors, Gaussian noise, correct spectral bounds) hold in practice.

4. **They only establish the need for assumptions.** Proposition 1 shows that without function-class restrictions, ZNE is undetermined. Proposition 2 shows that physical bounds are always valid constraints. Together, they motivate the research program: study what happens when you combine function-class restrictions with physical constraints.
