"""
Altera Digital Health Project 2: Sunrise CPOE Pharmacist Intervention Analytics
XmR (pharmacist intervention rate per 1000 orders) + p-chart (high-alert med override rate)
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

np.random.seed(75)

def intervention_xmr(n=24):
    base  = 18.4
    noise = np.random.normal(0, 0.6, n)
    x = base + noise
    x[3]  = 27.8   # Sunrise v22.1 formulary rebuild increases interventions
    x[11] = 11.2   # drug interaction rule optimisation reduces interventions
    x[20] = 28.4   # new resident cohort July increases interventions
    mr     = np.abs(np.diff(x))
    mr_bar = mr.mean()
    x_bar  = x.mean()
    sigma  = mr_bar / 1.128
    ucl    = x_bar + 3 * sigma
    lcl    = max(0.0, x_bar - 3 * sigma)
    return x, x_bar, ucl, lcl

def override_pchart(n=24):
    p_bar = 0.124
    ni    = 500
    ucl   = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / ni)
    lcl   = max(0.0, p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / ni))
    base  = np.random.normal(p_bar, 0.004, n)
    p     = np.clip(base, max(0, p_bar - 0.016), p_bar + 0.016)
    p[5]  = 0.178   # alert fatigue from new drug interaction panel
    p[13] = 0.072   # alert rationalization project reduces overrides
    p[21] = 0.184   # chemotherapy panel expansion increases overrides
    return p, p_bar, ucl, lcl

def plot_charts():
    months = [f"M{i+1}" for i in range(24)]
    x_vals, x_bar, ucl_x, lcl_x = intervention_xmr()
    p_vals, p_bar, ucl_p, lcl_p = override_pchart()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4))
    fig.patch.set_facecolor("white")

    # Left: Pharmacist Intervention Rate XmR
    ax1.set_facecolor(LGREY)
    ax1.plot(range(24), x_vals, color=BLUE, marker="o", markersize=4, linewidth=1.6, zorder=3)
    ax1.axhline(x_bar, color=TEAL, linestyle="--", linewidth=1.2, label=f"X-bar={x_bar:.1f}/1K")
    ax1.axhline(ucl_x, color=RED,  linestyle=":",  linewidth=1.2, label=f"UCL={ucl_x:.1f}/1K")
    ax1.axhline(lcl_x, color=RED,  linestyle=":",  linewidth=1.2, label=f"LCL={lcl_x:.1f}/1K")

    ooc = [i for i in range(24) if x_vals[i] > ucl_x or x_vals[i] < lcl_x]
    for i in ooc:
        ax1.plot(i, x_vals[i], "o", color=ORANGE, markersize=9, zorder=4)

    ann = {3: "Sunrise v22.1\nFormulary Rebuild", 11: "Interaction Rule\nOptimisation", 20: "Resident\nCohort July"}
    for i, lbl in ann.items():
        offset = 10 if x_vals[i] > x_bar else -28
        ax1.annotate(lbl, (i, x_vals[i]), textcoords="offset points",
                     xytext=(0, offset), fontsize=6.5, ha="center", color=ORANGE, fontweight="bold")

    # Intervention type mix
    cats   = ["Drug-Drug\n42.4%", "Dosing\n28.4%", "Allergy\n14.4%", "Duplication\n14.8%"]
    c_vals = [42.4, 28.4, 14.4, 14.8]
    c_col  = [BLUE, TEAL, ORANGE, RED]
    for j, (lbl, val, col) in enumerate(zip(cats, c_vals, c_col)):
        ax1.bar(14.8 + j * 2.1, val * 0.06, 1.6, bottom=lcl_x + 0.4,
                color=col, alpha=0.82, zorder=3)
        ax1.text(14.8 + j * 2.1, lcl_x + 0.4 + val * 0.06 + 0.2, lbl.split("\n")[1],
                 ha="center", fontsize=5.5, fontweight="bold")
        ax1.text(14.8 + j * 2.1, lcl_x - 0.8, lbl.split("\n")[0], ha="center", fontsize=5.5, color=col)

    ax1.set_xticks(range(24))
    ax1.set_xticklabels(months, fontsize=6.5, rotation=45)
    ax1.set_ylabel("Pharmacist Interventions per 1,000 CPOE Orders", fontsize=8)
    ax1.set_title("CPOE Pharmacist Intervention Rate XmR\n(X-bar=18.4/1K | Resident Cohort +10.0/1K | Rule Optimisation -7.2/1K | ISMP Canada)", fontsize=9, fontweight="bold", color=BLUE)
    ax1.legend(fontsize=7)
    ax1.grid(axis="y", alpha=0.4)
    ax1.tick_params(axis="y", labelsize=8)

    # Right: High-Alert Override p-chart
    ax2.set_facecolor(LGREY)
    ax2.plot(range(24), p_vals * 100, color=BLUE, marker="o", markersize=4, linewidth=1.6, zorder=3)
    ax2.axhline(p_bar * 100, color=TEAL, linestyle="--", linewidth=1.2, label=f"p-bar={p_bar*100:.1f}%")
    ax2.axhline(ucl_p * 100, color=RED,  linestyle=":",  linewidth=1.2, label=f"UCL={ucl_p*100:.1f}%")
    ax2.axhline(lcl_p * 100, color=RED,  linestyle=":",  linewidth=1.2, label=f"LCL={lcl_p*100:.1f}%")

    ooc_p = [i for i in range(24) if p_vals[i] > ucl_p or p_vals[i] < lcl_p]
    for i in ooc_p:
        ax2.plot(i, p_vals[i] * 100, "o", color=ORANGE, markersize=9, zorder=4)

    ann_p = {5: "Alert Fatigue\nNew Drug Panel", 13: "Alert\nRationalization", 21: "Chemo Panel\nExpansion"}
    for i, lbl in ann_p.items():
        offset = 12 if p_vals[i] > p_bar else -28
        ax2.annotate(lbl, (i, p_vals[i] * 100), textcoords="offset points",
                     xytext=(0, offset), fontsize=6.5, ha="center", color=ORANGE, fontweight="bold")

    ax2.set_xticks(range(24))
    ax2.set_xticklabels(months, fontsize=6.5, rotation=45)
    ax2.set_ylabel("High-Alert Medication CDS Alerts Overridden (%)", fontsize=8)
    ax2.set_title("High-Alert Medication Override Rate p-Chart\n(p-bar=12.4% | Alert Rationalization -5.2pp | Chemo Expansion +6.0pp | ISMP Canada)", fontsize=9, fontweight="bold", color=BLUE)
    ax2.legend(fontsize=7, loc="upper right")
    ax2.grid(axis="y", alpha=0.4)
    ax2.tick_params(axis="y", labelsize=8)

    fig.text(0.5, 0.01, "Nicholas Steven - github.com/nicholasstevenr",
             ha="center", fontsize=7, color="#888888", style="italic")
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    out = "/sessions/focused-epic-turing/mnt/job application/Applications/AlteraDigitalHealth/chart_p2.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out}")

if __name__ == "__main__":
    plot_charts()
