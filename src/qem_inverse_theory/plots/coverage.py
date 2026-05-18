"""Coverage and calibration plots for Bayesian ZNE."""

import numpy as np
import matplotlib.pyplot as plt


def plot_coverage(
    nominal_levels: list[float],
    empirical_coverages: list[float],
    title: str = "Credible Interval Calibration",
    save_path: str | None = None,
):
    """Plot empirical vs nominal coverage (calibration plot)."""
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Perfect calibration")
    ax.plot(nominal_levels, empirical_coverages, "o-", label="Empirical")
    ax.set_xlabel("Nominal coverage")
    ax.set_ylabel("Empirical coverage")
    ax.set_title(title)
    ax.legend()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return fig
