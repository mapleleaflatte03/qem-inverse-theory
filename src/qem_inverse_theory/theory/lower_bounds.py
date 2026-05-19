"""Two-point Le Cam lower bounds for ZNE estimation.

Formalizes the ambiguity-diameter intuition: if two admissible response
functions are nearly indistinguishable at observed noise scales but differ
at zero noise, no estimator can reliably recover f(0).
"""

import numpy as np


def two_point_total_variation_bound(delta_obs: float, sigma: float, n: int) -> float:
    """Upper bound on total variation between two Gaussian observation models.

    If two responses differ by at most delta_obs at each observed point,
    and observations have noise variance sigma^2 / n_shots_per_point,
    the squared Hellinger distance (and hence TV) is bounded.

    TV ≤ sqrt(1 - exp(-n * delta_obs^2 / (2 * sigma^2)))

    For small separation: TV ≈ sqrt(n) * delta_obs / (sqrt(2) * sigma)
    """
    if sigma <= 0 or n <= 0:
        return 0.0
    # KL divergence for n Gaussian observations differing by delta_obs each
    kl = n * delta_obs**2 / (2 * sigma**2)
    # Pinsker: TV ≤ sqrt(KL/2)
    tv = min(1.0, np.sqrt(kl / 2))
    return float(tv)


def lecam_mse_lower_bound(delta_f0: float, tv_bound: float) -> float:
    """Le Cam two-point MSE lower bound.

    If two hypotheses have f(0) differing by delta_f0 and the observation
    distributions have total variation at most tv_bound, then:

    MSE ≥ (delta_f0 / 2)^2 * (1 - tv_bound)

    This is the standard Le Cam testing lower bound converted to estimation.
    """
    if delta_f0 <= 0:
        return 0.0
    return (delta_f0 / 2)**2 * max(0.0, 1.0 - tv_bound)


def zne_two_point_lower_bound(
    delta_f0: float,
    delta_obs: float,
    sigma: float,
    n_points: int,
    shots_per_point: int,
) -> dict:
    """Compute ZNE-specific two-point lower bound.

    Args:
        delta_f0: separation at zero noise between two admissible responses
        delta_obs: maximum separation at observed noise scales
        sigma: single-shot standard deviation
        n_points: number of observed scale factors
        shots_per_point: shots allocated per scale factor

    Returns dict with:
        tv_bound, mse_lower_bound, interpretation, assumptions
    """
    # Effective noise per point
    sigma_eff = sigma / np.sqrt(shots_per_point)
    # Total TV across all observed points
    tv = two_point_total_variation_bound(delta_obs, sigma_eff, n_points)
    mse_lb = lecam_mse_lower_bound(delta_f0, tv)

    return {
        "delta_f0": delta_f0,
        "delta_obs": delta_obs,
        "sigma": sigma,
        "n_points": n_points,
        "shots_per_point": shots_per_point,
        "sigma_effective": float(sigma_eff),
        "tv_bound": float(tv),
        "mse_lower_bound": float(mse_lb),
        "interpretation": (
            f"Any estimator has MSE ≥ {mse_lb:.6f} when two admissible responses "
            f"differ by {delta_f0} at λ=0 but by at most {delta_obs} at observed scales, "
            f"with {shots_per_point} shots/point and {n_points} scale factors."
        ),
        "assumptions": [
            "Gaussian observation model",
            "Two specific admissible responses (not worst-case over all)",
            "Le Cam two-point method (not minimax over function class)",
            "Does not prove a universal QEM lower bound",
        ],
    }
