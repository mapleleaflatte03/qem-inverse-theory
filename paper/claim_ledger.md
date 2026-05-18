# Claim Ledger

What this project claims, at what level of rigor, and what it explicitly does not claim.

---

## Proven

These have complete proofs (see `paper/proofs.md`).

| Claim | Proof | Reference |
|-------|-------|-----------|
| Without function-class restrictions, f(0) is not identifiable from finite observations | Lagrange interpolation on n+1 distinct points | Proposition 1 |
| Expectation values lie within observable spectral bounds | Born rule + convex combination | Proposition 2 |
| Post-hoc projection of a scalar estimate onto the spectral interval cannot increase pointwise error when the true value lies inside | Non-expansiveness of projection onto convex set | Corollary 2.1 |

---

## Demonstrated Synthetically

These are supported by numerical experiments on synthetic data. They are not theorems.

| Claim | Evidence | Caveats |
|-------|----------|---------|
| Ambiguity diameter shrinks under physical bounds (vs unbounded) | Degree-4 experiment: 0.62 → 0.51 (Pauli), 0.62 → 0.51 (probability) at δ=0.01 | Single response function, polynomial class only |
| Ambiguity grows with tolerance δ | δ-sensitivity table: 0.0 → 0.001 → 0.01 → 0.05 → 0.1 shows monotone increase | Monotonicity not proven in general |
| Bounds matter most when function class is flexible or data uncertainty is large | At δ=0.1: unbounded 6.2 vs probability-bounded 1.0 (6.2× reduction) | Specific to degree-4, exponential response, n=5 |
| At low polynomial degree (d < n-1), function class alone constrains f(0) | Degrees 2–3 show same ambiguity regardless of bounds | Only tested for one response |

---

## Conjectural

These are believed plausible but have no proof or definitive numerical evidence.

| Claim | Status | Difficulty |
|-------|--------|------------|
| Constrained optimization (not just clipping) reduces MSE vs unconstrained | Open — proof sketch has gaps (Conjecture 1) | Medium: requires KKT sensitivity analysis |
| κ_B ≤ κ_U (bounded condition number ≤ unconstrained) | Open — non-expansiveness argument doesn't directly apply | Medium-hard |
| Structured local observables evade generic QEM lower-bound scaling | Research direction — no proof attempted | Hard |
| Bayesian GP-ZNE intervals achieve nominal coverage | Prototype exists but hyperparameters not optimized | Medium: requires calibration study |
| Help/harm phase boundary N* is computable from observable quantities | Formula exists for well-specified case; misspecified case open | Medium |

---

## Not Claimed

These are explicitly outside the scope of this project's current claims.

| Non-claim | Why |
|-----------|-----|
| Hardware improvement on real quantum processors | No hardware experiments conducted |
| Universal superiority of bounded ZNE over standard ZNE | Not supported by theory or experiments |
| General proof beyond polynomial function classes | Only polynomials analyzed so far |
| Defeating or circumventing QEM lower bounds | We search for structured exceptions, not violations |
| Peer-reviewed validation | No submission yet; draft is work-in-progress |
| Bounded ZNE always reduces MSE | Projection reduces pointwise error, but constrained optimization is different |
| Applicability to real noise channels | All experiments use synthetic/analytical responses |
