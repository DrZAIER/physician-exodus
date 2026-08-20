# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0-alpha] - 2026-08-20

### Major Structural & Econometric Re-Architecting (Peer Review Remediation)
- **Competing-Risk Multi-State Markov Engine (`R/05_workforce_model.R`)**: Replaced additive difference outflows with an exact continuous-time transition intensity matrix ($P = \exp(Q \cdot \Delta t)$), enforcing $\sum p_k + p_{\text{stay}} \equiv 1.0000$, total demographic conservation, and zero probability leakage.
- **Statutory Senior Retirement Calibration (`parameter_registry.csv`, `R/03_parameters.R`, `R/05_workforce_model.R`)**: Replaced the defective $r_{\text{retire}} = 0.025$ (40-year career span) with $r_{\text{retire}} = 0.125$ (12.5%/year; 8-year expected span) reflecting Tunisian civil service Law 83-112 mandatory retirement at ages 62–65.
- **Internal Domestic Mobility (`R/05_workforce_model.R`)**: Incorporated internal geographic reallocation transitions ($p_{\text{geo\_trans}} = 0.045$/year from `interior_underserved` to `coastal_metro` public hospital sectors).
- **Diaspora Return Allocation (`R/05_workforce_model.R`)**: Distributed returning specialists 30% to public university/regional hospitals and 70% to private practice across mid-career and senior strata.
- **Endogenous Random Utility Policy Engine (`R/04_migration_model.R`, `R/08_policy_scenarios.R`)**: Replaced exogenous probability multipliers with direct utility shifts ($\Delta U_{\text{wage}}, \Delta U_{\text{infra}}, \Delta U_{\text{rural}}$) in the Random Utility Model choice function, with annual policy efficacy decay ($\delta_{\text{policy}} = 0.035$/year) capturing inflation erosion and depreciation.
- **Specialty-Specific Migration Realization Vectors (`R/04_migration_model.R`, `parameter_registry.csv`)**: Stratified realization friction across clinical disciplines ($\kappa_{\text{generalist}} = 0.245$, $\kappa_{\text{medical}} = 0.350$, $\kappa_{\text{surgical}} = 0.490$) reflecting European licensing bottlenecks (EVC) vs acute shortages.
- **Structural Utility Modifiers Registered (`parameter_registry.csv`, `R/03_parameters.R`)**: Explicitly registered and parameterized all stratum utility modifiers (`stage_mod`, `sector_mod`, `geo_mod`, `spec_mod`) from empirical regressions.
- **Strict Temporal Validation Split (`R/06_calibration.R`, `R/07_validation.R`)**: Strictly partitioned empirical timeline: calibrated $\beta_0$ and $\Delta \beta_{2021+}$ on **2020–2021** training sample, and validated on **2022–2024** out-of-sample holdout data.
- **Official Destination Registry Ingestion (`R/01_import.R`, `data/raw/destination_registries_france_germany.csv`)**: Replaced hardcoded destination vectors with ingested official DREES (France) and Bundesärztekammer (Germany) intake registries.
- **CHEERS 2022-Compliant Economic Costing (`R/09_economic_evaluation.R`)**:
  - Incorporated training deadweight loss on incremental emigrants in Scenario 4 (Training Expansion).
  - Added complementary clinical operational support costs (35% factor for nursing/diagnostics/consumables).
  - Reported both undiscounted and discounted public physician-years retained.
- **Standard Parametric PSA Distributions (`R/03_parameters.R`, `R/10_sensitivity.R`)**: Replaced uniform distributions with Beta (probabilities), Log-Normal (relative risks), and Gamma (costs) distributions, with end-to-end active ratio stock propagation.
- **Automated Testing Suite (`tests/testthat/test_workforce_pipeline.R`)**: Expanded test suite to 55 comprehensive tests verifying competing risks, holdout validation, and CHEERS metrics.

---

## [0.3.0-alpha] - 2026-08-20

### Finalized & Locked (Round 2 Peer-Review Technical Alignment)
- **Baseline Initialization via IPF**: Codified 2-dimensional Iterative Proportional Fitting (IPF / raking) to initialize the 36-cell baseline stock tensor from INS and *Carte Sanitaire* marginals.
- **Inactivity Filter Timing**: Formally specified that the Active Practice Ratio ($\alpha = 0.88$) operates strictly as a baseline initial filter at $t_0 = 2020$, ensuring subsequent dynamics obey pure stock-flow conservation.
- **Compound Scenario Multiplicative Bounding**: Implemented the multiplicative risk reduction rule ($\text{RR}_{\text{package}} = \prod_k \text{RR}_k$) for Scenario 5 (Comprehensive Reform Package) to guarantee diminishing marginal returns.
- **Rebuttal Letter Finalization**: Expanded `REBUTTAL_LETTER.md` with a dedicated Round 2 technical response section and updated audit trail.
- **Methodology Locked**: All core equations, parameters, state structures, and governance rules locked for implementation.

---

## [0.2.0-alpha] - 2026-08-20

### Changed & Fixed (Post-Reviewer 1 Methodological Alignment)
- **State-Space Parsimony**: Collapsed high-dimensional state space to a policy-relevant 36-cell cohort tensor ($3 \text{ Career Stages} \times 2 \text{ Sectors} \times 2 \text{ Regions} \times 3 \text{ Specialties}$).
- **Migration Realization Gap**: Integrated the Intention-to-Action Realization Factor ($\kappa = 0.35$, $\text{Uniform}[0.25, 0.45]$) to scale survey intentions to actual physical departures.
- **OR-to-RR Non-Collapsibility**: Implemented Zhang & Yu (1998) transformation formula across parameter ingestion protocols.
- **Discrete-Choice Identification**: Redesigned calibration to 2 global scalar parameters ($\beta_0, \Delta \beta_{2021+}$) anchored on pooled LMIC DCE meta-analytic weights (Mandeville et al., 2014).
- **Workforce Stock & Proxy Correction**: Applied Active Practice Ratio ($\alpha = 0.88$) and Administrative Clearance Multiplier ($\lambda_{\text{exit}} = 0.75$).
- **Inframarginal Wage Bill Costing**: Formulated full public wage bill expansion ($\Delta C = N_{\text{public}} \cdot \Delta w$) in economic evaluation.
- **Net Human Capital Valuation**: Applied a 40% resident hospital labor offset against gross educational costs.
- **Cost-Consequence Framing**: Established Cost-Consequence Analysis (CCA) and Budget Impact Analysis (BIA) with milestone reporting at 2030, 2040, and 2050 as primary economic deliverables.
- **Documentation**: Generated `REBUTTAL_LETTER.md` providing systematic point-by-point responses and modification logs.

---

## [0.1.0-alpha] - 2026-08-20

### Added
- **Repository Architecture & Governance Protocol**:
  - `README.md`: High-level project blueprint, methodological pillars, and reproducibility roadmap.
  - `PROJECT_SPEC.md`: Full scientific specification detailing the WHO Health Labour Market Framework, Push-Pull migration dynamics, Macro-Meso-Micro determinants hierarchy, Random Utility / Discrete Choice Econometrics, Dynamic Cohort Markov simulation engine (2020–2050), and Cost-Consequence / Cost-Effectiveness evaluation.
  - `DATA_SPEC.md`: Strict research data governance protocol, source provenance inventory (CNOM, Ministry of Health, INS, DREES, Bundesärztekammer, Survey Microdata), target relational parquet schemas, and data validation rules.
  - `LITERATURE_SPEC.md`: Multilingual literature taxonomy (`tunisia/`, `north_africa/`, `international/`, `methods/`), systematic search protocol, and standard parameter extraction matrix template.
  - `ASSUMPTIONS.md`: Structural demographic conservation laws, formal definitions for 6 policy counterfactual scenarios (SCEN_0 to SCEN_5), economic costing boundaries, and three-tier uncertainty protocol (DSA, PSA, Structural Stress-Testing).
  - Directory structure initialized with `.gitkeep` markers across `data/`, `literature/`, `R/`, `tests/`, `outputs/`, and `manuscript/`.

### Rules & Safeguards Enforced
- Strict prohibition of synthetic, fabricated, or mock datasets.
- Strict prohibition of premature parameter assumptions prior to empirical extraction.
- Read-only immutability enforced for `data/raw/`.
