# Research Roadmap

4-week plan for moving from scaffold to submittable manuscript.

---

## Week 1: Formal Definitions + Proof Cleanup

- [x] Formalize all definitions (observation model, function class, ambiguity set, condition number, help/harm)
- [x] Prove Proposition 1 (non-identifiability)
- [x] Prove Proposition 2 (spectral validity) + Corollary 2.1
- [ ] Attempt proof of Conjecture 1 (κ_B ≤ κ_U) or identify counterexample
- [ ] Formalize Theorem 3 (help/harm criterion) with correct MSE expressions

## Week 2: Ambiguity Experiments + Sensitivity Analysis

- [x] Ambiguity diameter vs polynomial degree
- [x] Ambiguity diameter vs tolerance δ
- [ ] Ambiguity diameter vs number of scale factors n
- [ ] Ambiguity diameter for non-polynomial function classes (exponential)
- [ ] Multiple response functions (not just single exponential)
- [ ] Connect δ to shot budget: δ = z_{α/2} · σ_max

## Week 3: Literature Verification + BibTeX

- [ ] Verify all VERIFY-marked citations against arXiv/DOI
- [ ] Convert literature.md to refs.bib
- [ ] Read and summarize Takagi2022 and Quek2024 proof techniques
- [ ] Identify exactly which assumptions in lower-bound proofs might fail for structured problems
- [ ] Add any missing relevant citations found during verification

## Week 4: LaTeX Manuscript Skeleton

- [ ] Convert draft.md sections 1–5 to LaTeX
- [ ] Add proper theorem/proof environments
- [ ] Include ambiguity diameter figures (matplotlib → PDF)
- [ ] Write Discussion and Limitations section
- [ ] Internal review: check every claim against claim_ledger.md

---

## Stop Conditions

Do NOT proceed to submission/preprint until:

1. **All citations verified.** Every VERIFY-marked entry in `paper/literature.md` must be checked against the official source (arXiv page, DOI, publisher). Do not cite [Miranskyy2026] as fact until the arXiv ID is confirmed.

2. **No unsupported accuracy claims.** Do not claim constrained optimization reduces MSE unless either (a) a proof is complete or (b) systematic numerical experiments across multiple response classes support it with honest error bars.

3. **No hardware claims.** Do not mention hardware results unless experiments are actually run on quantum hardware.

4. **Claim ledger consistent.** Every claim in the manuscript must appear in `paper/claim_ledger.md` at the appropriate rigor level. If a claim is "Conjectural," it must be labeled as such in the paper text.

5. **Limitations section complete.** The paper must explicitly state what is not proven, what is synthetic-only, and what assumptions are made.

---

## Success Criteria

The manuscript is ready for arXiv when:
- Propositions 1, 2 are cleanly stated and proven
- At least one additional result (Conjecture 1 proven, or help/harm criterion formalized, or ambiguity diameter generalized)
- All citations verified
- Limitations section is honest and complete
- No claim exceeds its evidence level in the claim ledger
