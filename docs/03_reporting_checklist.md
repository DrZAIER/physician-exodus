# Reporting checklist

This study is reported against the domains of the good practice reporting
guideline for health workforce projection models proposed by Lee et al.
(*Human Resources for Health* 2024;22:25). The guideline contains 30 items; the
table below groups them by domain and indicates where each is addressed. Items
that are not applicable are marked.

| Domain | Item / requirement | Where addressed | Comment |
|---|---|---|---|
| Study identification | Title, aims, rationale | Title; Background | |
| Model type | Explicit statement of model class | Methods, "Model structure" | Cohort-component stock-and-flow model |
| Scope | Occupations, sectors, geographical scope | Methods, "Definitions and data" | Physicians in active practice, national |
| Time horizon | Base year, projection horizon, time step | Methods | 2008 base; 2017–2024 calibration; annual to 2040 |
| Population | Definition of the workforce counted | Methods; Table 1 | Practising physicians, excluding most residents |
| Data sources | Sources, periods, definitions, limitations | Table 1; Additional file 1 | |
| Data quality | Treatment of missing, incomplete or inconsistent data | Methods; Results, "The emigration level is not identifiable" | Explicit identifiability analysis |
| Model structure | Equations and flow diagram | Methods; Additional file 1, Fig. S1 | |
| Entry | Training pipeline and lag | Methods | Five-year lag; 29–33 entry ages |
| Exits | Retirement, mortality, emigration | Methods | Age-specific hazards |
| Migration | Immigration, emigration, return | Methods | Pre-entry and post-entry emigration; return pool |
| Assumptions | List of key assumptions and their basis | Methods; Table 2; Additional file 1 | Observed / estimated / assumed status |
| Parameterisation | Values, ranges, sources | Table 2; Additional file 1 | |
| Calibration | Target data and method | Methods, "Calibration and identifiability" | 2024 stock; root finding |
| Historical validation | Comparison with observed data | Results, "Retrospective fit"; Fig. 1 | Hindcast, not external validation |
| Uncertainty | Parameter and structural uncertainty | Methods; Results; Figs. 1–3, 6, 8 | Monte Carlo and structural scenarios |
| Sensitivity | Which parameters matter | Results, "Sensitivity"; Fig. 6 | PRCC and one-at-a-time |
| Scenario definitions | Policy levers and effect sizes | Table 3; Additional file 1 | Range-tested assumptions |
| Results | Workforce, flows, density | Tables 4–5; Figs. 1–5 | |
| Interpretation | What the model can and cannot establish | Discussion | |
| Generalisability | Applicability beyond Tunisia | Discussion | Methodological relevance to other LMICs |
| Limitations | Data, structure, validation | Strengths and limitations | |
| Reproducibility | Code, data, software | Declarations; README | Public repository |
| Ethical considerations | Data governance | Declarations | Aggregate secondary data |

## Notes on items that are only partly met

- **External validation.** No independent validation data exist. The
  retrospective comparison is a consistency check, and the manuscript says so
  explicitly.
- **Demand-side projections.** The model is supply-only, so the guideline's
  demand–supply gap items are not applicable. This is stated in the Methods and
  Limitations.
- **Micro-level heterogeneity.** The model does not represent individual
  physicians, specialty choice or region. This is a deliberate trade-off
  between transparency and granularity, justified by data availability.

## Software and code

- Language: Python 3.14
- Libraries: NumPy, pandas, SciPy, Matplotlib
- Random seed: 20261121
- Entry point: `python run_all.py`
- Outputs: `outputs/figures/`, `outputs/tables/`, `outputs/results_summary.json`
