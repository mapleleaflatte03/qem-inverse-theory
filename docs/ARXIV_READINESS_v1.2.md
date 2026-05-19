# arXiv Readiness Audit: v1.2

## Verdict

**Ready for arXiv as a technical report / workshop companion paper.**

Not yet ready for a full venue submission (PRA, Quantum, PRX Quantum) without additional theorem hardening.

## What Is Ready

- [x] Clean-room arXiv package builds (4 pages, no errors, no missing figures/citations)
- [x] All cited refs.bib entries verified (DOI or arXiv confirmed)
- [x] No VERIFY notes remain in refs.bib for cited entries
- [x] Claim safety checks pass (no overclaims)
- [x] 80 tests pass
- [x] Negative results preserved honestly
- [x] Non-exponential result now mentioned in manuscript
- [x] Paper scope explicitly stated as "framework paper"
- [x] Figures support central thesis (ambiguity diameter)

## What Was Resolved in v1.2

| Blocker | Resolution |
|---------|-----------|
| VERIFY in refs.bib (Miranskyy2026) | Confirmed from arXiv; note changed to "not yet peer-reviewed" |
| VERIFY in refs.bib (Hadamard1902) | Page numbers from secondary sources; note updated |
| Single-response dominance | Added quadratic response result sentence in §6 |
| Clean-room arXiv build | Rebuilt and passes (4 pages, 0 errors) |

## What Still Blocks Full Venue Submission

| Item | Status | Impact |
|------|--------|--------|
| Only 2 elementary propositions | No nontrivial theorem | Weak for theory venue |
| No circuit-family benchmarks | Synthetic exponential/quadratic only | Weak for methods venue |
| No hardware evaluation | Synthetic only | Cannot claim practical impact |
| literature.md still has 5 VERIFY entries | Not cited in main.tex; informational only | Low risk |

## Recommended Path

1. **Immediate (v1.2):** Submit to arXiv as `cs.LG` or `quant-ph` technical report.
2. **Short-term (v1.3):** Add Proposition 3 (help/harm threshold) for theory strengthening.
3. **Medium-term (v1.4):** Add TFIM/VQE circuit benchmarks for methods strengthening.
4. **Long-term (v2.0):** Full venue submission with theorem + benchmarks + possibly hardware.
