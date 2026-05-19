"""Experiment 14: Two-point Le Cam lower bound for ZNE.

Demonstrates that when two admissible responses are close at observed
scales but separated at zero noise, estimation is fundamentally hard.
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from qem_inverse_theory.theory.lower_bounds import zne_two_point_lower_bound

print("=" * 70)
print("Experiment 14: Two-Point Le Cam Lower Bound")
print("=" * 70)

# Fixed parameters
sigma = 1.0  # single-shot std (Pauli observable)
n_points = 5

# Sweep 1: lower bound vs shots
print("\n--- Lower bound vs shots (delta_f0=0.3, delta_obs=0.01) ---")
shots_values = [10, 50, 100, 500, 1000, 5000, 10000]
lb_vs_shots = []
for shots in shots_values:
    r = zne_two_point_lower_bound(0.3, 0.01, sigma, n_points, shots)
    lb_vs_shots.append(r["mse_lower_bound"])
    print(f"  shots={shots:5d}: MSE_lb={r['mse_lower_bound']:.6f}  TV={r['tv_bound']:.4f}")

# Sweep 2: lower bound vs delta_f0
print("\n--- Lower bound vs delta_f0 (delta_obs=0.01, shots=1000) ---")
delta_f0_values = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8]
lb_vs_delta = []
for df in delta_f0_values:
    r = zne_two_point_lower_bound(df, 0.01, sigma, n_points, 1000)
    lb_vs_delta.append(r["mse_lower_bound"])
    print(f"  delta_f0={df:.2f}: MSE_lb={r['mse_lower_bound']:.6f}")

# Sweep 3: lower bound vs delta_obs
print("\n--- Lower bound vs delta_obs (delta_f0=0.3, shots=1000) ---")
delta_obs_values = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
lb_vs_obs = []
for do in delta_obs_values:
    r = zne_two_point_lower_bound(0.3, do, sigma, n_points, 1000)
    lb_vs_obs.append(r["mse_lower_bound"])
    print(f"  delta_obs={do:.3f}: MSE_lb={r['mse_lower_bound']:.6f}")

# Figure
os.makedirs("figures", exist_ok=True)
fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))

axes[0].plot(shots_values, lb_vs_shots, "o-")
axes[0].set_xlabel("Shots per point")
axes[0].set_ylabel("MSE lower bound")
axes[0].set_xscale("log")
axes[0].set_title("LB vs shots")

axes[1].plot(delta_f0_values, lb_vs_delta, "s-")
axes[1].set_xlabel("Δf(0)")
axes[1].set_ylabel("MSE lower bound")
axes[1].set_title("LB vs separation at zero")

axes[2].plot(delta_obs_values, lb_vs_obs, "^-")
axes[2].set_xlabel("Δ_obs (separation at observed)")
axes[2].set_ylabel("MSE lower bound")
axes[2].set_xscale("log")
axes[2].set_title("LB vs observability")

plt.tight_layout()
plt.savefig("figures/two_point_lower_bound.pdf", bbox_inches="tight")
plt.savefig("figures/two_point_lower_bound.png", dpi=150, bbox_inches="tight")
plt.close()

# Save
os.makedirs("results", exist_ok=True)
lines = ["# Two-Point Le Cam Lower Bound", "",
         "## Statement (Proposition 4)", "",
         "If two admissible response functions f+ and f- satisfy:",
         "- |f+(0) - f-(0)| = Δf(0) (separated at zero noise)",
         "- |f+(λ_i) - f-(λ_i)| ≤ Δ_obs for all observed i (close at observed scales)",
         "- Observations have Gaussian noise with variance σ²/N per point",
         "",
         "Then any estimator has:", "",
         "  MSE ≥ (Δf(0)/2)² × (1 - TV)",
         "",
         "where TV ≤ √(n_points × Δ_obs² × N / (4σ²)) via Pinsker's inequality.", "",
         "## Interpretation", "",
         "- More shots (N) → TV increases → lower bound decreases (estimation becomes possible)",
         "- Larger Δf(0) → lower bound increases (harder to be accurate)",
         "- Smaller Δ_obs → TV decreases → lower bound increases (harder to distinguish hypotheses)",
         "",
         "This formalizes the ambiguity-diameter intuition: if the ambiguity set is large",
         "(many consistent f(0) values), no estimator can achieve small MSE.", "",
         "## Caveats", "",
         "- This is a two-point bound, not a minimax bound over a function class.",
         "- It does not prove a universal QEM lower bound.",
         "- It applies to the specific pair (f+, f-), not to all possible responses.",
         "- The Gaussian noise model is an approximation of shot noise."]

with open("results/two_point_lower_bound.md", "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nSaved: results/two_point_lower_bound.md")
print("Saved: figures/two_point_lower_bound.pdf")
