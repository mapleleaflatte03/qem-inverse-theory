"""Generate all paper figures for qem-inverse-theory."""

import numpy as np
import matplotlib.pyplot as plt
import os

from qem_inverse_theory.benchmarks import exponential_decay_response
from qem_inverse_theory.theory.identifiability import ambiguity_diameter
from qem_inverse_theory.estimators.unconstrained import predict_zero_noise_poly

os.makedirs("figures", exist_ok=True)

f0_true = 0.8
decay_rate = 0.25

# --- Figure 1: Ambiguity vs degree ---
scales = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
values = exponential_decay_response(scales, f0=f0_true, decay_rate=decay_rate)
degrees = [2, 3, 4]
diams_unbnd = [ambiguity_diameter(scales, values, (-10, 10), d, tol=0.01) for d in degrees]
diams_pauli = [ambiguity_diameter(scales, values, (-1, 1), d, tol=0.01) for d in degrees]
diams_prob = [ambiguity_diameter(scales, values, (0, 1), d, tol=0.01) for d in degrees]

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(degrees, diams_unbnd, "o-", label="No bounds [-10, 10]")
ax.plot(degrees, diams_pauli, "s-", label="Pauli [-1, 1]")
ax.plot(degrees, diams_prob, "^-", label="Probability [0, 1]")
ax.set_xlabel("Polynomial degree $d$")
ax.set_ylabel("Ambiguity diameter")
ax.set_title("Ambiguity diameter vs model complexity ($n=5$, $\\delta=0.01$)")
ax.legend()
ax.set_xticks(degrees)
plt.tight_layout()
plt.savefig("figures/ambiguity_degree_sweep.pdf", bbox_inches="tight")
plt.savefig("figures/ambiguity_degree_sweep.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Figure 2: Delta sensitivity ---
deltas = [0.001, 0.01, 0.05, 0.1]
d_fixed = 4
diams_d_unbnd = [ambiguity_diameter(scales, values, (-10, 10), d_fixed, tol=d) for d in deltas]
diams_d_pauli = [ambiguity_diameter(scales, values, (-1, 1), d_fixed, tol=d) for d in deltas]
diams_d_prob = [ambiguity_diameter(scales, values, (0, 1), d_fixed, tol=d) for d in deltas]

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(deltas, diams_d_unbnd, "o-", label="No bounds [-10, 10]")
ax.plot(deltas, diams_d_pauli, "s-", label="Pauli [-1, 1]")
ax.plot(deltas, diams_d_prob, "^-", label="Probability [0, 1]")
ax.set_xlabel("Tolerance $\\delta$")
ax.set_ylabel("Ambiguity diameter")
ax.set_title("Ambiguity vs measurement uncertainty ($d=4$, $n=5$)")
ax.legend()
ax.set_xscale("log")
plt.tight_layout()
plt.savefig("figures/delta_sensitivity.pdf", bbox_inches="tight")
plt.savefig("figures/delta_sensitivity.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Figure 3: n sensitivity (interpolation vs fixed) ---
n_vals = [3, 4, 5, 6, 7]
# Interpolation regime
interp_unbnd = []
fixed2_unbnd = []
for n in n_vals:
    sc = np.linspace(1.0, float(n), n)
    v = exponential_decay_response(sc, f0=f0_true, decay_rate=decay_rate)
    interp_unbnd.append(ambiguity_diameter(sc, v, (-10, 10), n - 1, tol=0.01))
    if n > 2:
        fixed2_unbnd.append(ambiguity_diameter(sc, v, (-10, 10), 2, tol=0.01))
    else:
        fixed2_unbnd.append(np.nan)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(n_vals, interp_unbnd, "o-", label="$d = n-1$ (interpolation)")
ax.plot(n_vals, fixed2_unbnd, "s-", label="$d = 2$ (fixed)")
ax.set_xlabel("Number of scale factors $n$")
ax.set_ylabel("Ambiguity diameter (unbounded)")
ax.set_title("n-sensitivity: interpolation vs fixed degree ($\\delta=0.01$)")
ax.legend()
ax.set_yscale("log")
plt.tight_layout()
plt.savefig("figures/n_sensitivity_interpolation_vs_fixed.pdf", bbox_inches="tight")
plt.savefig("figures/n_sensitivity_interpolation_vs_fixed.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Figure 4: Bias-ambiguity tradeoff ---
n = 7
scales7 = np.linspace(1.0, 7.0, 7)
values7 = exponential_decay_response(scales7, f0=f0_true, decay_rate=decay_rate)
degs = list(range(2, 7))
biases = [abs(predict_zero_noise_poly(scales7, values7, d) - f0_true) for d in degs]
ambigs = [ambiguity_diameter(scales7, values7, (0, 1), d, tol=0.01) for d in degs]

fig, ax1 = plt.subplots(figsize=(6, 4))
color1 = "tab:blue"
ax1.set_xlabel("Polynomial degree $d$")
ax1.set_ylabel("|Bias|", color=color1)
ax1.plot(degs, biases, "o-", color=color1, label="|Bias|")
ax1.tick_params(axis="y", labelcolor=color1)
ax1.set_yscale("log")

ax2 = ax1.twinx()
color2 = "tab:red"
ax2.set_ylabel("Ambiguity diameter", color=color2)
ax2.plot(degs, ambigs, "s-", color=color2, label="Ambiguity")
ax2.tick_params(axis="y", labelcolor=color2)
ax2.set_yscale("log")

ax1.set_title("Bias–ambiguity tradeoff ($n=7$, $\\delta=0.01$, bounds $[0,1]$)")
fig.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, 0.88))
plt.tight_layout()
plt.savefig("figures/bias_ambiguity_tradeoff.pdf", bbox_inches="tight")
plt.savefig("figures/bias_ambiguity_tradeoff.png", dpi=150, bbox_inches="tight")
plt.close()

print("Generated figures:")
for f in sorted(os.listdir("figures")):
    print(f"  figures/{f}")
