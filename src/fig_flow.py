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

fig, ax = plt.subplots(figsize=(7.8, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis("off")


def box(x, y, w, h, text, fc="#E8F0F8", ec="#2166AC", fs=8):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                       linewidth=1.0, edgecolor=ec, facecolor=fc)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


def arrow(x1, y1, x2, y2, color="#333333", style="-|>", lw=1.1, ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=10,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0")
    ax.add_patch(a)


# Top row
box(0.2, 3.55, 1.8, 0.95, "Medical graduates\nG(t−5)")
box(2.7, 3.55, 2.1, 0.95, "Enter Tunisian\npractice: σG")
box(5.4, 3.55, 2.3, 0.95, "Practising stock\nN_a(t) by age", fc="#E6F2E6", ec="#1B7837")
box(8.4, 3.55, 1.4, 0.95, "Retirement\nand death")

# Bottom row
box(2.7, 1.35, 2.1, 0.95, "Pre-entry\nemigration: (1−σ)G")
box(5.4, 1.35, 2.3, 0.95, "Return-eligible\npool D(t)", fc="#FDF0E0", ec="#E08214")
box(8.4, 1.35, 1.4, 1.0, "Attrition δD\n(death abroad,\nonward migration,\nsettlement)", fc="#FDF0E0", ec="#E08214", fs=6.3)

# Arrows
arrow(2.0, 4.02, 2.7, 4.02)
arrow(4.8, 4.02, 5.4, 4.02)
arrow(2.0, 3.75, 2.7, 1.9)
arrow(4.8, 1.82, 5.4, 1.82)
arrow(7.7, 3.75, 8.4, 3.75, color="#1B7837")
arrow(8.4, 1.9, 7.7, 1.9, color="#E08214")

# Post-entry emigration (stock to pool)
arrow(6.10, 3.55, 6.10, 2.3, color="#E08214")
ax.text(6.00, 2.95, "post-entry\nemigration\nM(t)", fontsize=6.6, color="#B35900",
        ha="right", va="center")

# Return migration (pool to stock)
arrow(7.05, 2.3, 7.05, 3.55, color="#1B7837", ls="--")
ax.text(7.15, 2.95, "return\nρD", fontsize=6.8, color="#1B6B2E",
        ha="left", va="center")

# Re-emigration (return to pool)
ax.text(5.55, 0.95,
        "Return migrants remain in practice with probability 0.85; the remainder rejoin D.",
        ha="center", fontsize=7, style="italic")
ax.text(5.0, 4.78,
        "Annual cohort-component model of the Tunisian physician workforce",
        ha="center", fontsize=9, weight="bold")
ax.text(5.0, 0.55,
        "D is a return-eligible pool, not a diaspora estimate. Entrants are spread over ages 29–33; returns over 33–50.",
        ha="center", fontsize=7, style="italic")

fig.savefig(os.path.join(OUT, "figS1_flow_diagram.png"))
fig.savefig(os.path.join(OUT, "figS1_flow_diagram.pdf"))
print("saved")
