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
| Increasing n reduces ambiguity only when model degree is fixed (overdetermined regime) | Fixed d=2: ambiguity 0.14→0.04 as n goes 3→7 | Single response, polynomial class only |
| In the interpolation regime d = n-1, ambiguity grows with n | d=n-1: ambiguity 0.14→2.54 as n goes 3→7 | Specific to evenly-spaced scales and exponential response |
| Bias–ambiguity tradeoff: lower degree reduces ambiguity but increases misspecification bias | n=7: d=2 has bias 0.035/ambiguity 0.04; d=6 has bias 0.000/ambiguity 2.54 | Single exponential response, noiseless, no proof of optimal selection |
| Higher degree reduces bias but increases ambiguity | Monotone in both directions across d=2..6 for this response | No proof this holds for all responses |
| Physical bounds are most valuable in the high-uncertainty regime | δ sensitivity shows bounds cap ambiguity as δ grows | Interpretation of synthetic results, not a theorem |
| Identifiability depends on n/(d+1) ratio, not n alone | n-sensitivity comparison: interpolation vs fixed degree | Observed pattern, not proven in general |
| Model selection is essential but fundamentally limited for ZNE | Bias-ambiguity tradeoff shows no single degree is optimal | Does not claim AICc or any criterion is optimal |
| Chebyshev-Tikhonov extrapolates outside basis domain (z0 < -1) | Diagnostics confirm z0 = -1.5 for scales [1,5] | Implementation detail, not a claim of superiority |
| Bounded polynomial ZNE helps in 16/20 phase diagram cells (exponential) | Experiment 08 aggregate | Single response, synthetic, 50 trials per cell |
| Bayesian GP with fixed hyperparameters harms in 13/20 cells | Experiment 08 aggregate | Demonstrates need for calibration, not method failure |
| Bayesian 90% CI achieves 89% coverage at low noise | Experiment 09 aggregate (noise=0.10) | Well-calibrated in this regime only |
| Bayesian 90% CI achieves only 70% coverage at high noise | Experiment 09 aggregate (noise=0.25) | Negative result: fixed hyperparameters insufficient |
| Sequential design (λ≥1) achieves 24.3% MSE reduction | Experiment 10 (50 trials, exponential) | Single response, greedy one-step, synthetic |
| Sequential design (λ≥0.5) achieves 66% but is non-standard ZNE | Experiment 10 | Clearly labeled synthetic near-zero, not ZNE-relevant |
| Locality-aware heuristic worsens MSE by 1-11% | Experiment 11 (100 trials) | Negative result: proxy over-regularizes |
| Six candidate escape-hatch structures identified | Taxonomy in docs + paper | Research directions, not proven escape hatches |

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
