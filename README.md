# Physician emigration and retention policies in Tunisia

A reproducible stock-and-flow model of Tunisia's physician workforce, with policy
scenarios for retention, return migration and training expansion (2024–2040).

This repository accompanies a manuscript prepared for *Human Resources for Health*.

---

## What the model does

The model projects the number of **physicians in active practice in Tunisia** by
single year of age. Each year, the stock changes through:

- entry of graduates who complete postgraduate training and remain in Tunisia;
- emigration before entry (during or immediately after training);
- emigration from the practising stock;
- return migration from the diaspora;
- retirement and mortality.

The model is deliberately parsimonious. It does **not** estimate demand, specialty
mix, public/private allocation or wages. It is a supply-side cohort-component
model in the tradition of the JRC SANDEM framework, adapted to a setting where
age-specific migration flows are not observed.

## Key data caveats

Three different quantities are often conflated in Tunisian policy debate:

| Concept | Approximate magnitude | Source |
|---|---|---|
| Physicians **registered** with the Ordre (CNOM) | 27,935 (2022); 31,804 directory records (2026) | CNOM |
| Physicians **in active practice** (public + private) | 15,315 (2024) | INS / Ministry of Health |
| Physicians **trained in Tunisia** practising abroad | ≥2,500 in France and Germany alone; ~4,000 in OECD countries (2015/16) | CNOM France; German statistics; OECD |

The model is calibrated to the **practising** stock, not to registrations. Annual
emigration is **not directly observed**; it is inferred from the stock path
conditional on training output and retirement. The repository includes an
explicit identifiability analysis showing which combinations of parameters are
consistent with the same observed history.

## Repository structure

```
.
├── data/
│   ├── raw/                     # downloaded source documents (PDF, text)
│   └── processed/               # analysis-ready CSV files
│       ├── tunisia_physician_workforce.csv
│       ├── tunisia_registration_and_flows.csv
│       └── population_tunisia.csv
├── src/
│   ├── model.py                 # model equations and simulation engine
│   ├── analysis.py              # calibration, scenarios, uncertainty, figures, tables
│   └── _flows.py                # flow-decomposition table (auxiliary)
├── outputs/
│   ├── figures/                 # publication figures (PNG + PDF)
│   ├── tables/                  # parameter, scenario, results, sensitivity tables
│   ├── mc_draws.csv             # Monte Carlo draws
│   └── results_summary.json     # all numbers cited in the manuscript
├── docs/
│   ├── 01_evidence_and_data_assessment.md
│   ├── 02_model_methodology.md
│   └── 03_reporting_checklist.md
├── manuscript/
│   ├── manuscript.md
│   └── references.md
├── run_all.py
├── requirements.txt
└── README.md
```

## Reproducing the analysis

Requires Python 3.10+ (tested with 3.14).

```bash
pip install -r requirements.txt
python run_all.py
```

Runtime is about 1–3 minutes on a laptop. All outputs are written to `outputs/`.
The random seed is fixed (`20261121`) so results are exactly reproducible.

To reproduce only the figures and tables from the saved Monte Carlo draws, run
the relevant functions in `src/analysis.py`; the full pipeline is inexpensive
enough that rerunning everything is simpler.

## Model parameters

All parameters, their plausible ranges and their evidence status (observed,
estimated, assumed) are documented in `docs/02_model_methodology.md` and
`outputs/tables/table2_parameters.csv`.

## What the model cannot establish

- It does not identify the true level of emigration. The observed stock path is
  consistent with a wide range of emigration flows depending on how many
  graduates enter practice.
- It does not estimate causal effects of policies. Scenario effects are
  **assumed effect sizes**, tested across plausible ranges.
- It does not model demand, vacancies, regional maldistribution, specialty mix
  or quality of care.
- It is not externally validated. The historical comparison is a retrospective
  consistency check (hindcast), not validation against independent data.

## Submission package (*Human Resources for Health*)

The journal requires a maximum of 4 000 words (excluding tables, figures and
additional files), a structured abstract of ≤350 words, Vancouver references,
page and line numbering, double spacing, and editable table objects.

`submission/` contains:

| File | Purpose |
|---|---|
| `Manuscript_HRH.docx` | Submission-formatted manuscript (double spacing, continuous line numbers, page numbers, tables, legends) |
| `Manuscript_HRH.md` | Editable source |
| `Title_page.md` | Standalone title page |
| `Cover_letter.docx` / `.md` | Cover letter with the journal's required declarations |
| `Additional_file_1.docx` / `.md` | Supplementary tables and reporting checklist |
| `Figures/Fig1.pdf` … `Fig8.pdf`, `FigS1.pdf` | Figure files, renamed for submission |
| `Submission_checklist.md` | Requirement-by-requirement checklist and author actions |

Current length: 2 876 words (Background–Conclusions) and 346 words (abstract),
i.e. 3 222 words including the abstract, within the 4 000-word limit.

To rebuild the Word files after editing the markdown:

```bash
python src/build_docx.py
```

## Licence and citation

Code: MIT licence. Derived data tables: CC BY 4.0, with attribution to the
original sources listed in each file.

If you use this work, please cite the accompanying manuscript (see
`manuscript/manuscript.md`).
