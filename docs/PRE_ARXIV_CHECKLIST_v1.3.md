# Pre-arXiv Checklist: v1.3

## Overall Verdict: PASS ✓

Ready for submission as arXiv technical report.

## Checklist

| Item | Status |
|------|--------|
| Tests pass (80) | ✅ |
| Smoke check passes | ✅ |
| Clean-room arXiv build passes | ✅ |
| No undefined citations | ✅ |
| No missing figures | ✅ |
| No VERIFY in cited refs.bib | ✅ (0 occurrences) |
| No unsafe wording | ✅ |
| No hardware validation claim | ✅ |
| No universal superiority claim | ✅ |
| No lower-bound defeat claim | ✅ |
| Proposition 3 described as model-conditional | ✅ |
| Negative results preserved | ✅ |
| Abstract states "all results are synthetic" | ✅ |
| Paper scope stated as "framework paper" | ✅ |

## arXiv Category Recommendation

- **Primary:** `quant-ph` (quantum physics — ZNE/QEM is core quantum computing)
- **Secondary (optional):** `cs.LG` (machine learning — model selection, Bayesian inference aspects)
- **Alternative:** `stat.ME` (methodology — inverse problems, identifiability)

## Title

"Zero-Noise Extrapolation as a Constrained Quantum Inverse Problem"

Status: Clear, descriptive, not overclaiming. Ready.

## Abstract

Status: Compressed single paragraph. States contributions, results (positive and negative), and non-claims. Ready.

## Source Package

- Path: `dist/qem-inverse-theory-arxiv-source.zip`
- Contents: main.tex, main.bbl, refs.bib, 4 PDF figures
- Clean-room build: 4 pages, 0 errors
- Status: Ready.

## Remaining Non-Blocking Improvements

These would strengthen the paper but do not block arXiv submission:

1. **Add δ-sensitivity figure** — would visually support the "6.2× reduction" claim (asset exists, just not in manuscript)
2. **Expand non-exponential results** — currently one sentence; a small table would be stronger
3. **Add ORCID** to author metadata
4. **Consider adding n-sensitivity figure** — asset exists, supports the n/(d+1) ratio insight
5. **Verify target venue formatting** — current revtex4-2/pra is fine for quant-ph arXiv

None of these are required for a valid arXiv technical report submission.
