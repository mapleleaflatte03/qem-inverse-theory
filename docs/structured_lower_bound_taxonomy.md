# Structured Lower-Bound Taxonomy

## What generic QEM lower bounds say

Takagi et al. (2022) and Quek et al. (2024) prove that generic quantum error mitigation requires exponential sampling overhead in the worst case. Specifically, for arbitrary circuits and observables, the sample cost of achieving fixed accuracy scales exponentially with circuit depth or system size.

## Why this repo does not claim to defeat them

We do not claim to circumvent, violate, or overcome these lower bounds. They are mathematically correct for their stated assumptions. Instead, we ask: **which structural assumptions place a problem instance outside the pessimistic generic regime?**

## Candidate structure classes

### 1. Low observable support

| Property | Value |
|----------|-------|
| Assumption | Observable acts on k ≪ n qubits |
| Why it may help | Effective dimension scales with k, not n; noise on distant qubits may be irrelevant |
| Lower-bound assumption it avoids | Worst-case bounds often use global observables or high-weight Paulis |
| Needed experiment | MSE scaling with n at fixed k |
| Needed theorem | Risk bound parameterized by k instead of n |
| Current repo support | `theory/locality.py` (support estimation), experiment 11 |

### 2. Low circuit depth

| Property | Value |
|----------|-------|
| Assumption | Circuit depth D is O(1) or O(log n) |
| Why it may help | Limited information propagation; noise response is smoother |
| Lower-bound assumption it avoids | Exponential bounds often require depth Ω(n) for full scrambling |
| Needed experiment | Ambiguity diameter vs depth |
| Needed theorem | Stability bound with explicit depth dependence |
| Current repo support | `StructureDescriptor.circuit_depth` in classification |

### 3. Symmetry-constrained observables

| Property | Value |
|----------|-------|
| Assumption | Observable commutes with a symmetry of the noise channel |
| Why it may help | Symmetry reduces effective Hilbert space; noise acts within symmetry sectors |
| Lower-bound assumption it avoids | Generic bounds do not exploit symmetry structure |
| Needed experiment | Compare mitigated MSE in symmetric vs non-symmetric sectors |
| Needed theorem | Dimension reduction from symmetry → reduced sample cost |
| Current repo support | `StructureDescriptor.symmetry_constraints` field |

### 4. Weak scrambling

| Property | Value |
|----------|-------|
| Assumption | Circuit does not fully scramble information (e.g., Clifford+few T gates, QAOA p=1) |
| Why it may help | Noise response remains structured; extrapolation is more stable |
| Lower-bound assumption it avoids | Worst-case bounds use maximally scrambling circuits |
| Needed experiment | Compare phase diagram for scrambling vs non-scrambling circuits |
| Needed theorem | Condition number bound parameterized by scrambling indicator |
| Current repo support | `StructureDescriptor.scrambling_indicator` |

### 5. Bounded smooth response class

| Property | Value |
|----------|-------|
| Assumption | f(λ) belongs to a known smooth class (analytic, Gevrey, bounded derivatives) |
| Why it may help | Smoothness constrains extrapolation; ambiguity diameter shrinks |
| Lower-bound assumption it avoids | Generic bounds allow arbitrary noise channels |
| Needed experiment | Ambiguity diameter for different smoothness classes |
| Needed theorem | Minimax rate over bounded smooth class |
| Current repo support | Ambiguity diameter experiments (polynomial class) |

### 6. Calibrated Bayesian uncertainty

| Property | Value |
|----------|-------|
| Assumption | Prior is well-specified; posterior is calibrated |
| Why it may help | Bayesian estimator can abstain when uncertain, avoiding harmful mitigation |
| Lower-bound assumption it avoids | Lower bounds assume worst-case estimation, not decision-theoretic abstention |
| Needed experiment | Coverage calibration + decision rule: mitigate only when CI is narrow |
| Needed theorem | Regret bound for Bayesian decision rule vs always-mitigate |
| Current repo support | Bayesian GP + coverage calibration (experiments 09, 10) |

## Status

All entries above are **research directions**, not claimed results. No theorem proves that any of these structures actually achieves polynomial-cost mitigation. The taxonomy organizes the search space for future work.
