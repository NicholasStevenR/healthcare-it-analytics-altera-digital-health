# Project 1: Paragon EHR Clinical Documentation Completion Analytics

**Employer:** Altera Digital Health | **Role:** Data Analyst, EHR Clinical Analytics
**Methods:** XmR Control Chart (Clinical Note Completion Rate) + p-Chart (Late/Incomplete Discharge Summary Rate)
**Tools:** Python (numpy, matplotlib), SPC, OHA Continuity of Care Standards, Accreditation Canada

---

## Business Context

Altera Digital Health's Paragon EHR is deployed across mid-sized community hospitals in Ontario and Western Canada. Clinical documentation completeness — measured by timely note completion and discharge summary quality — is a core accreditation KPI and a patient safety indicator for continuity of care. This project applied SPC to 24 months of Paragon clinical documentation audit data across Medicine (38.4%), Surgery (28.4%), ED (18.4%), and ICU (14.8%) departments to identify variation drivers and support go-live planning for future Paragon migrations.

---

## XmR Analysis: Clinical Note Completion Rate (X-bar = 92.4%)

The Individual (X) chart tracked the monthly proportion of clinical encounter notes completed within 24 hours. Control limits: X-bar ± 3σ (σ = MR-bar / 1.128).

**Out-of-Control Events:**

1. **Month 5 — Paragon v16.0 Migration Disruption (below LCL, 82.8%):** The go-live of Paragon v16.0 introduced a restructured charting workflow that required physicians to re-learn 14 documentation templates. Completion rate fell 9.6pp below X-bar during the parallel operation period. Root cause: insufficient physician super-user training hours pre-go-live. Corrective action: at-elbow support extended by 3 weeks; completion recovered to baseline within 5 weeks.

2. **Month 13 — Physician Champion Documentation Initiative (above UCL, 97.4%):** A structured Physician Champion programme — with peer-led educational sessions, real-time completion dashboards, and departmental scorecards — drove completion 5.0pp above UCL. Sustained improvement maintained for 6 consecutive months, consistent with a special-cause shift.

3. **Month 21 — ED Surge Staffing Gap (below LCL, 82.2%):** A sustained ED surge combined with a nursing agency contract gap led to 34% of physicians completing documentation outside the 24-hour window due to workload. Completion fell 10.2pp below X-bar. Corrective action: asynchronous voice-to-text documentation pilot (Dragon Medical One) fast-tracked in ED.

---

## p-Chart Analysis: Late/Incomplete Discharge Summary Rate (p-bar = 8.4%, n = 400/month)

The p-chart tracked the proportion of hospital discharges with late (>48h) or incomplete discharge summaries. UCL/LCL calculated as p-bar ± 3√(p-bar(1−p-bar)/n).

**Out-of-Control Events:**

1. **Month 6 — Parallel Operation Confusion During Migration (above UCL, 13.2%):** During the Paragon v16.0 parallel operation period, attending physicians occasionally completed discharge summaries in the legacy system rather than Paragon, resulting in reconciliation failures. Discharge summary incompleteness rose 4.8pp above UCL. Resolution: legacy system write access disabled at 4 weeks post-go-live.

2. **Month 14 — Dragon Medical One AI Integration (below LCL, 4.6%):** Rollout of Dragon Medical One ambient AI scribing across Medicine and Surgery reduced discharge summary completion time from 18 minutes to 6 minutes per patient. Incompleteness fell 3.8pp below LCL — a sustained quality improvement signal. Dragon adoption reached 78% of attending physicians within 6 months.

3. **Month 22 — Attending Physician Turnover Surge (above UCL, 13.8%):** A cluster of 12 attending physician departures within 6 weeks created a documentation gap during onboarding of new physicians unfamiliar with Paragon's discharge summary workflow. Incompleteness rose 5.4pp above UCL. Corrective action: Paragon-specific discharge summary training added to physician onboarding checklist.

---

## Key Findings & Impact

- Clinical note completion averaged 92.4% — 7.6pp below the Accreditation Canada 100% standard, with three distinct assignable causes identified.
- Dragon Medical One adoption produced the largest sustained improvement: -3.8pp discharge incompleteness and an estimated 240 physician-hours per month saved across the 400-patient cohort.
- SPC-based migration impact analysis directly informed go-live planning for two subsequent Paragon deployments: at-elbow support hours increased 40% and mandatory parallel-period training was added.
- Physician Champion scorecard programme adopted organisation-wide following the Month 13 above-UCL signal.
