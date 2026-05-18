"""Experiment 07: Bias–ambiguity tradeoff for fixed-degree polynomial ZNE.

Quantifies the fundamental tension: lower degree reduces ambiguity but
increases misspecification bias; higher degree reduces bias but increases
ambiguity.
"""

import numpy as np
import os
from qem_inverse_theory.benchmarks import exponential_decay_response
from qem_inverse_theory.theory.identifiability import ambiguity_diameter
from qem_inverse_theory.estimators.unconstrained import predict_zero_noise_poly

f0_true = 0.8
decay_rate = 0.25
tol = 0.01

constraint_sets = {
    "No bounds [-10,10]": (-10.0, 10.0),
    "Pauli [-1,1]": (-1.0, 1.0),
    "Probability [0,1]": (0.0, 1.0),
}

n_values = [5, 7]

print("=" * 70)
print("Experiment 07: Bias–Ambiguity Tradeoff")
print("=" * 70)
print(f"\nResponse: f(λ) = {f0_true} · exp(-{decay_rate}·λ), true f(0) = {f0_true}")
print(f"Tolerance δ = {tol}")
print()

all_results = {}

for n in n_values:
    scales = np.linspace(1.0, float(n), n)
    values = exponential_decay_response(scales, f0=f0_true, decay_rate=decay_rate)
    degrees = list(range(1, n))

    print(f"--- n = {n}, scales = {[round(float(s), 1) for s in scales]} ---")
    print(f"{'d':<4} | {'|Bias|':<8} | {'Ambig (unbnd)':<14} | {'Ambig (Pauli)':<14} | {'Ambig (prob)':<14}")
    print("-" * 62)

    results = []
    for deg in degrees:
        # Bias: least-squares polynomial fit evaluated at 0
        estimate = predict_zero_noise_poly(scales, values, deg)
        bias = abs(estimate - f0_true)

        # Ambiguity diameters
        diam_unbnd = ambiguity_diameter(scales, values, (-10.0, 10.0), deg, tol=tol)
        diam_pauli = ambiguity_diameter(scales, values, (-1.0, 1.0), deg, tol=tol)
        diam_prob = ambiguity_diameter(scales, values, (0.0, 1.0), deg, tol=tol)

        row = {
            "degree": deg,
            "estimate": estimate,
            "bias": bias,
            "ambig_unbounded": diam_unbnd,
            "ambig_pauli": diam_pauli,
            "ambig_prob": diam_prob,
        }
        results.append(row)

        def fmt(v):
            return f"{v:.4f}" if np.isfinite(v) else "infeasible"

        print(f"  {deg:<2} | {bias:<8.4f} | {fmt(diam_unbnd):<14} | {fmt(diam_pauli):<14} | {fmt(diam_prob):<14}")

    all_results[n] = results
    print()

# Save
lines = []
lines.append("# Bias–Ambiguity Tradeoff")
lines.append("")
lines.append("## Setup")
lines.append("")
lines.append(f"- True response: f(λ) = {f0_true} · exp(-{decay_rate}·λ), f(0) = {f0_true}")
lines.append(f"- Tolerance δ = {tol}")
lines.append("- Bias = |polynomial_estimate(0) - true f(0)| (noiseless least-squares fit)")
lines.append("- Ambiguity = diameter of the set of f(0) values consistent with data + bounds")
lines.append("")

for n in n_values:
    lines.append(f"## Results (n = {n})")
    lines.append("")
    lines.append("| d | |Bias| | Ambiguity (unbounded) | Ambiguity (Pauli) | Ambiguity (prob) |")
    lines.append("|---|--------|----------------------|-------------------|------------------|")
    for row in all_results[n]:
        def fmt(v):
            return f"{v:.4f}" if np.isfinite(v) else "infeasible"
        lines.append(f"| {row['degree']} | {row['bias']:.4f} | {fmt(row['ambig_unbounded']):<20} | {fmt(row['ambig_pauli']):<17} | {fmt(row['ambig_prob']):<16} |")
    lines.append("")

lines.append("## Interpretation")
lines.append("")
lines.append("**The tradeoff:**")
lines.append("- Lower polynomial degree (d=1, 2) gives small ambiguity diameter but")
lines.append("  large misspecification bias, because a low-degree polynomial cannot")
lines.append("  faithfully represent the exponential response.")
lines.append("- Higher polynomial degree (d=n-2, n-1) gives small bias (better fit)")
lines.append("  but large ambiguity diameter, because the flexible model admits many")
lines.append("  consistent f(0) values.")
lines.append("")
lines.append("**Implication for ZNE practice:**")
lines.append("Identifiability (small ambiguity) alone does not guarantee accuracy.")
lines.append("A model that tightly identifies f(0) may identify the *wrong* value")
lines.append("if the function class is misspecified. Model selection is needed to")
lines.append("balance bias against ambiguity.")
lines.append("")
lines.append("**What this does NOT prove:**")
lines.append("- It does not prove AICc or any specific criterion optimally resolves this tradeoff.")
lines.append("- It does not account for shot noise (bias here is from model misspecification only).")
lines.append("- It does not generalize beyond this single exponential response.")
lines.append("- The 'optimal' degree depends on the unknown true response — this is the")
lines.append("  fundamental difficulty of model selection in ZNE.")

os.makedirs("results", exist_ok=True)
with open("results/bias_ambiguity_tradeoff.md", "w") as f:
    f.write("\n".join(lines) + "\n")
print("Saved: results/bias_ambiguity_tradeoff.md")
