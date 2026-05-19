"""Experiment 11: Locality-aware regularization proxy.

Compares standard Chebyshev-Tikhonov (fixed reg_lambda) vs locality-aware
(adaptive reg_lambda based on support size) across observables of different support.
"""

import numpy as np
import os
from qem_inverse_theory.types import ZNEData
from qem_inverse_theory.estimators.chebyshev import fit_chebyshev_tikhonov_zne
from qem_inverse_theory.estimators.locality_aware import fit_locality_aware_zne
from qem_inverse_theory.benchmarks.shot_noise import add_gaussian_shot_noise
from qem_inverse_theory.benchmarks.metrics import mse

scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
shots = 500
n_trials = 100
depth = 10
noise_strength = 0.05
rng = np.random.default_rng(42)

# Synthetic: higher support → faster decay (more noise sensitivity)
observables = {
    "ZIII": {"support": 1, "decay": 0.1, "f0": 0.9},
    "ZZII": {"support": 2, "decay": 0.2, "f0": 0.85},
    "ZZZZ": {"support": 4, "decay": 0.4, "f0": 0.75},
}

print("=" * 70)
print("Experiment 11: Locality-Aware Regularization Proxy")
print("=" * 70)
print(f"\nDepth={depth}, noise_strength={noise_strength}, shots={shots}, trials={n_trials}")
print()

results = []
for pauli, cfg in observables.items():
    f0 = cfg["f0"]
    decay = cfg["decay"]
    clean = f0 * np.exp(-decay * scales)

    std_estimates, loc_estimates = [], []
    for _ in range(n_trials):
        noisy = add_gaussian_shot_noise(clean, shots=shots, rng=rng)
        data = ZNEData(scales=scales, estimates=noisy)

        r_std = fit_chebyshev_tikhonov_zne(data, degree=2, bounds=(-1, 1), reg_lambda=1e-3)
        r_loc = fit_locality_aware_zne(data, pauli, depth, noise_strength, base_degree=2, bounds=(-1, 1))

        std_estimates.append(r_std.estimate)
        loc_estimates.append(r_loc.estimate)

    mse_std = mse(np.array(std_estimates), f0)
    mse_loc = mse(np.array(loc_estimates), f0)
    # Get diagnostics from last run
    r_loc_last = fit_locality_aware_zne(
        ZNEData(scales=scales, estimates=clean), pauli, depth, noise_strength
    )
    reg_used = r_loc_last.diagnostics["recommended_reg_lambda"]
    envelope = r_loc_last.diagnostics["envelope_proxy"]

    improvement = (1 - mse_loc / mse_std) * 100 if mse_std > 0 else 0
    results.append({
        "pauli": pauli, "support": cfg["support"], "mse_std": mse_std,
        "mse_loc": mse_loc, "reg_lambda": reg_used, "improvement": improvement,
        "envelope": envelope,
    })
    print(f"  {pauli}: support={cfg['support']}  MSE_std={mse_std:.5f}  MSE_loc={mse_loc:.5f}  "
          f"reg_λ={reg_used:.4f}  improvement={improvement:+.1f}%")

# Save
os.makedirs("results", exist_ok=True)
lines = ["# Locality-Aware Regularization Proxy", "",
         "## Setup", "",
         f"- Depth: {depth}, noise_strength: {noise_strength}",
         f"- Scales: {list(scales)}, shots: {shots}, trials: {n_trials}",
         "- Standard: Chebyshev-Tikhonov deg=2, reg_λ=0.001 (fixed)",
         "- Locality-aware: reg_λ adapted from support-size envelope proxy", "",
         "## Results", "",
         "| Observable | Support | MSE (standard) | MSE (locality) | reg_λ used | Improvement |",
         "|------------|---------|----------------|----------------|------------|-------------|"]
for r in results:
    lines.append(f"| {r['pauli']} | {r['support']} | {r['mse_std']:.5f} | {r['mse_loc']:.5f} | "
                 f"{r['reg_lambda']:.4f} | {r['improvement']:+.1f}% |")
lines += ["", "## Interpretation", "",
          "The locality-aware proxy adapts regularization strength based on observable",
          "support size: higher-support observables get stronger regularization because",
          "they are expected to have more extrapolation instability.",
          "",
          "**Caveats:**",
          "- This is a heuristic proxy, not a rigorous theorem.",
          "- The relationship between support size and noise sensitivity is synthetic.",
          "- Real quantum systems may not follow this simple scaling.",
          "- The envelope proxy is not derived from commutator bounds (future work).",
          "- Results are synthetic and do not generalize to hardware."]

with open("results/locality_aware_proxy.md", "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nSaved: results/locality_aware_proxy.md")
