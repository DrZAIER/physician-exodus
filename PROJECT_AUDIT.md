# Critical Scientific Audit: Physician Exodus from Tunisia Project Specification

**Target Document**: `PROJECT_SPEC.md`  
**Auditor**: Senior Health Economist, Health Workforce Modeller, and Biostatistician  
**Status**: Formal Independent Pre-Implementation Audit  
**Date**: 2026-08-20  

---

## Executive Summary

The project specification (`PROJECT_SPEC.md`) outlines an ambitious, highly policy-relevant research design aimed at modeling physician emigration from Tunisia and projecting workforce, sectoral, geographic, and economic outcomes through 2050. It appropriately mandates the integration of established international frameworks (WHO Health Labour Market Framework, push-pull theory, macro-meso-micro hierarchy, random-utility choice modeling, dynamic stock-flow simulation, and cost-consequence/cost-effectiveness evaluation).

However, an exhaustive methodological audit identifies several critical bottlenecks across **parameter identifiability**, **causal identification**, **data availability**, **state-space dimensionality**, and **economic evaluation structure**. If left unaddressed prior to implementation, these vulnerabilities will expose the project to severe peer-reviewer objections, computational instability, and spurious policy recommendations.

This audit details the findings across eight evaluation criteria and provides concrete, publication-grade recommendations.

---

## 1. Scientific Feasibility

### 1.1. Feasibility of Translating Multidimensional Determinants into Dynamic Flows
- **The Core Challenge**: The specification proposes modeling annual migration probability via a random-utility formulation:
  $$\Delta V_{i,t} = \beta_0 + \beta_{\text{macro}} X_{\text{macro},i,t} + \beta_{\text{meso}} X_{\text{meso},i,t} + \beta_{\text{micro}} X_{\text{micro},i,t} + \beta_{\text{pull}} X_{\text{pull},i,t} + \beta_{\text{peer}} X_{\text{peer},i,t}$$
  While conceptually sound (grounded in Sousa et al., 2023, [DOI: 10.1186/s12960-023-00810-7](https://doi.org/10.1186/s12960-023-00810-7)), dynamically simulating this equation forward over 25 years (to 2050) requires forecasting future values for all constituent $X$ variables across cohorts.
- **Feasibility Assessment**: Forecasting micro-level personal circumstances, hospital-level equipment stockouts, and peer network exposure for 25 annual steps creates an unmanageable propagation of arbitrary forecast assumptions.
- **Remedy**: The micro-meso-macro framework must be implemented as a **structural elasticity index** at baseline with policy counterfactuals represented as discrete scenario shifts in relative utility $\Delta V$, rather than attempting to generate dynamic 25-year time-series forecasts of unobservable individual attributes.

### 1.2. Feasibility of the 2050 Projection Horizon
- **Scientific Horizon Justification**: Projecting health workforce dynamics over a 25–30 year horizon is standard in health labor market planning because medical training pipelines require 9–12 years from matriculation to specialty practice (AAMC, 2020, [PubMed: 33913440](https://pubmed.ncbi.nlm.nih.gov/33913440/); WHO, 2021, [WHO IRIS: 9789240035546](https://iris.who.int/bitstream/handle/10665/348069/9789240035546-eng.pdf)).
- **Feasibility Assessment**: The 2050 horizon is scientifically valid **only** if explicitly framed as a conditional counterfactual simulation (i.e., *"What happens if policy X vs. Y is maintained under explicit demographic scenarios?"*) rather than an unconditional deterministic forecast. Milestone reporting at 2030, 2040, and 2050 is essential to capture short-, medium-, and long-term lag dynamics.

---

## 2. Parameter Identifiability

### 2.1. Overparameterization and Empirical Unidentifiability
- **The Issue**: The aggregate historical calibration dataset consists of annual national physician stock (2015–2024, $N \approx 10$ time points) and reported annual departures (~1,450 in 2024; multi-year aggregates for 2015–2020 and 2021–2024; [Tunisie Tribune, 2025](https://www.tunisie-tribune.com/2025/01/07/1450-medecins-ont-quitte-la-tunisie-en-2024/)).
- **Identifiability Failure**: Estimating independent coefficients for $\beta_{\text{macro}}$, $\beta_{\text{meso}}$, $\beta_{\text{micro}}$, $\beta_{\text{pull}}$, $\beta_{\text{peer}}$, and baseline intercepts $\beta_0$ from ~10 macro data points is mathematically impossible due to severe degrees-of-freedom deficit and collinearity (equifinality).
- **Remedy**:
  1. The behavioral relative utility weights ($\beta$) must be established *a priori* from microeconometric literature / discrete-choice evidence (e.g., Mandeville et al., 2014, [DOI: 10.1016/j.socscimed.2014.06.019](https://doi.org/10.1016/j.socscimed.2014.06.019); Ben Romdhane et al., 2022, [DOI: 10.1186/s12913-022-08630-y](https://doi.org/10.1186/s12913-022-08630-y)).
  2. Historical calibration must be restricted to estimating a low-dimensional structural parameter vector: the baseline migration scale parameter, the structural regime shift intercept ($\Delta \beta_{2021+}$), and the reporting/observation multiplier.

### 2.2. Unidentifiability of the Observation/Definition Factor
- **The Issue**: Section 6 proposes: $\text{Observed reported departures} = \text{true migration flow} \times \text{observation factor}$.
- **Identifiability Failure**: When both the true flow and the observation factor are unknown, their product is fundamentally unidentified without external anchoring.
- **Remedy**: Triangulate Tunisian CNOM good-standing certificate requests with destination country foreign physician entry records (French DREES/RPPS and German Bundesärztekammer Ärztestatistik) to constrain the observation factor within a defensible empirical prior (e.g., Uniform[0.70, 0.95]).

### 2.3. Return Migration Probability
- **The Issue**: Return migration from Europe or the Gulf is noted in the conceptual framework, but Tunisia possesses no systematic registry of returning physicians.
- **Identifiability Failure**: Attempting to estimate return probabilities freely during calibration will destabilize the Markov transition matrix.
- **Remedy**: Formally classify return migration as a Class D (structural assumption) or Class E (scenario parameter) in the Parameter Provenance Registry, and set base-case return rates to conservative literature-derived bounds (e.g., 1–3% annual return among expatriates), subjected to comprehensive sensitivity analysis.

---

## 3. Data Availability & Gaps

| Data Component | Available Empirical Data | Data Gaps / Limitations | Methodological Mitigation |
| :--- | :--- | :--- | :--- |
| **National Stock** | Annual headcounts (Total, Public, Private) from INS ([INS Stat 123](https://ins.tn/en/statistiques/123)). | Joint cross-tabulations (Age $\times$ Specialty $\times$ Sector) are not published as a continuous panel. | Use iterative proportional fitting (IPF / raking) to synthesize marginal distributions from *Carte Sanitaire* and INS into a consistent base-year tensor. |
| **Regional Distribution** | Governorate physician headcounts from *Carte Sanitaire 2023* ([Ministère de la Santé, 2023](https://santetunisie.rns.tn/images/carte-sanitaire-2023.pdf)) & INS Population ([INS Stat 111](https://www.ins.tn/statistiques/111)). | Public sector only at governorate level; private sector regional counts are less frequently updated. | Model geographic redistribution across 7 planning regions (District of Tunis, North East, North West, Center East, Center West, South East, South West) rather than 24 governorates to preserve statistical stability. |
| **Emigration Flows** | CNOM reported departures (~1,450 in 2024; ~6,000 in 2021–2024; [Tunisie Tribune, 2025](https://www.tunisie-tribune.com/2025/01/07/1450-medecins-ont-quitte-la-tunisie-en-2024/)). | Certificates of good standing represent intent/clearance, not realized border exit timestamps. | Explicitly model certificate requests with an empirical realization factor ($\kappa$) cross-validated against French and German immigration registries. |
| **Training Pipeline** | Faculty admission quotas and residency openings (*JORT* ministerial decrees). | Attrition/dropout rates between 1st year and thesis completion are not systematically compiled in open data. | Use published faculty estimates (4 medical faculties: Tunis, Sousse, Monastir, Sfax) and parameterize completion rates with beta distributions. |
| **Discrete Choice / Preferences** | Cross-sectional surveys on young doctors/residents (Ben Romdhane et al., 2022, [DOI: 10.1186/s12913-022-08630-y](https://doi.org/10.1186/s12913-022-08630-y); Dhouib et al., 2024, [DOI: 10.1186/s12960-024-00977-z](https://doi.org/10.1186/s12960-024-00977-z)). | No national, fully stated-preference DCE with experimentally varied monetary vs non-monetary trade-offs. | Anchor relative attribute weights on international/LMIC health workforce DCE systematic reviews (Mandeville et al., 2014, [PMC4161911](https://pmc.ncbi.nlm.nih.gov/articles/PMC4161911/)) calibrated to Tunisian survey odds ratios. |

---

## 4. Internal Contradictions in the Specification

1. **Cohort Model vs. Individual-Level Peer/Micro Variables**:
   - *Contradiction*: Section 8 specifies a cohort/state-transition stock-flow model: $N(a,s,r,t)$, while simultaneously introducing individual-level peer exposure ($X_{\text{peer}}$: "migration exposure among colleagues") and micro personal circumstances ($X_{\text{micro}}$).
   - *Impact*: In a deterministic cohort state-transition model, individual peer networks cannot be tracked without an agent-based microsimulation, which Section 2 and Section 8 explicitly forbid.
   - *Resolution*: Define $X_{\text{peer}}$ as an **aggregate sectoral/cohort feedback term** (e.g., cumulative emigration rate of cohort $a$ in preceding 2 years) rather than an individual network variable.
2. **"No Arbitrary Behavioral Weights" vs. Ad-Hoc Composite Utility Formula**:
   - *Contradiction*: Section 2 instructs not to assign arbitrary weights, yet Section 8 specifies a 5-component linear utility index ($\Delta V = \beta_0 + \beta_{\text{macro}} X_{\text{macro}} + \dots + \beta_{\text{pull}} X_{\text{pull}}$) without an existing unified econometric dataset in Tunisia that simultaneously measures all 5 levels.
   - *Resolution*: Standardize the utility function using normalized attribute indices weighted by pooled meta-analytic DCE coefficients (Class C) and calibrate only the global scale and baseline propensity to Tunisian data (Class A).

---

## 5. Inappropriate Causal Assumptions

### 5.1. Treating Cross-Sectional Intention Odds Ratios as Causal Realization Elasticities
- **The Flaw**: Studies like Ben Romdhane et al. (2022) and Dhouib et al. (2024) report odds ratios (ORs) for *intention to emigrate*. In health workforce economics, stated intention significantly exceeds actual realization.
- **Empirical Evidence**: The intention-to-migration realization gap in middle-income countries is substantial; empirical studies demonstrate that only 20% to 50% of individuals expressing strong migration intentions actually emigrate within a 3–5 year window (Docquier, Peri, & Ruyssen, 2014, [DOI: 10.1111/ecoj.12119](https://doi.org/10.1111/ecoj.12119); Clemens & Mendola, 2020, [DOI: 10.1016/j.jdeveco.2020.102580](https://doi.org/10.1016/j.jdeveco.2020.102580); Creighton, 2013, [DOI: 10.1111/imre.12027](https://doi.org/10.1111/imre.12027)).
- **Remedy**: Explicitly introduce an intention-to-action realization parameter ($\kappa \in [0.25, 0.50]$) and conduct sensitivity analysis across this range. Never equate an odds ratio of intention directly to an odds ratio of physical departure.

### 5.2. Omitted Variable Bias and Macroeconomic Confounding
- **The Flaw**: Attributing the post-2021 surge in departures to public salary stagnation alone ignores simultaneous systemic shocks: political restructuring, high inflation, currency devaluation, legal vulnerabilities under medical liability legislation, and post-COVID recruitment expansions by France and Germany.
- **Remedy**: Model the post-2021 acceleration as a **structural regime intercept shift** ($\Delta \text{Regime}_{2021+}$) rather than attributing it entirely to a single endogenous economic variable.

---

## 6. Unnecessary Model Complexity vs. Parsimonious Design

### 6.1. Curse of Dimensionality in the State Tensor
- **The Problem**: A fully stratified state space of $\text{Age (50 single years)} \times \text{Sex (2)} \times \text{Specialty (11 groups)} \times \text{Sector (5)} \times \text{Governorate (24)} \times \text{Migration Status (6)}$ creates $50 \times 2 \times 11 \times 5 \times 24 \times 6 = 792,000$ cells.
- **The Absurdity**: With a total national stock of ~15,315 physicians in 2024 ([INS, 2024](https://ins.tn/en/statistiques/123)), the average cell count would be $15,315 / 792,000 \approx 0.019$ physicians per cell. This creates empty cells, numerical instability, and zero empirical identifiability.
- **The Parsimonious Solution**: Collapse the state space into an empirically supported $3 \times 2 \times 3 \times 2 = 36$-cell or $4 \times 2 \times 3 \times 2 = 48$-cell tensor:
  1. **Career Stage / Age** (3 strata): Resident/In-Training ($<35$), Mid-Career ($35–54$), Senior ($55+$).
  2. **Sector** (2 strata): Public Sector, Private Sector.
  3. **Specialty Cluster** (3 strata): General Practice, Medical Specialties, Surgical/Anesthesia/Critical Care Specialties.
  4. **Geography** (2 strata): Coastal/Metropolitan (Greater Tunis, Center East) vs. Interior/Underserved (North West, Center West, South).

```
+-----------------------------------------------------------------------------------+
|               Proposed Parsimonious State Tensor Structure (48 Cells)             |
+-----------------------------------------------------------------------------------+
| Career Stage (3):  [Resident / Early (<35)] [Mid-Career (35-54)] [Senior (55+)]   |
| Sector (2):        [Public (Hospital/Primary)]   [Private (Clinic/Solo)]          |
| Specialty (3):     [General Medicine] [Medical Specialties] [Surgical/ICU]        |
| Geography (2):     [Metropolitan/Coastal]        [Interior/Underserved]           |
+-----------------------------------------------------------------------------------+
| Multiplied by 2 Core Statuses: [Domestic Practicing] vs. [Cumulative Emigrated]   |
+-----------------------------------------------------------------------------------+
```

---

## 7. Economic Evaluation Weaknesses

### 7.1. Valuation of Public Training Investment (Sunk Cost vs. Human Capital)
- **The Issue**: Section 16 proposes calculating training loss as the sum of direct operating costs per student over 9–12 years.
- **Weakness**: This ignores the substantial clinical service delivered by medical residents and interns during their 4–5 years of postgraduate training in public hospitals. Residents provide essential frontline labor at below-market wages.
- **Correction**: Net training cost per specialist must be formalized as:
  $$\text{Net Training Cost} = \text{Direct Educational Outlay} - \text{Imputed Value of Resident Clinical Service Delivered}$$
  Without this adjustment, the gross training loss is substantially overstated (Drummond et al., 2015; Sanders et al., 2016, [DOI: 10.1001/jama.2016.12195](https://doi.org/10.1001/jama.2016.12195)).

### 7.2. Inframarginal Wage Bill Spillover (Deadweight Cost)
- **The Issue**: Simulating a salary increase (e.g., Scenario 1) to retain marginal emigrating physicians requires paying the higher wage to *all* practicing public-sector physicians who would have remained anyway (the inframarginal majority).
- **Weakness**: If $\Delta C$ only counts the wage increment of the *retained* physicians, the economic cost of the policy is underestimated by an order of magnitude.
- **Correction**: The cost function must include the entire expanded public wage bill:
  $$\Delta C_{\text{salary}} = \sum_{t} \frac{N_{\text{public}, t} \cdot \Delta w_t}{(1 + r)^t}$$

### 7.3. Outcome Metrics and Distributional Weighting
- **The Issue**: The primary outcome is "Cost per additional physician-year retained".
- **Weakness**: This treats an additional physician-year in an over-supplied coastal private clinic identically to an anesthesiologist-year in an underserved regional hospital in Kasserine or Gafsa.
- **Correction**: Supplement the primary ICER with targeted secondary metrics:
  - Cost per **public-sector** physician-year retained ($\text{ICER}_{\text{public}}$).
  - Cost per **interior/underserved** physician-year retained ($\text{ICER}_{\text{interior}}$).
  - Cost per **critical specialty** physician-year retained ($\text{ICER}_{\text{critical}}$).

---

## 8. Potential Peer Reviewer Objections & Methodological Defenses

### Reviewer Objection 1: "The study relies on migration intention surveys, which do not reflect true emigration."
- **Audit Assessment**: Major vulnerability if unaddressed.
- **Mandatory Defense**: Explicitly document the intention-to-realization literature (Docquier et al., 2014; Clemens & Mendola, 2020), apply the realization scaling parameter $\kappa$, and demonstrate in calibration that model flows match verified historical destination counts (DREES/RPPS and Bundesärztekammer).

### Reviewer Objection 2: "The long-term 2050 projections are speculative and unfalsifiable."
- **Audit Assessment**: Standard critique for long-horizon health policy models.
- **Mandatory Defense**: Frame all results beyond 2030 as **policy counterfactual comparative statics** rather than demographic point forecasts. Conduct extensive Probabilistic Sensitivity Analysis (PSA, 1,000+ Monte Carlo runs) and report 95% Credible Intervals alongside Cost-Effectiveness Acceptability Curves (CEACs).

### Reviewer Objection 3: "The model ignores macroeconomic general equilibrium constraints (fiscal deficit, IMF wage bill caps)."
- **Audit Assessment**: Valid critique from health economists.
- **Mandatory Defense**: Include a **Fiscal Budget Impact Assessment** comparing annual intervention costs against the Tunisian Ministry of Health budget envelope and public-sector wage ceiling constraints.

### Reviewer Objection 4: "Policy interventions are assigned arbitrary effectiveness values."
- **Audit Assessment**: High-risk critique if intervention effects are not traceable.
- **Mandatory Defense**: Formulate all policy scenarios strictly through the lens of empirical discrete choice attribute levels (e.g., wage $+25\%$, rural hardship allowance $+40\%$, equipment modernization to Level 2) using published utility weights from international DCE meta-analyses (Mandeville et al., 2014, [PMC4161911](https://pmc.ncbi.nlm.nih.gov/articles/PMC4161911/)) and classify all policy assumptions transparently in the Parameter Provenance Registry as Class E.

---

## 9. Comprehensive Parameter Provenance Registry Blueprint

Every parameter in the implementation codebase must be classified into the formal 5-tier provenance taxonomy:

```
+-----------------------------------------------------------------------------------------+
|                        Parameter Provenance Classification (5 Tiers)                    |
+-------+---------------------------------------------------------------------------------+
| Class | Definition & Scientific Requirement                                             |
+-------+---------------------------------------------------------------------------------+
|   A   | Directly estimated from Tunisian administrative/registry data (INS, CNOM, MS).  |
|   B   | Estimated from North African / Maghreb empirical microdata or surveys.          |
|   C   | Derived from pooled international / LMIC health workforce meta-analyses / DCEs. |
|   D   | Structural / Demographic accounting identity (e.g., age advance, conservation). |
|   E   | Explicit policy scenario assumption (tested across wide uncertainty bounds).    |
+-------+---------------------------------------------------------------------------------+
```

---

## 10. Audit Checklist & Verdict

| Audit Dimension | Status | Key Remediation Required Before Code Implementation |
| :--- | :--- | :--- |
| **1. Scientific Feasibility** | **Passed with Conditions** | Refactor dynamic micro/meso forecasting into baseline structural elasticities and discrete scenario shifts. |
| **2. Parameter Identifiability** | **Requires Correction** | Restrict free calibration parameters to baseline scale, post-2021 regime shift, and observation multiplier; anchor relative choice weights on literature. |
| **3. Data Availability** | **Passed** | High-level national and regional calibration data exist (INS, *Carte Sanitaire*, CNOM, DREES); use raking for missing sub-tables. |
| **4. Internal Contradictions** | **Requires Correction** | Eliminate individual-level peer variables from the cohort model; reformulate as aggregate cohort/sector feedback loops. |
| **5. Causal Assumptions** | **Requires Correction** | Introduce the intention-to-action realization factor ($\kappa \in [0.25, 0.50]$) to avoid overestimating migration flows. |
| **6. Model Complexity** | **Requires Correction** | Collapse the 792,000-cell state space to a parsimonious 48-cell tensor ($3 \text{ Career Stages} \times 2 \text{ Sectors} \times 3 \text{ Specialties} \times 2 \text{ Regions}$). |
| **7. Economic Evaluation** | **Requires Correction** | Include inframarginal public wage bill costs, adjust training costs for resident clinical service delivery, and report disaggregated public/rural ICERs. |
| **8. Reviewer Defenses** | **Passed with Guidelines** | Implement 1,000+ Monte Carlo PSA, report CEACs, and include fiscal budget impact bounds. |

### Final Audit Verdict
**PROCEED TO IMPLEMENTATION SUBJECT TO PARSIMONIOUS RESTRUCTURING**:  
The conceptual foundation is scientifically sound and highly relevant. Implementation must strictly incorporate the parsimonious state tensor (48 cells), the 5-tier parameter provenance taxonomy, the intention-realization scaling factor, and the corrected economic wage bill costing equations.

---

## References & Data Citations

1. World Health Organization. *A labour market approach to investing in health and social care workforce development*. Geneva: WHO; 2021. URL: [https://iris.who.int/bitstream/handle/10665/348069/9789240035546-eng.pdf](https://iris.who.int/bitstream/handle/10665/348069/9789240035546-eng.pdf).
2. Sousa A, Scheffler RM, Nyoni J, et al. A comprehensive review of the health workforce literature on migration determinants. *Hum Resour Health*. 2023;21(1):31. DOI: [10.1186/s12960-023-00810-7](https://doi.org/10.1186/s12960-023-00810-7). PMC: [PMC10174016](https://pmc.ncbi.nlm.nih.gov/articles/PMC10174016/).
3. Mandeville KL, Lagarde M, Hanson K. The use of discrete choice experiments in health workforce strategy in low and middle income countries: a systematic review. *Soc Sci Med*. 2014;114:148-158. DOI: [10.1016/j.socscimed.2014.06.019](https://doi.org/10.1016/j.socscimed.2014.06.019). PMC: [PMC4161911](https://pmc.ncbi.nlm.nih.gov/articles/PMC4161911/).
4. Amorim-Lopes M, Almeida A, Almada-Lobo B. Physician Emigration: Should They Stay or Should They Go? A Policy Analysis. *Comput Econ*. 2019;54(3):905-931. DOI: [10.1007/s10614-018-9854-1](https://doi.org/10.1007/s10614-018-9854-1). URL: [https://ciencia.ucp.pt/en/publications/physician-emigration-should-they-stay-or-should-they-go-a-policy-/](https://ciencia.ucp.pt/en/publications/physician-emigration-should-they-stay-or-should-they-go-a-policy-/).
5. Zhang X, Lin D, Pfuntner A, et al. Physician workforce projections in the United States, 2019-2034. *AAMC Health Workforce Research*. 2020. PubMed: [33913440](https://pubmed.ncbi.nlm.nih.gov/33913440/). DOI: [10.1097/ACM.0000000000003859](https://doi.org/10.1097/ACM.0000000000003859).
6. Ben Romdhane M, Ben Cheikh A, Bougmiza I, et al. Study of immigration projects among young Tunisian physicians: a cross-sectional study. *BMC Health Serv Res*. 2022;22(1):1276. DOI: [10.1186/s12913-022-08630-y](https://doi.org/10.1186/s12913-022-08630-y). PMC: [PMC9567516](https://pmc.ncbi.nlm.nih.gov/articles/PMC9567516/).
7. Dhouib W, Maatoug J, Ben Cheikh A, et al. Migration intentions among medical residents in Tunisia: a national survey of determinants and destination preferences. *Hum Resour Health*. 2024;22(1):45. DOI: [10.1186/s12960-024-00977-z](https://doi.org/10.1186/s12960-024-00977-z). PMC: [PMC11862060](https://pmc.ncbi.nlm.nih.gov/articles/PMC11862060/).
8. Ben Salem S, Triki S, Loukil M. Workplace incivility and intention to expatriate among healthcare professionals in Tunisia. *Hum Resour Manage Rev*. 2024;34(2):101016. DOI: [10.1016/j.hrmr.2024.101016](https://doi.org/10.1016/j.hrmr.2024.101016). ScienceDirect: [S2049879924000160](https://www.sciencedirect.com/org/science/article/abs/pii/S2049879924000160).
9. Docquier F, Peri G, Ruyssen I. The cross-country determinants of potential and actual migration. *Int Migr Rev*. 2014;48(1_suppl):S37-S99. DOI: [10.1111/imre.12119](https://doi.org/10.1111/ecoj.12119).
10. Clemens MA, Mendola M. Migration from developing countries: Selection, sorting, and the role of knowledge. *J Dev Econ*. 2020;146:102580. DOI: [10.1016/j.jdeveco.2020.102580](https://doi.org/10.1016/j.jdeveco.2020.102580).
11. Creighton MJ. The role of intentions in the migration process: Evidence from the Mexican Migration Project. *Int Migr Rev*. 2013;47(2):241-271. DOI: [10.1111/imre.12027](https://doi.org/10.1111/imre.12027).
12. Drummond MF, Sculpher MJ, Claxton K, Stoddart GL, Torrance GW. *Methods for the Economic Evaluation of Health Care Programmes*. 4th ed. Oxford: Oxford University Press; 2015.
13. Sanders GD, Neumann PJ, Basu A, et al. Recommendations for Conduct, Methodological Practices, and Reporting of Cost-effectiveness Analyses: Second Panel on Cost-Effectiveness in Health and Medicine. *JAMA*. 2016;316(10):1093-1103. DOI: [10.1001/jama.2016.12195](https://doi.org/10.1001/jama.2016.12195).
14. Institut National de la Statistique (INS). *Statistiques de la Santé - Effectif des Médecins*. Tunis: INS; 2024. URL: [https://ins.tn/en/statistiques/123](https://ins.tn/en/statistiques/123).
15. Institut National de la Statistique (INS). *Statistiques Démographiques et Estimations de Population par Gouvernorat*. Tunis: INS; 2023. URL: [https://www.ins.tn/statistiques/111](https://www.ins.tn/statistiques/111).
16. Ministère de la Santé, République Tunisienne. *Carte Sanitaire 2023*. Direction des Études et de la Planification; 2023. URL: [https://santetunisie.rns.tn/images/carte-sanitaire-2023.pdf](https://santetunisie.rns.tn/images/carte-sanitaire-2023.pdf).
17. Tunisie Tribune. *1 450 médecins ont quitté la Tunisie en 2024 selon l'Ordre des Médecins*. 2025. URL: [https://www.tunisie-tribune.com/2025/01/07/1450-medecins-ont-quitte-la-tunisie-en-2024/](https://www.tunisie-tribune.com/2025/01/07/1450-medecins-ont-quitte-la-tunisie-en-2024/).
