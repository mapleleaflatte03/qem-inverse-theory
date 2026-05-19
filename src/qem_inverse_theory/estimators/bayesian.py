"""Bayesian ZNE via Gaussian process with bounded output transform.

Uses a latent GP g(λ) with f(λ) = midpoint + radius * tanh(g(λ)),
ensuring all estimates lie within physical bounds.
"""

import numpy as np
from scipy.linalg import cho_solve, cho_factor

from ..types import ZNEData, FitResult


def _rbf_kernel(x1, x2, length_scale=1.0, amplitude=1.0):
    sq_dist = np.subtract.outer(x1, x2) ** 2
    return amplitude**2 * np.exp(-0.5 * sq_dist / length_scale**2)


def _matern32_kernel(x1, x2, length_scale=1.0, amplitude=1.0):
    r = np.abs(np.subtract.outer(x1, x2)) / length_scale
    return amplitude**2 * (1.0 + np.sqrt(3.0) * r) * np.exp(-np.sqrt(3.0) * r)


def fit_bayesian_zne_gp(
    data: ZNEData,
    bounds: tuple[float, float] = (-1.0, 1.0),
    kernel: str = "rbf",
    bounded_transform: str = "tanh",
    length_scale: float | None = None,
    amplitude: float = 1.0,
    jitter: float = 1e-6,
) -> FitResult:
    """Bounded Bayesian ZNE using GP on latent space with tanh output transform.

    Model: f(λ) = midpoint + radius * tanh(g(λ)), where g ~ GP(0, K).
    This guarantees f(λ) ∈ (bounds[0], bounds[1]) for all λ.
    """
    lo, hi = bounds
    midpoint = (lo + hi) / 2.0
    radius = (hi - lo) / 2.0

    x = data.scales
    y = data.estimates
    n = data.n

    # Auto length scale: half the scale range
    if length_scale is None:
        length_scale = max(0.5, (x.max() - x.min()) / 2.0)

    # Transform observations to latent space: g = arctanh((y - mid) / radius)
    y_normalized = (y - midpoint) / radius
    clipped_count = int(np.sum(np.abs(y_normalized) >= 0.999))
    y_clipped = np.clip(y_normalized, -0.999, 0.999)  # avoid ±inf
    g_obs = np.arctanh(y_clipped)

    # Noise variance in latent space (delta method: dg/df = 1/(radius*(1-tanh²(g))))
    if data.variances is not None:
        # Jacobian: df/dg = radius * (1 - tanh²(g)) = radius * sech²(g)
        sech2 = 1.0 - np.tanh(g_obs)**2
        latent_var = data.variances / (radius * sech2)**2
    else:
        latent_var = np.full(n, 0.01)

    # Kernel
    kernel_fn = _rbf_kernel if kernel == "rbf" else _matern32_kernel

    K = kernel_fn(x, x, length_scale, amplitude) + np.diag(latent_var) + jitter * np.eye(n)
    k_star = kernel_fn(np.array([0.0]), x, length_scale, amplitude).flatten()
    k_ss = amplitude**2

    # GP posterior at λ=0
    L, low = cho_factor(K)
    alpha = cho_solve((L, low), g_obs)
    mu_g0 = float(np.dot(k_star, alpha))
    v = cho_solve((L, low), k_star)
    var_g0 = max(0.0, k_ss - np.dot(k_star, v))

    # Transform back: f(0) = midpoint + radius * tanh(mu_g0)
    mu_f0 = midpoint + radius * np.tanh(mu_g0)

    # Delta method for variance in f-space
    jac = radius * (1.0 - np.tanh(mu_g0)**2)
    var_f0 = jac**2 * var_g0

    # Credible intervals (in f-space, clipped to bounds)
    std_g = np.sqrt(var_g0)
    ci90 = (
        max(lo, midpoint + radius * np.tanh(mu_g0 - 1.645 * std_g)),
        min(hi, midpoint + radius * np.tanh(mu_g0 + 1.645 * std_g)),
    )
    ci95 = (
        max(lo, midpoint + radius * np.tanh(mu_g0 - 1.96 * std_g)),
        min(hi, midpoint + radius * np.tanh(mu_g0 + 1.96 * std_g)),
    )

    return FitResult(
        estimate=mu_f0,
        variance=var_f0,
        method="bayesian_gp_bounded",
        diagnostics={
            "posterior_mean_g0": mu_g0,
            "posterior_var_g0": var_g0,
            "posterior_mean_f0": mu_f0,
            "posterior_var_f0": var_f0,
            "ci90": ci90,
            "ci95": ci95,
            "length_scale": length_scale,
            "amplitude": amplitude,
            "kernel": kernel,
            "bounded_transform": bounded_transform,
            "clipped_observation_count": clipped_count,
            "latent_noise_variance_min": float(latent_var.min()),
            "latent_noise_variance_max": float(latent_var.max()),
        },
        assumptions=[
            f"GP on latent g(λ) with {kernel} kernel",
            f"f(λ) = {midpoint} + {radius}·tanh(g(λ))",
            f"bounds: [{lo}, {hi}]",
            "Delta-method variance propagation",
            "Hyperparameters not optimized",
        ],
    )
