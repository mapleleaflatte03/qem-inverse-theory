"""Experiment 09: Bayesian ZNE coverage calibration.

Evaluates whether the 90% and 95% credible intervals from the bounded
Bayesian GP estimator achieve nominal coverage across repeated trials.
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators.bayesian import fit_bayesian_zne_gp
from qem_inverse_theory.benchmarks.shot_noise import add_gaussian_shot_noise

scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
n_trials = 200
rng = np.random.default_rng(42)

responses = {
    "exponential": (lambda s, a: 0.8 * np.exp(-a * s), 0.8),
    "quadratic": (lambda s, a: 0.8 - a * s + 0.3 * a**2 * s**2, 0.8),
    "mild_decay": (lambda s, a: 0.9 * np.exp(-a * s * 0.5), 0.9),
}

shots_values = [200, 1000, 5000]
noise_strengths = [0.1, 0.25]

print("=" * 70)
print("Experiment 09: Bayesian ZNE Coverage Calibration")
print("=" * 70)

all_results = []

for resp_name, (resp_fn, f0_true) in responses.items():
    for noise in noise_strengths:
        for shots in shots_values:
            clean = resp_fn(scales, noise)
            cover90, cover95 = 0, 0
            widths_95 = []
            for _ in range(n_trials):
                noisy = add_gaussian_shot_noise(clean, shots=shots, rng=rng)
                variances = np.maximum(1.0 - noisy**2, 0.01) / shots
                data = ZNEData(scales=scales, estimates=noisy, variances=variances)
                result = fit_bayesian_zne_gp(data, bounds=(-1, 1))
                ci90 = result.diagnostics["ci90"]
                ci95 = result.diagnostics["ci95"]
                if ci90[0] <= f0_true <= ci90[1]:
                    cover90 += 1
                if ci95[0] <= f0_true <= ci95[1]:
                    cover95 += 1
                widths_95.append(ci95[1] - ci95[0])

            emp90 = cover90 / n_trials
            emp95 = cover95 / n_trials
            avg_width = np.mean(widths_95)
            all_results.append({
                "response": resp_name, "noise": noise, "shots": shots,
                "coverage_90": emp90, "coverage_95": emp95, "avg_width_95": avg_width,
            })
            print(f"  {resp_name:12s} noise={noise:.2f} shots={shots:5d}: "
                  f"90%={emp90:.2%} 95%={emp95:.2%} width={avg_width:.3f}")

# Summary figure: coverage vs nominal
os.makedirs("figures", exist_ok=True)
emp90s = [r["coverage_90"] for r in all_results]
emp95s = [r["coverage_95"] for r in all_results]

fig, ax = plt.subplots(figsize=(5, 5))
ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Perfect calibration")
ax.scatter([0.9] * len(emp90s), emp90s, alpha=0.5, label="90% CI", marker="o")
ax.scatter([0.95] * len(emp95s), emp95s, alpha=0.5, label="95% CI", marker="s")
ax.set_xlabel("Nominal coverage")
ax.set_ylabel("Empirical coverage")
ax.set_title("Bayesian ZNE Coverage Calibration")
ax.legend()
ax.set_xlim(0.8, 1.0)
ax.set_ylim(0.0, 1.1)
plt.tight_layout()
plt.savefig("figures/bayesian_coverage.pdf", bbox_inches="tight")
plt.savefig("figures/bayesian_coverage.png", dpi=150, bbox_inches="tight")
plt.close()

# Save results
os.makedirs("results", exist_ok=True)
lines = ["# Bayesian ZNE Coverage Calibration", "",
         "## Setup", "",
         f"- Scales: {list(scales)}",
         f"- Trials: {n_trials}",
         f"- Shots: {shots_values}",
         f"- Noise strengths: {noise_strengths}",
         "- Responses: exponential, quadratic, mild_decay",
         "- Estimator: bounded GP with tanh transform, RBF kernel", "",
         "## Results", "",
         "| Response | Noise | Shots | 90% coverage | 95% coverage | Avg width |",
         "|----------|-------|-------|--------------|--------------|-----------|"]
for r in all_results:
    lines.append(f"| {r['response']:12s} | {r['noise']:.2f}  | {r['shots']:5d} | "
                 f"{r['coverage_90']:.2%}       | {r['coverage_95']:.2%}       | {r['avg_width_95']:.3f}     |")
lines += ["", "## Interpretation", "",
          "Coverage below nominal indicates the intervals are too narrow (overconfident).",
          "Coverage above nominal indicates the intervals are too wide (conservative).",
          "Neither case proves the estimator is good or bad — only that calibration",
          "depends on the response function, noise level, and shot budget.",
          "",
          "Hyperparameters are not optimized. Improved calibration may be achievable",
          "with marginal likelihood optimization or cross-validation.",
          "These results are synthetic and do not generalize to hardware."]

with open("results/bayesian_coverage.md", "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nSaved: results/bayesian_coverage.md")
print("Saved: figures/bayesian_coverage.pdf")
