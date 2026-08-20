# Physician Exodus from Tunisia: Workforce Projections, Policy Simulation, and Economic Evaluation to 2050

[![Project Status: Conceptualization / Repository Inception](https://img.shields.io/badge/status-specification-blue.svg)](PROJECT_SPEC.md)

---

## 1. Project Overview

This repository hosts the quantitative and economic modeling framework for analyzing and projecting the migration dynamics of physicians from Tunisia. Grounded in health economics, labor market analysis, and epidemiology, this project aims to:

1. Quantify historical and current physician mobility and attrition.
2. Model physician migration decisions using random-utility and discrete-choice frameworks.
3. Project national and sub-national physician workforce stock and density under alternative policy and macroeconomic scenarios through **2050**.
4. Conduct formal cost-consequence (CCA) and cost-effectiveness (CEA) evaluations of proposed retention and recruitment policies.

---

## 2. Methodological Pillars

The research is structured across six integrated analytical frameworks:

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
| Determinants Analysis         |                         | Dynamic Workforce Simulation      |
| - Push-Pull Migration Theory  |                         | - Cohort / State-Transition Model |
| - Macro-Meso-Micro Framework  |                         | - Stock-and-Flow Dynamics (2050)  |
| - Random Utility & DCE Models |                         | - Multi-Scenario Policy Engine    |
+-------------------------------+                         +-----------------------------------+
                                                                     |
                                                                     v
                                                          +-----------------------------------+
                                                          | Economic & Policy Evaluation      |
                                                          | - Fiscal Training Loss Valuation  |
                                                          | - Cost-Consequence Analysis (CCA) |
                                                          | - Cost-Effectiveness / PSA (CEA)  |
                                                          +-----------------------------------+
```

1. **WHO Health Labour Market Framework**: Guides structural supply-and-demand relationships, training entry, labor force participation, and geographic distribution.
2. **Push-Pull Migration Theory**: Categorizes international and domestic drivers of mobility.
3. **Macro-Meso-Micro Determinants Framework**: Systematically links macro-level structural factors, meso-level organizational/workplace factors, and micro-level individual characteristics.
4. **Random-Utility / Discrete-Choice Modeling (RUM / DCE)**: Evaluates physician preferences and relative valuation of wages, working conditions, career development, and geographical incentives.
5. **Cohort / State-Transition Physician Workforce Modeling**: Dynamic Markov stock-and-flow projections stratifying physicians by age, sex, specialty, sector (public/private), and region through **2050**.
6. **Cost-Consequence & Economic Evaluation**: Evaluates budget impact, training cost loss, benefit-cost tradeoffs, and incremental cost-effectiveness of retention packages.

---

## 3. Repository Architecture

The repository adheres strictly to standards for reproducible research:

```
physician-exodus-tunisia/
│
├── README.md                  # Project overview, architecture, and workflow guide
├── PROJECT_SPEC.md            # Detailed scientific specification and analytical plan
├── DATA_SPEC.md               # Data dictionary, source provenance, schema, and governance
├── LITERATURE_SPEC.md         # Literature taxonomy, search protocols, and evidence matrices
├── ASSUMPTIONS.md             # Policy scenario definitions, parameter log, and structural bounds
├── CHANGELOG.md               # Versioning log and project audit trail
│
├── data/                      # Data assets (raw data is strictly read-only and uncommitted)
│   ├── raw/                   # Immutable primary & secondary data extracts
│   ├── processed/             # Cleaned, validated, analysis-ready harmonized datasets
│   └── metadata/              # Data schemas, codebooks, provenance records, validation logs
│
├── literature/                # Literature synthesis and parameter extraction logs
│   ├── tunisia/               # Country-specific workforce studies, reports, ministerial data
│   ├── north_africa/          # Regional LMIC / MENA comparative workforce studies
│   ├── international/         # Global health labor market, brain drain, OECD destination data
│   └── methods/               # Methodological papers (DCE, Markov modeling, CEA/CCA)
│
├── R/                         # Modular R codebase (pipeline scripts, model engines)
├── tests/                     # Unit, regression, and data-integrity tests
│
├── outputs/                   # Generated artifacts (git-ignored raw outputs)
│   ├── figures/               # High-resolution vector and raster visualization outputs
│   ├── tables/                # Formatted regression, projection, and economic tables
│   └── results/               # Model checkpoints, simulation summaries, MCMC / PSA draws
│
└── manuscript/                # Academic manuscript drafts, LaTeX/Rmd source, bibliography
```

---

## 4. Reproducibility & Scientific Governance

- **No Premature Parameterization**: Model parameters must be empirically grounded via systematic data extraction from verified sources or documented calibration protocols.
- **No Synthetic / Fabricated Data**: Placeholder or synthetic datasets are prohibited in production branches.
- **Data Immutability**: `data/raw/` is treated as strictly read-only. All transformations are scripted, idempotent, and logged in `data/processed/`.
- **Modularity & Testing**: Analytical routines in `R/` must be paired with test suites in `tests/` verifying boundary conditions, demographic conservation laws (e.g., population balance equations), and numerical stability.

---

## 5. Development Roadmap & Milestones

- [x] **Phase 0: Inception & Architectural Protocol** (Current)
  - Establish specifications (`PROJECT_SPEC.md`, `DATA_SPEC.md`, `LITERATURE_SPEC.md`, `ASSUMPTIONS.md`).
  - Configure directory tree and reproducible standards.
- [ ] **Phase 1: Literature Synthesis & Parameter Extraction**
  - Systematic evidence synthesis across Tunisia, MENA, and destination countries.
  - Parameter log population in `literature/`.
- [ ] **Phase 2: Data Acquisition & Governance Harmonization**
  - Ingestion of CNOM, Ministry of Health, INS, and international destination registries.
- [ ] **Phase 3: Discrete-Choice & Determinant Econometric Modeling**
  - Estimation of utility functions and marginal willingness-to-pay (MWTP) for retention attributes.
- [ ] **Phase 4: Dynamic Cohort Workforce Simulation (2020–2050)**
  - Development and validation of stock-and-flow Markov engine.
- [ ] **Phase 5: Policy Scenario Simulation & Economic Evaluation (CCA / CEA)**
  - Counterfactual evaluation and multi-criteria sensitivity analysis.
- [ ] **Phase 6: Manuscript Drafting & Dissemination**

---

## 6. License & Citation

*Citation and licensing details to be established upon formal institutional ethical clearance and preprint publication.*
