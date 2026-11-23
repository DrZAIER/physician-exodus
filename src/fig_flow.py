"""Supplementary flow diagram (Figure S1)."""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "outputs", "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})

fig, ax = plt.subplots(figsize=(7.6, 3.9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis("off")


def box(x, y, w, h, text, fc="#E8F0F8", ec="#2166AC"):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                       linewidth=1.0, edgecolor=ec, facecolor=fc)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8)


def arrow(x1, y1, x2, y2, color="#333333", style="-|>", lw=1.1, ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=10,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0")
    ax.add_patch(a)


# Boxes
box(0.2, 3.5, 1.8, 0.95, "Medical graduates\n$G(t-5)$")
box(2.7, 3.5, 2.0, 0.95, "Enter Tunisian\npractice: $\\sigma G$")
box(2.7, 1.5, 2.0, 0.95, "Pre-entry\nemigration: $(1-\\sigma)G$")
box(5.2, 3.5, 2.3, 0.95, "Practising stock\n$N_a(t)$ by age", fc="#E6F2E6", ec="#1B7837")
box(5.2, 1.2, 2.3, 0.8, "Diaspora pool\n$D(t)$", fc="#FDF0E0", ec="#E08214")
box(8.2, 3.5, 1.6, 0.95, "Retirement\nand death")
box(8.2, 1.2, 1.6, 0.8, "Return\nmigration $\\rho D$",
    fc="#FDF0E0", ec="#E08214")

# Arrows
arrow(2.0, 3.97, 2.7, 3.97)
arrow(4.7, 3.97, 5.2, 3.97)
arrow(2.0, 3.75, 2.7, 2.0)
arrow(4.7, 1.97, 5.2, 1.6)
arrow(6.35, 3.5, 6.35, 2.0, color="#E08214")
ax.text(6.55, 2.75, "post-entry\nemigration $M(t)$", fontsize=7, color="#B35900")
arrow(7.5, 1.6, 8.2, 1.6, color="#E08214")
arrow(8.2, 2.0, 7.5, 3.5, color="#E08214", ls="--")
arrow(7.5, 3.97, 8.2, 3.97, color="#1B7837")

ax.text(5.0, 4.75, "Annual cohort-component model of the Tunisian physician workforce",
        ha="center", fontsize=9, weight="bold")
ax.text(5.0, 0.55,
        "Return migrants re-enter the practising stock at ages 33–50. "
        "The diaspora pool is an accounting device, not a calibrated stock.",
        ha="center", fontsize=7, style="italic")

fig.savefig(os.path.join(OUT, "figS1_flow_diagram.png"))
fig.savefig(os.path.join(OUT, "figS1_flow_diagram.pdf"))
print("saved")
