"""Experiment 12: Circuit-family benchmark suite with noise model grid.

Runs ZNE benchmarks across circuit families AND noise models.
All results are synthetic — no hardware or circuit simulation claims.
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from qem_inverse_theory.benchmarks.suite import run_benchmark_suite

families = ["ghz", "tfim", "heisenberg", "vqe", "qaoa"]
noise_models = ["depolarizing", "amplitude_damping", "coherent_overrotation", "pauli_lindblad", "time_correlated", "non_markovian"]
shots = 5000
seeds = [42, 123, 456]

print("=" * 70)
print("Experiment 12: Circuit-Family × Noise-Model Benchmark")
print("=" * 70)
print("\nAll results are synthetic response models. No hardware claims.\n")

results = []
for family in families:
    for nm in noise_models:
        errors = []
        for seed in seeds:
            r = run_benchmark_suite(family, noise_model=nm, shots_total=shots, seed=seed)
            errors.append(r["chebyshev_error"])
            results.append(r)
        avg = np.mean(errors)
        print(f"  {family:12s} + {nm:22s}: cheb_err={avg:.4f}")

# Summary figure: family × noise heatmap
os.makedirs("figures", exist_ok=True)
grid = np.zeros((len(families), len(noise_models)))
for i, f in enumerate(families):
    for j, nm in enumerate(noise_models):
        subset = [r["chebyshev_error"] for r in results if r["family"] == f and r["noise_model"] == nm]
        grid[i, j] = np.mean(subset)

fig, ax = plt.subplots(figsize=(9, 4))
im = ax.imshow(grid, aspect="auto", cmap="YlOrRd")
ax.set_xticks(range(len(noise_models)))
ax.set_xticklabels([nm[:8] for nm in noise_models], rotation=45, ha="right")
ax.set_yticks(range(len(families)))
ax.set_yticklabels([f.upper() for f in families])
ax.set_title("Mean |error| by family × noise model (Chebyshev-Tikhonov, synthetic)")
fig.colorbar(im, ax=ax, label="Mean absolute error")
plt.tight_layout()
plt.savefig("figures/circuit_family_noise_benchmark_summary.pdf", bbox_inches="tight")
plt.savefig("figures/circuit_family_noise_benchmark_summary.png", dpi=150, bbox_inches="tight")
plt.close()

# Also save the simpler family-only figure
fig, ax = plt.subplots(figsize=(8, 4))
x = np.arange(len(families))
width = 0.25
raw_avgs = [np.mean([r["raw_error"] for r in results if r["family"] == f]) for f in families]
bnd_avgs = [np.mean([r["bounded_error"] for r in results if r["family"] == f]) for f in families]
chb_avgs = [np.mean([r["chebyshev_error"] for r in results if r["family"] == f]) for f in families]
ax.bar(x - width, raw_avgs, width, label="Raw")
ax.bar(x, bnd_avgs, width, label="Bounded poly")
ax.bar(x + width, chb_avgs, width, label="Chebyshev-Tikhonov")
ax.set_xlabel("Circuit family")
ax.set_ylabel("Mean absolute error")
ax.set_title("ZNE benchmark across circuit families (synthetic, all noise models)")
ax.set_xticks(x)
ax.set_xticklabels([f.upper() for f in families])
ax.legend()
plt.tight_layout()
plt.savefig("figures/circuit_family_benchmark_summary.pdf", bbox_inches="tight")
plt.savefig("figures/circuit_family_benchmark_summary.png", dpi=150, bbox_inches="tight")
plt.close()

# Save results
os.makedirs("results", exist_ok=True)
lines = ["# Circuit-Family × Noise-Model Benchmark Results", "",
         "## Setup", "",
         f"- Families: {', '.join(f.upper() for f in families)}",
         f"- Noise models: {', '.join(noise_models)}",
         f"- Shots: {shots}, Seeds: {seeds}",
         "- Methods: raw, bounded polynomial deg-2, Chebyshev-Tikhonov deg-2",
         "- **All results are synthetic response models.**", "",
         "## Results (Chebyshev-Tikhonov mean |error|)", "",
         "| Family | " + " | ".join(nm[:8] for nm in noise_models) + " |",
         "|--------" + "|--------" * len(noise_models) + "|"]
for i, f in enumerate(families):
    row = " | ".join(f"{grid[i,j]:.4f}" for j in range(len(noise_models)))
    lines.append(f"| {f.upper()} | {row} |")
lines += ["", "## Interpretation", "",
          "Different noise models produce different error profiles for the same circuit family.",
          "Non-Markovian and coherent noise tend to be harder for polynomial extrapolation.",
          "This does not prove any method is universally best across all noise/family combinations.",
          "Results are synthetic and do not generalize to hardware."]

with open("results/circuit_family_benchmarks.md", "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"\nTotal benchmark combinations: {len(families)} × {len(noise_models)} × {len(seeds)} = {len(results)}")
print("Saved: results/circuit_family_benchmarks.md")
print("Saved: figures/circuit_family_noise_benchmark_summary.pdf")
