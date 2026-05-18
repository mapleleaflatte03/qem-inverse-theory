"""Experiment 02: AICc small-sample failure modes.

Shows how high-degree polynomials overfit with n≤7 data points,
and how AICc's finite-sample correction prevents this.
"""

import numpy as np
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators import fit_polynomial_zne, select_by_aicc
from qem_inverse_theory.estimators.model_selection import aicc, aic
from qem_inverse_theory.benchmarks import exponential_decay_response, add_gaussian_shot_noise

rng = np.random.default_rng(42)
scales = np.array([1.0, 1.5, 2.0, 2.5, 3.0])  # n=5
f0_true = 0.8

clean = exponential_decay_response(scales, f0=f0_true, decay_rate=0.3)
noisy = add_gaussian_shot_noise(clean, shots=200, rng=rng)
data = ZNEData(scales=scales, estimates=noisy)

print("=" * 60)
print("Experiment 02: AICc Small-Sample Failure Modes")
print("=" * 60)
print(f"\nn = {data.n} observations")
print(f"True f(0) = {f0_true}")
print()

print("Degree | f(0) estimate | AIC    | AICc   | Note")
print("-" * 60)
for deg in range(1, data.n):
    result = fit_polynomial_zne(data, deg)
    k = deg + 1
    rss_val = result.diagnostics["rss"]
    aic_val = aic(data.n, k, rss_val)
    aicc_val = aicc(data.n, k, rss_val)
    note = "INFINITE (n-k-1≤0)" if aicc_val == np.inf else ""
    print(f"  {deg}    | {result.estimate:+.4f}        | {aic_val:6.2f} | {aicc_val:6.2f} | {note}")

print()
best = select_by_aicc(data, max_degree=4, bounds=(-1.0, 1.0))
print(f"AICc-selected: degree {best.diagnostics['selected_degree']}, f(0) = {best.estimate:.4f}")
print(f"True f(0) = {f0_true}, |error| = {abs(best.estimate - f0_true):.4f}")
