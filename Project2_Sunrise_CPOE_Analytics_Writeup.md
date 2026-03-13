# Project 2: Sunrise CPOE Pharmacist Intervention and High-Alert Override Analytics

**Employer:** Altera Digital Health | **Role:** Data Analyst, EHR Clinical Analytics
**Methods:** XmR Control Chart (Pharmacist Intervention Rate per 1,000 Orders) + p-Chart (High-Alert Medication Override Rate)
**Tools:** Python (numpy, matplotlib), SPC, ISMP Canada High-Alert Medication Standards

---

## Business Context

Altera Digital Health's Sunrise Acute EHR incorporates CPOE with integrated clinical decision support (CDS) for drug interaction checking, allergy screening, and high-alert medication alerts. The pharmacist intervention rate (per 1,000 CPOE orders) and the high-alert medication override rate are primary medication safety KPIs tracked in alignment with ISMP Canada standards. This project applied SPC to 24 months of Sunrise CPOE audit data — spanning drug-drug interactions (42.4%), dosing alerts (28.4%), allergy alerts (14.4%), and duplication alerts (14.8%) — to identify variation drivers and inform CDS governance.

---

## XmR Analysis: Pharmacist Intervention Rate per 1,000 CPOE Orders (X-bar = 18.4/1K)

The Individual (X) chart tracked monthly pharmacist interventions triggered by Sunrise CPOE. Control limits: X-bar ± 3σ (σ = MR-bar / 1.128).

**Out-of-Control Events:**

1. **Month 4 — Sunrise v22.1 Formulary Rebuild (above UCL, 27.8/1K):** The v22.1 update included a full formulary rebuild with 312 new drug entries, 28 revised dosing protocols, and 44 new drug interaction rules. The intervention rate spiked 9.4/1K above X-bar as pharmacists responded to a high volume of newly triggered alerts. Action: priority triage queue established in pharmacy to manage surge volume.

2. **Month 12 — Drug Interaction Rule Optimisation (below LCL, 11.2/1K):** A systematic CDS rule rationalisation project — eliminating 61 low-specificity drug interaction rules that generated clinically irrelevant alerts — reduced the intervention rate 7.2/1K below X-bar. Signal confirmed as a favourable special cause; rule library updated quarterly thereafter.

3. **Month 21 — New Resident Cohort July (above UCL, 28.4/1K):** Annual July resident cohort turnover produced a predictable spike: 124 new residents unfamiliar with Sunrise CPOE order entry generated 10.0/1K above X-bar in pharmacist interventions. Corrective action: Sunrise CPOE orientation module added to resident onboarding curriculum, reducing the Month 22 spike by 40% in the following year.

---

## p-Chart Analysis: High-Alert Medication CDS Override Rate (p-bar = 12.4%, n = 500/month)

The p-chart tracked the proportion of Sunrise high-alert medication CDS alerts that were overridden by the ordering physician without documented clinical justification. UCL/LCL: p-bar ± 3√(p-bar(1−p-bar)/n).

**Out-of-Control Events:**

1. **Month 6 — Alert Fatigue from New Drug Interaction Panel (above UCL, 17.8%):** Following the Sunrise v22.1 formulary rebuild, 44 new drug interaction rules generated a 38% increase in daily CDS alerts within the first 60 days. Override rate rose 5.4pp above UCL — a classic alert fatigue signal. Response: low-value alerts suppressed via a 60-day override audit; 19 rules de-activated.

2. **Month 14 — Alert Rationalisation Project (below LCL, 7.2%):** Following the de-activation of 19 low-specificity rules, the remaining alerts carried higher clinical relevance. Override rate fell 5.2pp below LCL — confirming that alert burden reduction improved meaningful alert adherence. Published internally as a CDS governance case study.

3. **Month 22 — Chemotherapy Panel Expansion (above UCL, 18.4%):** Expansion of the Sunrise oncology CPOE panel added 84 new chemotherapy protocols with complex drug interaction rules unfamiliar to non-oncology prescribers. Override rate rose 6.0pp above UCL. Corrective action: oncology-specific CPOE training deployed; pharmacist co-signature requirement added for high-alert chemotherapy orders.

---

## Key Findings & Impact

- Pharmacist intervention rate averaged 18.4/1K orders — with seasonal July cohort peaks and CDS rule changes as dominant assignable causes.
- Alert rationalisation reduced the override rate from 17.8% to 7.2% — a 59% relative reduction — demonstrating that fewer, more specific alerts improve clinical adherence more effectively than comprehensive rule coverage.
- SPC-based CDS governance framework presented to the Pharmacy and Therapeutics Committee; quarterly rule rationalisation cycle adopted organisation-wide.
- Resident CPOE onboarding module reduced July cohort intervention spike by 40% in the subsequent year, quantifying the value of targeted training.
