"""Bayesian ZNE via Gaussian process. EXPERIMENTAL.

This is a minimal prototype to explore uncertainty quantification for ZNE.
It uses a simple GP with RBF kernel. Not production-ready.
"""

import numpy as np
from scipy.linalg import cho_solve, cho_factor

from ..types import ZNEData, FitResult


def _rbf_kernel(x1: np.ndarray, x2: np.ndarray, length_scale: float = 1.0, variance: float = 1.0) -> np.ndarray:
    """RBF (squared exponential) kernel."""
    sq_dist = np.subtract.outer(x1, x2) ** 2
    return variance * np.exp(-0.5 * sq_dist / length_scale**2)


def fit_bayesian_zne_gp(
    data: ZNEData,
    bounds: tuple[float, float] = (-1.0, 1.0),
    length_scale: float = 2.0,
    kernel_variance: float = 1.0,
    noise_variance: float | None = None,
) -> FitResult:
    """Gaussian process regression for ZNE with posterior at λ=0.

    Returns posterior mean, variance, and 95% credible interval.
    The estimate is projected onto physical bounds if needed.

    EXPERIMENTAL: hyperparameters are not optimized.
    """
    x = data.scales
    y = data.estimates
    n = data.n

    # Noise variance: use provided variances or estimate
    if noise_variance is not None:
        sigma2 = noise_variance
    elif data.variances is not None:
        sigma2 = float(np.mean(data.variances))
    else:
        sigma2 = 0.01  # default small noise

    # Kernel matrices
    K = _rbf_kernel(x, x, length_scale, kernel_variance) + sigma2 * np.eye(n)
    k_star = _rbf_kernel(np.array([0.0]), x, length_scale, kernel_variance).flatten()
    k_ss = kernel_variance  # K(0, 0)

    # Posterior
    L, low = cho_factor(K)
    alpha = cho_solve((L, low), y)
    mu = float(np.dot(k_star, alpha))
    v = cho_solve((L, low), k_star)
    var = max(0.0, k_ss - np.dot(k_star, v))

    # Project mean onto bounds
    mu_bounded = float(np.clip(mu, bounds[0], bounds[1]))

    # 95% credible interval
    std = np.sqrt(var)
    ci_low = max(bounds[0], mu - 1.96 * std)
    ci_high = min(bounds[1], mu + 1.96 * std)

    return FitResult(
        estimate=mu_bounded,
        variance=var,
        method="bayesian_gp",
        diagnostics={
            "posterior_mean_raw": mu,
            "posterior_variance": var,
            "ci_95": (ci_low, ci_high),
            "length_scale": length_scale,
            "kernel_variance": kernel_variance,
            "noise_variance": sigma2,
        },
        assumptions=[
            "EXPERIMENTAL: hyperparameters not optimized",
            "RBF kernel (smoothness assumption)",
            f"bounds: {bounds}",
            "Gaussian noise model",
        ],
    )
