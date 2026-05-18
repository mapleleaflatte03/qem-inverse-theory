# qem-inverse-theory

**Zero-noise extrapolation as a constrained quantum inverse problem.**

We do not propose another extrapolation curve; we study when extrapolation is physically identifiable.

## Mission

This repository studies when quantum error mitigation is physically identifiable, statistically stable, and worth applying under finite-shot constraints.

## Motivation

Standard ZNE asks: "Which curve fits the noisy data best?"

This project asks: "Under which physical and statistical assumptions is the zero-noise limit identifiable from finite noisy observations?"

The distinction matters. Without physical constraints, ZNE is an ill-posed inverse problem: infinitely many curves pass through noisy data points but disagree at zero noise. Finite shots compound the problem by adding statistical uncertainty to already-ambiguous observations.

We study the mathematical structure of this problem: when constraints restore identifiability, when finite shots make mitigation harmful, and what structured assumptions allow escape from generic QEM lower bounds.

## How this differs from `quantum-noise-optimizer`

| | quantum-noise-optimizer | qem-inverse-theory |
|---|---|---|
| Goal | Production mitigation engine | Theoretical research |
| Output | Mitigated expectation values | Theorems, phase diagrams, risk bounds |
| Approach | AICc + bounded optimization | Inverse problem theory + Bayesian inference |
| Hardware | Wukong 180 calibration | Synthetic only |
| Claims | Empirical benchmark results | Mathematical conditions and conjectures |

## Research questions

1. **Identifiability**: Under what physical constraints is the zero-noise limit uniquely determined from finite noisy observations?
2. **Stability**: How does the estimation error amplify as a function of noise strength, model complexity, and shot budget?
3. **Help–harm boundary**: For a given circuit class and shot budget, when does ZNE reduce MSE versus amplify it?
4. **Bayesian calibration**: Can posterior credible intervals provide reliable coverage for the zero-noise estimate?
5. **Structured escape hatches**: Which problem structures (locality, symmetry, spectral gaps) allow mitigation to remain useful despite generic lower bounds?

## Mathematical framing

Let $\lambda_1 < \lambda_2 < \cdots < \lambda_n$ be noise scale factors and $y_i = f(\lambda_i) + \epsilon_i$ the observed expectations with shot noise $\epsilon_i \sim \mathcal{N}(0, \sigma_i^2)$.

ZNE seeks $f(0)$ subject to:
- **Physical admissibility**: $f(0) \in [\lambda_{\min}(O), \lambda_{\max}(O)]$ for observable $O$
- **Smoothness/structure**: $f$ belongs to some function class $\mathcal{F}$
- **Finite data**: only $n \leq 7$ observations available

This is a constrained inverse problem. We study its well-posedness in the sense of Hadamard: existence, uniqueness, and continuous dependence on data.

## Modules

- `constraints/` — Spectral bounds, probability simplex, physical admissibility
- `estimators/` — Unconstrained, constrained, regularized, Bayesian, model selection
- `theory/` — Inverse problem formulation, risk bounds, identifiability, phase diagrams
- `benchmarks/` — Synthetic response generators, shot noise, metrics
- `plots/` — Phase diagrams, risk frontiers, coverage plots
- `experiments/` — Runnable scripts demonstrating each research question

## Out of scope

- Hardware integration or SDK
- Production-ready mitigation pipeline
- MCP server or AI-agent tooling
- Claims of solving QEM lower bounds
- Peer-reviewed theorems (this is early-stage research)

## Roadmap

1. ✅ Scaffold: types, constraints, estimators, synthetic benchmarks
2. 🔜 Finite-shot phase diagrams for polynomial ZNE
3. 🔜 Bayesian GP-based ZNE with calibrated intervals
4. 🔜 Adversarial identifiability examples
5. 🔜 Theorem sketches → rigorous proofs
6. 🔜 Paper draft: "ZNE as a Constrained Quantum Inverse Problem"

## Status

Early research prototype. See [STATUS.md](STATUS.md).

## Checkpoint

Current: **v0.1-research-scaffold**

Verify with:
```bash
bash scripts/smoke_check.sh
```
Expected: 41 tests pass, all safety checks green.

## Current Paper Status

- LaTeX skeleton exists (`paper/main.tex`) with 7 sections, 2 proven propositions
- 4 figures reproducible via `python experiments/generate_figures.py`
- `refs.bib` scaffold with verified DOIs for key citations
- All results are synthetic — no hardware claims
- Not peer-reviewed; draft is work-in-progress
- Claim safety enforced by automated tests

## Install

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
