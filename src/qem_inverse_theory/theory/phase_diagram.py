"""Finite-shot help–harm phase diagram utilities."""

import numpy as np
from numpy.typing import NDArray


def compute_help_harm_ratio(raw_mse: float, mitigated_mse: float) -> float:
    """Ratio of raw MSE to mitigated MSE. >1 means mitigation helps."""
    if mitigated_mse <= 0:
        return np.inf
    return raw_mse / mitigated_mse


def classify_region(raw_mse: float, mitigated_mse: float) -> str:
    """Classify as 'help', 'harm', or 'neutral'."""
    ratio = compute_help_harm_ratio(raw_mse, mitigated_mse)
    if ratio > 1.05:
        return "help"
    elif ratio < 0.95:
        return "harm"
    else:
        return "neutral"


def build_phase_grid(
    results: list[dict],
) -> dict[str, NDArray]:
    """Build phase diagram grid from experiment results.

    Each result dict should have keys:
        'shots', 'noise_strength', 'raw_mse', 'mitigated_mse'

    Returns arrays suitable for pcolormesh plotting.
    """
    shots_vals = sorted(set(r["shots"] for r in results))
    noise_vals = sorted(set(r["noise_strength"] for r in results))

    grid = np.full((len(noise_vals), len(shots_vals)), np.nan)

    for r in results:
        i = noise_vals.index(r["noise_strength"])
        j = shots_vals.index(r["shots"])
        ratio = compute_help_harm_ratio(r["raw_mse"], r["mitigated_mse"])
        grid[i, j] = np.log10(ratio) if ratio > 0 else 0.0

    return {
        "shots_axis": np.array(shots_vals),
        "noise_axis": np.array(noise_vals),
        "log_ratio_grid": grid,
    }
