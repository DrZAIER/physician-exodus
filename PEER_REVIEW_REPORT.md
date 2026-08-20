# PEER REVIEW REPORT

**Journals**: *Social Science & Medicine* / *Human Resources for Health*  
**Manuscript Reference**: SSM-HRH-2026-8842-REV  
**Manuscript Title**: *Physician Exodus from Tunisia: Workforce Projections, Retention Policy Counterfactuals, and Economic Evaluation to 2050*  
**Reviewer Specialization**: Senior Health Economist, Health Workforce Modeller & Migration Econometrician  
**Date of Review**: August 20, 2026  
**Final Recommendation**: **REJECT & RESUBMIT / MAJOR STRUCTURAL RE-ARCHITECTING**

---

## 1. Executive Summary & Reviewer Verdict

This manuscript and its underlying computational codebase attempt to model the accelerating brain drain of Tunisian physicians through 2050, evaluating six policy retention counterfactuals via a 36-cell discrete-time Markov cohort simulation paired with a Cost-Consequence and Budget Impact economic framework. 

The authors have constructed a superficially elegant, highly polished narrative that pays lip service to modern modeling conventions: they cite the WHO Health Labour Market Framework, deploy the Zhang & Yu (1998) non-collapsibility transformation on survey odds ratios, borrow discrete choice experiment (DCE) meta-analytic weights from Mandeville et al. (2014), implement Iterative Proportional Fitting (IPF) for baseline stock initialization, incorporate an intention-to-action discount ($\kappa = 0.35$), and present a 1,000-draw Monte Carlo Probabilistic Sensitivity Analysis (PSA).

However, a **forensic audit of the underlying mathematical equations, parameter provenance, R codebase (`R/01`–`R/11`), and output matrices reveals profound econometric, structural, and health-economic vulnerabilities**. Behind the appearance of parsimony and rigor lie fatal conflations between cross-sectional intention surveys and causal policy elasticities, undisclosed hard-coded behavioral modifiers, an unvalidated and circular calibration routine, demographic leakage in the Markov transitions (including an implicit 40-year senior career span), severe underestimation of training expansion costs, and critical non-compliance with CHEERS 2022 guidelines.

The study in its present form **cannot be accepted for publication in *Social Science & Medicine* or *Human Resources for Health***. To become publishable, the entire modeling engine must undergo deep structural and econometric re-architecting.

---

## 2. Comprehensive Forensic Audit Across 7 Target Areas

---

### AREA 1: Confounding Migration Intention (Survey Data) with Actual Migration Behavior

#### Critique 1.1 [CRITICAL] | Causal Misattribution of Cross-Sectional Grievances as Policy Elasticities
The core behavioral engine commits a severe econometric error: it treats cross-sectional associational odds ratios from intention surveys (Ben Romdhane et al., 2022; Dhouib et al., 2024) as direct policy response functions for physical border departures. 
- In `evidence_registry.csv` and `parameter_registry.csv`, the authors note that young doctors dissatisfied with remuneration had an $\text{OR} = 2.14$ of *stating an intention to emigrate* ($p_0 = 0.686$). The authors mathematically transformed this to $\text{RR} = 1.19$ via Zhang & Yu (1998), and then inverted this to claim that a domestic salary increase (+30%) yields a permanent 18% Relative Risk Reduction ($\text{RRR}_{\text{wage}} = 0.18$) in physical border exits.
- **The Fatal Flaw**: Stating on an anonymous survey that one is "dissatisfied with public remuneration" is a reflection of general economic grievance, not a structural wage elasticity of migration. In Tunisia, an entry-level public hospital specialist earns approximately 3,000 TND/month ($\approx €900$–€950/month). A +30% nominal raise increases earnings to ~3,900 TND/month ($\approx €1,200$/month). In France (under PADHUE/Practicien Contractuel status) or Germany, starting salaries range from €4,500 to €8,500/month—a purchasing power disparity of 400% to 700%. 
- Assuming that a +30% domestic salary increment eliminates migration risk at the magnitude suggested by survey dissatisfaction ignores the overwhelming absolute wage gap, currency depreciation, and international demand pull. The model mistakes subjective dissatisfaction for a marginal price elasticity.

#### Critique 1.2 [CRITICAL] | Structural Collinearity and Redundancy of the Realization Factor ($\kappa$)
The manuscript boasts an empirical "Intention-to-Action Realization Factor" ($\kappa = 0.35$, bounded $[0.25, 0.45]$ based on Clemens & Mendola, 2020 and Docquier et al., 2014) to prevent "runaway simulated departures."
- In `R/04_migration_model.R` (line 70), the probability of departure is defined as:
  $$P(\text{Emigration}_{i,t}) = \kappa \cdot \text{logit}^{-1}(\Delta V_{i,t})$$
- However, in `R/06_calibration.R`, the baseline logit intercept $\beta_0$ and the post-2021 regime shift $\Delta \beta_{2021+}$ are calibrated via BFGS optimization to match historical realized departure headcounts (CNOM $\times \lambda_{\text{exit}}$) *conditional on a fixed $\kappa = 0.35$*.
- **The Identifiability Violation**: In a single-equation logit formulation, multiplying a logistic function by a constant scalar $\kappa$ before matching a single aggregate count target creates exact structural collinearity with the intercept $\beta_0$. Any variation in $\kappa$ is mathematically offset by a shift in $\beta_0$. The parameter $\kappa$ provides zero independent empirical identification; it is an illusion of behavioral anchoring that is wholly absorbed by the calibrated intercept.

#### Critique 1.3 [MAJOR] | Uniform Realization Across Asymmetric Professional Strata
In reality, the intention-to-realization gap is highly asymmetric across specialties and career stages:
- A resident specializing in anesthesia, intensive care, or radiology faces near-zero institutional friction when emigrating to France or Germany (immediate fast-track licensing, recruitment agency signing bonuses, immediate hospital placement). Their realization rate $\kappa$ is near $0.80$–$0.90$.
- Conversely, a primary care general practitioner faces severe licensing quotas, the French *Épreuves de Vérification des Connaissances* (EVC) bottleneck, and language barriers, resulting in a realization rate $\kappa < 0.15$.
- Applying a uniform $\kappa = 0.35$ across all 36 cells in `R/04_migration_model.R` flattens clinical realities, leading to severe misprojections of specialty-specific public hospital collapse.

---

### AREA 2: Parameter Identifiability and Over-Reliance on International / Non-Tunisian Odds Ratios

#### Critique 2.1 [CRITICAL] | Undisclosed Hardcoded Behavioral Modifiers in R Code
The manuscript and `PARAMETER_AUDIT.md` assert that the behavioral choice model is fully identified through Mandeville et al. (2014) meta-analytic weights and two calibrated macro scalars ($\beta_0, \Delta \beta_{2021+}$).
- Inspection of `R/04_migration_model.R` (lines 22–32) reveals extensive, **unregistered hardcoded logit modifiers** that appear nowhere in `parameter_registry.csv`, `PARAMETER_AUDIT.md`, or the manuscript tables:
  ```r
  stage_mod <- c(early_resident = 0.65, mid_career = 0.0, senior = -0.85)
  sector_mod <- c(public = 0.40, private = -0.20)
  geo_mod <- c(coastal_metro = 0.0, interior_underserved = 0.30)
  spec_mod <- c(general_medicine = 0.0, medical_specialties = 0.15, surgical_critical_care = 0.35)
  ```
- **The Concealment**: These numbers ($+0.65, -0.85, +0.40, -0.20, +0.30, +0.15, +0.35$) represent immense structural shifts in baseline migration odds ($\exp(0.65) = 1.92\times$ odds for residents; $\exp(-0.85) = 0.43\times$ odds for seniors; $\exp(0.40) = 1.49\times$ odds for public sector; $\exp(0.35) = 1.42\times$ odds for surgical/critical care).
- Not a single one of these 7 coefficients is empirically estimated from Tunisian data, nor are they subjected to uncertainty sampling in `R/03_parameters.R` or `R/10_sensitivity.R`. They are completely arbitrary deterministic constants hardcoded into the R script. This invalidates all claims of rigorous parameter identifiability.

#### Critique 2.2 [CRITICAL] | Deceptive Window-Dressing of the Discrete Choice Framework
In `PARAMETER_AUDIT.md` (lines 74–81) and `PROJECT_SPEC.md`, the authors emphasize their reliance on the Mandeville et al. (2014) *Social Science & Medicine* meta-analysis of 28 LMIC Discrete Choice Experiments to fix relative utility weights ($\beta_{\text{wage}} = 0.48, \beta_{\text{infra}} = 0.36, \beta_{\text{rural}} = 0.31$).
- In `R/04_migration_model.R` (lines 49–62), these weights are theoretically set up to modify $\Delta V$.
- **The Disconnect**: In `R/08_policy_scenarios.R` (lines 42, 61, 80, 111–112), when simulating the actual policy counterfactuals, the code **completely bypasses the utility function and Mandeville coefficients**! Instead, it directly applies ad-hoc percentage multipliers to the final probability:
  ```r
  policy_modifiers = list(comp_multiplier_public = 1 - params$scen1_rrr_wage)
  ```
- The entire discrete-choice random-utility architecture is non-functional window-dressing. The policy engine does not simulate utility shifts; it applies crude exogenous percentage decrements ($18\%, 14\%, 22\%$).

#### Critique 2.3 [MAJOR] | Extreme Ecological Fallacy in Borrowing LMIC Rural Posting DCEs
Even if Mandeville et al. (2014) were actively driving the simulation, borrowing its coefficients for Tunisian international emigration is an indefensible ecological fallacy.
- Mandeville et al. (2014) synthesized stated-preference experiments evaluating *domestic rural posting choices among primary nurses and midwives in Sub-Saharan Africa* (Malawi, Ghana, Tanzania, Kenya).
- Applying preference weights regarding rural housing and pit latrines in Sub-Saharan Africa to Tunisian specialist physicians deciding whether to move to Paris or Frankfurt represents an irreconcilable context mismatch.

---

### AREA 3: Internal Validity of the State-Transition Matrix and Stock-Flow Conservation

#### Critique 3.1 [CRITICAL] | Mathematical Probability Leakage and Competing Risk Violations
In `R/05_workforce_model.R` (lines 89–192), annual transitions out of each cell are computed independently as linear products of `current_stock[i]`:
- Emigration: $\Delta N_{\text{emig}} = N_t \cdot P_{\text{emig}}$
- Public-to-Private Transition: $\Delta N_{\text{trans}} = N_t \cdot p_{\text{trans}}$ ($p_{\text{trans}} = 0.018$)
- Statutory Retirement: $\Delta N_{\text{retire}} = N_t \cdot r_{\text{retire}}$ ($r_{\text{retire}} = 0.025$)
- Career Progression / Aging: $\Delta N_{\text{age}} = N_t \cdot p_{\text{age}}$ ($p_{\text{age}} = 0.10$ or $0.05$)
- The update equation (line 185) subtracts all these outflows additively:
  $$N_{t+1} = N_t + \text{Inflows} + \text{Returns} + \text{AgingIn} - \text{AgingOut} + \text{TransIn} - \text{TransOut} - \text{Emigrants} - \text{Retirements}$$
- **The Mathematical Flaw**: In a discrete-time Markov model with a 1-year time step, outflows are **competing risks**. Subtracting independent marginal rates additively from the same initial stock assumes that individuals can simultaneously emigrate, retire, age into the next cohort, and transition to the private sector in the same year. 
- For an early-career public surgeon in the interior post-2021:
  $$P_{\text{emig}} \approx 0.14, \quad p_{\text{age}} = 0.10, \quad p_{\text{trans}} = 0.018 \implies \text{Total Outflow} = 25.8\%/\text{year}$$
  Without computing a multinomial transition intensity matrix ($P = \exp(Q \cdot \Delta t)$), the model introduces severe probability leakage. The authors had to insert an ad-hoc clamp `pmax(next_stock, 0.0)` (line 194) to prevent negative physician headcounts.

#### Critique 3.2 [CRITICAL] | The Senior Cohort Retention Trap (Implicit 40-Year Senior Careers)
In `PARAMETER_AUDIT.md` and `parameter_registry.csv`, the senior retirement parameter `PAR_RETIRE_SENIOR_RATE` is set to $r_{\text{retire}} = 0.025$ (2.5% per annum) for all physicians aged $55+$ years.
- **Demographic Absurdity**: In a stationary Markov cohort, an annual exit probability of $2.5\%$ implies an expected sojourn time in the senior state of:
  $$\mathbb{E}[\text{Duration}] = \frac{1}{r_{\text{retire}}} = \frac{1}{0.025} = 40 \text{ years}$$
- Under this assumption, a physician entering the senior cohort at age 55 is expected to practice until **age 95**! 
- In Tunisia, public hospital doctors face statutory mandatory retirement under Law 83-112 between ages 62 and 65 (a 7- to 10-year span). The true annual exit rate in a $55+$ public cohort must be between $10\%$ and $15\%$ per annum. Setting $r = 0.025$ artificially traps senior physicians inside the public stock for decades, creating a massive artificial demographic buffer that masks the true collapse of public hospital staffing in Table 2 and Figure 3.

#### Critique 3.3 [MAJOR] | Total Absence of Internal Geographic Mobility
In `R/05_workforce_model.R`, the 36-cell tensor tracks `coastal_metro` and `interior_underserved`.
- However, there is **zero inter-regional domestic transition** in the transition engine ($\text{Transition}_{\text{interior}\rightarrow\text{coastal}} \equiv 0$).
- In Tunisian health economics, it is well established that the primary driver of regional disparity is internal brain drain: doctors assigned to interior regional hospitals (Kasserine, Sidi Bouzid, Gafsa) actively seek reassignment or migrate to private clinics in Tunis, Sousse, and Sfax within 2–4 years.
- By setting internal geographic mobility to zero, the model falsely attributes all interior workforce depletion to international emigration, biasing the policy impact and cost-effectiveness of Scenario 3 (Rural Hardship Package).

#### Critique 3.4 [MAJOR] | Unjustified 100% Private Sector Allocation of Returnees
In `R/05_workforce_model.R` (lines 114–122), all returning diaspora physicians are assigned $100\%$ to mid-career private practice:
```r
if (baseline_stock_36$career_stage[i] == "mid_career" && baseline_stock_36$sector[i] == "private") {
  return_weights[i] <- 1
}
```
Zero returnees are allowed to enter public university hospitals (CHUs), despite historical initiatives by the Ministry of Health attempting to recruit senior diaspora academics into public surgical and oncology departments. This structural assumption artificially boosts private sector growth while depressing public sector recovery under return-migration scenarios.

---

### AREA 4: Methodological Rigor of Calibration vs. Out-of-Sample Validation

#### Critique 4.1 [CRITICAL] | False Claim of Out-of-Sample Temporal Validation Split
The manuscript (`PROJECT_SPEC.md`, line 480; `PARAMETER_AUDIT.md`, line 48) explicitly claims:
*"Temporal validation split: Calibration period: 2015–2021; Out-of-sample temporal validation: 2022–2024."*
- **The Empirical Reality**: Inspection of `R/06_calibration.R` (lines 18–24) proves this claim is false:
  ```r
  ins_df <- imported_data$ins_physicians %>% filter(year >= 2020 & year <= 2024)
  cnom_df <- imported_data$cnom_emigration %>% filter(year >= 2020 & year <= 2024)
  ```
- The calibration routine optimizes $\beta_0$ and $\Delta \beta_{2021+}$ against the **entire 2020–2024 series simultaneously**.
- There is **no temporal holdout sample whatsoever**. The 2022–2024 data points were directly fitted inside the objective function `obj_fn`. Claiming out-of-sample temporal validation when all available data were used in calibration is scientific misrepresentation.

#### Critique 4.2 [CRITICAL] | Fabricated Hardcoded Validation Vectors in `R/07_validation.R`
In `R/07_validation.R` (lines 18–23), the authors present an "out-of-sample directional validation check" against French DREES (PADHUE) and German Bundesärztekammer (BAK) registries, claiming a correlation of $r = 0.933$.
- Look at the actual R code:
  ```r
  dest_obs <- tibble(
    year = 2020:2024,
    france_padhue_inflow = c(180, 480, 560, 580, 600),
    germany_bak_inflow = c(70, 210, 270, 290, 315)
  )
  ```
- **The Fabrication**: These numbers are **manually typed constants hardcoded into the R script**. They are not ingested from raw data files, they have no accompanying data dictionary records, and they are not traceable to official DREES or BAK statistical yearbooks. 
- Furthermore, correlating these hardcoded vectors with simulated departures that were already calibrated to jump in 2021 via $\Delta \beta_{2021+}$ is completely circular. Both series have a single step-function jump in 2021; calculating Pearson's $r$ on two 5-point series sharing a structural break is a textbook example of spurious correlation.

---

### AREA 5: Econometric Defense of Intervention Effect Sizes and ICER Discounting

#### Critique 5.1 [CRITICAL] | The Training Expansion Paradox (Perverse Policy Ranking)
In Table 3 (`table3_economic_evaluation_cca.csv`) and Figure 5 (`fig5_cost_effectiveness_frontier`), Scenario 4 (Medical Training Quota Expansion +15%) is presented as the most "cost-effective" single policy, with an ICER of **23,557 TND per public physician-year retained**, dominating Remuneration Reform (89,514 TND) and Rural Incentives (123,757 TND).
- **The Economic Absurdity**: Table 3 reveals that Scenario 4 results in **$-2,246$ cumulative emigrants averted**—meaning that increasing medical school quotas without fixing retention causes **2,246 ADDITIONAL Tunisian physicians to emigrate to Europe**!
- Why does SCEN_4 appear "cost-effective"? Because the model calculates ICER as:
  $$\text{ICER} = \frac{\Delta \text{Cost}}{\Delta \text{Public Physician-Years}}$$
  By pumping 150 extra graduates into the system each year, even if 70% emigrate, the remaining 30% spend their 3–4 residency years in public hospitals before leaving. The model counts these temporary residency years as "retained public physician-years," completely ignoring the fact that Tunisian taxpayers spent tens of millions of dinars subsidizing the medical training of doctors who immediately relocate to France and Germany.
- Presenting a policy that accelerates brain drain by $+2,246$ departures as the "frontier-dominant" cost-effective solution is a catastrophic failure of health economic framing.

#### Critique 5.2 [MAJOR] | Unrealistic Invariant Policy Efficacy (2025–2050)
All six policy scenarios assume instantaneous implementation on January 1, 2025, and **100% constant, invariant risk reductions ($\text{RRR}$) across all 25 years through 2050**.
- In reality:
  1. A nominal wage increase of 30% implemented in 2025 will be completely eroded in real terms within 3 to 5 years under Tunisia's historical 7%–9% annual inflation rate, unless public sector wages are index-linked (which would drastically inflate the wage bill).
  2. Infrastructure capital investments suffer from severe operational depreciation, maintenance stockouts, and administrative decay.
  3. Bonded return-of-service schemes face increasing legal challenges, contract buyouts, and non-compliance over time.
- The omission of policy decay rates ($\delta_{\text{policy}} \in [0.05, 0.10]$/year) severely overestimates long-term retention benefits.

#### Critique 5.3 [MAJOR] | Methodological Flaws in Outcome Discounting
In `R/09_economic_evaluation.R` (lines 77–79), physical physician-years are discounted at $3\%$ per annum:
$$\text{Disc\_Phys\_Years} = \sum_{t=2025}^{2050} \Delta N_{\text{public}, t} \cdot (1 + 0.03)^{-(t - 2025)}$$
- While discounting health utility (QALYs/DALYs) at the social time preference rate is standard, discounting *physical human workforce headcounts* in a health labor supply model requires careful justification. 
- Discounting physician-years makes a doctor retained in 2050 worth only $47.7\%$ of a doctor retained in 2025. When evaluating long-term health system sustainability and Universal Health Coverage (UHC) milestones, this artificially penalizes upstream structural reforms (like infrastructure and training) whose returns materialize 10–15 years into the simulation.

---

### AREA 6: Treatment of 2050 Uncertainty Propagation in the PSA

#### Critique 6.1 [CRITICAL] | Broken Sensitivity Links (Zero Swing Parameters)
In Table 5 (`table5_tornado_sensitivity.csv`) and `R/10_sensitivity.R`, the deterministic one-way sensitivity analysis reveals that three key parameters have a **swing of exactly 0.0 retained physician-years**:
- `active_ratio`: Swing = 0.0
- `clearance_mult`: Swing = 0.0
- `net_train_cost`: Swing = 0.0
- **The Code Error**: In `R/10_sensitivity.R` (lines 38–49), `run_one_way_sensitivity` passes the pre-cleaned `baseline_stock_36` directly into `run_all_policy_scenarios`. 
  - The parameter `active_ratio` is only used inside `02_clean.R` during initial baseline stock filtering; changing `active_ratio` in `param_ranges` does not re-clean the stock, resulting in a zero effect!
  - `clearance_mult` is only used to compute the historical diaspora baseline, which has zero feedback on public sector retention.
- The tornado analysis is computationally defective, giving a false impression of parameter insensitivity.

#### Critique 6.2 [MAJOR] | Unbounded Uniform Distributions and Wild Tail Risks in PSA
In `R/03_parameters.R` (lines 69–104), almost all parameters (`realization_kappa`, `clearance_mult`, `scen1_rrr_wage`, `scen2_rrr_infra`, `scen3_rrr_rural`, `scen4_quota_exp`, `retire_senior_rate`, `return_mig_rate`, `pub_priv_trans_rate`, `peer_feedback`) are sampled from **Uniform distributions** $\text{Uniform}[a, b]$.
- Standard health economic modeling (Briggs et al., 2006) mandates that transition probabilities and risk ratios follow Beta or Log-Normal distributions, and cost parameters follow Gamma distributions.
- Using uniform distributions across dozens of compounding parameters over a 25-year projection horizon artificially flattens probability density and produces absurd tail outcomes.
- In Table 4 (`table4_psa_credible_intervals.csv`), the 95% Credible Interval for cumulative emigrants averted under Scenario 5 ranges from **$-614$ to $+2,683$**! The authors fail to explain why a comprehensive retention package could result in a massive increase in physician emigration in 2.5% of simulations.

#### Critique 6.3 [MAJOR] | Independent Sampling of Orthogonal Macroeconomic Parameters
In `R/03_parameters.R`, Monte Carlo parameters are sampled completely independently.
- In macroeconomic reality, public base salary levels, infrastructure budgets, currency depreciation, and baseline emigration propensities are highly correlated. A fiscal crisis that lowers public health salaries also slashes hospital infrastructure investment and increases push factors.
- By ignoring the parameter covariance matrix ($\boldsymbol{\Sigma}$), the PSA underestimates extreme downside systemic collapse scenarios.

---

### AREA 7: Compliance with CHEERS 2022 Guidelines for Health Economic Evaluations

The manuscript was evaluated against the **Consolidated Health Economic Evaluation Reporting Standards (CHEERS 2022)** 28-item checklist. It fails across multiple core items:

| CHEERS Item | Standard Requirement | Manuscript Implementation Status | Severity |
| :--- | :--- | :--- | :---: |
| **Item 4: Perspective** | Clearly define perspective and ensure all relevant costs/benefits align. | Claims "Public Payer (MoH/MoF)", but includes educational training loss offsets (societal human capital) while excluding private patient out-of-pocket costs and travel burdens. Inconsistent hybrid perspective. | `[MAJOR]` |
| **Item 7: Target Population** | Disaggregate outcomes across vulnerable subpopulations. | Evaluates broad macro-regions (Coastal vs Interior), but omits any socioeconomic or vulnerable population health equity subgroup analyses. | `[MINOR]` |
| **Item 11: Outcome Measurement** | Measure health outcomes in standardized units (QALY/DALY) or justify intermediate metrics. | Uses "physician-years retained" as a crude proxy for health gain. Zero attempt to link retained physician-years to preventable mortality, surgical wait times, or maternal/infant health outcomes. | `[MAJOR]` |
| **Item 13: Estimating Costs** | Include all relevant direct and complementary resource costs. | Excludes all complementary clinical inputs. Retaining a surgeon or ICU specialist costs 0 TND in nurses, anesthetics, and medical devices in the model. Infrastructure Capex has zero operational expenditure (Opex) escalation. | `[MAJOR]` |
| **Item 18: Discounting** | Justify discount rate choices for costs and outcomes. | Applies a flat 3% discount rate to human headcounts without normative or economic defense. | `[MINOR]` |
| **Item 20: Characterizing Uncertainty** | Explore parameter, structural, and methodological uncertainty. | Only conducts parameter Monte Carlo PSA. Structural uncertainty (e.g., non-Markovian memory, dynamic wage feedback, variable retirement age) is completely unexamined. | `[MAJOR]` |
| **Item 24: Distributional Effects** | Report distributional cost-effectiveness across settings. | Reports regional ICERs, but ignores local municipal fiscal space and interior hospital absorptive capacity. | `[MINOR]` |

---

## 3. Summary Classification Matrix of All Reviewer Critiques

```
+---------------------------------------------------------------------------------------------------------+
|                                    SUMMARY AUDIT CLASSIFICATION MATRIX                                  |
+----+--------+------------------------------------------------------------------+------------------------+
| ID | Level  | Methodological Domain & Specific Issue                           | Code / File Location   |
+----+--------+------------------------------------------------------------------+------------------------+
| 1  | [CRIT] | Causal misattribution of survey intention ORs as policy RRR      | evidence_registry.csv  |
| 2  | [CRIT] | Realization factor (kappa) is structurally collinear with beta_0 | R/04, R/06             |
| 3  | [CRIT] | Undisclosed hardcoded behavioral modifiers in R choice engine    | R/04_migration_model.R |
| 4  | [CRIT] | DCE meta-analytic utility model bypassed in policy simulation    | R/08_policy_scenarios.R|
| 5  | [CRIT] | Competing risk violation & additive probability leakage          | R/05_workforce_model.R |
| 6  | [CRIT] | Senior retirement rate (r=0.025) implies 40-year senior careers  | parameter_registry.csv |
| 7  | [CRIT] | False temporal holdout validation claim (2020-2024 all fitted)   | R/06_calibration.R     |
| 8  | [CRIT] | Fabricated hardcoded destination intake vectors in validation    | R/07_validation.R      |
| 9  | [CRIT] | Training quota expansion paradox (accelerates brain drain)       | R/09, outputs/table3   |
| 10 | [CRIT] | Defective Tornado sensitivity analysis (Zero swing parameters)   | R/10_sensitivity.R     |
| 11 | [MAJ]  | Uniform kappa across asymmetric clinical specialties             | R/04_migration_model.R |
| 12 | [MAJ]  | Ecological fallacy borrowing Sub-Saharan rural midwife DCEs      | data/metadata/         |
| 13 | [MAJ]  | Total absence of internal geographic migration (interior->coast) | R/05_workforce_model.R |
| 14 | [MAJ]  | 100% arbitrary allocation of diaspora returnees to private sector| R/05_workforce_model.R |
| 15 | [MAJ]  | Invariant policy effectiveness across 25 years (zero decay)      | R/08_policy_scenarios.R|
| 16 | [MAJ]  | Methodological flaws in discounting physical physician-years     | R/09_economic_evaluation|
| 17 | [MAJ]  | Unbounded uniform distributions producing negative PSA intervals | R/03_parameters.R      |
| 18 | [MAJ]  | Independent Monte Carlo sampling ignoring macro covariance       | R/03_parameters.R      |
| 19 | [MAJ]  | CHEERS non-compliance: Inconsistent hybrid perspective           | ASSUMPTIONS.md         |
| 20 | [MAJ]  | CHEERS non-compliance: Zero linkage of headcounts to health gains| PROJECT_SPEC.md        |
| 21 | [MAJ]  | CHEERS non-compliance: Omission of complementary clinical inputs | R/09_economic_evaluation|
| 22 | [MAJ]  | CHEERS non-compliance: Omission of structural uncertainty testing| ASSUMPTIONS.md         |
| 23 | [MIN]  | CHEERS non-compliance: Missing vulnerable subgroup reporting     | PROJECT_SPEC.md        |
| 24 | [MIN]  | CHEERS non-compliance: Normative defense of outcome discount rate| R/09_economic_evaluation|
| 25 | [MIN]  | CHEERS non-compliance: Fiscal space constraints in interior      | PROJECT_SPEC.md        |
+----+--------+------------------------------------------------------------------+------------------------+
```

---

## 4. Mandatory Remediation Protocol for Resubmission

Should the Editor permit a resubmission, the authors must satisfy all of the following requirements:

1. **Re-architect the State-Transition Matrix**:
   - Replace the additive difference equations with a continuous-time transition intensity matrix ($P(t) = \exp(Q \cdot \Delta t)$) to guarantee proper competing risk accounting and eliminate probability leakage.
   - Re-parameterize senior retirement with an empirical step-function or Weibull hazard reflecting mandatory public retirement at age 62–65 ($r_{\text{retire}} \approx 0.12$–$0.15$/year).
   - Incorporate a domestic inter-regional migration transition matrix ($\text{Interior} \rightarrow \text{Coastal}$).

2. **Fix Calibration and Validation Integrity**:
   - Strictly separate calibration (2015–2020) from temporal validation (2021–2024).
   - Remove hardcoded vectors from `R/07_validation.R`; ingest real, documented DREES and Bundesärztekammer data tables via `01_import.R`.
   - Provide a formal out-of-sample log-likelihood score or Mean Absolute Prediction Error (MAPE) on the true holdout sample.

3. **Econometric Grounding of Policy Levers**:
   - Stop treating cross-sectional survey odds ratios as unconfounded policy response elasticities. Replace static $\text{RRR}$ multipliers with calibrated discrete choice elasticities that account for the massive purchasing-power wage gap between Tunisia and OECD destinations.
   - Introduce policy efficacy decay functions ($\delta \approx 0.05$/year) to reflect inflation erosion, infrastructure depreciation, and retention fatigue.

4. **Correct the Economic Evaluation and Policy Ranking**:
   - Re-frame the Training Expansion scenario (SCEN_4) to account for the deadweight fiscal loss of training physicians who emigrate. The cost per retained physician-year must include the unrecovered public training subsidies of the $2,246$ additional emigrating doctors.
   - Include complementary input costs (nursing ratios, operating consumables, diagnostic reagents) in the intervention costing equations.

5. **Re-run PSA with Standardized Parametric Distributions**:
   - Replace arbitrary Uniform distributions with Beta/Log-Normal distributions for probabilities and risk ratios, and Gamma distributions for costs.
   - Fix the broken code in `R/10_sensitivity.R` so that `active_ratio`, `clearance_mult`, and `net_train_cost` correctly propagate into the Tornado diagram.

---

## 5. Final Concluding Remarks to the Editor

This paper addresses a vital, time-critical public health crisis in North Africa. However, the current manuscript and codebase rely on computational shortcuts, arbitrary hardcoded parameters masquerading as identified econometrics, demographic leakage, and defective validation procedures.

In its present state, the study risks misleading Tunisian health planners and international workforce economists into adopting flawed policy priorities (such as expanding medical school quotas to compensate for unaddressed structural brain drain). 

I strongly recommend **REJECT & RESUBMIT**, with an invitation to completely overhaul the mathematical and econometric foundations of the model in accordance with the forensic audit detailed above.

---
*End of Peer Review Report.*
