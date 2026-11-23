# Reporting checklist

This study is reported against the 30-item Good Practice Reporting Guideline for
Health Workforce Models proposed by Lee et al. (*Human Resources for Health*
2024;22:25). The item-level checklist is reproduced in Additional file 1,
Table S13. This document records the status of each item and the reasons for
items that are not applicable to a supply-only model.

| Item | Guideline requirement | Where addressed | Status |
|---|---|---|---|
| 1 | Identify the study as health workforce planning and specify the professionals | Title; Background | Reported |
| 2 | Structured abstract with context, methods, results and alternative analyses | Abstract | Reported |
| 3 | Context, aims and practical relevance | Background | Reported |
| 4 | Study population characteristics | Methods, "Definitions and data"; Table 1 | Reported |
| 5 | Geographical area and level | Methods; Title | Reported (national) |
| 6 | Whether a specific health condition is the focus | Methods, "Design" | Reported (none; workforce supply) |
| 7 | Health professionals covered | Title; Methods | Reported (physicians) |
| 8 | Time horizon | Methods, "Design" | Reported (2008–2040; projection 2024–2040) |
| 9 | Scope of activities | Methods, "Design" | Reported (healthcare only) |
| 10 | Overall analytical framework | Methods, "Model structure"; Figure S1 | Reported |
| 11 | Parameters and variables, and how estimated | Methods; Table 2; Table S4 | Reported |
| 12 | Demand-side model and statistical approach | — | NA: supply-only model |
| 13 | Supply-side model and statistical approach | Methods, "Model structure" | Reported |
| 14 | Gap analysis methodology | — | NA: no demand projection |
| 15 | Budgetary analysis methodology | Methods, "Illustrative costs"; Table 6 | Partially reported: illustrative cost per physician-year, not a fiscal budget model |
| 16 | Characterising uncertainty | Methods, "Uncertainty and sensitivity"; Table S4 | Reported |
| 17 | Key assumptions and justification | Methods; Table 2; "Strengths and limitations" | Reported |
| 18 | Methods for validation and scenario parameter derivation | Methods; Table S12 | Reported (internal consistency and hindcast; no external validation) |
| 19 | Data sources, quality and relevance | Table 1; Additional file 1 | Reported |
| 20 | Summary of projection results for each profession | Results; Table 5; Table S5 | Reported |
| 21 | Projections for geographical areas | — | NA: national model |
| 22 | Supply–demand gap over time | — | NA: no demand model |
| 23 | Geographical distribution | — | NA: no regional disaggregation |
| 24 | Effects of policies and scenarios, including financial impact | Results, "Policy scenarios"; Tables 5–6 | Reported (supply effects and illustrative costs) |
| 25 | Effects of uncertainty and sensitivity | Results, "Sensitivity"; Fig. 6; Table S5 | Reported |
| 26 | Model validation and robustness | Results, "Structural uncertainty"; Table 7; Table S12 | Reported (internal robustness; no external validation) |
| 27 | Key findings, implications and limitations | Discussion | Reported |
| 28 | Policy recommendations on planning, education, training, recruitment and retention | Discussion, "Policy implications" | Reported |
| 29 | Source of funding | Declarations | Reported |
| 30 | Conflicts of interest | Declarations | Reported |

## Notes on items that are only partly met

- **External validation.** No independent validation data exist. The
  retrospective comparison is a consistency check, and the manuscript says so
  explicitly.
- **Demand-side projections.** The model is supply-only, so the guideline's
  demand–supply gap items are not applicable. This is stated in the Methods and
  Limitations.
- **Budgetary analysis.** The cost analysis is illustrative: it attaches unit
  costs to supply effects but does not model the government budget, financing
  mix or cost offsets from improved health outcomes.
- **Micro-level heterogeneity.** The model does not represent individual
  physicians, specialty choice or region. This is a deliberate trade-off
  between transparency and granularity, justified by data availability.

## Software and code

- Language: Python 3.14
- Libraries: NumPy, pandas, SciPy, Matplotlib
- Random seed: 20261121
- Entry point: `python run_all.py`
- Tests: `pytest -q`
- Outputs: `outputs/figures/`, `outputs/tables/`, `outputs/results_summary.json`,
  `outputs/key_numbers.md`, `outputs/validation_report.md`
