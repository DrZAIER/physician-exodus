# Physician Exodus from Tunisia: Dynamic Workforce Projections, Retention Policy Counterfactuals, and Economic Evaluation to 2050

[![Pipeline Status: Verified & Passing](https://img.shields.io/badge/pipeline-passing-brightgreen.svg)](run_analysis.R)
[![Test Suite: 55/55 Passing](https://img.shields.io/badge/tests-55%2F55%20passed-success.svg)](tests/test_runner.R)
[![Methodology: Continuous--Time Competing--Risk Markov](https://img.shields.io/badge/methodology-competing--risk%20Markov-blue.svg)](R/05_workforce_model.R)
[![Behavioral Framework: Calibrated Macro Hazard](https://img.shields.io/badge/framework-Calibrated%20Macro%20Hazard-purple.svg)](R/04_migration_model.R)
[![Reporting Standard: CHEERS 2022](https://img.shields.io/badge/standard-CHEERS%202022-orange.svg)](R/09_economic_evaluation.R)
[![Manuscript: Quarto PDF Ready](https://img.shields.io/badge/manuscript-PDF%20Compiled-red.svg)](manuscript/main.pdf)
[![Version: 1.0.0-final](https://img.shields.io/badge/version-1.0.0--final-teal.svg)](CHANGELOG.md)

---

## 1. Executive Overview

This repository hosts the complete, reproducible, and empirically grounded simulation model and health economic evaluation engine investigating physician migration from Tunisia over the 2020–2050 planning horizon.

Integrating the **WHO Health Labour Market Framework (HLMF)**, the **Push-Pull Macro-Meso-Micro Taxonomy**, a **Calibrated Macro-Policy Proportional Hazard / Elasticity Multiplier Framework**, and an exact **Continuous-Time Competing-Risk Multi-State Markov Transition Engine**, the model tracks dynamic physician stocks across a parsimonious **36-cell demographic state tensor** ($3 \text{ Career Stages} \times 2 \text{ Sectors} \times 2 \text{ Regions} \times 3 \text{ Specialties}$).

The platform evaluates **6 policy counterfactual scenarios**, conducts **CHEERS 2022-compliant Cost-Consequence (CCA) and Budget Impact Analyses (BIA)**, and quantifies decision uncertainty via **1,000-draw Parametric Monte Carlo Probabilistic Sensitivity Analysis (PSA)** and deterministic tornado elasticity stress-testing.

```
+-----------------------------------------------------------------------------------+
|                        WHO Health Labour Market Framework                         |
|   (Supply, Demand, Production, Need, Remuneration, Working Conditions, Mobility)  |
+-----------------------------------------------------------------------------------+
                                         |
     +-----------------------------------+-----------------------------------+
     |                                                                       |
     v                                                                       v
+-------------------------------+                         +-----------------------------------+
| Determinants & Choice Engine  |                         | Competing-Risk Multi-State Engine |
| - Push-Pull Migration Theory  |                         | - 36-Cell State-Space Tensor      |
| - Macro-Meso-Micro Hierarchy  |                         | - Continuous-Time Hazard Matrix   |
| - Calibrated Macro Hazard     |                         | - Inflows, Aging, Transfers, Exit |
+-------------------------------+                         +-----------------------------------+
                                                                     |
                                                                     v
                                                          +-----------------------------------+
                                                          | Economic & Policy Evaluation      |
                                                          | - CHEERS 2022 Cost-Consequence    |
                                                          | - Budget Impact Analysis (BIA)    |
                                                          | - Public Wage Bill Expansion      |
                                                          | - Training Deadweight Valuation   |
                                                          | - Efficiency Frontier & CEAC      |
                                                          +-----------------------------------+
```

---

## 2. Core Methodological Architecture

### 1. Continuous-Time Competing-Risk Hazard Engine
Workforce dynamics are governed by continuous-time demographic hazard rates converted into discrete annual transition probabilities via matrix exponential integration ($P = \exp(Q \cdot \Delta t)$):
$$\Lambda_i = \lambda_{\text{emig}, i} + \lambda_{\text{retire}, i} + \lambda_{\text{trans}, i} + \lambda_{\text{geo}, i} + \lambda_{\text{age}, i}$$
$$p_{k, i} = \frac{\lambda_{k, i}}{\Lambda_i}\left(1 - e^{-\Lambda_i}\right), \quad p_{\text{stay}, i} = e^{-\Lambda_i}$$
This formulation guarantees that transition probabilities sum identically to $\sum p_k + p_{\text{stay}} \equiv 1.00000000$ with zero probability leakage across all parameter permutations.

### 2. Calibrated Macro-Policy Proportional Hazard Framework
Annual physical migration probabilities are scaled by empirical **Intention-to-Action Realization Factors** ($\kappa_k$) to account for international licensing friction and visa filters:
$$P(\text{Emigration}_{i,t}) = \kappa_k \cdot \frac{1}{1 + \exp\left(-\Delta V_{i,t}\right)}$$
- $\kappa_{\text{gen}} = 0.245$ (Generalists facing strict French EVC examination quotas)
- $\kappa_{\text{med}} = 0.350$ (Medical Specialists with intermediate recognition)
- $\kappa_{\text{surg}} = 0.490$ (Surgical, Anesthesia, and Critical Care Specialists facing expedited foreign recruitment)

Reported survey odds ratios from Tunisian cross-sectional studies are converted to conservative relative risks using the **Zhang & Yu (1998)** non-collapsibility transformation:
$$\text{RR} = \frac{\text{OR}}{(1 - p_0) + (p_0 \cdot \text{OR})}$$
preventing artificial overestimation of retention elasticities.

### 3. Econometric Identification & Calibration Strategy
To eliminate collinearity, relative attribute weights are fixed from the pooled LMIC Discrete Choice Experiment meta-analysis of Mandeville et al. (2014) ($N = 10 \text{ studies}$). Two global scalar parameters are estimated on a **2015–2021 historical training sample ($N = 7 \text{ time points}, df = 5$)**:
- Baseline Logit Intercept: $\beta_0 = -1.87$
- Post-2021 Crisis Structural Shift: $\Delta \beta_{2021+} = 0.94$

The model is validated out-of-sample on a **2022–2024 holdout dataset** ($\text{MAPE}_{\text{stock}} = 6.88\%$) and cross-checked against independent French DREES (RPPS/PADHUE) and German Bundesärztekammer (BÄK) foreign doctor registration registries ($r = 0.871$, 86.7% overseas coverage).

### 4. CHEERS 2022-Compliant Economic Costing & Decision Rules
- **Payer Perspective**: Evaluated from the Tunisian Public Health System Payer perspective (Ministry of Health and Ministry of Finance).
- **Costing Components**: Inframarginal public salary bill expansion, complementary clinical support costs (35% factor for nursing/diagnostics/consumables), capital modernizations, regional hardship packages, and unrecovered public educational training losses on emigrating physicians ($C_{\text{net}} = 51,000\text{ TND/MD}$, net of a 40% resident hospital clinical service offset).
- **Ethical Dominance Exclusion Rule**: Policy options generating severe negative external brain drain (such as SCEN_4: $-2,303$ emigrants averted; >117M TND in unrecovered deadweight loss) are ruled out via **Ethical / Extended Dominance**.

---

## 3. Summary of Policy Counterfactual Scenarios (2025–2050)

All financial figures in Million Tunisian Dinars (M TND), discounted at a baseline social discount rate of 3.0% annually:

| Scenario ID | Policy Strategy | Key Mechanisms & Levers | Undisc. Net Cost (M TND) | Disc. Net Cost (M TND) | Cumulative Emigrants Averted | Undisc. Public Doc-Years | Disc. Public Doc-Years | Disc. Interior Doc-Years | Public ICER (TND / Doc-Year) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **SCEN_0** | **Status Quo (Baseline)** | Baseline crisis conditions continue without policy reform. | 0.00 | 0.00 | 0 (Ref) | 0 (Ref) | 0 (Ref) | 0 (Ref) | — |
| **SCEN_1** | **Public Remuneration Reform** | +30% basic salary increase across public sector; $\text{RRR}_{\text{wage}} = 0.12$. | 1,895.59 | 1,332.39 | 301 | 3,879 | 2,615 | 402 | 509,451 |
| **SCEN_2** | **Hospital Infrastructure Modernization** | Dedicated capital fund (25M TND/yr) for PCT drug stabilization & security; $\text{RRR}_{\text{infra}} = 0.10$. | 637.39 | 449.77 | 247 | 3,188 | 2,151 | 330 | **209,137** *(Most Efficient Lever)* |
| **SCEN_3** | **Regional Retention Package** | +40% hardship allowance, subsidized housing, 3-yr OTJM contracts with CHU transfer rights; $\text{RRR}_{\text{rural}} = 0.18$. | 475.42 | 335.13 | 194 | 1,076 | 732 | 1,693 | 198,001 *(Interior ICER)* |
| **SCEN_4** | **Training Quota Expansion** | +15% admissions & residency posts; 75% return-of-service compliance ($R_{\text{ros}} = 0.75$). | 419.37 | 290.56 | -2,303 *(Brain Drain)* | 12,938 | 8,412 | 2,985 | *Ethically Dominated* |
| **SCEN_5** | **Comprehensive Synergistic Reform** | Bundled reform (Scenarios 1–4 with multiplicative risk reduction $\text{RRR} = 0.350$). | 3,015.30 | 2,112.10 | -361 *(Pipeline leak)* | **15,151** | **10,040** | **4,058** | **210,374** *(Optimal Strategy)* |

---

## 4. Key Scientific & Policy Findings

1. **Status Quo Health System Collapse**:
   - Inaction reduces national practicing physician density strictly and monotonically from **11.4 per 10,000 population in 2020 to 7.7 per 10k by 2050**, falling far below the WHO Sustainable Development Goal minimum benchmark of 23.0 skilled health personnel per 10,000.
   - The cumulative emigrated diaspora expands to **23,767 physicians abroad by 2050**, exceeding the total domestic active practicing workforce by a factor of 2.17.
2. **The "Training-Only Trap" (SCEN_4)**:
   - Expanding medical school admissions without hospital retention reforms acts as an unrecovered state subsidy for foreign healthcare systems, generating **2,303 additional cumulative emigrants** and causing **>117 Million TND in unrecovered public educational deadweight loss**.
3. **Pipeline Expansion Dynamics in Comprehensive Reform (SCEN_5)**:
   - SCEN_5 maximizes domestic practicing capacity, generating **10,040 discounted public physician-years** (15,151 undiscounted) and **4,058 interior physician-years**, stabilizing interior density at **5.4 per 10k in 2050**.
   - However, because SCEN_5 expands intake (+7.5%), enlarging the student pool under partial compliance ($R_{\text{ros}} = 0.75$) results in a net increase in cumulative emigrants abroad ($-361$ deterministic; median $-920$ PSA; 95% CrI: $-1,658$ to $-172$).
4. **Superior Cost-Effectiveness of Infrastructure Modernization (SCEN_2)**:
   - Modernizing hospital facilities, stabilizing *Pharmacie Centrale de Tunisie* (PCT) drug supplies, and enforcing emergency department security protocols represents the most cost-effective single intervention ($\text{ICER}_{\text{public}} = 209,137\text{ TND}$).
5. **Macro-Fiscal Feasibility for the Tunisian Government**:
   - The discounted cost of Comprehensive Reform (SCEN_5) averages **~84.5 Million TND per year**, representing **2.8% of the Ministry of Health's annual operating budget**.

---

## 5. Repository Directory Architecture

```
physician-exodus-tunisia/
├── R/                                      # Modular simulation & econometric pipeline
│   ├── 01_import.R                         # Empirical data ingestion & schema validation
│   ├── 02_clean.R                          # 36-cell IPF tensor initialization (t0 = 2020)
│   ├── 03_parameters.R                     # Parameter registry parsing & PSA sampler
│   ├── 04_migration_model.R                # Macro hazard choice & realization engine
│   ├── 05_workforce_model.R                # Competing-risk continuous-time Markov engine
│   ├── 06_calibration.R                    # 2-parameter MLE training calibration (df = 5)
│   ├── 07_validation.R                     # 2022-2024 holdout & DREES/BÄK validation
│   ├── 08_policy_scenarios.R               # 6 policy counterfactual simulations (2020-2050)
│   ├── 09_economic_evaluation.R            # CHEERS 2022 Cost-Consequence & BIA evaluation
│   ├── 10_sensitivity.R                    # Deterministic tornado & 1,000-draw Monte Carlo PSA
│   └── 11_figures_tables.R                 # 7 publication figures (PDF/SVG/PNG) & tables
│
├── data/                                   # Empirical and metadata assets (read-only)
│   ├── raw/                                # Official census, ministerial, and foreign registries
│   │   ├── ins_physicians_2015_2024.csv    # National Institute of Statistics series (Stat 123)
│   │   ├── ins_population_2015_2024.csv    # Sub-national population census series (Stat 111)
│   │   ├── carte_sanitaire_2022.csv        # Ministry of Health hospital resource allocations
│   │   ├── cnom_good_standing_2015_2024.csv# National Council of Physicians certificates
│   │   └── destination_registries_france_germany.csv # French DREES & German BÄK intake
│   └── metadata/                           # Transparent provenance and codebooks
│       ├── source_registry.csv             # Primary source catalog and DOI/URL registry
│       ├── data_dictionary.csv             # Relational schema and variable definitions
│       └── parameter_registry.csv          # 37 model parameters with identification classes (A-E)
│
├── literature/                             # Literature extraction assets
│   └── evidence_registry.csv               # 31 audited primary studies & extraction records
│
├── manuscript/                             # Quarto publication manuscript
│   ├── main.qmd                            # Master Quarto manuscript source document
│   ├── main.pdf                            # Compiled publication-grade PDF manuscript (3.95 MB)
│   ├── journal_style.tex                   # LaTeX journal formatting template
│   ├── references.bib                      # Complete BibTeX bibliography
│   └── sections/                           # Modular manuscript sections
│       ├── 01_introduction.qmd             # Introduction & research objectives
│       ├── 02_methods.qmd                  # State space, Markov engine, and calibration
│       ├── 03_results.qmd                  # Validation, baseline 2050, and scenario results
│       ├── 04_discussion.qmd               # Policy implications, institutional depth, limitations
│       └── 05_appendix.qmd                 # Math proofs, parameter registry, CHEERS/STROBE/PRISMA
│
├── outputs/                                # Simulation deliverables
│   ├── figures/                            # 7 publication-quality figures
│   │   ├── fig1_conceptual_framework.*     # Framework topology & 36-cell flow diagram
│   │   ├── fig2_historical_calibration.*   # Training calibration & holdout validation
│   │   ├── fig3_status_quo_trajectory_2050.*# 2050 Status Quo stock & diaspora trajectory
│   │   ├── fig4_policy_retention_dynamics.*# Policy scenario retention & annual outflow curves
│   │   ├── fig5_cost_effectiveness_frontier.* # Cost-effectiveness plane & efficiency frontier
│   │   ├── fig6_sensitivity_and_ceac.*     # Tornado elasticity & CEAC curves
│   │   ├── fig7_spatial_equity_disparity.* # Coastal vs. interior regional density paths
│   │   ├── pdf/                            # Vector PDF format
│   │   ├── svg/                            # Scalable Vector Graphics format
│   │   └── png_600dpi/                     # 600-DPI publication raster format
│   └── tables/                             # Formatted CSV summary tables
│       ├── table1_baseline_stock_36cells.csv
│       ├── table2_workforce_milestones_2030_2040_2050.csv
│       ├── table3_economic_evaluation_cca.csv
│       ├── table4_psa_credible_intervals.csv
│       └── table5_tornado_sensitivity.csv
│
├── tests/                                  # Automated unit test suite
│   ├── testthat/
│   │   └── test_workforce_pipeline.R       # 55 unit tests covering conservation & accounting
│   └── test_runner.R                       # Command-line test orchestrator
│
├── run_analysis.R                          # Master execution pipeline script
├── CHANGELOG.md                            # Comprehensive release history (v1.0.0-final)
├── PARAMETER_AUDIT.md                      # Complete 37-parameter identification audit matrix
├── FINAL_AUDIT.md                          # Systematic audit matrix of peer-review remediations
├── REVISION_PLAN.md                        # Master revision plan
├── PROJECT_SPEC.md                         # Theoretical and mathematical modeling specification
├── DATA_SPEC.md                            # Research data governance protocol
└── LITERATURE_SPEC.md                      # Systematic literature protocol
```

---

## 6. Quick Start & Execution Guide

### Prerequisites
- **R (>= 4.4.0)**
- **Quarto CLI (>= 1.4.0)** and a standard TeX distribution (`pdflatex`).
- Required R packages:
  ```R
  install.packages(c("tidyverse", "readr", "dplyr", "tidyr", "purrr", 
                     "ggplot2", "scales", "patchwork", "ggrepel", "testthat"))
  ```

### 1. Run Complete Simulation Pipeline
Execute the full end-to-end data ingestion, 36-cell IPF initialization, calibration, holdout validation, 6 policy simulations, CHEERS economic evaluation, 1,000-draw Monte Carlo PSA, and generate all figures/tables:
```bash
Rscript run_analysis.R
```

### 2. Run Automated Unit Test Suite
Execute all 55 unit tests verifying demographic conservation, non-negative states, competing-risk unity sum, and CHEERS economic accounting:
```bash
Rscript tests/test_runner.R
```

### 3. Compile Quarto Publication Manuscript to PDF
Render the complete publication-ready manuscript with embedded figures, tables, cross-references, and BibTeX citations:
```bash
quarto render manuscript/main.qmd --to pdf
```
*(The compiled artifact is generated at [`manuscript/main.pdf`](manuscript/main.pdf)).*

---

## 7. Audit & Scientific Governance

- **Strict Data Provenance**: Zero synthetic or mock data; every empirical data point is traceable to official administrative series (INS Stat 123/111, Ministry of Health *Carte Sanitaire 2023*, CNOM registers, French DREES, German BÄK) or peer-reviewed literature.
- **Formal 5-Tier Parameter Identification**: Every parameter is categorized from Class A (Direct Tunisian Empirical) to Class E (Policy Scenario Levers). Complete metadata is audited in [`PARAMETER_AUDIT.md`](PARAMETER_AUDIT.md).
- **Peer-Review Alignment**: Every modification from peer review rounds is logged and cross-referenced in [`FINAL_AUDIT.md`](FINAL_AUDIT.md) and [`CHANGELOG.md`](CHANGELOG.md).

---

## 8. License & Citation

This project is licensed under the MIT License - see the `LICENSE` file for details.

### Citation
```bibtex
@article{tunisia_physician_exodus_2026,
  title={Physician Exodus from Tunisia: Dynamic Workforce Projections, Retention Policy Counterfactuals, and Economic Evaluation to 2050},
  author={Health Workforce and Health Economics Research Consortium for Tunisia},
  year={2026},
  journal={Health Policy and Planning / Human Resources for Health},
  note={Reproducible R Simulation Engine v1.0.0-final}
}
```
