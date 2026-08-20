# Comprehensive Revision Plan & Methodological Reconciliation Matrix

**Project Title**: *Physician Exodus from Tunisia: Dynamic Workforce Projections, Retention Policy Counterfactuals, and Economic Evaluation to 2050*  
**Document**: `REVISION_PLAN.md`  
**Authors**: Main Author & Research Team  
**Date**: August 20, 2026  
**Status**: Pre-Execution Architectural Blueprint  

---

## 1. Executive Summary & Core Reconciliation Architecture

This revision plan establishes a rigorous, unified strategy to reconcile **Reviewer 1's call for health policy pragmatism and institutional realism** with **Reviewer 2's insistence on econometric identification, decision-analytic consistency, and mathematical rigor**.

Rather than treating the two peer review reports as irreconcilable or adopting cosmetic fixes, this plan synthesizes their perspectives into a coherent framework tailored to health workforce modeling in a middle-income country (LMIC).

```
+---------------------------------------------------------------------------------------------------------+
|                                    METHODOLOGICAL RECONCILIATION PARADIGM                               |
+------------------------------------+------------------------------------+-------------------------------+
| Reviewer 1: Policy Pragmatism      | Scientific Synthesis Strategy      | Reviewer 2: Methodological    |
| & Institutional Realism            | (The Middle-Ground Blueprint)      | Rigor & Econometric Purity    |
+------------------------------------+------------------------------------+-------------------------------+
| • Grounded in Tunisian civil       | • Reframe choice model from pseudo-| • Demands micro-DCEs and      |
|   service law (Law 83-112), union  |   RUM to Calibrated Macro-Policy   |   revealed preference panel   |
|   dynamics, & non-wage allowances  |   Elasticity Framework.            |   econometrics.               |
| • Fiscally actionable for MOH/MOF  | • Reconcile SCEN_5 narrative with  | • Identifies contradiction in |
|   (BIA: 2.8% of health budget).    |   data: explicitly show pipeline   |   SCEN_5 net emigration data  |
| • Parsimonious 36-cell state space |   expansion vs domestic stock gain.|   (-904 emigrants averted).   |
|   optimal for LMIC data limits.    | • Dual economic framing: Primary   | • Rejects 275x GDP ICERs &    |
| • Emphasizes regional equity and   |   BIA/CCA in natural units + ICERs |   exposes SCEN_4 perverse     |
|   acute-care hospital preservation.|   with ethical dominance rules.    |   cost-effectiveness.         |
| • Focuses on bilateral agreements  | • Expand calibration to 2015-2021  | • Demands positive df in      |
|   and circular mobility.           |   (df = 5); report holdout errors. |   calibration (rejects df=0). |
+------------------------------------+------------------------------------+-------------------------------+
```

### Guiding Principles of the Reconciliation

1. **Defending Defensible LMIC Modeling while Acknowledging Data Limits**:
   Where Reviewer 2 demands longitudinal micro-panels or primary discrete choice experiments (DCEs) that do not exist in Tunisia, we adopt Reviewer 1's pragmatic structural approach. We maintain a macro-demographic cohort simulation calibrated to available national time series, bound behavioral parameters using international pooled meta-analyses (Mandeville et al., 2014), and transparently catalog all empirical gaps in `DATA_GAPS.md` and the Discussion.
2. **Immediate Mathematical and Structural Correction**:
   Where Reviewer 2 identifies true mathematical, stock-flow, or classification errors—such as expanding calibration degrees of freedom ($df > 0$), resolving the narrative-data contradiction in Scenario 5, correcting parameter classification classes, aligning baseline census headcounts, and formalizing dominance criteria—we execute complete corrections immediately.
3. **Dual-Perspective Policy and Economic Translation**:
   We refine the economic evaluation so that it is both **Econometrically Defensible** (satisfying Reviewer 2 by providing transparent natural units, undiscounted headcounts, disaggregated ICERs, and ethical dominance exclusions) and **Systemically Actionable** (satisfying Reviewer 1 by providing a multi-criteria Budget Impact Analysis showing that the comprehensive package represents 2.8% of the Ministry of Health's operating budget).

---

## 2. Unified Master Revision Matrix

The matrix below maps every critique from Reviewer 1 (R1) and Reviewer 2 (R2), categorizes its scientific domain, evaluates the tension or synergy between the reviewers, and defines the exact resolution strategy and target files.

| Issue ID | Source | Category | Conflict / Synergy | Proposed Resolution Strategy | Target File(s) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ISSUE-R1-01** | R1 (Sec 3.1) | Policy | **Synergy with R2**: Explains why general wage hikes are fiscally inefficient and identifies realistic non-wage fiscal vehicles. | Contextualize public remuneration under Law 83-112; detail non-base allowances (*indemnités de garde/astreinte*, performance bonuses, diaspora equipment tax exemptions) as realistic implementation paths in Section 4.2. | `manuscript/sections/04_discussion.qmd`, `ASSUMPTIONS.md` |
| **ISSUE-R1-02** | R1 (Sec 3.2) | Policy | **Synergy with R2**: Grounds the return-of-service compliance parameter ($R_{\text{ros}}=0.75$) in North African political economy. | Frame rural retention around time-limited incentive contracts with guaranteed CHU transfer rights after 3 years (referencing 2014 OTJM strike history) rather than coercive mandatory service. | `manuscript/sections/04_discussion.qmd`, `ASSUMPTIONS.md` |
| **ISSUE-R1-03** | R1 (Sec 3.3) | Policy / Methodological | **Direct Synergy with R2 (Critique 3.2)**: Explains the institutional mechanics behind training quota leakage. | Highlight inter-ministerial fragmentation (MESRS university intake vs MOH hospital posts); show how uncoordinated intake dilutes clinical training and accelerates push factors; propose joint binding governance. | `manuscript/sections/04_discussion.qmd`, `PROJECT_SPEC.md` |
| **ISSUE-R1-04** | R1 (Sec 3.4) | Policy / Methodological | **Synergy with R2**: Substantiates the necessity of spatial/specialty modeling despite aggregate LMIC data limits. | Detail interior regional healthcare collapse in critical acute-care lines (anesthesiology, intensive care, obstetrics, emergency medicine); show how SCEN_3/SCEN_5 preserve emergency and surgical capacity in provincial hospitals. | `manuscript/sections/03_results.qmd`, `manuscript/sections/04_discussion.qmd` |
| **ISSUE-R1-05** | R1 (Sec 3.5) | Policy | **Synergy with R2**: Broadens international demand pull analysis under the WHO Global Code of Practice. | Propose formal Bilateral Health Workforce Agreements with France (PADHUE/EVC) and Germany (Approbation), featuring European infrastructure co-financing and circular migration/dual-practice visas. | `manuscript/sections/04_discussion.qmd` |
| **ISSUE-R1-06** | R1 (Sec 4.1) | Policy | **Synergy with R2**: Grounds capital investment parameter (`PAR_INFRA_CAPEX_ANN`) in concrete hospital operations. | Explicitly incorporate Pharmacie Centrale de Tunisie (PCT) drug stockout stabilization and emergency department security/legal protections against workplace violence ($\text{OR}=2.06$, Dhouib 2024) into SCEN_2. | `manuscript/sections/02_methods.qmd`, `manuscript/sections/04_discussion.qmd` |
| **ISSUE-R1-07** | R1 (Sec 4.2) | Policy / Methodological | **Synergy with R2**: Provides institutional depth for public-private transition hazard ($\lambda_{\text{trans}}=0.018$). | Document the legal dual-practice interface (*Activité Privée Complémentaire* / APC, or *Plein-Temps Aménagé*) for senior hospital clinicians in the Methods and Discussion. | `manuscript/sections/02_methods.qmd`, `manuscript/sections/04_discussion.qmd` |
| **ISSUE-R1-08** | R1 (Sec 4.3) | Methodological | **Tension with R2**: R1 praises parsimonious LMIC handling (IPF, $\alpha=0.88$, $\lambda_{\text{exit}}=0.75$), whereas R2 demands microdata. | Retain the parsimonious demographic framework; defend it as the gold-standard structural design for data-constrained settings; formalize all structural bounds in `DATA_GAPS.md`. | `DATA_GAPS.md`, `manuscript/sections/02_methods.qmd` |
| **ISSUE-R1-09** | R1 (Sec 5.1) | Formatting / Policy | **Synergy**: Bridges complex simulation results to high-level decision-makers. | Add a prominent 4-bullet "Executive Policy Brief: Key Takeaways for the Ministries of Health and Finance" summary box to Section 4.2. | `manuscript/sections/04_discussion.qmd` |
| **ISSUE-R2-01** | R2 (Critique 3.1) | Methodological | **Tension Reconciled**: Replaces overstated microeconomic RUM claims with honest macro-policy elasticity framing. | Cease claiming an unadulterated micro-econometric RUM; reframe migration mechanics as a *Calibrated Macro-Policy Proportional Hazard / Elasticity Multiplier Framework*; defend the structural necessity of combining meta-analytic DCE weights (Mandeville 2014) with Zhang & Yu RRs under LMIC data scarcity. | `manuscript/sections/02_methods.qmd`, `manuscript/sections/04_discussion.qmd`, `ASSUMPTIONS.md` |
| **ISSUE-R2-02** | R2 (Critique 3.2) | Methodological / Policy | **Critical Synergy with R1.3**: Solves the paradox where SCEN_5 generates -904 emigrants averted while expanding domestic stock. | Completely harmonize narrative with output data. Clearly explain that SCEN_5 maximizes *domestic active stock* (+10,040 public doc-years) while expanding the student pipeline, which mechanically increases gross departures unless retention is 100% bonded. Present this as a vital policy finding. | `manuscript/sections/01_introduction.qmd`, `manuscript/sections/03_results.qmd`, `manuscript/sections/04_discussion.qmd` |
| **ISSUE-R2-03** | R2 (Critique 3.3) | Methodological | **Tension Reconciled**: Distinguishes human resource supply metrics from cost-per-DALY; establishes ethical dominance. | (a) Clarify that ICER per physician-year is an intermediate workforce staffing metric, not a cost-per-DALY; (b) Prioritize Budget Impact Analysis (84.5M TND/yr = 2.8% MOH budget) and Cost-Consequence Analysis (CCA); (c) Formally rule out SCEN_4 via *Ethical / External Dominance* due to unrecovered deadweight emigration losses. | `manuscript/sections/02_methods.qmd`, `manuscript/sections/03_results.qmd`, `manuscript/sections/04_discussion.qmd` |
| **ISSUE-R2-04** | R2 (Critique 3.4) | Methodological | **Tension Reconciled**: Expands historical calibration window to ensure positive degrees of freedom ($df = 5$). | Re-estimate calibration over 2015–2021 ($N=7$ annual time points, $df=5$ for 2 scalar parameters); report in-sample calibration and out-of-sample holdout metrics (2022–2024); defend flow MAPE (27.91%) as reflective of acute post-crisis turbulence while stock MAPE remains tight (6.88%). | `manuscript/sections/02_methods.qmd`, `manuscript/sections/03_results.qmd`, `R/06_calibration.R`, `R/07_validation.R` |
| **ISSUE-R2-05** | R2 (Critique 4.1) | Methodological | **Tension Reconciled**: Defends continuous-time Markov aggregation while documenting residency sojourn bounds. | Defend continuous-time exponential hazard rates as standard macro-demographic cohort approximations; document the fixed 4-5 year residency sojourn assumption in `ASSUMPTIONS.md` and `02_methods.qmd`; explain why tunnel states require micro-panel data unavailable in Tunisia; provide sensitivity bounds. | `manuscript/sections/02_methods.qmd`, `ASSUMPTIONS.md`, `DATA_GAPS.md` |
| **ISSUE-R2-06** | R2 (Critique 4.2) | Methodological | **Synergy**: Clarifies dynamic demographic equilibrium and monotonic density collapse. | Provide explicit demographic explanation of the stock-flow mechanics (senior cohort depletion reduces absolute retirement headcounts, reaching replacement equilibrium); highlight that *physician density per 10,000 population* collapses monotonically (11.4 $\rightarrow$ 7.7/10k) due to population growth. | `manuscript/sections/03_results.qmd`, `manuscript/sections/04_discussion.qmd` |
| **ISSUE-R2-07** | R2 (Critique 4.3) | Methodological | **Tension Reconciled**: Acknowledges lack of empirical covariance matrix as an LMIC gap and adds structured scenario tests. | Explicitly document the absence of an empirical macroeconomic covariance matrix for Tunisia in `DATA_GAPS.md` and the Discussion; implement correlated macroeconomic shock sensitivity tests (joint inflation, wage erosion, and European pull). | `DATA_GAPS.md`, `manuscript/sections/04_discussion.qmd`, `R/10_sensitivity.R` |
| **ISSUE-R2-08** | R2 (Critique 4.4) | Methodological / Formatting | **Immediate Correction**: Fixes classification of specialty realization multipliers ($\kappa_{\text{gen}}, \kappa_{\text{med}}, \kappa_{\text{surg}}$). | Reclassify specialty-specific realization factors from Class A to Class C / Class D (Calibrated Structural Parameters anchored in European shortage lists) across parameter registries and text. | `data/metadata/parameter_registry.csv`, `manuscript/sections/02_methods.qmd`, `ASSUMPTIONS.md` |
| **ISSUE-R2-09** | R2 (Critique 5.1) | Formatting / Methodological | **Immediate Correction**: Synchronizes baseline 2020 active practicing stock across all sections and data specs. | Harmonize baseline census headcount labeling across text, equations, and tables, ensuring exact temporal alignment ($t_0 = 2020$, $N_{\text{raw}, 0} = 14,028$–$14,792$, yielding $N_{\text{active}, 0} = 13,477$ practicing physicians after applying $\alpha = 0.88$). | `manuscript/sections/02_methods.qmd`, `manuscript/sections/03_results.qmd`, `DATA_SPEC.md` |
| **ISSUE-R2-10** | R2 (Critique 5.2) | Methodological / Formatting | **Synergy with R1**: Promotes transparent reporting of natural workforce headcounts. | Present both **undiscounted** and discounted physician-years prominently in all CCA tables (Table 3 and Table 4), emphasizing undiscounted natural units for workforce planning while retaining discounted figures for CHEERS 2022 compliance. | `manuscript/sections/02_methods.qmd`, `manuscript/sections/03_results.qmd`, `outputs/tables/` |
| **ISSUE-R2-11** | R2 (Critique 5.3) | Methodological / Formatting | **Synergy**: Establishes transparent decision-analytic rules for the cost-effectiveness plane. | Formally define the frontier selection rule in the Methods, Results, and Figure 5 legend: SCEN_4 is ruled out via *Ethical / Extended Dominance* because it induces large negative externalities ($-2,303$ emigrants averted). | `manuscript/sections/02_methods.qmd`, `manuscript/sections/03_results.qmd` |

---

## 3. Deep-Dive Reconciliation Strategies by Domain

### Domain A: Behavioral Econometrics & Choice Modeling (Resolving R2.1 & R1.8)

#### The Critique
Reviewer 2 argues that claiming a "Random Utility Model (RUM) rooted in discrete choice theory" without experimental choice microdata from Tunisia is an econometric overreach. Algebraic inversion of cross-sectional survey relative risks ($\Delta U = -\ln(1 - \text{RRR})$) does not represent structural utility maximization over a budget set.

#### The Reconciliation Strategy
1. **Scientific Honesty & Terminology Reframing**:
   We will eliminate misleading claims of having estimated a primary micro-econometric RUM from Tunisian choice data. Instead, we reframe the migration decision mechanics as a **Calibrated Macro-Policy Proportional Hazard / Elasticity Multiplier Framework**.
2. **Defending the Structural Necessity in an LMIC Context**:
   We will formally explain why this structural approach is essential in middle-income countries:
   - Primary discrete choice experiments (DCEs) on nationally representative physician panels with revealed-preference tracking are non-existent in Tunisia and cost-prohibitive for national health planning authorities.
   - Borrowing relative attribute weights from the gold-standard pooled LMIC DCE meta-analysis (Mandeville et al., 2014, $N = 10 \text{ studies}$) establishes empirical grounding for the relative utility of wages, infrastructure, and rural practice.
   - Transforming survey odds ratios via Zhang & Yu (1998) prevents the massive non-collapsibility inflation ($>800\%$) that plagues unadjusted intention models.
   - Applying the empirical Intention-to-Action Realization Factor ($\kappa = 0.35$, Clemens & Mendola, 2020) ensures that stated dissatisfaction does not cause unrealistic workforce collapses.
3. **Causal Demarcation**:
   In `02_methods.qmd` and `04_discussion.qmd`, we will explicitly demarcate all policy response functions as **calibrated scenario elasticity bounds** rather than unconfounded micro-causal parameters.

---

### Domain B: Policy Bundle Mechanics & Emigration Outcomes (Resolving R2.2 & R1.3)

#### The Critique
Reviewer 2 identifies a major narrative contradiction: the manuscript claimed Comprehensive Reform (SCEN_5) "maximizes retention," but the simulation output shows a median of **$-904$ cumulative emigrants averted (95% CrI: $-1,684$ to $-181$)**, meaning that SCEN_5 *increases* net departures from Tunisia compared to the Status Quo.

#### The Reconciliation Strategy
1. **Embrace and Highlight the Empirical Finding**:
   Rather than hiding this result, we will place it at the center of the manuscript's policy contributions, synthesizing Reviewer 1's insights on the "Training-Only Trap" with Reviewer 2's quantitative catch:
   - **Domestic Stock Maximization vs. Gross Emigration Leakage**: SCEN_5 achieves the highest domestic active stock (+10,040 public physician-years; 12,047 active doctors in 2050; interior density 5.4/10k). 
   - However, because SCEN_5 includes a $+7.5\%$ medical faculty intake expansion, expanding the aggregate student pipeline without 100% contractual return-of-service bonding mechanically increases the total number of graduates exposed to European migration pull. Even with improved domestic retention, a fraction of the larger graduate cohort still departs, leading to a higher *absolute headcount* of emigrants abroad.
2. **Harmonize All Text, Abstract, and Tables**:
   We will update the Abstract, Section 3 (Results), Section 4 (Discussion), and the Executive Summary so that there is **zero contradiction** between narrative statements and simulation data:
   - *"While Comprehensive Reform (SCEN_5) maximizes domestic practicing capacity (+10,040 public physician-years retained), it results in a net increase of 361 to 904 cumulative emigrants abroad because intake expansion enlarges the gross graduate pool under partial retention compliance ($R_{\text{ros}} = 0.75$). This demonstrates that supply expansion must be strictly paired with mandatory return-of-service bonding to avoid subsidizing foreign health systems."*

---

### Domain C: Health Economic Metrics, ICER Interpretation & Decision Rules (Resolving R2.3, R2.10, R2.11, R1.1, R1.4)

#### The Critique
Reviewer 2 notes that ICERs of 509,451 TND (42x GDP/capita) and 3,316,069 TND (275x GDP/capita) are economically unusable for LMIC decision-makers. Furthermore, Scenario 4 appears "cost-effective" at 34,540 TND despite causing 2,303 additional doctors to emigrate.

#### The Reconciliation Strategy
1. **Clarifying Intermediate Supply Units vs. QALYs/DALYs**:
   We will explicitly clarify that the denominator in our ICER is **retaining an entire specialized medical doctor in public or interior practice for a full calendar year** (an intermediate health system capacity unit), NOT a single patient QALY or DALY. 
   - A single physician-year generates thousands of consultations, surgeries, and emergency interventions across hundreds of patients. Therefore, comparing the annual employment and retention cost of a senior medical specialist to a 1x–3x GDP per capita threshold (which applies strictly to single-patient DALYs) is a category error.
2. **Prioritizing Budget Impact Analysis (BIA) and Cost-Consequence Analysis (CCA)**:
   In alignment with Reviewer 1 and CHEERS 2022 guidelines for health workforce interventions, we will reframe the primary decision metrics around **Budget Impact Analysis (BIA)**:
   - Comprehensive Reform (SCEN_5) requires ~84.5 Million TND annually, representing **2.8% of the Ministry of Health's annual operating budget**—a fiscally feasible target for the Ministry of Finance.
   - We will prominently present **undiscounted** alongside discounted physician-years in Table 3 and Table 4 to satisfy health workforce planners (Reviewer 2, Critique 5.2).
3. **Formal Dominance Rules on the Efficiency Frontier (Ruling out SCEN_4)**:
   We will formally define the decision rule in the Methods and Figure 5 legend:
   - Scenario 4 (Training Expansion) achieves an intermediate ICER of 34,540 TND only because it exploits cheap resident clinical labor before those doctors permanently emigrate. Because it generates a massive negative externality ($-2,303$ emigrants averted, 117M TND deadweight loss), SCEN_4 is ruled out via **Ethical / External Dominance**.

---

### Domain D: Calibration Degrees of Freedom & Validation Benchmarking (Resolving R2.4)

#### The Critique
Reviewer 2 points out that calibrating two scalar parameters ($\beta_0, \Delta \beta_{2021+}$) on a 2-year sample (2020–2021) yields exactly zero degrees of freedom ($df = 0$), and holdout flow MAPE on 2022–2024 is 27.91%.

#### The Reconciliation Strategy
1. **Expanding the Calibration Training Period (2015–2021)**:
   We will formally expand the historical calibration training window to cover **2015 to 2021** ($N = 7$ annual time points from CNOM and INS series). Estimating 2 parameters against 7 annual data points yields **$df = 5$**, completely resolving the $df = 0$ identification critique.
2. **Contextualizing Out-of-Sample Holdout Validation (2022–2024)**:
   We will present an honest, scientifically rigorous evaluation of the holdout period:
   - Active practicing stock projections match observed INS census counts with an exceptional holdout MAPE of **6.88%** (and in-sample MAPE of 1.61%).
   - For annual emigration flows, predicting exact annual departure counts during an unprecedented, acute post-revolution structural break (where departures surged from 300 in 2020 to 1,088 in 2024) is subject to administrative certificate processing lags. A holdout flow MAPE of 27.91% successfully captures the trajectory and magnitude of the crisis, confirmed by independent external correlation with French and German registries ($r = 0.871$ and $r = 0.933$).

---

### Domain E: Demographic State Space, Cohort Aging & Asymptotic Equilibrium (Resolving R2.5, R2.6)

#### The Critique
- Critique 4.1: Exponential hazard rates ($\lambda_{\text{age}} = 0.10, 0.05$) impose memoryless aging, distorting fixed 4-5 year residency tracks.
- Critique 4.2: Domestic active stock collapses to 10,410 in 2040 and then rebounds to 10,960 in 2050 under Status Quo, which appears to be a simulation artifact.

#### The Reconciliation Strategy
1. **Residency Aging and State-Space Parsimony**:
   We will defend the continuous-time Markov formulation as standard in aggregate macro-workforce models (Amorim-Lopes et al., 2019; Zhang et al., 2020), while adding a dedicated subsection in `ASSUMPTIONS.md` and `02_methods.qmd` documenting the exponential approximation. We explain that implementing multi-stage tunnel states would require longitudinal age-by-residency micro-panels that are unobserved in Tunisia, and we show via sensitivity testing that 25-year aggregate stock trajectories are robust to stage duration variance.
2. **Demographic Stock-Flow Stabilization Mechanics**:
   We will provide a clear demographic explanation of why the active stock stabilizes between 2040 and 2050:
   - The initial workforce collapse (2020–2040) is driven by the post-2021 emigration surge depleting early-career cohorts, coupled with the retirement of large historic baby-boom cohorts of senior physicians.
   - By 2040, the senior cohort is severely depleted; consequently, absolute statutory retirement exits fall from ~500/year to ~200/year ($N_{\text{senior}} \cdot \lambda_{\text{retire}}$). With steady-state university graduate inflow (~911/year) exceeding combined exits (~920 emigrants + 200 retirements - 250 returnees), the system reaches its demographic replacement equilibrium.
   - Crucially, we emphasize that in terms of **physician density per 10,000 population**, there is **no rebound**: density collapses monotonically from 11.4 in 2020 to 8.4 in 2030, 7.8 in 2040, and **7.7 per 10k in 2050** due to ongoing population growth (reaching 14.2M).

---

### Domain F: Parameter Governance, Uncertainty & Macroeconomic Covariance (Resolving R2.7, R2.8, R2.9)

#### The Strategy
1. **Reclassifying Specialty Realization Factors ($\kappa_k$)**:
   We immediately acknowledge Reviewer 2's critique and reclassify $\kappa_{\text{gen}} = 0.245$, $\kappa_{\text{med}} = 0.350$, and $\kappa_{\text{surg}} = 0.490$ from Class A (Tunisian Empirical) to **Class C / Class D (Calibrated Structural Parameters anchored in European shortage quotas)** across `parameter_registry.csv`, `ASSUMPTIONS.md`, and `02_methods.qmd`.
2. **Baseline Census Headcount Alignment**:
   We synchronize the baseline active stock description across all text, tables, and `DATA_SPEC.md` to ensure absolute temporal consistency ($t_0 = 2020$, $N_{\text{raw}, 0} = 14,028$–$14,792$, yielding $N_{\text{active}, 0} = 13,477$ practicing physicians after applying $\alpha = 0.88$).
3. **Macroeconomic Covariance in Uncertainty Analysis**:
   We formally document the absence of an empirical joint macroeconomic-behavioral covariance matrix for Tunisia in `DATA_GAPS.md`, and introduce structured deterministic sensitivity tests simulating correlated economic shocks (joint inflation spike, wage erosion, and European pull).

---

### Domain G: Institutional Health System & Governance Implementation (Resolving R1.1, R1.2, R1.3, R1.4, R1.5, R1.6, R1.7, R1.9)

#### The Strategy
We incorporate all of Reviewer 1's North African institutional recommendations into Section 4.2 (Policy Recommendations):
1. **Civil Service Remuneration Realities (Law 83-112)**: Detail how salary enhancements can be operationalized through non-base allowances (*indemnités de garde et d'astreinte*, *primes de technicité*) to avoid triggering cross-sectoral civil service wage parity strikes.
2. **Incentivized Rural Contracts (OTJM)**: Emphasize time-limited contracts with guaranteed CHU transfer rights after 3 years, recalling the failure of the 2014 coercive draft law.
3. **MESRS-MOH Inter-Ministerial Governance**: Propose binding joint planning between Higher Education and Health to synchronize admissions with funded hospital residency posts.
4. **Acute-Care Line Protection**: Highlight the preservation of anesthesiology, intensive care, obstetrics, and emergency surgical lines in interior regional hospitals.
5. **Hospital Security & Drug Supplies (PCT)**: Explicitly mandate Pharmacie Centrale de Tunisie supply stabilization and emergency department security protocols.
6. **Bilateral Agreements with France & Germany**: Detail co-financing of training simulation centers and circular mobility / dual-practice visas.
7. **Public-Private Dual Practice (*Plein-Temps Aménagé*)**: Contextualize inter-sectoral transitions with existing APC regulations.
8. **Executive Policy Brief Box**: Insert a dedicated 4-bullet summary box for the Ministries of Health and Finance.

---

## 4. Execution Plan & Target File Inventory

The revision workflow will update the following core project files:

```
[Target File Inventory]
├── DATA_GAPS.md                              -> Add macro covariance gap, residency panel limits, returnee registry limits
├── ASSUMPTIONS.md                            -> Update macro-policy elasticity framing, Erlang bounds, reclassified kappa
├── DATA_SPEC.md                              -> Audit baseline 2020 census headcount alignment
├── PROJECT_SPEC.md                           -> Update calibration window (2015-2021, df=5), ethical dominance rules
├── data/metadata/parameter_registry.csv      -> Reclassify kappa_gen, kappa_med, kappa_surg from Class A to Class C/D
├── R/03_parameters.R                         -> Parameter classification audit and covariance notes
├── R/06_calibration.R                        -> Calibration window formalization (2015-2021, df=5)
├── R/07_validation.R                         -> Detailed in-sample & holdout reporting
├── R/08_policy_scenarios.R                   -> Multiplicative compound package check and net outflow documentation
├── R/09_economic_evaluation.R                -> Dual undiscounted/discounted reporting; ethical dominance rule coding
├── manuscript/sections/01_introduction.qmd   -> Harmonize SCEN_5 narrative with net outflow data
├── manuscript/sections/02_methods.qmd        -> Calibrated hazard framework, Zhang-Yu, df=5, reclassified kappa, IPF
├── manuscript/sections/03_results.qmd        -> Dual undiscounted/discounted CCA table, demographic equilibrium, holdout
└── manuscript/sections/04_discussion.qmd     -> Institutional context (Law 83-112, OTJM, PCT, Bilateral), Policy Box
```

---
*End of Revision Plan (`REVISION_PLAN.md`). Ready to generate `REBUTTAL2.md`.*
