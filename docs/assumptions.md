# Assumptions

## Current working assumptions

1. **Bounded observables**: The true expectation value lies in [λ_min(O), λ_max(O)].
2. **Known scale factors**: Noise amplification factors λ_i are exact (no calibration error).
3. **Independent shot noise**: Each measurement y_i = f(λ_i) + ε_i with ε_i ~ N(0, σ_i²).
4. **Pauli variance**: σ_i² ≈ (1 - f(λ_i)²) / N_shots for Pauli observables.
5. **Smoothness**: The noise response f(λ) is smooth (at least C¹) on [0, λ_max].
6. **Monotonicity** (optional): For depolarizing-like noise, f(λ) interpolates between f(0) and the maximally mixed value.

## Assumptions to relax (future work)

- Calibration uncertainty in scale factors
- Correlated shot noise (e.g., from simultaneous Pauli measurements)
- Non-Gaussian noise (heavy tails from readout errors)
- Unknown spectral bounds (estimated from data)
- Non-smooth response (phase transitions in noise)
