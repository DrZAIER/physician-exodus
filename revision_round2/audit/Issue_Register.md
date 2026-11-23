# Issue Register

**Revision:** 2.0
**Status key:** Closed = corrected and re-run; Documented = retained as a limitation; Open = unresolved and requiring author or external data.

| ID | Issue | Severity | Action taken | Status |
|---|---|---|---|---|
| A1 | Pipeline non-entry was treated as international emigration | Major | Added φ; split pre-entry international emigration and domestic non-entry; only international emigration enters the pool | Closed |
| A2 | Destination-stock screen presented as identification/validation | Major | Relabelled as plausibility screen; results reported with and without; no validation claim | Closed |
| A3 | Five-year postgraduate lag not audited | Major | Labelled assumption; 3–7 year sensitivity; code timing made explicit | Closed |
| A4 | Retirement shift discretized; 1.5 and 2 years identical | Moderate | Continuous interpolation implemented; sensitivity table | Closed |
| A5 | 2008 age distribution reconstructed from registered physicians | Moderate | Labelled reconstruction; younger/older age-shape sensitivity | Documented |
| A6 | 1 900 graduate figure unverified and mislabelled as ministerial | Major | Removed from main analysis; identified as unverified press report | Closed |
| A7 | 30% admissions expansion described as practising-physician increase | Moderate | Text clarifies admissions vs graduates vs practising physicians | Closed |
| A8 | 2017 observed 14 892 vs modelled 14 928 | Minor | Table note distinguishes observed and simulated; over-prediction reported | Closed |
| A9 | Density 1.26 vs 1.27 | Minor | Deterministic and MC densities now both 1.25; labels clarify | Closed |
| A10 | δ central 0.08 vs MC mean 0.095 | Moderate | MC prior changed to uniform 0.04–0.12 (mean 0.08); wider sensitivity retained | Closed |
| A11 | Deterministic and MC physician-years mixed | Moderate | Tables label deterministic vs MC separately | Closed |
| A12 | Emigration cap 0.35 might bind | Minor | Diagnostic added; maximum hazard 0.057; cap does not bind | Closed |
| A13 | Initial pool fixed in MC but varied in sensitivity | Moderate | Initial pool added as MC prior (2 000–8 000) | Closed |
| A14 | Flow identity under scenarios | Moderate | Validated for all scenarios; pipeline identity added | Closed |
| A15 | PRCC sign/interpretation | Major | True PRCC by rank residualisation; marginal Spearman reported separately; calibration ridge explained | Closed |
| A16 | Cost analysis mixed transfers and resource costs | Major | Fiscal/resource split; caveats; not called cost-effectiveness | Closed |
| A17 | Return scenario treated as comparable to retention | Major | Central φ shows return below training; ranking uncertainty reported | Closed |
| A18 | Policy ranking presented as robust | Major | Rank distribution computed; only combined/remuneration robust; career/training/return overlap | Closed |
| A19 | Reporting checklist incomplete | Moderate | Item-level 30-item checklist in Table S13 | Closed |
| A20 | Author metadata placeholders | Required | Firas Zaier and Mariem Zribi metadata applied exactly; third author removed | Closed |
| A21 | Declarations invented or incomplete | Required | Contributions, funding, competing interests, acknowledgements retained as placeholders | Open (author action) |
| A22 | Repository DOI placeholder | Required | Data availability statement flagged as pending | Open (author action) |
| A23 | Reference details unverified for some sources | Moderate | Reference audit created; key empirical claims checked; media sources flagged | Documented |
| A24 | 2020–2021 discontinuity attribution | Moderate | Described as unresolved; no assertion of reporting artefact | Documented |
| A25 | Temporary vs permanent migration | Moderate | Modelled implicitly via return retention/attrition; limitation stated | Documented |
| A26 | No external validation | Moderate | Explicitly stated; no validation claim | Documented |

---

## Round 2 issues (v2.1.0)

| ID | Issue | Severity | Action taken | Status |
|---|---|---|---|---|
| R2-1 | Return-pool accounting inconsistent with reported 20% eventual return and 10-year duration | Major | Corrected metrics: 20% attempt, 17.5% success, 10.3 years; added no-recycling sensitivity | Closed |
| R2-2 | Remuneration “robustly” outperforms training, but at φ=0 it is 27 below training | Major | Bounded claim to Monte Carlo φ prior; explicit φ=0 exception in Abstract, Results, Discussion, Conclusion | Closed |
| R2-3 | Policy effect sizes presented too confidently | Major | Added conservative effect grid; 10% remuneration, 5% career, 1.35× return below training; only combined above | Closed |
| R2-4 | Training scenario could be read as the announced admissions policy | Major | Relabelled hypothetical graduate-output expansion; completion 80–100% sensitivity | Closed |
| R2-5 | Initial return-eligible pool anchored to OECD country-of-birth estimate | Major | Reframed as illustrative anchor, not lower bound or measured population; 2 000–8 000 sensitivity | Closed |
| R2-6 | 2020–2023 residual and endpoint not sufficiently interrogated | Moderate | Added 2019/2022 calibration endpoints; residual described as unresolved, not migration evidence | Closed |
| R2-7 | Age structure uncertainty underemphasised | Major | 14 961–16 570 range added to Abstract, Results, Discussion, limitations | Closed |
| R2-8 | Administrative/press indicators compared loosely | Moderate | Defined 374 as annualised H1 2023 removal requests; press estimates near φ=1 upper bound only | Closed |
| R2-9 | Cost analysis mixed fiscal and resource categories | Moderate | Removed cost from Table 5/abstract; moved panel to Fig. S2; explicit non-comparability | Closed |
| R2-10 | PRCC stability not documented | Moderate | Bootstrap 90% intervals from 1 000 resamples; conditional interpretation stated | Closed |
| R2-11 | Flow decomposition cohort year ambiguous | Minor | Added 2019 cohort (1 091) note; 2024 cohort (1 305) enters 2029 | Closed |
| R2-12 | Calibration could be read as validation | Minor | Calibration labelled fitting condition; QA wording corrected | Closed |
