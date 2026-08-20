# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
