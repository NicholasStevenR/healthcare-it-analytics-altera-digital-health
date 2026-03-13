"""
Altera Digital Health Project 1: Paragon EHR Clinical Documentation Analytics
XmR (clinical note completion rate) + p-chart (late/incomplete discharge summary rate)
Author: Nicholas Steven | github.com/nicholasstevenr
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE   = "#1F4E79"
ORANGE = "#E36C09"
TEAL   = "#00B0A8"
RED    = "#C00000"
LGREY  = "#F2F2F2"

np.random.seed(74)

def note_completion_xmr(n=24):
    base  = 92.4
    noise = np.random.normal(0, 0.7, n)
    x = base + noise
    x[4]  = 82.8   # Paragon v16.0 migration disruption
    x[12] = 97.4   # Physician Champion documentation initiative
    x[20] = 82.2   # ED surge staffing gap
    mr     = np.abs(np.diff(x))
    mr_bar = mr.mean()
    x_bar  = x.mean()
    sigma  = mr_bar / 1.128
    ucl    = min(100.0, x_bar + 3 * sigma)
    lcl    = max(0.0,   x_bar - 3 * sigma)
    return x, x_bar, ucl, lcl

def discharge_summary_pchart(n=24):
    p_bar = 0.084
    ni    = 400
    ucl   = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / ni)
    lcl   = max(0.0, p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / ni))
    base  = np.random.normal(p_bar, 0.003, n)
    p     = np.clip(base, max(0, p_bar - 0.012), p_bar + 0.012)
    p[5]  = 0.132   # parallel operation confusion during migration
    p[13] = 0.046   # Dragon Medical One AI integration
    p[21] = 0.138   # attending physician turnover surge
    return p, p_bar, ucl, lcl

def plot_charts():
    months = [f"M{i+1}" for i in range(24)]
    x_vals, x_bar, ucl_x, lcl_x = note_completion_xmr()
    p_vals, p_bar, ucl_p, lcl_p = discharge_summary_pchart()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4))
    fig.patch.set_facecolor("white")

    # Left: Note Completion XmR
    ax1.set_facecolor(LGREY)
    ax1.plot(range(24), x_vals, color=BLUE, marker="o", markersize=4, linewidth=1.6, zorder=3)
    ax1.axhline(x_bar, color=TEAL, linestyle="--", linewidth=1.2, label=f"X-bar={x_bar:.1f}%")
    ax1.axhline(ucl_x, color=RED,  linestyle=":",  linewidth=1.2, label=f"UCL={ucl_x:.1f}%")
    ax1.axhline(lcl_x, color=RED,  linestyle=":",  linewidth=1.2, label=f"LCL={lcl_x:.1f}%")

    ooc = [i for i in range(24) if x_vals[i] > ucl_x or x_vals[i] < lcl_x]
    for i in ooc:
        ax1.plot(i, x_vals[i], "o", color=ORANGE, markersize=9, zorder=4)

    ann = {4: "Paragon v16\nMigration", 12: "Physician\nChampion Init.", 20: "ED Surge\nStaffing Gap"}
    for i, lbl in ann.items():
        offset = 10 if x_vals[i] > x_bar else -28
        ax1.annotate(lbl, (i, x_vals[i]), textcoords="offset points",
                     xytext=(0, offset), fontsize=6.5, ha="center", color=ORANGE, fontweight="bold")

    # Department mix
    cats   = ["Medicine\n38.4%", "Surgery\n28.4%", "ED\n18.4%", "ICU\n14.8%"]
    c_vals = [38.4, 28.4, 18.4, 14.8]
    c_col  = [BLUE, TEAL, ORANGE, RED]
    for j, (lbl, val, col) in enumerate(zip(cats, c_vals, c_col)):
        ax1.bar(14.8 + j * 2.1, val * 0.06, 1.6, bottom=lcl_x + 0.4,
                color=col, alpha=0.82, zorder=3)
        ax1.text(14.8 + j * 2.1, lcl_x + 0.4 + val * 0.06 + 0.2, lbl.split("\n")[1],
                 ha="center", fontsize=5.5, fontweight="bold")
        ax1.text(14.8 + j * 2.1, lcl_x - 1.2, lbl.split("\n")[0], ha="center", fontsize=5.5, color=col)

    ax1.set_xticks(range(24))
    ax1.set_xticklabels(months, fontsize=6.5, rotation=45)
    ax1.set_ylabel("Clinical Notes Completed within 24h of Encounter (%)", fontsize=8)
    ax1.set_title("Clinical Documentation Completion Rate XmR\n(X-bar=92.4% | Physician Champion +5.0pp | Migration -9.6pp | Accreditation Standard)", fontsize=9, fontweight="bold", color=BLUE)
    ax1.legend(fontsize=7)
    ax1.grid(axis="y", alpha=0.4)
    ax1.tick_params(axis="y", labelsize=8)

    # Right: Discharge Summary p-chart
    ax2.set_facecolor(LGREY)
    ax2.plot(range(24), p_vals * 100, color=BLUE, marker="o", markersize=4, linewidth=1.6, zorder=3)
    ax2.axhline(p_bar * 100, color=TEAL, linestyle="--", linewidth=1.2, label=f"p-bar={p_bar*100:.1f}%")
    ax2.axhline(ucl_p * 100, color=RED,  linestyle=":",  linewidth=1.2, label=f"UCL={ucl_p*100:.1f}%")
    ax2.axhline(lcl_p * 100, color=RED,  linestyle=":",  linewidth=1.2, label=f"LCL={lcl_p*100:.1f}%")

    ooc_p = [i for i in range(24) if p_vals[i] > ucl_p or p_vals[i] < lcl_p]
    for i in ooc_p:
        ax2.plot(i, p_vals[i] * 100, "o", color=ORANGE, markersize=9, zorder=4)

    ann_p = {5: "Parallel Op.\nConfusion", 13: "Dragon Medical\nAI Integration", 21: "Attending\nTurnover Surge"}
    for i, lbl in ann_p.items():
        offset = 12 if p_vals[i] > p_bar else -28
        ax2.annotate(lbl, (i, p_vals[i] * 100), textcoords="offset points",
                     xytext=(0, offset), fontsize=6.5, ha="center", color=ORANGE, fontweight="bold")

    ax2.set_xticks(range(24))
    ax2.set_xticklabels(months, fontsize=6.5, rotation=45)
    ax2.set_ylabel("Discharge Summaries Late or Incomplete (%)", fontsize=8)
    ax2.set_title("Late/Incomplete Discharge Summary p-Chart\n(p-bar=8.4% | Dragon Medical AI -3.8pp | Migration +4.8pp | OHA Continuity Standard)", fontsize=9, fontweight="bold", color=BLUE)
    ax2.legend(fontsize=7, loc="upper right")
    ax2.grid(axis="y", alpha=0.4)
    ax2.tick_params(axis="y", labelsize=8)

    fig.text(0.5, 0.01, "Nicholas Steven - github.com/nicholasstevenr",
             ha="center", fontsize=7, color="#888888", style="italic")
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    out = "/sessions/focused-epic-turing/mnt/job application/Applications/AlteraDigitalHealth/chart_p1.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out}")

if __name__ == "__main__":
    plot_charts()
