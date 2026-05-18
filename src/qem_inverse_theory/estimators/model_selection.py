"""Information-theoretic model selection for ZNE."""

import numpy as np

from ..types import ZNEData, FitResult
from .unconstrained import fit_polynomial_zne
from .constrained import fit_bounded_polynomial_zne


def rss(residuals: np.ndarray) -> float:
    """Residual sum of squares."""
    return float(np.sum(np.asarray(residuals) ** 2))


def aic(n: int, k: int, rss_val: float) -> float:
    """Akaike Information Criterion. k = number of parameters."""
    if rss_val <= 0:
        return -np.inf
    return n * np.log(rss_val / n) + 2 * k


def aicc(n: int, k: int, rss_val: float) -> float:
    """Corrected AIC for small samples (Hurvich & Tsai 1989)."""
    if n - k - 1 <= 0:
        return np.inf  # undefined / infinite penalty
    return aic(n, k, rss_val) + (2 * k * (k + 1)) / (n - k - 1)


def bic(n: int, k: int, rss_val: float) -> float:
    """Bayesian Information Criterion."""
    if rss_val <= 0:
        return -np.inf
    return n * np.log(rss_val / n) + k * np.log(n)


def select_by_aicc(
    data: ZNEData,
    max_degree: int = 4,
    bounds: tuple[float, float] | None = (-1.0, 1.0),
) -> FitResult:
    """Select polynomial degree by AICc, optionally with bounds."""
    best_aicc = np.inf
    best_result = None

    for deg in range(1, min(max_degree + 1, data.n)):
        if bounds is not None:
            result = fit_bounded_polynomial_zne(data, deg, bounds)
        else:
            result = fit_polynomial_zne(data, deg)

        k = deg + 1  # number of polynomial parameters
        rss_val = result.diagnostics.get("rss", np.inf)
        score = aicc(data.n, k, rss_val)

        if score < best_aicc:
            best_aicc = score
            best_result = result
            best_result.diagnostics["aicc"] = score
            best_result.diagnostics["selected_degree"] = deg

    return best_result


def model_average_aicc(
    data: ZNEData,
    max_degree: int = 4,
    bounds: tuple[float, float] | None = (-1.0, 1.0),
) -> FitResult:
    """AICc-weighted model averaging over polynomial degrees."""
    results = []
    scores = []

    for deg in range(1, min(max_degree + 1, data.n)):
        if bounds is not None:
            result = fit_bounded_polynomial_zne(data, deg, bounds)
        else:
            result = fit_polynomial_zne(data, deg)
        k = deg + 1
        rss_val = result.diagnostics.get("rss", np.inf)
        score = aicc(data.n, k, rss_val)
        results.append(result)
        scores.append(score)

    # Akaike weights
    scores = np.array(scores)
    delta = scores - scores.min()
    weights = np.exp(-0.5 * delta)
    weights /= weights.sum()

    avg_estimate = sum(w * r.estimate for w, r in zip(weights, results))

    return FitResult(
        estimate=float(avg_estimate),
        method="model_average_aicc",
        diagnostics={"weights": weights.tolist(), "scores": scores.tolist()},
        assumptions=["AICc-weighted average over polynomial degrees"],
    )
