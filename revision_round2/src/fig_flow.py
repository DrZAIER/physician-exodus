"""Supplementary flow diagram (Figure S1), revision 2.0."""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "outputs", "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})

fig, ax = plt.subplots(figsize=(8.2, 4.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.4)
ax.axis("off")


def box(x, y, w, h, text, fc="#E8F0F8", ec="#2166AC", fs=7.5):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.10",
                       linewidth=1.0, edgecolor=ec, facecolor=fc)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


def arrow(x1, y1, x2, y2, color="#333333", style="-|>", lw=1.0, ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=9,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0.0")
    ax.add_patch(a)


# Top row
box(0.2, 4.05, 1.8, 0.85, "Medical graduates\nG(t−L)")
box(2.6, 4.05, 2.0, 0.85, "Enter Tunisian\npractice: σG")
box(5.1, 4.05, 2.0, 0.85, "Practising stock\nN_a(t) by age", fc="#E6F2E6", ec="#1B7837")
box(7.7, 4.05, 1.8, 0.85, "Retirement\nand death")

# Pipeline non-entry and its split
box(2.6, 2.65, 2.0, 0.85, "Pipeline non-entry\n(1−σ)G")
box(2.6, 1.25, 2.0, 0.85, "Pre-entry international\nemigration φ(1−σ)G", fc="#FDF0E0", ec="#E08214")
box(0.2, 1.25, 2.0, 0.85, "Domestic non-entry\n(1−φ)(1−σ)G", fc="#F5F5F5", ec="#777777")
box(5.1, 1.25, 2.0, 0.95, "Return-eligible\npool D(t)", fc="#FDF0E0", ec="#E08214")
box(7.7, 1.25, 1.8, 0.95, "Attrition δD\n(death abroad,\nonward migration,\nsettlement)", fc="#FDF0E0", ec="#E08214", fs=6.2)

# Arrows
arrow(2.0, 4.47, 2.6, 4.47)
arrow(4.6, 4.47, 5.1, 4.47)
arrow(7.1, 4.47, 7.7, 4.47, color="#1B7837")
arrow(1.1, 4.05, 1.1, 3.07)
arrow(1.1, 3.07, 2.6, 3.07)
arrow(2.6, 2.65, 1.2, 2.10)
arrow(3.6, 2.65, 3.6, 2.10)
arrow(4.6, 1.67, 5.1, 1.67)
arrow(6.1, 4.05, 6.1, 2.20, color="#E08214")
ax.text(6.25, 3.05, "post-entry\nemigration M(t)", fontsize=6.6, color="#B35900",
        ha="left", va="center")
arrow(5.95, 2.20, 5.95, 4.05, color="#1B7837", ls="--")
ax.text(5.80, 3.05, "return\nρD", fontsize=6.8, color="#1B6B2E",
        ha="right", va="center")
# 15% re-emigration loop back to the return-eligible pool
loop = FancyArrowPatch((5.95, 3.55), (6.55, 2.20),
                       arrowstyle="-|>", mutation_scale=9,
                       linewidth=0.9, color="#1B6B2E", linestyle=":",
                       connectionstyle="arc3,rad=0.45")
ax.add_patch(loop)
ax.text(6.55, 3.25, "15% re-emigrate", fontsize=6.1, color="#1B6B2E",
        ha="left", va="center")
arrow(7.1, 1.72, 7.7, 1.72, color="#E08214")

ax.text(5.0, 5.15,
        "Annual cohort-component model of the Tunisian physician workforce",
        ha="center", fontsize=9, weight="bold")
ax.text(5.0, 0.55,
        "Only international emigration enters D. Domestic non-entry does not. "
        "Return migrants remain in practice with probability 0.85.",
        ha="center", fontsize=6.8, style="italic")
ax.text(5.0, 0.25,
        "D is a return-eligible pool, not a diaspora estimate. Entrants are spread over ages 29–33; returns over 33–50.",
        ha="center", fontsize=6.8, style="italic")

fig.savefig(os.path.join(OUT, "figS1_flow_diagram.png"))
fig.savefig(os.path.join(OUT, "figS1_flow_diagram.pdf"))
print("saved")
