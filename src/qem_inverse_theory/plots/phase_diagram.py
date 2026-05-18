"""Phase diagram plotting: help vs harm regions."""

import numpy as np
import matplotlib.pyplot as plt


def plot_phase_diagram(
    phase_grid: dict,
    title: str = "ZNE Help–Harm Phase Diagram",
    save_path: str | None = None,
):
    """Plot help/harm heatmap.

    x-axis: log10(total shots)
    y-axis: noise strength
    color: log10(MSE_raw / MSE_method)
    """
    shots = phase_grid["shots_axis"]
    noise = phase_grid["noise_axis"]
    grid = phase_grid["log_ratio_grid"]

    fig, ax = plt.subplots(figsize=(8, 5))
    vmax = max(abs(np.nanmin(grid)), abs(np.nanmax(grid)))
    im = ax.pcolormesh(
        np.log10(shots),
        noise,
        grid,
        cmap="RdBu",
        vmin=-vmax,
        vmax=vmax,
        shading="auto",
    )
    ax.set_xlabel("log₁₀(total shots)")
    ax.set_ylabel("Noise strength")
    ax.set_title(title)
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("log₁₀(MSE_raw / MSE_method)")
    ax.axhline(y=0, color="k", linewidth=0.5, linestyle="--", alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return fig
