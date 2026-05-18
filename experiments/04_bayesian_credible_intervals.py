"""Experiment 04: Bayesian credible intervals for ZNE.

Demonstrates GP-based Bayesian ZNE with posterior uncertainty.
EXPERIMENTAL: hyperparameters not optimized.
"""

import numpy as np
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators import fit_bayesian_zne_gp
from qem_inverse_theory.benchmarks import exponential_decay_response, add_gaussian_shot_noise
from qem_inverse_theory.benchmarks.metrics import interval_coverage

rng = np.random.default_rng(42)
scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
f0_true = 0.75
shots = 500
n_trials = 100

print("=" * 60)
print("Experiment 04: Bayesian Credible Intervals")
print("=" * 60)
print(f"\nTrue f(0) = {f0_true}, shots = {shots}, n_trials = {n_trials}")
print()

intervals = []
estimates = []
for i in range(n_trials):
    clean = exponential_decay_response(scales, f0=f0_true, decay_rate=0.25)
    noisy = add_gaussian_shot_noise(clean, shots=shots, rng=rng)
    data = ZNEData(scales=scales, estimates=noisy)

    result = fit_bayesian_zne_gp(data, bounds=(-1.0, 1.0))
    estimates.append(result.estimate)
    intervals.append(result.diagnostics["ci_95"])

coverage = interval_coverage(intervals, f0_true)
mean_width = np.mean([hi - lo for lo, hi in intervals])

print(f"Posterior mean (avg): {np.mean(estimates):.4f}")
print(f"Posterior std (avg):  {np.std(estimates):.4f}")
print(f"95% CI coverage:      {coverage:.2%} (nominal: 95%)")
print(f"Mean CI width:        {mean_width:.4f}")
print(f"|Bias|:               {abs(np.mean(estimates) - f0_true):.4f}")
print()
print("Note: Coverage may differ from nominal due to fixed hyperparameters.")
print("Hyperparameter optimization is future work.")
