"""Experiment 10: Sequential design vs static scale selection.

Compares fixed static scales against adaptive next-scale selection
under the same total measurement budget, with two candidate regimes:
A. ZNE-relevant: candidates λ ≥ 1 (standard noise amplification)
B. Synthetic near-zero: candidates λ ≥ 0.5 (includes sub-unit scales)
"""

import numpy as np
import os
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators.bayesian import fit_bayesian_zne_gp, design_next_scale
from qem_inverse_theory.benchmarks.shot_noise import add_gaussian_shot_noise
from qem_inverse_theory.benchmarks.metrics import mse

f0_true = 0.8
decay_rate = 0.25
response_fn = lambda s: f0_true * np.exp(-decay_rate * s)
shots_per_point = 500
n_trials = 50
rng = np.random.default_rng(42)

static_scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
initial_scales = np.array([1.0, 3.0, 5.0])

# Two candidate regimes
regimes = {
    "ZNE-relevant (λ≥1)": np.arange(1.0, 6.25, 0.25),
    "Synthetic near-zero (λ≥0.5)": np.arange(0.5, 6.25, 0.25),
}

print("=" * 70)
print("Experiment 10: Sequential Design vs Static Scales")
print("=" * 70)
print(f"\nResponse: f(λ) = {f0_true}·exp(-{decay_rate}·λ)")
print(f"Shots per point: {shots_per_point}, Trials: {n_trials}")
print(f"Static: [1,2,3,4,5] (5 points)")
print(f"Sequential: start [1,3,5], add 2 adaptively")
print()

all_results = {}

# Static baseline
static_estimates = []
for _ in range(n_trials):
    clean = response_fn(static_scales)
    noisy = add_gaussian_shot_noise(clean, shots=shots_per_point, rng=rng)
    var = np.maximum(1.0 - noisy**2, 0.01) / shots_per_point
    data = ZNEData(scales=static_scales, estimates=noisy, variances=var)
    r = fit_bayesian_zne_gp(data, bounds=(-1, 1), optimize_hyperparameters=True)
    static_estimates.append(r.estimate)

mse_static = mse(np.array(static_estimates), f0_true)
mae_static = float(np.mean(np.abs(np.array(static_estimates) - f0_true)))
all_results["Static (5 fixed)"] = {"mse": mse_static, "mae": mae_static, "scales": list(static_scales)}
print(f"  Static (5 fixed):        MSE={mse_static:.5f}  MAE={mae_static:.4f}")

# Sequential for each regime
for regime_name, candidates in regimes.items():
    seq_estimates = []
    example_scales = None
    for trial in range(n_trials):
        current_scales = initial_scales.copy()
        clean_init = response_fn(current_scales)
        noisy_init = add_gaussian_shot_noise(clean_init, shots=shots_per_point, rng=rng)
        var_init = np.maximum(1.0 - noisy_init**2, 0.01) / shots_per_point
        current_estimates = noisy_init.copy()
        current_variances = var_init.copy()

        for _ in range(2):
            data_curr = ZNEData(scales=current_scales, estimates=current_estimates, variances=current_variances)
            next_s = design_next_scale(data_curr, candidates, bounds=(-1, 1))
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
            example_scales = current_scales.tolist()

    mse_seq = mse(np.array(seq_estimates), f0_true)
    mae_seq = float(np.mean(np.abs(np.array(seq_estimates) - f0_true)))
    improvement = (1 - mse_seq / mse_static) * 100
    all_results[regime_name] = {"mse": mse_seq, "mae": mae_seq, "scales": example_scales, "improvement": improvement}
    print(f"  Sequential {regime_name}: MSE={mse_seq:.5f}  MAE={mae_seq:.4f}  "
          f"({improvement:+.1f}% vs static)  scales={example_scales}")

# Save
os.makedirs("results", exist_ok=True)
lines = ["# Sequential Design Comparison", "",
         "## Setup", "",
         f"- Response: f(λ) = {f0_true}·exp(-{decay_rate}·λ), true f(0) = {f0_true}",
         f"- Shots per point: {shots_per_point}",
         f"- Static scales: [1, 2, 3, 4, 5]",
         f"- Sequential: start [1, 3, 5], add 2 via posterior variance minimization",
         f"- Trials: {n_trials}", "",
         "## Results", "",
         "| Strategy | MSE | MAE | vs Static |",
         "|----------|-----|-----|-----------|"]
for name, r in all_results.items():
    imp = f"{r.get('improvement', 0):+.1f}%" if "improvement" in r else "baseline"
    lines.append(f"| {name} | {r['mse']:.5f} | {r['mae']:.4f} | {imp} |")

lines += ["", "## Interpretation", "",
          "**ZNE-relevant regime (λ≥1):** Sequential design selects additional noise-amplified",
          "measurement points that are most informative for extrapolation. This is the",
          "operationally meaningful comparison for standard ZNE practice.",
          "",
          "**Synthetic near-zero regime (λ≥0.5):** Allowing sub-unit scale factors (λ<1)",
          "is not standard ZNE (which amplifies noise, λ≥1). This regime tests the",
          "mathematical design principle but is not directly applicable to hardware ZNE.",
          "It should not be cited as a ZNE improvement without this caveat.",
          "",
          "**Caveats:**",
          "- Single response function (exponential decay)",
          "- Greedy one-step lookahead (not globally optimal)",
          "- Same total measurements (5 points × same shots per point)",
          "- Synthetic only, no hardware validation"]

with open("results/sequential_design.md", "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nSaved: results/sequential_design.md")
