#!/usr/bin/env python3
"""Defense-slide charts (bar version), data from thesis Table 4.4 (Ch4).

Outputs (presentation/figures/):
  fig_mae_vs_wlen.png     - Slide 11: grouped bars, MAE vs window length
                            (NBD | NRD panels, SHARED y-axis)
  fig_cycles_vs_wlen.png  - Slide 12: both series in ONE chart, relative
                            inference cost (wlen 20 = 1), absolute cycles
                            labeled at the endpoints

Figures deliberately carry NO title --- the caption lives on the slide
(copyable text in slides_content.md, slides 11 and 12).

Entity colors fixed across the deck: LightGBM = blue, BiLSTM = orange
(reference palette slots 1-2, validated light mode). Re-run anytime to regenerate.
"""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ---- palette (reference instance, light mode, slots 1-2) ----
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK_P, INK_S, INK_M = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#ffffff"

WLEN = [20, 30, 40, 50, 60]
X = np.arange(5)

# ---- thesis Table 4.4 ----
mae_nbd_l = [1.013, 0.840, 0.738, 0.921, 0.932]
mae_nbd_b = [1.045, 0.873, 2.160, 1.551, 1.514]
mae_nrd_l = [2.256, 2.208, 2.183, 1.881, 1.751]
mae_nrd_b = [2.908, 4.127, 4.002, 4.751, 4.368]
# LightGBM cycles: mean of NBD & NRD (they differ by <1%)
cyc_l = [(a + b) / 2 for a, b in zip([72.6, 74.7, 77.1, 79.0, 81.3],
                                     [73.3, 75.4, 77.8, 79.6, 82.0])]
cyc_b = [838, 1250, 1670, 2080, 2500]  # identical on both datasets

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.edgecolor": BASELINE,
    "axes.linewidth": 1.0,
    "axes.labelcolor": INK_S,
    "xtick.color": INK_M,
    "ytick.color": INK_M,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


def style(ax):
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xticks(X)
    ax.set_xticklabels(WLEN)
    ax.set_xlabel("Window length (samples)")


def vlabel(ax, x, y, text, dy=3):
    """Direct label above a bar tip (endpoints / extremes only)."""
    ax.annotate(text, (x, y), xytext=(0, dy), textcoords="offset points",
                color=INK_P, ha="center", fontsize=9.5, fontweight="bold")


# ---------------- chart 3: MAE vs window length (grouped bars) ----------------
BAR_W, GAP = 0.34, 0.02
LOFF, BOFF = -(BAR_W + GAP) / 2, (BAR_W + GAP) / 2

fig, axs = plt.subplots(1, 2, figsize=(10.6, 3.9), dpi=220, sharey=True)
fig.subplots_adjust(wspace=0.16, left=0.065, right=0.975, top=0.86, bottom=0.15)

for ax, name, ml, mb, peak in zip(axs, ["NBD", "NRD"],
                                  [mae_nbd_l, mae_nrd_l],
                                  [mae_nbd_b, mae_nrd_b],
                                  [True, False]):
    ax.bar(X + LOFF, ml, BAR_W, color=BLUE)
    ax.bar(X + BOFF, mb, BAR_W, color=ORANGE)
    style(ax)
    ax.set_title(name, color=INK_P, fontweight="bold", fontsize=13,
                 loc="left", pad=8)
    # endpoint labels
    vlabel(ax, X[0] + LOFF, ml[0], f"{ml[0]:.2f}")
    vlabel(ax, X[0] + BOFF, mb[0], f"{mb[0]:.2f}")
    vlabel(ax, X[-1] + LOFF, ml[-1], f"{ml[-1]:.2f}")
    vlabel(ax, X[-1] + BOFF, mb[-1], f"{mb[-1]:.2f}")
    if peak:  # BiLSTM's NBD peak at wlen 40 - the extreme worth labeling
        vlabel(ax, X[2] + BOFF, mb[2], "2.16")

axs[0].set_ylim(0, 5.6)      # shared axis: identical scale on both panels
axs[0].set_ylabel("MAE (%)")
axs[1].tick_params(labelleft=True)  # show the shared-scale ticks on both panels

handles = [Line2D([0], [0], color=BLUE, lw=6),
           Line2D([0], [0], color=ORANGE, lw=6)]
fig.legend(handles, ["LightGBM (this work)", "BiLSTM (baseline)"],
           loc="upper center", frameon=False, ncol=2, handlelength=1.0,
           borderaxespad=0.1, fontsize=11)
fig.savefig(os.path.join(OUT, "fig_mae_vs_wlen.png"))
plt.close(fig)

# ---------------- chart 4: relative inference cost (ONE chart) ----------------
# Absolute cycles differ by ~30x, so a single linear axis would flatten the
# LightGBM bars to slivers. Both series are therefore indexed to wlen = 20
# (= 1.0); the absolute endpoint values are labeled on the bars.
cyc_l_rel = [c / cyc_l[0] for c in cyc_l]
cyc_b_rel = [c / cyc_b[0] for c in cyc_b]

fig, ax = plt.subplots(figsize=(10.6, 3.9), dpi=220)
fig.subplots_adjust(left=0.065, right=0.975, top=0.86, bottom=0.15)

ax.bar(X + LOFF, cyc_l_rel, BAR_W, color=BLUE)
ax.bar(X + BOFF, cyc_b_rel, BAR_W, color=ORANGE)
style(ax)
ax.set_ylim(0, 3.2)
ax.set_ylabel("Relative inference cost (wlen 20 = 1)")
# endpoint labels carry the absolute cycles; the wlen-20 baseline is the axis itself
vlabel(ax, X[-1] + LOFF, cyc_l_rel[-1], f"{cyc_l_rel[-1]:.2f}x ({cyc_l[-1]:.1f}k)")
vlabel(ax, X[-1] + BOFF, cyc_b_rel[-1], f"{cyc_b_rel[-1]:.2f}x ({cyc_b[-1]:,}k)")

handles = [Line2D([0], [0], color=BLUE, lw=6),
           Line2D([0], [0], color=ORANGE, lw=6)]
fig.legend(handles, ["LightGBM (this work)", "BiLSTM (baseline)"],
           loc="upper center", frameon=False, ncol=2, handlelength=1.0,
           borderaxespad=0.1, fontsize=11)

fig.savefig(os.path.join(OUT, "fig_cycles_vs_wlen.png"))
plt.close(fig)

print("bar charts written to", OUT)
