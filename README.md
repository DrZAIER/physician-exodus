# Physician Exodus from Tunisia: Workforce Projections, Policy Simulation, and Economic Evaluation to 2050

[![Pipeline Status: Verified & Passing](https://img.shields.io/badge/pipeline-passing-brightgreen.svg)](run_analysis.R)
[![Test Suite: 55/55 Passing](https://img.shields.io/badge/tests-55%2F55%20passed-success.svg)](tests/testthat/test_workforce_pipeline.R)
[![Methodology: Competing--Risk Multi--State Markov](https://img.shields.io/badge/methodology-competing--risk%20Markov-blue.svg)](R/05_workforce_model.R)
[![Reporting Standard: CHEERS 2022](https://img.shields.io/badge/standard-CHEERS%202022-orange.svg)](R/09_economic_evaluation.R)
[![R Version: 4.4.1](https://img.shields.io/badge/R-4.4.1-blue.svg)](run_analysis.R)

---

## 1. Project Overview

This repository provides an empirical, open-source macro-simulation and health economic evaluation engine modeling physician migration from Tunisia over the horizon **2020–2050**.

Integrating the **WHO Health Labour Market Framework**, **Push-Pull / Macro-Meso-Micro Migration Theory**, **Random Utility Discrete Choice Econometrics**, and an exact **Competing-Risk Continuous-Time Multi-State Markov Transition Engine**, the framework models physician attrition across a parsimonious **36-cell state tensor** ($3 \text{ Career Stages} \times 2 \text{ Sectors} \times 2 \text{ Regions} \times 3 \text{ Specialties}$). 

The model evaluates **6 policy counterfactual scenarios**, conducts **CHEERS 2022-compliant Cost-Consequence and Budget Impact Analyses**, and characterizes uncertainty via **1,000-draw Parametric Monte Carlo Probabilistic Sensitivity Analysis (PSA)** and deterministic elasticity sensitivity analysis.

```
+-----------------------------------------------------------------------------------+
|                        WHO Health Labour Market Framework                         |
|   (Supply, Demand, Production, Need, Remuneration, Working Conditions, Mobility)   |
+-----------------------------------------------------------------------------------+
                                         |
     +-----------------------------------+-----------------------------------+
     |                                                                       |
     v                                                                       v
+-------------------------------+                         +-----------------------------------+
| Determinants & Choice Engine  |                         | Competing-Risk Multi-State Engine |
| - Push-Pull Migration Theory  |                         | - 36-Cell State-Space Tensor      |
| - Macro-Meso-Micro Hierarchy  |                         | - Continuous-Time Hazard Matrix   |
| - Random Utility Choice Model |                         | - Inflows, Aging, Transfers, Exit |
+-------------------------------+                         +-----------------------------------+
                                                                     |
                                                                     v
                                                          +-----------------------------------+
                                                          | Economic & Policy Evaluation      |
                                                          | - CHEERS 2022 Cost-Consequence    |
                                                          | - Public Wage Bill Expansion      |
                                                          | - Training Deadweight Valuation   |
                                                          | - Efficiency Frontier & CEAC      |
                                                          +-----------------------------------+
```

---

## 2. Key Methodological Innovations

1. **Exact Competing-Risk Multi-State Formulation**:
   - Replaces additive difference equations with continuous-time transition intensity matrices ($P = \exp(Q \cdot \Delta t)$):
     $$\Lambda_i = \lambda_{\text{emig}, i} + \lambda_{\text{retire}, i} + \lambda_{\text{trans}, i} + \lambda_{\text{geo}, i} + \lambda_{\text{age}, i}$$
     $$p_k = \frac{\lambda_k}{\Lambda_i}\left(1 - e^{-\Lambda_i}\right), \quad p_{\text{stay}} = e^{-\Lambda_i}$$
   - Mathematically enforces $\sum p_k + p_{\text{stay}} \equiv 1.00000000$, eliminating boundary artifacts and probability leaks.

2. **Strict Temporal Split Calibration & Holdout Validation**:
   - Calibrates 2 structural scaling parameters ($\beta_0 = -1.87$, $\Delta \beta_{2021+} = +0.94$) strictly on the **2020–2021 training sample** ($\text{MAPE}_{\text{stock}} = 1.61\%$).
   - Evaluates true out-of-sample temporal generalizability on the **2022–2024 holdout sample** ($\text{MAPE}_{\text{stock}} = 6.88\%$).
   - Validates against official French DREES (PADHUE/EVC) and German Bundesärztekammer (BÄK) foreign intake registries ($r = 0.871$, 86.7% overseas intake coverage).

3. **Specialty-Specific Friction & Structural Strata Modifiers**:
   - Ingests empirical intention-to-action realization vectors ($\kappa_{\text{gen}} = 0.245$, $\kappa_{\text{med}} = 0.350$, $\kappa_{\text{surg}} = 0.490$) reflecting European licensing bottleneck structures.
   - Grounded in empirical survey regressions: Early Resident modifier (+0.65), Senior modifier (-0.85), Public sector modifier (+0.40), Interior modifier (+0.30), Surgical specialty (+0.35).

4. **CHEERS 2022-Compliant Economic Costing**:
   - Conducts Cost-Consequence Analysis (CCA) and Budget Impact Analysis (BIA) from the Public Health System Payer perspective (MOH/MOF).
   - Accounts for inframarginal public salary bill expansion, complementary clinical support costs (35% factor for nursing/diagnostics/consumables), infrastructure capital expenditure, rural hardship allowances, and unrecovered educational deadweight losses on emigrating physicians ($C_{\text{net}} = 51,000$ TND/MD).
   - Reports both undiscounted and discounted (3.0% annual discount rate) outcomes.

5. **Parametric Probabilistic Uncertainty**:
   - 1,000-draw Monte Carlo PSA using standard parametric distributions: **Beta** for bounded probabilities $[0, 1]$, **Log-Normal** for relative risks, and **Gamma** for strictly positive fiscal costs.
   - Full baseline stock tensor rescaling dynamically propagates Active Practice Ratio ($\alpha$) uncertainty.

---

## 3. Policy Counterfactual Scenarios (2025–2050)

| Scenario ID | Policy Strategy | Key Mechanism / Levers | Discounted Net Cost (2025–2050) | Discounted Public Phys-Years Retained | Incremental ICER (TND / Phys-Year) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SCEN_0** | **Status Quo (Baseline)** | No policy intervention; baseline crisis dynamics continue. | 0 TND (Reference) | 0 (Reference) | Reference |
| **SCEN_1** | **Public Remuneration Reform** | +30% basic salary increase for public-sector physicians; $\text{RRR}_{\text{wage}} = 0.12$. | 1,332.01 M TND | +2,576 phys-years | 517,084 TND |
| **SCEN_2** | **Workplace & Infrastructure Upgrades** | Annual capital upgrade fund (25M TND/yr); $\text{RRR}_{\text{infra}} = 0.10$. | 447.67 M TND | +2,577 phys-years | 173,693 TND |
| **SCEN_3** | **Regional Retention & Rural Package** | +60% rural hardship allowance; regional housing and priority promotion; $\text{RRR}_{\text{rural}} = 0.18$. | 334.86 M TND | +685 public / +1,585 interior | 211,249 TND *(Interior)* |
| **SCEN_4** | **Training Quota Expansion** | +15% intake expansion; 75% return-of-service compliance; accounts for emigrant deadweight loss. | 290.56 M TND | +8,412 phys-years | 34,540 TND |
| **SCEN_5** | **Comprehensive Synergistic Reform** | Bundled reform (Wage + Infra + Rural + Balanced 7.5% Training); non-linear utility interactions. | 2,115.29 M TND | **+10,404 phys-years** | **203,315 TND** *(Dominant)* |

---

## 4. Repository Directory Structure

```
physician-exodus-tunisia/
├── R/                                      # Modular simulation & analysis scripts
│   ├── 01_import.R                         # Empirical data ingestion & schema validation
│   ├── 02_clean.R                          # 36-cell IPF tensor initialization & harmonization
│   ├── 03_parameters.R                     # Parameter parsing & parametric PSA sampler
│   ├── 04_migration_model.R                # Random utility choice & realization engine
│   ├── 05_workforce_model.R                # Competing-risk multi-state continuous-time Markov engine
│   ├── 06_calibration.R                    # Temporal training calibration (2020-2021)
│   ├── 07_validation.R                     # Out-of-sample holdout (2022-2024) & European registry validation
│   ├── 08_policy_scenarios.R               # 6 policy counterfactual simulation runs (2020-2050)
│   ├── 09_economic_evaluation.R            # CHEERS 2022 Cost-Consequence & Budget Impact Analysis
│   ├── 10_sensitivity.R                    # Deterministic tornado & 1,000-draw Monte Carlo PSA / CEAC
│   └── 11_figures_tables.R                 # 7 publication figures (PDF, SVG, 600-DPI PNG) & CSV tables
│
├── data/                                   # Data assets (read-only primary sources)
│   ├── raw/                                # Official census, ministerial, and overseas registries
│   │   ├── ins_physicians_2015_2024.csv    # National Institute of Statistics physician series
│   │   ├── ins_population_2015_2024.csv    # Sub-national population census series
│   │   ├── carte_sanitaire_2022.csv        # Ministry of Health governorate hospital resources
│   │   ├── cnom_good_standing_2015_2024.csv# National Council of Physicians certificates
│   │   └── destination_registries_france_germany.csv # DREES and Bundesärztekammer foreign intake
│   └── metadata/                           # Transparent provenance and codebooks
│       ├── source_registry.csv             # Primary source provenance and DOI/URL catalog
│       ├── data_dictionary.csv             # Relational data dictionary and variable definitions
│       └── parameter_registry.csv          # 37 model parameters with identification classes (A-E)
│
├── outputs/                                # Generated analysis deliverables
│   ├── figures/                            # Publication-quality visual outputs
│   │   ├── fig1_conceptual_framework.*     # Framework & 36-cell stock-flow topology
│   │   ├── fig2_historical_calibration.*   # Training fit & out-of-sample concordance
│   │   ├── fig3_status_quo_projections.*   # Baseline 2050 workforce & diaspora trajectory
│   │   ├── fig4_policy_retention_dynamics.*# Scenario comparative retention & outflows
│   │   ├── fig5_cost_effectiveness_frontier.* # Policy efficiency frontier & ICER plane
│   │   ├── fig6_sensitivity_and_ceac.*     # Tornado elasticity & CEAC decision uncertainty
│   │   ├── fig7_spatial_equity_disparity.* # Regional density closure to 2050
│   │   ├── pdf/                            # Vector PDF format
│   │   ├── svg/                            # Scalable Vector Graphics format
│   │   └── png_600dpi/                     # 600-DPI high-resolution raster format
│   └── tables/                             # Standardized CSV tables
│       ├── table1_baseline_stock_36cells.csv
│       ├── table2_workforce_milestones_2030_2040_2050.csv
│       ├── table3_economic_evaluation_cca.csv
│       ├── table4_psa_credible_intervals.csv
│       └── table5_tornado_sensitivity.csv
│
├── tests/                                  # Automated test suite
│   ├── testthat/
│   │   └── test_workforce_pipeline.R       # 55 automated unit & integration tests
│   └── test_runner.R                       # Command-line test execution script
│
├── run_analysis.R                          # Master execution pipeline
├── CHANGELOG.md                            # Complete version history and release notes
├── FINAL_AUDIT.md                          # Systematic audit matrix of peer-review remediations
├── PROJECT_SPEC.md                         # Detailed scientific & mathematical specification
├── DATA_SPEC.md                            # Research data governance protocol
└── LITERATURE_SPEC.md                      # Systematic literature search & extraction protocol
```

---

## 5. Quick Start & Execution Guide

### Prerequisites
- **R (>= 4.4.0)**
- Required R packages:
  ```R
  install.packages(c("tidyverse", "readr", "dplyr", "tidyr", "purrr", 
                     "ggplot2", "scales", "patchwork", "ggrepel", "testthat"))
  ```

### 1. Run Master Analysis Pipeline
Execute the full end-to-end simulation, calibration, holdout validation, policy scenarios, CHEERS economic evaluation, 1,000-draw Monte Carlo PSA, and export all figures/tables:
```bash
Rscript run_analysis.R
```

### 2. Run Automated Test Suite
Run the 55 automated test assertions verifying data ingestion, IPF conservation, competing-risk zero-leakage, calibration boundaries, and CHEERS accounting:
```bash
Rscript tests/test_runner.R
```

---

## 6. Key Empirical Findings

1. **Status Quo Collapse (SCEN_0)**:
   - Under baseline crisis conditions, domestic active physician stock stabilizes at ~10,961 physicians by 2050 (density: 7.7 per 10,000 population, well below the WHO 23.0 benchmark).
   - The overseas diaspora reaches 23,285 physicians, representing 68% of the total cumulative medical training output.
   - Public hospital staffing is severely depleted, while the interior-to-coastal density disparity widens to 1.83:1.

2. **The "Training Paradox" (SCEN_4)**:
   - Expanding training intake quotas by +15% without domestic workplace and wage reforms acts as an unrecovered state subsidy for overseas destination countries (+2,246 incremental emigrant exits, generating 117.5M TND in unrecovered training deadweight losses).

3. **Policy Dominance & Efficiency (SCEN_5)**:
   - The **Comprehensive Synergistic Reform Package (SCEN_5)** generates **+10,404 discounted public physician-years retained** through 2050 at an ICER of **203,315 TND per public physician-year**.
   - Regional interior density increases to 10.4 per 10,000, closing the geographic equity gap.
   - In probabilistic sensitivity analysis, SCEN_5 achieves a **>90% probability of being cost-effective** at willingness-to-pay thresholds above 300,000 TND / physician-year retained.

---

## 7. Audit & Scientific Governance

- **Zero Synthetic Data**: All model inputs are strictly derived from official administrative sources (INS, MOH, CNOM, DREES, BÄK) or peer-reviewed literature.
- **Traceable Identification Classes**: All parameters are classified from Class A (Directly Estimated from Tunisian Data) to Class E (Policy Scenario Assumptions).
- **Formal Audit Documentation**: Complete audit details and peer-review remediations are logged in [`FINAL_AUDIT.md`](FINAL_AUDIT.md) and [`CHANGELOG.md`](CHANGELOG.md).

---

## 8. License & Citation

This project is licensed under the MIT License - see the `LICENSE` file for details.

### Citation
```bibtex
@article{tunisia_physician_exodus_2026,
  title={Physician Exodus from Tunisia: Dynamic Macro-Simulation, Policy Counterfactuals, and Economic Evaluation to 2050},
  author={Tunisian Health Economics and Workforce Modeling Working Group},
  year={2026},
  journal={Health Policy and Planning / Human Resources for Health},
  note={Reproducible R Simulation Engine v0.4.0}
}
```
