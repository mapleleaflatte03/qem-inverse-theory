"""Bayesian ZNE via Gaussian process with bounded output transform.

Uses a latent GP g(λ) with f(λ) = midpoint + radius * tanh(g(λ)),
ensuring all estimates lie within physical bounds.
"""

import numpy as np
from scipy.linalg import cho_solve, cho_factor
from scipy.optimize import minimize as sp_minimize

from ..types import ZNEData, FitResult


def _rbf_kernel(x1, x2, length_scale=1.0, amplitude=1.0):
    sq_dist = np.subtract.outer(x1, x2) ** 2
    return amplitude**2 * np.exp(-0.5 * sq_dist / length_scale**2)


def _matern32_kernel(x1, x2, length_scale=1.0, amplitude=1.0):
    r = np.abs(np.subtract.outer(x1, x2)) / length_scale
    return amplitude**2 * (1.0 + np.sqrt(3.0) * r) * np.exp(-np.sqrt(3.0) * r)


def _neg_log_marginal_likelihood(log_params, x, g_obs, latent_var, kernel_fn, jitter):
    """Negative log marginal likelihood for GP hyperparameter optimization."""
    length_scale = np.exp(log_params[0])
    amplitude = np.exp(log_params[1])
    n = len(x)
    K = kernel_fn(x, x, length_scale, amplitude) + np.diag(latent_var) + jitter * np.eye(n)
    try:
        L, low = cho_factor(K)
        alpha = cho_solve((L, low), g_obs)
        nll = 0.5 * np.dot(g_obs, alpha) + np.sum(np.log(np.diag(L))) + 0.5 * n * np.log(2 * np.pi)
        return float(nll)
    except np.linalg.LinAlgError:
        return 1e10


def _prepare_latent(data, bounds):
    """Transform observations to latent space."""
    lo, hi = bounds
    midpoint = (lo + hi) / 2.0
    radius = (hi - lo) / 2.0
    y_normalized = (data.estimates - midpoint) / radius
    y_clipped = np.clip(y_normalized, -0.999, 0.999)
    clipped_count = int(np.sum(np.abs(y_normalized) >= 0.999))
    g_obs = np.arctanh(y_clipped)

    if data.variances is not None:
        sech2 = 1.0 - np.tanh(g_obs)**2
        latent_var = data.variances / (radius * sech2)**2
    else:
        latent_var = np.full(data.n, 0.01)

    return g_obs, latent_var, clipped_count, midpoint, radius


def fit_bayesian_zne_gp(
    data: ZNEData,
    bounds: tuple[float, float] = (-1.0, 1.0),
    kernel: str = "rbf",
    bounded_transform: str = "tanh",
    length_scale: float | None = None,
    amplitude: float = 1.0,
    optimize_hyperparameters: bool = False,
    jitter: float = 1e-6,
) -> FitResult:
    """Bounded Bayesian ZNE using GP on latent space with tanh output transform.

    Model: f(λ) = midpoint + radius * tanh(g(λ)), where g ~ GP(0, K).
    This guarantees f(λ) ∈ (bounds[0], bounds[1]) for all λ.

    If optimize_hyperparameters=True, length_scale and amplitude are optimized
    via marginal likelihood maximization.
    """
    lo, hi = bounds
    midpoint = (lo + hi) / 2.0
    radius = (hi - lo) / 2.0
    x = data.scales
    n = data.n

    if length_scale is None:
        length_scale = max(0.5, (x.max() - x.min()) / 2.0)

    g_obs, latent_var, clipped_count, _, _ = _prepare_latent(data, bounds)
    kernel_fn = _rbf_kernel if kernel == "rbf" else _matern32_kernel

    # Hyperparameter optimization
    nll_before = _neg_log_marginal_likelihood(
        np.log([length_scale, amplitude]), x, g_obs, latent_var, kernel_fn, jitter
    )
    optimized = False
    if optimize_hyperparameters:
        res = sp_minimize(
            _neg_log_marginal_likelihood,
            x0=np.log([length_scale, amplitude]),
            args=(x, g_obs, latent_var, kernel_fn, jitter),
            method="L-BFGS-B",
            bounds=[(-2, 3), (-2, 3)],
        )
        if res.success:
            length_scale = float(np.exp(res.x[0]))
            amplitude = float(np.exp(res.x[1]))
            optimized = True
    nll_after = _neg_log_marginal_likelihood(
        np.log([length_scale, amplitude]), x, g_obs, latent_var, kernel_fn, jitter
    )

    # GP posterior at λ=0
    K = kernel_fn(x, x, length_scale, amplitude) + np.diag(latent_var) + jitter * np.eye(n)
    k_star = kernel_fn(np.array([0.0]), x, length_scale, amplitude).flatten()
    k_ss = amplitude**2

    L, low = cho_factor(K)
    alpha = cho_solve((L, low), g_obs)
    mu_g0 = float(np.dot(k_star, alpha))
    v = cho_solve((L, low), k_star)
    var_g0 = max(0.0, k_ss - np.dot(k_star, v))

    # Transform back
    mu_f0 = midpoint + radius * np.tanh(mu_g0)
    jac_val = radius * (1.0 - np.tanh(mu_g0)**2)
    var_f0 = jac_val**2 * var_g0

    # Credible intervals
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
            "optimize_hyperparameters": optimized,
            "nll_before": nll_before,
            "nll_after": nll_after,
        },
        assumptions=[
            f"GP on latent g(λ) with {kernel} kernel",
            f"f(λ) = {midpoint} + {radius}·tanh(g(λ))",
            f"bounds: [{lo}, {hi}]",
            "Delta-method variance propagation",
            f"Hyperparameters {'optimized via marginal likelihood' if optimized else 'fixed'}",
        ],
    )


def design_next_scale(
    data: ZNEData,
    candidate_scales: np.ndarray,
    bounds: tuple[float, float] = (-1.0, 1.0),
    kernel: str = "rbf",
    length_scale: float | None = None,
    amplitude: float = 1.0,
    jitter: float = 1e-6,
) -> float:
    """Select next scale factor to minimize posterior variance at λ=0.

    Greedy one-step lookahead: for each candidate, compute the posterior
    variance at λ=0 if that candidate were added (with a dummy observation
    at the current posterior mean), and return the candidate giving lowest variance.
    """
    lo, hi = bounds
    midpoint = (lo + hi) / 2.0
    radius = (hi - lo) / 2.0
    x = data.scales
    n = data.n
    candidates = np.asarray(candidate_scales, dtype=np.float64)

    if length_scale is None:
        length_scale = max(0.5, (x.max() - x.min()) / 2.0)

    g_obs, latent_var, _, _, _ = _prepare_latent(data, bounds)
    kernel_fn = _rbf_kernel if kernel == "rbf" else _matern32_kernel

    # Current posterior variance at 0
    K = kernel_fn(x, x, length_scale, amplitude) + np.diag(latent_var) + jitter * np.eye(n)
    k_star = kernel_fn(np.array([0.0]), x, length_scale, amplitude).flatten()
    k_ss = amplitude**2
    L, low = cho_factor(K)

    best_var = np.inf
    best_scale = candidates[0]

    for c in candidates:
        # Augmented system: add candidate with estimated latent noise
        x_aug = np.append(x, c)
        latent_var_aug = np.append(latent_var, np.mean(latent_var))
        n_aug = n + 1

        K_aug = kernel_fn(x_aug, x_aug, length_scale, amplitude) + np.diag(latent_var_aug) + jitter * np.eye(n_aug)
        k_star_aug = kernel_fn(np.array([0.0]), x_aug, length_scale, amplitude).flatten()

        try:
            L_aug, low_aug = cho_factor(K_aug)
            v_aug = cho_solve((L_aug, low_aug), k_star_aug)
            var_aug = k_ss - np.dot(k_star_aug, v_aug)
            if var_aug < best_var:
                best_var = var_aug
                best_scale = c
        except np.linalg.LinAlgError:
            continue

    return float(best_scale)
