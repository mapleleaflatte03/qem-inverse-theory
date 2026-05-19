"""Experiment 10: Sequential design vs static scale selection.

Compares fixed static scales against adaptive next-scale selection
under the same total shot budget.
"""

import numpy as np
import os
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators.bayesian import fit_bayesian_zne_gp, design_next_scale
from qem_inverse_theory.benchmarks.shot_noise import add_gaussian_shot_noise
from qem_inverse_theory.benchmarks.metrics import mse, absolute_error

f0_true = 0.8
decay_rate = 0.25
response_fn = lambda s: f0_true * np.exp(-decay_rate * s)
shots_per_point = 500
n_trials = 50
rng = np.random.default_rng(42)

# Static: 5 evenly spaced points
static_scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

# Sequential: start with 3 points, add 2 adaptively
initial_scales = np.array([1.0, 3.0, 5.0])
candidate_pool = np.arange(0.5, 6.0, 0.25)

print("=" * 70)
print("Experiment 10: Sequential Design vs Static Scales")
print("=" * 70)
print(f"\nResponse: f(λ) = {f0_true}·exp(-{decay_rate}·λ)")
print(f"Shots per point: {shots_per_point}")
print(f"Static: {list(static_scales)} (5 points)")
print(f"Sequential: start {list(initial_scales)}, add 2 from candidates")
print(f"Trials: {n_trials}")
print()

static_estimates = []
seq_estimates = []
seq_selected_scales = []

for trial in range(n_trials):
    # Static
    clean_static = response_fn(static_scales)
    noisy_static = add_gaussian_shot_noise(clean_static, shots=shots_per_point, rng=rng)
    var_static = np.maximum(1.0 - noisy_static**2, 0.01) / shots_per_point
    data_static = ZNEData(scales=static_scales, estimates=noisy_static, variances=var_static)
    r_static = fit_bayesian_zne_gp(data_static, bounds=(-1, 1), optimize_hyperparameters=True)
    static_estimates.append(r_static.estimate)

    # Sequential: start with initial, add 2 points
    current_scales = initial_scales.copy()
    clean_init = response_fn(current_scales)
    noisy_init = add_gaussian_shot_noise(clean_init, shots=shots_per_point, rng=rng)
    var_init = np.maximum(1.0 - noisy_init**2, 0.01) / shots_per_point

    current_estimates = noisy_init.copy()
    current_variances = var_init.copy()

    for _ in range(2):  # add 2 points
        data_curr = ZNEData(scales=current_scales, estimates=current_estimates, variances=current_variances)
        next_s = design_next_scale(data_curr, candidate_pool, bounds=(-1, 1))
        # "Measure" at the selected scale
        clean_new = response_fn(np.array([next_s]))
        noisy_new = add_gaussian_shot_noise(clean_new, shots=shots_per_point, rng=rng)
        var_new = np.maximum(1.0 - noisy_new**2, 0.01) / shots_per_point

        current_scales = np.append(current_scales, next_s)
        current_estimates = np.append(current_estimates, noisy_new)
        current_variances = np.append(current_variances, var_new)

    data_seq = ZNEData(scales=current_scales, estimates=current_estimates, variances=current_variances)
    r_seq = fit_bayesian_zne_gp(data_seq, bounds=(-1, 1), optimize_hyperparameters=True)
    seq_estimates.append(r_seq.estimate)
    if trial == 0:
        seq_selected_scales.append(current_scales.tolist())

static_arr = np.array(static_estimates)
seq_arr = np.array(seq_estimates)

mse_static = mse(static_arr, f0_true)
mse_seq = mse(seq_arr, f0_true)
mae_static = float(np.mean(np.abs(static_arr - f0_true)))
mae_seq = float(np.mean(np.abs(seq_arr - f0_true)))

print(f"Results ({n_trials} trials):")
print(f"  Static (5 fixed):     MSE={mse_static:.5f}  MAE={mae_static:.4f}")
print(f"  Sequential (3+2):     MSE={mse_seq:.5f}  MAE={mae_seq:.4f}")
print(f"  Improvement:          {(1 - mse_seq/mse_static)*100:.1f}% MSE reduction")
print(f"  Example selected scales: {seq_selected_scales[0]}")

# Save
os.makedirs("results", exist_ok=True)
lines = ["# Sequential Design Comparison", "",
         "## Setup", "",
         f"- Response: f(λ) = {f0_true}·exp(-{decay_rate}·λ)",
         f"- Shots per point: {shots_per_point}",
         f"- Static scales: {list(static_scales)}",
         f"- Sequential: start with {list(initial_scales)}, add 2 via posterior variance minimization",
         f"- Trials: {n_trials}",
         "- Estimator: bounded Bayesian GP with optimized hyperparameters", "",
         "## Results", "",
         f"| Strategy | MSE | MAE |",
         f"|----------|-----|-----|",
         f"| Static (5 fixed) | {mse_static:.5f} | {mae_static:.4f} |",
         f"| Sequential (3+2) | {mse_seq:.5f} | {mae_seq:.4f} |", "",
         f"MSE improvement: {(1 - mse_seq/mse_static)*100:.1f}%", "",
         "## Interpretation", "",
         "Sequential design selects measurement points to minimize posterior uncertainty at λ=0.",
         "In this synthetic setup, adaptive selection can improve estimation by choosing scales",
         "that are more informative for extrapolation to zero noise.",
         "",
         "**Caveats:**",
         "- Single response function (exponential decay)",
         "- Greedy one-step lookahead (not globally optimal)",
         "- Same total measurements (5 points × same shots)",
         "- Does not account for the cost of the design computation itself",
         "- Results are synthetic and do not generalize to hardware"]

with open("results/sequential_design.md", "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nSaved: results/sequential_design.md")
