"""Experiment 06: Ambiguity diameter vs number of scale factors n.

Studies how adding more measurement points affects identifiability
in the interpolation regime (degree = n-1).
"""

import numpy as np
import os
from qem_inverse_theory.benchmarks import exponential_decay_response
from qem_inverse_theory.theory.identifiability import ambiguity_diameter

f0_true = 0.8
decay_rate = 0.25

constraint_sets = {
    "No bounds [-10,10]": (-10.0, 10.0),
    "Pauli [-1,1]": (-1.0, 1.0),
    "Probability [0,1]": (0.0, 1.0),
}

n_values = [3, 4, 5, 6, 7]
delta_values = [0.01, 0.05]

print("=" * 70)
print("Experiment 06: Ambiguity Diameter vs Number of Scale Factors")
print("=" * 70)
print(f"\nResponse: f(λ) = {f0_true} · exp(-{decay_rate}·λ)")
print(f"Degree: d = n-1 (interpolation regime)")
print(f"Scales: evenly spaced from 1 to n")
print()

all_results = {}

for delta in delta_values:
    print(f"--- δ = {delta} ---")
    print(f"{'n':<4} | {'No bounds [-10,10]':<20} | {'Pauli [-1,1]':<20} | {'Probability [0,1]':<20}")
    print("-" * 70)

    results = {}
    for n in n_values:
        scales = np.linspace(1.0, float(n), n)
        values = exponential_decay_response(scales, f0=f0_true, decay_rate=decay_rate)
        degree = n - 1

        row = {}
        row_strs = []
        for name, bounds in constraint_sets.items():
            diam = ambiguity_diameter(scales, values, bounds, degree, tol=delta)
            row[name] = diam
            row_strs.append(f"{diam:.4f}" if np.isfinite(diam) else "infeasible")
        results[n] = row
        print(f"  {n:<2} | {row_strs[0]:<20} | {row_strs[1]:<20} | {row_strs[2]:<20}")

    all_results[delta] = results
    print()

# Save results
lines = []
lines.append("# Ambiguity Diameter: n-Sensitivity")
lines.append("")
lines.append("## Setup")
lines.append("")
lines.append(f"- Response: f(λ) = {f0_true} · exp(-{decay_rate}·λ), true f(0) = {f0_true}")
lines.append("- Polynomial degree: d = n-1 (interpolation regime)")
lines.append("- Scales: evenly spaced from 1 to n")
lines.append("")

for delta in delta_values:
    lines.append(f"## Results (δ = {delta})")
    lines.append("")
    lines.append("| n | No bounds [-10, 10] | Pauli [-1, 1] | Probability [0, 1] |")
    lines.append("|---|---------------------|---------------|---------------------|")
    for n in n_values:
        row = all_results[delta][n]
        cells = []
        for name in constraint_sets:
            d = row[name]
            cells.append(f"{d:.4f}" if np.isfinite(d) else "infeasible")
        lines.append(f"| {n} | {cells[0]:<19} | {cells[1]:<13} | {cells[2]:<19} |")
    lines.append("")

lines.append("## Interpretation")
lines.append("")
lines.append("**Does more data reduce ambiguity?**")
lines.append("In this synthetic setup, increasing n while keeping d = n-1 does NOT")
lines.append("reduce ambiguity, because the polynomial degree grows with n (maintaining")
lines.append("the interpolation regime). The system remains underdetermined at λ=0")
lines.append("regardless of how many points are added, since each new point comes with")
lines.append("a new free parameter.")
lines.append("")
lines.append("The pattern suggests that more data helps only if the model complexity is")
lines.append("held fixed (d < n-1), creating an overdetermined system. In the interpolation")
lines.append("regime, physical bounds remain the primary constraint on f(0).")
lines.append("")
lines.append("**When does physical bounding still matter?**")
lines.append("Physical bounds matter whenever the polynomial class is flexible enough to")
lines.append("accommodate the data with multiple f(0) values. In the d = n-1 regime,")
lines.append("this is always the case, so bounds are always relevant.")
lines.append("")
lines.append("**What does this NOT prove?**")
lines.append("- It does not prove that more data is useless (it would help if d were fixed).")
lines.append("- It does not prove anything about non-polynomial function classes.")
lines.append("- It does not account for shot noise or statistical estimation.")
lines.append("- The evenly-spaced scale factor choice may not be optimal.")
lines.append("- Results are specific to this single exponential response.")

os.makedirs("results", exist_ok=True)
with open("results/ambiguity_n_sensitivity.md", "w") as f:
    f.write("\n".join(lines) + "\n")
print("Saved: results/ambiguity_n_sensitivity.md")
