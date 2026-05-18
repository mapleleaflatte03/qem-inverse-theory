"""Experiment 01: Constrained vs unconstrained polynomial ZNE.

Demonstrates that physical bounds prevent unphysical extrapolation
while constrained optimization (not clipping) maintains accuracy.
"""

import numpy as np
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators import fit_polynomial_zne, fit_bounded_polynomial_zne
from qem_inverse_theory.benchmarks import exponential_decay_response, add_gaussian_shot_noise

rng = np.random.default_rng(42)
scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
f0_true = 0.95  # close to bound → unconstrained may exceed 1.0

# Generate noisy data
clean = exponential_decay_response(scales, f0=f0_true, decay_rate=0.1)
noisy = add_gaussian_shot_noise(clean, shots=100, rng=rng)
data = ZNEData(scales=scales, estimates=noisy)

print("=" * 60)
print("Experiment 01: Constrained vs Unconstrained Polynomial ZNE")
print("=" * 60)
print(f"\nTrue f(0) = {f0_true}")
print(f"Physical bounds: [-1, 1]")
print(f"Scales: {scales}")
print(f"Noisy observations: {noisy.round(4)}")
print()

for degree in [1, 2, 3, 4]:
    unc = fit_polynomial_zne(data, degree)
    con = fit_bounded_polynomial_zne(data, degree, bounds=(-1.0, 1.0))
    flag = " *** UNPHYSICAL" if abs(unc.estimate) > 1.0 else ""
    print(f"Degree {degree}:")
    print(f"  Unconstrained: f(0) = {unc.estimate:.4f}{flag}")
    print(f"  Constrained:   f(0) = {con.estimate:.4f}")
    print(f"  |Error| unconstrained: {abs(unc.estimate - f0_true):.4f}")
    print(f"  |Error| constrained:   {abs(con.estimate - f0_true):.4f}")
    print()
