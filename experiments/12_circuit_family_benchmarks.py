"""Experiment 12: Circuit-family benchmark suite.

Runs ZNE benchmarks across multiple circuit families and noise models.
All results are synthetic — no hardware claims.
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from qem_inverse_theory.benchmarks.suite import run_benchmark_suite

families = ["ghz", "tfim", "heisenberg", "vqe", "qaoa"]
shots_values = [1000, 10000]
seeds = [42, 123, 456]

print("=" * 70)
print("Experiment 12: Circuit-Family Benchmark Suite")
print("=" * 70)
print("\nAll results are synthetic circuit-family response models.")
print("No quantum hardware or circuit simulation is involved.\n")

results = []
for family in families:
    for shots in shots_values:
        errors_raw, errors_bounded, errors_cheb = [], [], []
        for seed in seeds:
            r = run_benchmark_suite(family, n_qubits=4, depth=4, shots_total=shots, seed=seed)
            errors_raw.append(r["raw_error"])
            errors_bounded.append(r["bounded_error"])
            errors_cheb.append(r["chebyshev_error"])
            results.append(r)

        avg_raw = np.mean(errors_raw)
        avg_bnd = np.mean(errors_bounded)
        avg_chb = np.mean(errors_cheb)
        print(f"  {family:12s} shots={shots:5d}: "
              f"raw={avg_raw:.4f}  bounded={avg_bnd:.4f}  chebyshev={avg_chb:.4f}")

# Summary figure
os.makedirs("figures", exist_ok=True)
fig, ax = plt.subplots(figsize=(8, 4))
x = np.arange(len(families))
width = 0.25

# Average over shots and seeds
raw_avgs = [np.mean([r["raw_error"] for r in results if r["family"] == f]) for f in families]
bnd_avgs = [np.mean([r["bounded_error"] for r in results if r["family"] == f]) for f in families]
chb_avgs = [np.mean([r["chebyshev_error"] for r in results if r["family"] == f]) for f in families]

ax.bar(x - width, raw_avgs, width, label="Raw")
ax.bar(x, bnd_avgs, width, label="Bounded poly")
ax.bar(x + width, chb_avgs, width, label="Chebyshev-Tikhonov")
ax.set_xlabel("Circuit family")
ax.set_ylabel("Mean absolute error")
ax.set_title("ZNE benchmark across circuit families (synthetic)")
ax.set_xticks(x)
ax.set_xticklabels([f.upper() for f in families])
ax.legend()
plt.tight_layout()
plt.savefig("figures/circuit_family_benchmark_summary.pdf", bbox_inches="tight")
plt.savefig("figures/circuit_family_benchmark_summary.png", dpi=150, bbox_inches="tight")
plt.close()

# Save results
os.makedirs("results", exist_ok=True)
lines = ["# Circuit-Family Benchmark Results", "",
         "## Setup", "",
         "- Families: GHZ, TFIM, Heisenberg, VQE, QAOA",
         "- n_qubits: 4, depth: 4, noise_strength: 0.04",
         f"- Shots: {shots_values}",
         f"- Seeds: {seeds}",
         "- Methods: raw, bounded polynomial deg-2, Chebyshev-Tikhonov deg-2",
         "- **All results are synthetic response models, not circuit simulations.**", "",
         "## Results (mean absolute error)", "",
         "| Family | Raw | Bounded | Chebyshev |",
         "|--------|-----|---------|-----------|"]
for f in families:
    r_raw = np.mean([r["raw_error"] for r in results if r["family"] == f])
    r_bnd = np.mean([r["bounded_error"] for r in results if r["family"] == f])
    r_chb = np.mean([r["chebyshev_error"] for r in results if r["family"] == f])
    lines.append(f"| {f.upper()} | {r_raw:.4f} | {r_bnd:.4f} | {r_chb:.4f} |")

lines += ["", "## Interpretation", "",
          "These synthetic benchmarks illustrate how different circuit-family response",
          "profiles interact with ZNE estimators. Results vary by family because each",
          "has different decay characteristics (fast/slow, oscillatory, saturating).",
          "",
          "**Caveats:**",
          "- These are synthetic response models, not actual circuit simulations.",
          "- Real circuits may behave differently under noise amplification.",
          "- No hardware validation is claimed.",
          "- Rankings may change with different noise models or shot budgets."]

with open("results/circuit_family_benchmarks.md", "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nSaved: results/circuit_family_benchmarks.md")
print("Saved: figures/circuit_family_benchmark_summary.pdf")
