"""Evaluation metrics for ZNE estimators."""

import numpy as np
from numpy.typing import NDArray


def absolute_error(estimate: float, truth: float) -> float:
    return abs(estimate - truth)


def mse(estimates: NDArray[np.float64], truth: float) -> float:
    """Mean squared error over repeated trials."""
    return float(np.mean((np.asarray(estimates) - truth) ** 2))


def bias_variance_decomposition(
    estimates: NDArray[np.float64], truth: float
) -> dict[str, float]:
    """Decompose MSE = Bias² + Variance."""
    est = np.asarray(estimates)
    mean_est = float(est.mean())
    bias = mean_est - truth
    variance = float(est.var())
    return {
        "bias": bias,
        "bias_squared": bias**2,
        "variance": variance,
        "mse": bias**2 + variance,
    }


def physical_validity_rate(
    estimates: NDArray[np.float64], bounds: tuple[float, float]
) -> float:
    """Fraction of estimates within physical bounds."""
    est = np.asarray(estimates)
    valid = np.sum((est >= bounds[0]) & (est <= bounds[1]))
    return float(valid / len(est))


def interval_coverage(
    intervals: list[tuple[float, float]], truth: float
) -> float:
    """Fraction of credible intervals containing the true value."""
    covered = sum(1 for lo, hi in intervals if lo <= truth <= hi)
    return covered / len(intervals)
