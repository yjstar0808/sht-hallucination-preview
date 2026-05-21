"""
Lite version of the method overview for the public preview.
Deliberately omits the specific score function formula, theorem numbers,
mixture weight choice, and betting strategy — those live in the
private/full repo and are reserved for the under-review paper.
"""
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).parent


def draw_box(ax, x, y, w, h, label, sublabel="", facecolor="#E8F1FB", edgecolor="#2F5496",
             lw=1.5, fontsize=11, sub_fontsize=9):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.04",
        linewidth=lw, edgecolor=edgecolor, facecolor=facecolor,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h * 0.62, label, ha="center", va="center",
            fontsize=fontsize, fontweight="bold", color="#1F3864")
    if sublabel:
        ax.text(x + w / 2, y + h * 0.30, sublabel, ha="center", va="center",
                fontsize=sub_fontsize, color="#404040", style="italic")


def draw_arrow(ax, x1, y1, x2, y2, color="#404040", lw=1.2, style="-|>"):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=14, color=color, lw=lw,
        connectionstyle="arc3,rad=0.0", shrinkA=2, shrinkB=2,
    )
    ax.add_patch(arrow)


def main():
    fig, ax = plt.subplots(figsize=(11.5, 6.0), dpi=150)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text(6.0, 6.15, "SHT: Three-Layer Hallucination Detection (overview)",
            ha="center", va="center", fontsize=14, fontweight="bold", color="#1F3864")

    draw_box(ax, 0.4, 4.8, 11.2, 0.95,
             "Token stream from an LLM (sampling distribution available)",
             facecolor="#F4F4F4", edgecolor="#666666", fontsize=10.5)

    draw_box(ax, 0.4, 3.4, 11.2, 1.05,
             "Layer 1   ▸   Anytime-valid token-level monitor",
             sublabel="Statistical guarantee on false-alarm rate at any stopping time",
             facecolor="#DCEAF7", edgecolor="#2F5496", fontsize=12)

    draw_box(ax, 0.4, 2.0, 11.2, 1.05,
             "Layer 2   ▸   Claim-level calibration",
             sublabel="Distribution-free factual false-alarm bound",
             facecolor="#DAE9D6", edgecolor="#548235", fontsize=12)

    draw_box(ax, 0.4, 0.6, 11.2, 1.05,
             "Layer 3   ▸   Empirical bridge to hallucination labels",
             sublabel="Validation across 5 hallucination categories on Qwen2.5-7B",
             facecolor="#FBE4D5", edgecolor="#C55A11", fontsize=12)

    draw_arrow(ax, 6.0, 4.78, 6.0, 4.46)
    draw_arrow(ax, 6.0, 3.38, 6.0, 3.06)
    draw_arrow(ax, 6.0, 1.98, 6.0, 1.66)

    handles = [
        mpatches.Patch(facecolor="#DCEAF7", edgecolor="#2F5496", label="Theoretical guarantee"),
        mpatches.Patch(facecolor="#DAE9D6", edgecolor="#548235", label="Theoretical guarantee"),
        mpatches.Patch(facecolor="#FBE4D5", edgecolor="#C55A11", label="Empirical"),
    ]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.05),
              ncol=3, frameon=False, fontsize=9)

    plt.tight_layout()
    fig.savefig(OUT / "method_overview_lite.png", dpi=200, bbox_inches="tight")
    print(f"Saved: {OUT / 'method_overview_lite.png'}")


if __name__ == "__main__":
    main()
