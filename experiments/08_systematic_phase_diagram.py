"""Experiment 08: Systematic finite-shot phase diagram.

Compares multiple estimators across shot budgets and noise strengths
for several synthetic response functions.
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators import (
    fit_polynomial_zne,
    fit_bounded_polynomial_zne,
    fit_chebyshev_tikhonov_zne,
    fit_bayesian_zne_gp,
)
from qem_inverse_theory.benchmarks.shot_noise import add_gaussian_shot_noise
from qem_inverse_theory.benchmarks.metrics import mse
from qem_inverse_theory.theory.phase_diagram import compute_help_harm_ratio

# Response functions
def exp_response(scales, strength):
    return 0.8 * np.exp(-strength * scales)

def quad_response(scales, strength):
    return 0.8 - strength * scales + 0.5 * strength**2 * scales**2

def mixed_response(scales, strength):
    return 0.6 * np.exp(-strength * scales) + 0.2 * np.cos(strength * scales)

RESPONSES = {
    "exponential": (exp_response, 0.8),
    "quadratic": (quad_response, 0.8),
    "mixed_oscillatory": (mixed_response, 0.8),
}

scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
shots_grid = [100, 300, 1000, 3000, 10000]
noise_grid = [0.05, 0.1, 0.2, 0.4]
n_trials = 50
rng = np.random.default_rng(42)

methods = {
    "raw": lambda data: data.estimates[0],
    "poly_deg2": lambda data: fit_polynomial_zne(data, 2).estimate,
    "bounded_poly2": lambda data: fit_bounded_polynomial_zne(data, 2, (-1, 1)).estimate,
    "chebyshev_tik": lambda data: fit_chebyshev_tikhonov_zne(data, degree=2, bounds=(-1, 1)).estimate,
    "bayesian_gp": lambda data: fit_bayesian_zne_gp(data, bounds=(-1, 1)).estimate,
}

print("=" * 70)
print("Experiment 08: Systematic Finite-Shot Phase Diagram")
print("=" * 70)

all_results = {}

for resp_name, (resp_fn, f0_true) in RESPONSES.items():
    print(f"\n--- Response: {resp_name}, f(0) = {f0_true} ---")
    results = {}
    for noise in noise_grid:
        for shots in shots_grid:
            clean = resp_fn(scales, noise)
            estimates_by_method = {m: [] for m in methods}
            for _ in range(n_trials):
                noisy = add_gaussian_shot_noise(clean, shots=shots, rng=rng)
                data = ZNEData(scales=scales, estimates=noisy)
                for m_name, m_fn in methods.items():
                    try:
                        estimates_by_method[m_name].append(m_fn(data))
                    except Exception:
                        estimates_by_method[m_name].append(np.nan)

            row = {}
            for m_name, ests in estimates_by_method.items():
                ests_arr = np.array([e for e in ests if np.isfinite(e)])
                row[m_name] = mse(ests_arr, f0_true) if len(ests_arr) > 0 else np.inf
            results[(noise, shots)] = row
    all_results[resp_name] = results

# Generate phase diagram for bounded_poly2 vs raw (exponential response)
print("\n--- Phase diagram: bounded_poly2 help/harm (exponential) ---")
grid = np.zeros((len(noise_grid), len(shots_grid)))
for i, noise in enumerate(noise_grid):
    for j, shots in enumerate(shots_grid):
        row = all_results["exponential"][(noise, shots)]
        ratio = compute_help_harm_ratio(row["raw"], row["bounded_poly2"])
        grid[i, j] = np.log10(ratio) if ratio > 0 and np.isfinite(ratio) else 0
        status = "help" if ratio > 1.05 else ("harm" if ratio < 0.95 else "neutral")
        print(f"  noise={noise:.2f} shots={shots:5d}: ratio={ratio:.2f} [{status}]")

# Save figure
os.makedirs("figures", exist_ok=True)
fig, ax = plt.subplots(figsize=(7, 4))
im = ax.imshow(grid, origin="lower", aspect="auto", cmap="RdBu",
               extent=[np.log10(shots_grid[0]), np.log10(shots_grid[-1]),
                       noise_grid[0], noise_grid[-1]],
               vmin=-max(abs(grid.min()), abs(grid.max())),
               vmax=max(abs(grid.min()), abs(grid.max())))
ax.set_xlabel("log₁₀(total shots)")
ax.set_ylabel("Noise strength")
ax.set_title("Help/harm: bounded poly2 vs raw (exponential response)")
fig.colorbar(im, ax=ax, label="log₁₀(MSE_raw / MSE_method)")
plt.tight_layout()
plt.savefig("figures/systematic_phase_diagram.pdf", bbox_inches="tight")
plt.savefig("figures/systematic_phase_diagram.png", dpi=150, bbox_inches="tight")
plt.close()

# Save summary
os.makedirs("results", exist_ok=True)
lines = ["# Systematic Phase Diagram Results", "",
         "## Setup", "",
         "- Responses: exponential, quadratic, mixed_oscillatory",
         "- Scales: [1, 2, 3, 4, 5]",
         f"- Shots: {shots_grid}",
         f"- Noise strengths: {noise_grid}",
         f"- Trials per cell: {n_trials}",
         "- Methods: raw, poly_deg2, bounded_poly2, chebyshev_tik, bayesian_gp", "",
         "## Key findings (exponential response)", ""]

for noise in noise_grid:
    for shots in shots_grid:
        row = all_results["exponential"][(noise, shots)]
        best = min(row, key=row.get)
        lines.append(f"- noise={noise}, shots={shots}: best={best} (MSE={row[best]:.4f})")

lines += ["", "## Aggregate summary (exponential response)", "",
          "| Method | Avg log10(MSE_raw/MSE_method) | Help cells | Harm cells | Neutral |",
          "|--------|-------------------------------|------------|------------|---------|"]

method_names = [m for m in methods if m != "raw"]
for m_name in method_names:
    ratios = []
    help_c, harm_c, neut_c = 0, 0, 0
    for noise in noise_grid:
        for shots in shots_grid:
            row = all_results["exponential"][(noise, shots)]
            r = compute_help_harm_ratio(row["raw"], row[m_name])
            if np.isfinite(r) and r > 0:
                ratios.append(np.log10(r))
                if r > 1.05: help_c += 1
                elif r < 0.95: harm_c += 1
                else: neut_c += 1
    avg_lr = np.mean(ratios) if ratios else 0
    lines.append(f"| {m_name:<14} | {avg_lr:+.3f}                         | {help_c:<10} | {harm_c:<10} | {neut_c:<7} |")

lines += ["", "## Interpretation", "",
          "These synthetic results illustrate the finite-shot help/harm landscape.",
          "At low shots, variance amplification from extrapolation can make mitigation harmful.",
          "At high shots, bias reduction dominates and mitigation helps.",
          "This does not prove any method is universally superior.",
          "Results are specific to these synthetic responses and do not generalize to hardware."]

with open("results/systematic_phase_diagram.md", "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nSaved: results/systematic_phase_diagram.md")
print("Saved: figures/systematic_phase_diagram.pdf")
