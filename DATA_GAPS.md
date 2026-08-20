# Empirical Data Gaps & Methodological Treatment Plan

**Project**: Physician Exodus from Tunisia: Workforce Projections, Policy Simulation, and Economic Evaluation to 2050  
**Document**: `DATA_GAPS.md`  
**Classification**: Empirical Audit & Data Governance Document  
**Date**: 2026-08-20  

---

## 1. Overview & Data Hierarchy

In accordance with strict reproducible research standards, all data inputs are audited and organized following the formal 7-tier data governance hierarchy:

```
+---------------------------------------------------------------------------------------------------+
|                                 DATA SOURCE GOVERNANCE HIERARCHY                                  |
+-------+-------------------------------------------------------------------------------------------+
| Tier  | Source Category & Description                                                             |
+-------+-------------------------------------------------------------------------------------------+
| Tier 1| Official Tunisian administrative/statistical data (INS, Ministry of Health, CNOM, MESRS)  |
| Tier 2| Multilateral databases (WHO NHWA, World Bank, UNESCO, OECD Health Statistics)             |
| Tier 3| Peer-reviewed Tunisian empirical studies & microdata (Ben Romdhane 2022, Dhouib 2024)     |
| Tier 4| Peer-reviewed North African & Maghreb comparative studies (Sylla 2021, El Morabety 2022)  |
| Tier 5| International peer-reviewed meta-analyses & DCEs (Mandeville 2014, Docquier 2014)         |
| Tier 6| Professional medical associations & trade unions (OTJM, STML, Syndicat des Médecins)     |
| Tier 7| Media reports (corroboration & triangulation only; strictly prohibited as behavioral base)|
+-------+-------------------------------------------------------------------------------------------+
```

---

## 2. Comprehensive Data Audit & Gap Analysis

| Variable Name | Required? | Available? | Source & Identifier | Coverage Years | Limitations & Measurement Issues | Proposed Methodological Treatment |
| :--- | :---: | :---: | :--- | :--- | :--- | :--- |
| **National Total Physician Stock** | **Yes** | **Yes** | Institut National de la Statistique (`SRC_INS_STAT123`) | 2017–2024 (Annual) | Raw administrative count includes cumulative non-purged inactive/emigrated registrations ("ghost registrations"). | Apply Active Practice Ratio ($\alpha \sim \text{Uniform}[0.85, 0.90]$, base $\alpha = 0.88$) as initial filter at $t_0 = 2020$. Dynamic stock-flow conservation thereafter. |
| **Public-Sector Physician Stock** | **Yes** | **Yes** | INS & Ministère de la Santé (`SRC_INS_STAT123`, `SRC_MS_CARTE2023`) | 2017–2024 (Annual) | Disaggregated by sector, but joint cross-tabulation with detailed age brackets is not published continuously. | Use marginal totals as calibration targets; synthesize multi-way cells using Iterative Proportional Fitting (IPF). |
| **Private-Sector Physician Stock** | **Yes** | **Yes** | INS (`SRC_INS_STAT123`) | 2017–2024 (Annual) | Annual headcounts available; sub-national distribution less frequently updated than public sector. | Retain INS official counts (e.g., 9,197 in 2023); calibrate private sector transition rates in baseline model. |
| **Physician Stock by Governorate** | **Yes** | **Yes** | Ministère de la Santé, *Carte Sanitaire* (`SRC_MS_CARTE2023`) | 2020–2023 | High detail for public hospital staff; private sector governorate breakdowns are intermittent. | Aggregate 24 governorates into 2 robust planning macro-strata: Coastal/Metropolitan vs. Interior/Underserved. |
| **Resident Population by Governorate** | **Yes** | **Yes** | Institut National de la Statistique (`SRC_INS_STAT111`) | 2015–2023 (Projections to 2050) | Official census conducted decennially; intercensal figures are demographic model estimates. | Ingest official INS demographic series and projections to 2050 by governorate and age/sex strata. |
| **Physician Emigration Flows** | **Yes** | **Yes** | Conseil National de l'Ordre des Médecins (`SRC_CNOM_ANN`) | 2015–2024 (Annual) | Certificates of Good Standing (*Attestations de bonne conduite*) measure administrative clearance, not physical exit timestamp. | Apply Administrative Clearance Multiplier ($\lambda_{\text{exit}} \sim \text{Uniform}[0.65, 0.90]$, base $\lambda_{\text{exit}} = 0.75$), cross-validated with French/German registries. |
| **Destination Physician Entries (France)** | **Yes** | **Yes** | French DREES & RPPS Open Data (`SRC_DREES_RPPS`) | 2015–2024 (Annual) | Tracks foreign-trained practitioners (PADHUE); administrative reporting lag of 12–18 months. | Ingest as independent external directional validation target for realized outflows. |
| **Destination Physician Entries (Germany)**| **Yes** | **Yes** | Bundesärztekammer Ärztestatistik (`SRC_BAK_ARZTE`) | 2015–2024 (Annual) | Disaggregated by country of medical degree; covers *Approbation* and *Berufserlaubnis*. | Ingest as secondary external directional validation check. |
| **Medical Faculty Intake & Quotas** | **Yes** | **Yes** | Ministère de l'Enseignement Supérieur & JORT (`SRC_MESRS_JORT`) | 2015–2025 (Annual) | *Numerus clausus* and residency quotas published in JORT; annual curriculum dropout rates not in open data. | Ingest official quotas (4 faculties); parameterize completion rate ($\sim 92\%$) using Beta distribution. |
| **Return Migration Inflows** | **Yes** | **No** | None (No dedicated registry exists in Tunisia) | None | Physicians returning from abroad re-enter CNOM licensure without a dedicated "returnee" tracking code. | Classify as Class D/E structural assumption (1.0%–3.0% annual return rate among expatriates); test in PSA. |
| **Discrete Choice / Preference Microdata** | **Yes** | **Partial** | Ben Romdhane 2022 (`SRC_SURV_ROMDHANE`), Dhouib 2024 (`SRC_SURV_DHOUIB`) | 2022, 2024 | Surveys measure cross-sectional intention odds ratios; no national stated-preference experimental DCE exists. | Borrow relative weights from LMIC DCE meta-analysis (Mandeville 2014); convert survey ORs to RRs via Zhang & Yu (1998); calibrate 2 global scalars. |
| **Unit Educational Cost per Physician** | **Yes** | **Partial** | MESRS Budget Reports & UNESCO Database | 2018–2023 | Aggregate university operating expenditures available; faculty-specific medical cost per student not separated. | Use Human Capital replacement methodology based on higher education unit costs; apply 40% resident clinical labor offset. |
| **Public Sector Statutory Retirements** | **Yes** | **Partial** | Ministère de la Santé & CNRPS | 2018–2023 | General civil service retirement age (62–65 yrs) fixed by law; exact specialty retirement panel not open. | Model statutory exit deterministically at career stage Senior ($55+$ yrs) using baseline exit rates ($2.0\%\text{--}2.5\%$/yr). |

---

## 3. Data Integration & Validation Protocols

1. **Zero Data Fabrication**: Where longitudinal data points are unobserved (e.g., return migration or sub-specialty private practice rosters), parameters are explicitly coded as bounded structural priors in `ASSUMPTIONS.md` and evaluated through 1,000-draw Probabilistic Sensitivity Analysis (PSA).
2. **Iterative Proportional Fitting (IPF)**: The 36-cell baseline state tensor at $t_0 = 2020$ is generated via 2D raking to match INS national public/private totals and *Carte Sanitaire* regional distributions exactly.
3. **No Spurious Precision**: All reporting maintains standard demographic conservation identities and disaggregates outcomes across the 36-cell parsimonious space without creating empty or unstable strata.
