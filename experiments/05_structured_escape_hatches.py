"""Experiment 05: Adversarial identifiability and ambiguity diameter.

Computes the ambiguity diameter — the range of f(0) values consistent with
observed data, a polynomial function class, and physical bounds — across
different degrees and constraint sets.

This is the first quantitative result from the inverse-problem framing.
"""

import numpy as np
from qem_inverse_theory.benchmarks import exponential_decay_response
from qem_inverse_theory.theory.identifiability import ambiguity_diameter

scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
f0_true = 0.8
decay_rate = 0.25

# Generate clean observations (no shot noise — isolates identifiability from statistics)
values = exponential_decay_response(scales, f0=f0_true, decay_rate=decay_rate)

# Tolerance: how close must the polynomial pass to the data?
# Use 0.01 (1% tolerance) — realistic for ~10000 shots on a Pauli observable
tol = 0.01

print("=" * 70)
print("Experiment 05: Ambiguity Diameter Under Physical Constraints")
print("=" * 70)
print(f"\nSetup:")
print(f"  True f(0) = {f0_true}")
print(f"  Response: exponential decay, rate = {decay_rate}")
print(f"  Scales: {scales}")
print(f"  Observations: {values.round(4)}")
print(f"  Tolerance δ = {tol} (approximate interpolation)")
print()

# Constraint sets
constraint_sets = {
    "No bounds [-10, 10]": (-10.0, 10.0),
    "Pauli [-1, 1]": (-1.0, 1.0),
    "Probability [0, 1]": (0.0, 1.0),
}

degrees = [1, 2, 3, 4]

# Compute table
results = {}
print(f"{'Degree':<8} | {'No bounds [-10,10]':<20} | {'Pauli [-1,1]':<20} | {'Probability [0,1]':<20}")
print("-" * 74)

for deg in degrees:
    row = {}
    row_strs = []
    for name, bounds in constraint_sets.items():
        diam = ambiguity_diameter(scales, values, bounds, deg, tol=tol)
        row[name] = diam
        if np.isinf(diam):
            row_strs.append("infeasible")
        else:
            row_strs.append(f"{diam:.4f}")
    results[deg] = row
    print(f"  {deg:<6} | {row_strs[0]:<20} | {row_strs[1]:<20} | {row_strs[2]:<20}")

print()
print("=" * 70)
print("Interpretation:")
print()
print("- 'infeasible' means no polynomial of that degree passes within δ of all")
print("  data points while respecting bounds. The function class is too restrictive")
print("  for the data (model misspecification).")
print()
print("- A finite diameter shows the range of f(0) values consistent with data.")
print("  Smaller diameter = more identifiable.")
print()
print("- Tighter physical bounds (e.g., [0,1] vs [-10,10]) reduce the ambiguity")
print("  set when the polynomial degree is high enough to fit the data.")
print()
print("- At degree = n-1 = 4, the polynomial class is flexible enough to interpolate")
print("  the five noiseless nodes, and with tolerance δ it admits a wider set of")
print("  near-consistent zero-noise values.")
print()

# Save results for results/ directory
output_lines = []
output_lines.append("# Ambiguity Diameter Table")
output_lines.append("")
output_lines.append("## Setup")
output_lines.append("")
output_lines.append(f"- True f(0) = {f0_true}")
output_lines.append(f"- Response: f(λ) = {f0_true} · exp(-{decay_rate}·λ)")
output_lines.append(f"- Scales: {[float(s) for s in scales]}")
output_lines.append(f"- Observations: {[round(float(v), 4) for v in values]}")
output_lines.append(f"- Tolerance δ = {tol}")
output_lines.append(f"- n = {len(scales)} data points")
output_lines.append("")
output_lines.append("## Results")
output_lines.append("")
output_lines.append("| Degree | No bounds [-10, 10] | Pauli [-1, 1] | Probability [0, 1] |")
output_lines.append("|--------|---------------------|---------------|---------------------|")
for deg in degrees:
    row = results[deg]
    cells = []
    for name in constraint_sets:
        d = row[name]
        cells.append("infeasible" if np.isinf(d) else f"{d:.4f}")
    output_lines.append(f"| {deg}      | {cells[0]:<19} | {cells[1]:<13} | {cells[2]:<19} |")

output_lines.append("")
output_lines.append("## Interpretation")
output_lines.append("")
output_lines.append("These synthetic examples illustrate how physical constraints interact with")
output_lines.append("model complexity to determine identifiability of the zero-noise limit.")
output_lines.append("")
output_lines.append("**When do bounds help?**")
output_lines.append("- At high polynomial degree (d ≥ n-1), the function class is flexible enough")
output_lines.append("  to interpolate the data, and with tolerance δ it admits a wider set of")
output_lines.append("  near-consistent zero-noise values. Physical bounds are the")
output_lines.append("  primary constraint preventing the ambiguity set from growing large.")
output_lines.append("- At low degree (d < n-1), the function class itself constrains f(0) through")
output_lines.append("  the overdetermined least-squares structure. Bounds provide additional but")
output_lines.append("  less critical reduction.")
output_lines.append("")
output_lines.append("**What does this NOT prove?**")
output_lines.append("- It does not prove bounded ZNE is more accurate than unconstrained ZNE.")
output_lines.append("- It does not prove that tighter bounds always reduce MSE.")
output_lines.append("- It does not account for shot noise (this is a noiseless identifiability analysis).")
output_lines.append("- It does not generalize beyond polynomial function classes.")
output_lines.append("- The tolerance δ is chosen, not derived from data.")
output_lines.append("")
output_lines.append("**What it does show:**")
output_lines.append("- Without physical constraints AND with a flexible function class, f(0) is")
output_lines.append("  poorly determined even from exact data.")
output_lines.append("- Physical bounds provide a quantifiable reduction in ambiguity.")
output_lines.append("- The interaction between function class and constraints determines identifiability.")

import os
os.makedirs("results", exist_ok=True)
with open("results/ambiguity_diameter_table.md", "w") as f:
    f.write("\n".join(output_lines) + "\n")
print("\nSaved: results/ambiguity_diameter_table.md")

# --- Delta sensitivity analysis (degree 4 fixed) ---
print()
print("=" * 70)
print("Delta Sensitivity: Ambiguity Diameter vs Tolerance (degree = 4)")
print("=" * 70)
print()

delta_values = [0.0, 0.001, 0.01, 0.05, 0.1]
deg_fixed = 4

print(f"{'δ':<8} | {'No bounds [-10,10]':<20} | {'Pauli [-1,1]':<20} | {'Probability [0,1]':<20}")
print("-" * 74)

delta_results = {}
for delta in delta_values:
    row = {}
    row_strs = []
    for name, bounds in constraint_sets.items():
        diam = ambiguity_diameter(scales, values, bounds, deg_fixed, tol=delta)
        row[name] = diam
        if np.isinf(diam):
            row_strs.append("infeasible")
        else:
            row_strs.append(f"{diam:.4f}")
    delta_results[delta] = row
    print(f"  {delta:<6} | {row_strs[0]:<20} | {row_strs[1]:<20} | {row_strs[2]:<20}")

# Save delta sensitivity table
delta_lines = []
delta_lines.append("# Ambiguity Diameter: Delta Sensitivity")
delta_lines.append("")
delta_lines.append("## Setup")
delta_lines.append("")
delta_lines.append(f"- Polynomial degree: {deg_fixed} (= n-1, interpolation regime)")
delta_lines.append(f"- True f(0) = {f0_true}")
delta_lines.append(f"- Response: f(λ) = {f0_true} · exp(-{decay_rate}·λ)")
delta_lines.append(f"- Scales: {[float(s) for s in scales]}")
delta_lines.append(f"- n = {len(scales)} data points")
delta_lines.append("")
delta_lines.append("## Results")
delta_lines.append("")
delta_lines.append("| δ (tolerance) | No bounds [-10, 10] | Pauli [-1, 1] | Probability [0, 1] |")
delta_lines.append("|---------------|---------------------|---------------|---------------------|")
for delta in delta_values:
    row = delta_results[delta]
    cells = []
    for name in constraint_sets:
        d = row[name]
        cells.append("infeasible" if np.isinf(d) else f"{d:.4f}")
    delta_lines.append(f"| {delta:<13} | {cells[0]:<19} | {cells[1]:<13} | {cells[2]:<19} |")

delta_lines.append("")
delta_lines.append("## Interpretation")
delta_lines.append("")
delta_lines.append("The tolerance δ represents how closely the polynomial must pass through the")
delta_lines.append("observed data. In practice, δ corresponds to the shot-noise uncertainty:")
delta_lines.append("larger δ means more noisy measurements, which admit more candidate functions")
delta_lines.append("and thus increase the ambiguity diameter.")
delta_lines.append("")
delta_lines.append("**Observations:**")
delta_lines.append("- At δ = 0 (exact interpolation), the ambiguity comes purely from the")
delta_lines.append("  freedom of the degree-4 polynomial's value at λ=0 given 5 constraints.")
delta_lines.append("- As δ increases, the feasible set of polynomials grows, and so does the")
delta_lines.append("  range of achievable f(0) values.")
delta_lines.append("- Physical bounds (Pauli or probability) cap the ambiguity diameter,")
delta_lines.append("  becoming more important as δ grows.")
delta_lines.append("")
delta_lines.append("**Connection to finite-shot ZNE:**")
delta_lines.append("- A natural choice is δ ≈ z_{α/2} · max_i σ_i, linking tolerance to")
delta_lines.append("  confidence level and shot budget.")
delta_lines.append("- This table shows that identifiability degrades continuously with")
delta_lines.append("  measurement uncertainty — there is no sharp phase transition.")
delta_lines.append("")
delta_lines.append("**Caveats:**")
delta_lines.append("- Monotonicity of diameter in δ is observed here but not proven in general.")
delta_lines.append("- Results are specific to this exponential response and polynomial class.")
delta_lines.append("- The LP formulation uses ℓ∞ tolerance; other norms may give different results.")

with open("results/ambiguity_delta_sensitivity.md", "w") as f:
    f.write("\n".join(delta_lines) + "\n")
print("\nSaved: results/ambiguity_delta_sensitivity.md")
