"""Experiment 03: Finite-shot help–harm phase diagram.

Generates a toy phase diagram showing when ZNE helps vs harms
as a function of shot budget and noise strength.
"""

import numpy as np
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators import fit_bounded_polynomial_zne
from qem_inverse_theory.benchmarks import exponential_decay_response, add_gaussian_shot_noise
from qem_inverse_theory.benchmarks.metrics import mse
from qem_inverse_theory.theory.phase_diagram import build_phase_grid, classify_region

rng = np.random.default_rng(42)
scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
f0_true = 0.7
n_trials = 50

shot_values = [50, 100, 500, 1000, 5000]
noise_strengths = [0.05, 0.1, 0.2, 0.4, 0.8]

print("=" * 60)
print("Experiment 03: Finite-Shot Help–Harm Phase Diagram")
print("=" * 60)
print(f"\nTrue f(0) = {f0_true}, n_trials = {n_trials}")
print()

results = []
for noise in noise_strengths:
    for shots in shot_values:
        raw_estimates = []
        mit_estimates = []
        for _ in range(n_trials):
            clean = exponential_decay_response(scales, f0=f0_true, decay_rate=noise)
            noisy = add_gaussian_shot_noise(clean, shots=shots, rng=rng)
            data = ZNEData(scales=scales, estimates=noisy)

            raw_estimates.append(noisy[0])  # raw = first scale factor
            result = fit_bounded_polynomial_zne(data, degree=2, bounds=(-1.0, 1.0))
            mit_estimates.append(result.estimate)

        raw_mse = mse(np.array(raw_estimates), f0_true)
        mit_mse = mse(np.array(mit_estimates), f0_true)
        region = classify_region(raw_mse, mit_mse)
        results.append({
            "shots": shots,
            "noise_strength": noise,
            "raw_mse": raw_mse,
            "mitigated_mse": mit_mse,
        })
        ratio = raw_mse / mit_mse if mit_mse > 0 else np.inf
        print(f"  noise={noise:.2f}, shots={shots:5d}: "
              f"raw_MSE={raw_mse:.4f}, mit_MSE={mit_mse:.4f}, "
              f"ratio={ratio:.2f} [{region}]")

grid = build_phase_grid(results)
print(f"\nPhase grid shape: {grid['log_ratio_grid'].shape}")
print("Positive = help, Negative = harm")
