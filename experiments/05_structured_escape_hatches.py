"""Experiment 05: Structured escape hatches — adversarial vs structured responses.

Demonstrates that without physical constraints, different response functions
can agree at observed noise levels but disagree at zero noise (non-identifiability).
With constraints, the ambiguity is reduced.
"""

import numpy as np
from qem_inverse_theory.benchmarks import adversarial_response_with_same_observed_nodes
from qem_inverse_theory.theory.identifiability import ambiguity_diameter

scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

print("=" * 60)
print("Experiment 05: Structured Escape Hatches")
print("=" * 60)

# Adversarial example
vals_a, vals_b, f0_a, f0_b = adversarial_response_with_same_observed_nodes(
    scales, f0_a=0.9, f0_b=0.4, decay_a=0.15, decay_b=0.6
)

print(f"\nTwo response functions agreeing at observed scales:")
print(f"  Response A at nodes: {vals_a.round(4)}")
print(f"  Response B at nodes: {vals_b.round(4)}")
print(f"  Max |A - B| at nodes: {np.max(np.abs(vals_a - vals_b)):.6f}")
print(f"\n  True f(0) for A: {f0_a:.4f}")
print(f"  True f(0) for B: {f0_b:.4f}")
print(f"  Disagreement at zero: {abs(f0_a - f0_b):.4f}")
print()
print("→ Without constraints, the data cannot distinguish A from B.")
print("  This is the identifiability problem.")

# Ambiguity diameter with and without bounds
print("\n--- Ambiguity diameter analysis ---")
for degree in [2, 3, 4]:
    # Without bounds (wide)
    diam_wide = ambiguity_diameter(scales, vals_a, bounds=(-10.0, 10.0), degree=degree)
    # With Pauli bounds
    diam_pauli = ambiguity_diameter(scales, vals_a, bounds=(-1.0, 1.0), degree=degree)
    print(f"  Degree {degree}: diameter (no bounds) = {diam_wide:.4f}, "
          f"diameter (Pauli bounds) = {diam_pauli:.4f}")

print()
print("→ Physical bounds reduce the ambiguity set.")
print("  Structured constraints are the 'escape hatch' from non-identifiability.")
