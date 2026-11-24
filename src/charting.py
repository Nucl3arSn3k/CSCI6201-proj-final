from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

CELL = 0.003  # degrees; same grid as build_cell_table in analysis.py


SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
BLUE = "#2a78d6"    # 311 complaints
ORANGE = "#eb6834"  # alcohol licenses
SEQ_BLUE = LinearSegmentedColormap.from_list("seq_blue", ["#eef4fc", BLUE, "#0d3a73"])


def _style(ax) -> None:
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK_2)
    ax.tick_params(colors=INK_2)
    ax.xaxis.label.set_color(INK_2)
    ax.yaxis.label.set_color(INK_2)
    ax.title.set_color(INK)


def plot_complaints_by_bar_count(cells: pd.DataFrame, out_dir: Path) -> None:
    """Box plot: smell-type complaints per cell, grouped by number of licenses in the cell."""
    bars = cells["bars_total"].to_numpy()
    groups = [("0", bars == 0), ("1", bars == 1), ("2-3", (bars >= 2) & (bars <= 3)), ("4+", bars >= 4)]
    data = [cells.loc[mask, "sancompcount"].to_numpy() for _, mask in groups]
    labels = [f"{name}\n(n={len(d)} cells)" for (name, _), d in zip(groups, data)]

    print("\n=== Complaints per cell by number of licenses in the cell ===")
    for (name, _), d in zip(groups, data):
        print(f"{name:>4} licenses: n={len(d):4d}  median={np.median(d):.0f}  mean={d.mean():.1f}")

    fig, ax = plt.subplots(figsize=(8, 5), facecolor=SURFACE)
    ax.boxplot(
        data, tick_labels=labels, patch_artist=True, widths=0.5,
        boxprops={"facecolor": BLUE, "alpha": 0.35, "edgecolor": BLUE, "linewidth": 1.2},
        medianprops={"color": INK, "linewidth": 2},
        whiskerprops={"color": BLUE}, capprops={"color": BLUE},
        flierprops={"marker": "o", "markersize": 3, "markerfacecolor": BLUE,
                    "markeredgecolor": "none", "alpha": 0.4},
    )
    ax.set_title("Smell-type 311 requests per cell, by number of alcohol licenses in the cell")
    ax.set_xlabel("Alcohol licenses in the cell")
    ax.set_ylabel("Smell-type requests per cell (2025)")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    fig.tight_layout()
    path = out_dir / "03_complaints_by_bar_count.png"
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    plt.close(fig)
    print("Saved:", path)


def plot_bars_and_complaints_map(cells: pd.DataFrame, lic: pd.DataFrame, out_dir: Path) -> None:
    """Map: complaints per cell (shaded) with alcohol license locations on top."""
    shaw = {"lon_min": -77.034, "lon_max": -77.019, "lat_min": 38.907, "lat_max": 38.916}
    lon = (cells["cell_x"].to_numpy() + 0.5) * CELL
    lat = (cells["cell_y"].to_numpy() + 0.5) * CELL
    counts = cells["sancompcount"].to_numpy()
    vmax = float(np.percentile(counts, 95))  # skewed: cap the colour scale so it stays readable

    fig, ax = plt.subplots(figsize=(8, 8), facecolor=SURFACE)
    sc = ax.scatter(lon, lat, c=counts, cmap=SEQ_BLUE, vmin=0, vmax=vmax, marker="s", s=14, linewidths=0)
    ax.scatter(lic["LONGITUDE"], lic["LATITUDE"], s=5, color=ORANGE, alpha=0.7,
               edgecolors="none", label="Alcohol license")
    ax.plot(
        [shaw["lon_min"], shaw["lon_max"], shaw["lon_max"], shaw["lon_min"], shaw["lon_min"]],
        [shaw["lat_min"], shaw["lat_min"], shaw["lat_max"], shaw["lat_max"], shaw["lat_min"]],
        color=INK, linewidth=1.5, label="Shaw box",
    )
    cbar = fig.colorbar(sc, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("Smell-type requests per cell (colour capped at 95th percentile)", color=INK_2)
    cbar.ax.tick_params(colors=INK_2)

    ax.set_title("Smell-type 311 requests and alcohol licenses, Washington DC")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect("equal")
    ax.legend(loc="lower left", frameon=False, labelcolor=INK_2)
    _style(ax)
    fig.tight_layout()
    path = out_dir / "04_bars_and_complaints_map.png"
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    plt.close(fig)
    print("Saved:", path)
