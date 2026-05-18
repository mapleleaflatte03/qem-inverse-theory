"""Risk frontier plots: bias-variance tradeoff visualization."""

import numpy as np
import matplotlib.pyplot as plt


def plot_risk_frontier(
    degrees: list[int],
    biases_sq: list[float],
    variances: list[float],
    title: str = "Bias-Variance Tradeoff",
    save_path: str | None = None,
):
    """Plot bias² and variance as function of model complexity."""
    fig, ax = plt.subplots(figsize=(7, 4))
    mses = [b + v for b, v in zip(biases_sq, variances)]

    ax.plot(degrees, biases_sq, "o-", label="Bias²")
    ax.plot(degrees, variances, "s-", label="Variance")
    ax.plot(degrees, mses, "^-", label="MSE", linewidth=2)
    ax.set_xlabel("Polynomial degree")
    ax.set_ylabel("Error")
    ax.set_title(title)
    ax.legend()
    ax.set_yscale("log")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return fig
