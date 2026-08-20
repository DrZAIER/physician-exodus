# PEER REVIEW REPORT (REVIEWER 1)

**Journal Target**: *Human Resources for Health* / *Health Policy and Planning* / *Health Economics*  
**Manuscript Title**: *Physician Exodus from Tunisia: Dynamic Workforce Projections, Retention Policy Counterfactuals, and Economic Evaluation to 2050*  
**Reviewer Role**: Senior Health Economist & Health Workforce Modeller (Specialist in LMIC Health Labour Markets & Policy Simulation)  
**Review Date**: 2026-08-20  
**Initial Recommendation**: **Major Revision (Pragmatic Re-alignment for High Policy Impact)**

---

## 1. Executive Summary & Reviewer Perspective

As a health economist and workforce researcher who has worked extensively on low- and middle-income country (LMIC) health systems, I commend the authors for tackling a critical, high-stakes policy crisis: the accelerating brain drain of Tunisian physicians to Europe and the Gulf. Tunisia’s health system faces acute public-sector shortages and severe coastal-interior inequities. A rigorous, forward-looking workforce and economic simulation is urgently needed by policymakers in the Ministry of Health, the Ministry of Finance, and the *Conseil National de l'Ordre des Médecins* (CNOM).

I approach this review with a **pragmatic, LMIC-aware perspective**. In health workforce research across North Africa and similar LMIC settings, data scarcity, sparse administrative panels, and absent experimental choice datasets are the norm, not the exception. The goal of peer review should **not** be to demand unachievable primary data collection (e.g., executing a multi-year national DCE or individual-level longitudinal tracing), nor to impose baroque computational architectures (e.g., agent-based microsimulations, structural equation modeling, or high-dimensional Bayesian MCMC) that obscure policy insights behind black-box mechanics.

Instead, this review identifies the **essential methodological vulnerabilities** that would currently invite rejection from top health policy and health economics journals, and provides **pragmatic, maximum-ROI (Return on Effort) solutions**. These remedies require **no new primary data collection** and **minimal computational overhead**, yet they will immediately elevate the study's methodological credibility, policy relevance, and publication readiness.

---

## 2. Methodological Critiques & Pragmatic LMIC Solutions

Below, I evaluate the study across the 12 core methodological areas, pairing each critical concern with an actionable, low-burden pragmatic solution.

```
+-------------------------------------------------------------------------------------------------------+
|                                 SUMMARY OF PRAGMATIC HIGH-ROI SOLUTIONS                               |
+------------------------------------+------------------------------------------------------------------+
| Methodological Challenge           | Pragmatic LMIC Solution (Maximal ROI)                            |
+------------------------------------+------------------------------------------------------------------+
| 1. Intention vs. Actual Migration  | Apply literature realization factor (kappa = 0.35); test in PSA. |
| 2. Non-Collapsible Odds Ratios     | Convert survey ORs to Relative Risks using baseline prevalence.  |
| 3. Latent Behavioral Utility       | Use a normalized composite index with literature DCE weights.    |
| 4. Discrete-Choice Identification  | Calibrate only global scale + 2021 regime intercept to macro data|
| 5. State-Space Dimensionality      | Collapse 792k cells to a parsimonious 24-to-36 cell cohort model.|
| 6. Calibration vs. Validation      | Calibrate 2015–2021; validate on 2022–2024 + destination checks. |
| 7. Stock-Flow Accounting           | Include administrative inactivity rate (alpha = 0.85-0.90).      |
| 8. Migration Observation Error     | Treat CNOM certificates as proxy with clearance multiplier (0.75)|
| 9. Policy Effectiveness & Costing  | Include full public wage bill; scale policy levers by DCE bounds.|
| 10. Cost-Effectiveness Validity    | Compute Net Training Costs (offset resident labor); report CCA.  |
| 11. 2050 Projection Uncertainty    | Frame as conditional policy counterfactuals; run 1,000-draw PSA. |
| 12. Computational Parsimony        | Use deterministic difference equations in base R (<5 sec runtime)|
+------------------------------------+------------------------------------------------------------------+
```

---

### 2.1. Construct Validity & Latent Determinant Operationalisation

- **The Critique**: The conceptual framework (Section 2 & 8) lists dozens of multi-level determinants (macro, meso, micro, peer, pull). Attempting to forecast individual-level psychological attributes (e.g., workplace incivility, personal family stress) dynamically over 25 years in an LMIC cohort model is impossible and undermines construct validity.
- **Pragmatic LMIC Solution (High ROI)**:
  - Do **not** attempt dynamic forecasting of individual micro-variables.
  - Structure the macro-meso-micro determinants as a **static baseline taxonomy** that defines initial cohort relative utilities ($\Delta V_0$).
  - Represent policy reforms and external shocks as **discrete, standardized scenario shifts** in utility ($\Delta V_{\text{policy}} = \Delta V_0 + \sum \beta_k \Delta X_k$), keeping the underlying variable tracking clean and aggregate.

---

### 2.2. Migration-Intention versus Actual Migration (The Realization Gap)

- **The Critique**: Tunisian resident surveys (Ben Romdhane et al., 2022; Dhouib et al., 2024) report intention-to-emigrate rates between 70% and 90%. Converting these survey intentions directly into annual physical migration probabilities will cause the simulated domestic workforce to implode within 5 years—a catastrophic simulation artifact. In reality, strict European licensing exams (French *EVC*, German *Approbation*), visa limits, and family inertia prevent the majority from leaving.
- **Pragmatic LMIC Solution (High ROI)**:
  - Introduce an explicit, literature-anchored **Intention-to-Action Realization Factor** ($\kappa \in [0.25, 0.45]$, base case $\kappa = 0.35$, drawing on Clemens & Mendola, 2020; Docquier et al., 2014):
    $$P(\text{Emigration}_{i,t}) = \kappa \cdot P(\text{Intention}_{i,t})$$
  - Include $\kappa$ as a primary uncertainty parameter in the Probabilistic Sensitivity Analysis (PSA). This takes 2 lines of R code, requires no new data, and aligns model flows with real-world observed departure counts.

---

### 2.3. Transferability of Tunisian Odds Ratios (Mathematical Adjustment)

- **The Critique**: The authors propose taking Odds Ratios from cross-sectional logistic regressions in Tunisian surveys (e.g., $\text{OR} = 2.4$ for poor working conditions) and applying them directly as multiplicative risk multipliers. When baseline intention is high ($p_0 = 0.75$), an OR of 2.4 translates to a true Relative Risk of only $1.16$. Treating an OR as a Relative Risk inflates policy effects by hundreds of percent.
- **Pragmatic LMIC Solution (High ROI)**:
  - Apply the standard epidemiologic conversion formula (Zhang & Yu, *JAMA* 1998) to transform published survey ORs into conservative **Relative Risks (RR)** before using them in the policy response function:
    $$\text{RR} = \frac{\text{OR}}{(1 - p_0) + (p_0 \cdot \text{OR})}$$
  - Explicitly document in the Methods that these cross-sectional parameters represent *associational scenario bounds*, avoiding unsupportable causal claims.

---

### 2.4. Discrete-Choice Identification (Empirical Anchoring)

- **The Critique**: Tunisia lacks a national, experimentally designed stated-preference Discrete Choice Experiment (DCE). Attempting to estimate both behavioral choice weights and baseline migration scale parameters from ~10 macro data points creates total parameter unidentifiability (equifinality).
- **Pragmatic LMIC Solution (High ROI)**:
  - Do **not** attempt to estimate the relative choice weights from historical time-series data.
  - Borrow standardized relative utility weights from the established LMIC health workforce DCE meta-analysis (Mandeville et al., 2014, *Soc Sci Med* [Class C parameters]).
  - Fix the relative weight ratios (e.g., wage improvement vs. infrastructure vs. rural hardship allowance) and use the Tunisian macro data to calibrate **only two scalar parameters**:
    1. Global baseline migration scale ($\beta_0$).
    2. Post-2021 structural regime shift ($\Delta \beta_{2021+}$).
  - This reduces a 15-parameter unidentifiable problem to a 2-parameter perfectly identified model.

---

### 2.5. Overparameterisation & State-Space Parsimony

- **The Critique**: Specifying a tensor of Age (50) $\times$ Sex (2) $\times$ Specialty (11) $\times$ Sector (5) $\times$ Governorate (24) $\times$ Status (6) yields **792,000 cells** for a national physician stock of 15,315 (~0.019 doctors/cell). This creates severe matrix sparsity, empty cells, and pseudo-precision.
- **Pragmatic LMIC Solution (High ROI)**:
  - Collapse the state space into a robust, policy-relevant **24-cell or 36-cell cohort tensor**:
    - **Career Stage** (3): Early-Career/Resident ($<35$ yrs), Mid-Career ($35–54$ yrs), Senior ($55+$ yrs).
    - **Sector** (2): Public Hospital/Clinic vs. Private Practice.
    - **Geography** (2): Coastal/Metropolitan (Greater Tunis, Center East) vs. Interior/Underserved (North West, Center West, South).
    - **Specialty Group** (2 or 3): General Medicine vs. Medical/Surgical Specialists (or General vs. Medical vs. Surgical/Critical Care).
    - **Migration Status** (2): Active Domestic vs. Cumulative Emigrated.
  - Total active domestic state space: $3 \times 2 \times 2 \times 3 = 36 \text{ cells}$. Every cell has substantial empirical mass, transitions are fully identifiable, and simulation runtime is virtually instantaneous.

---

### 2.6. Workforce Stock Accounting & Administrative Inactivity

- **The Critique**: National administrative data (INS) show total registered doctors growing from ~13,000 in 2015 to 15,315 in 2024, despite ~9,300 departures and ~9,000 graduates. This occurs because administrative licensing registers rarely purge emigrated or inactive doctors ("ghost registrations").
- **Pragmatic LMIC Solution (High ROI)**:
  - Explicitly define the modeled stock as **Active Practicing Workforce** rather than cumulative licensed registrations.
  - Apply an empirical **Active Practice Ratio** ($\alpha \in [0.85, 0.90]$) to raw administrative headcounts to adjust baseline stocks, or add an annual unobserved attrition/inactivity exit rate ($1.0–1.5\%$).
  - This reconciles the graduate inflows, retirement outflows, and departure counts into an exact, conserved stock-flow identity:
    $$N_{t+1} = N_t + \text{Graduates}_{t+1} + \text{Returns}_{t+1} - \text{Emigrants}_{t+1} - \text{Retirements}_{t+1} - \text{OtherExits}_{t+1}$$

---

### 2.7. Emigration Observation Modeling & Measurement Error

- **The Critique**: Media reports citing CNOM data (~1,450 departures in 2024) reflect *Certificates of Good Standing* (*Attestations de bonne conduite*), not verified physical border departures. Treating this raw number as true emigration creates measurement error.
- **Pragmatic LMIC Solution (High ROI)**:
  - Specify a transparent, single-parameter **Administrative Clearance Multiplier**:
    $$\text{True Emigration Flow}_t = \lambda_{\text{exit}} \cdot \text{CNOM Certificates}_t, \quad \lambda_{\text{exit}} \sim \text{Uniform}[0.70, 0.85]$$
  - Justify $\lambda_{\text{exit}} \approx 0.75$ using published French DREES / German foreign physician entry ratios. Vary $\lambda_{\text{exit}}$ across $[0.65, 0.90]$ in the PSA.

---

### 2.8. Calibration versus Validation Split

- **The Critique**: Attempting complex Bayesian global optimization or splitting 10 time points into 2017–2022 (calibration) and 2023–2024 (validation) is fragile due to the post-2021 structural crisis in Tunisia.
- **Pragmatic LMIC Solution (High ROI)**:
  - Use transparent **Ordinary Least Squares (OLS) or Maximum Likelihood** on aggregate annual stock and departure flows to calibrate the 2 free parameters ($\beta_0, \Delta \beta_{2021+}$).
  - Use 2015–2021 for baseline calibration, and 2022–2024 for out-of-sample temporal testing.
  - Supplement temporal validation with a **directional plausibility check** against French DREES foreign doctor influx trends. This avoids unnecessary optimization packages and is 100% reproducible.

---

### 2.9. Intervention Costing & Inframarginal Deadweight Costs

- **The Critique**: Calculating salary increase costs by multiplying the raise only by the *marginal retained* physicians underestimates public fiscal expenditure by $>95\%$, because the raise must be paid to all practicing public doctors (inframarginal majority).
- **Pragmatic LMIC Solution (High ROI)**:
  - Use the standard health-economic **Public Wage Bill Expansion formula**:
    $$\Delta \text{Cost}_{\text{salary}, t} = N_{\text{public}, t} \cdot \Delta w_t$$
  - This single equation immediately fixes the economic validity of the model, takes seconds to implement, and provides the Ministry of Finance with an honest Budget Impact Analysis (BIA).

---

### 2.10. Cost-Effectiveness Validity & Net Human Capital Valuation

- **The Critique**: 
  1. Gross educational outlays (~$60k–$100k per doctor) overstate training losses by ignoring the massive clinical service delivered by residents during 4–5 years of postgraduate hospital training.
  2. "Cost per physician-year" has no established willingness-to-pay (WTP) threshold.
- **Pragmatic LMIC Solution (High ROI)**:
  - Calculate **Net Training Investment**:
    $$\text{Net Training Cost} = \text{Gross University Outlay} - (\text{Years of Residency} \times \text{Net Imputed Value of Resident Clinical Labor})$$
    (A simple 40% offset rule of thumb is well-supported in human capital accounting).
  - Frame the primary economic evaluation as a **Cost-Consequence Analysis (CCA)** and **Budget Impact Analysis (BIA)** across 2030, 2040, and 2050, reporting disaggregated costs per *public-sector* and *interior-region* physician-year. This is far more useful to Tunisian policymakers than abstract ICERs.

---

### 2.11. 2050 Horizon & Epistemic Uncertainty Management

- **The Critique**: Unconditional point forecasts to 2050 over 25 compounding years are scientifically indefensible.
- **Pragmatic LMIC Solution (High ROI)**:
  - Explicitly label all 2025–2050 results as **Conditional Policy Counterfactuals** (*"What happens under Status Quo vs. Policy Package X under baseline demographic assumptions?"*).
  - Report milestone results at **2030 (short-term), 2040 (medium-term), and 2050 (long-term)**.
  - Run a standard **1,000-draw Monte Carlo PSA** drawing from beta/gamma distributions around the realization rate ($\kappa$), clearance multiplier ($\lambda_{\text{exit}}$), policy effect sizes, and discount rates (3%, tested at 0%, 5%, 8%), reporting 95% Credible Intervals for all milestone outcomes.

---

### 2.12. Computational Simplicity & Reproducibility

- **The Critique**: Using Agent-Based Models (ABM) or complex microsimulations introduces unnecessary random seeds, heavy dependencies, slow runtimes, and opaque debugging without adding any empirical insight.
- **Pragmatic LMIC Solution (High ROI)**:
  - Implement the entire model as a **deterministic Markov cohort stock-flow model using standard matrix difference equations in base R / tidyverse**.
  - A 36-cell model running 25 annual steps and 1,000 Monte Carlo PSA iterations will execute in **under 5 seconds** on any standard laptop without requiring external optimization libraries, GPUs, or C++ wrappers.
  - This ensures effortless peer-review reproduction and straightforward handover to Tunisian Ministry of Health analysts.

---

## 3. Pragmatic Parameter Provenance Classification (5 Tiers)

To ensure total transparency without excessive data-engineering overhead, classify all model inputs into this clear 5-tier registry:

```
+-------------------------------------------------------------------------------------------------------+
|                                    PARAMETER PROVENANCE REGISTRY                                      |
+-------+-----------------------------+-----------------------------------------------------------------+
| Class | Category                    | Tunisian / LMIC Data Source                                     |
+-------+-----------------------------+-----------------------------------------------------------------+
|   A   | Direct Tunisian Macro Data  | INS (Stocks 2015–2024), MS Carte Sanitaire (Regional 2023),     |
|       |                             | Ministry of Higher Education / JORT (Graduate intakes).         |
|   B   | Regional / Maghreb Evidence | Tunisian & Moroccan resident surveys (Ben Romdhane 2022,        |
|       |                             | Dhouib 2024) converted to Relative Risks.                       |
|   C   | Pooled LMIC DCE Literature  | Mandeville et al. (2014) meta-analytic discrete choice weights. |
|   D   | Demographic / Accounting    | Deterministic age advancement (+1 yr), stock-flow conservation. |
|   E   | Policy Scenarios & Bounded  | Intention realization factor (kappa = 0.35 in [0.25, 0.45]),    |
|       | Uncertainty Parameters      | Clearance multiplier (lambda = 0.75 in [0.65, 0.85]), PSA bounds|
+-------+-----------------------------+-----------------------------------------------------------------+
```

---

## 4. Prioritized Action Checklist for Authors (Maximum ROI)

The authors can resolve all major reviewer concerns by completing these five straightforward tasks:

1. **State-Space Simplification**: Refactor the state tensor to 36 cells ($3 \text{ Career Stages} \times 2 \text{ Sectors} \times 2 \text{ Regions} \times 3 \text{ Specialties}$).
2. **Behavioral Calibration Fix**: Insert the intention-to-realization parameter ($\kappa = 0.35$) and convert survey ORs to Relative Risks.
3. **Observation & Stock Alignment**: Adjust raw INS stock by $\alpha = 0.88$ (active rate) and CNOM departures by $\lambda_{\text{exit}} = 0.75$.
4. **Economic Costing Correction**: Implement the inframarginal public wage bill formula and net training cost offset in the economic script.
5. **Clean Uncertainty Reporting**: Run a 1,000-iteration Monte Carlo PSA and report median trajectories with 95% Credible Intervals at 2030, 2040, and 2050 alongside Cost-Consequence summary tables.

---

## 5. Final Recommendation to the Editor

With these **pragmatic, high-ROI adjustments**, this study will avoid the fatal traps of overparameterisation, unidentifiable choice modeling, and costing bias, while delivering an elegant, transparent, and highly defensible health workforce model. It will provide actionable policy intelligence for Tunisia and serve as a benchmark methodology for other LMICs facing health workforce emigration.

I recommend **MAJOR REVISION (PRAGMATIC RE-ALIGNMENT)** with an enthusiastic invitation to resubmit upon implementing this parsimonious framework.

---
*End of Pragmatic Reviewer 1 Report.*
