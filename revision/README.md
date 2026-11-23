# Revision 2.0 workspace

This directory contains the scientific and computational revision of the Tunisia physician workforce manuscript. The v1.1.0 and pre-review materials are preserved; this workspace does not overwrite the original submission files outside `revision/`.

## Deliverables

| File | Purpose |
|---|---|
| `Manuscript_HRH_Revised.docx` / `.md` | Revised manuscript (two authors) |
| `Additional_file_1_Revised.docx` / `.md` | Revised supplementary material |
| `Scientific_Audit_Report.md` | What was wrong, what was changed and why |
| `Revision_Log.md` | Change log |
| `Figure_Revision_Register.md` | Figure-by-figure update register |
| `Reference_Audit.csv` | Reference verification register |
| `Final_QA_Report.md` | Automated and manual QA |
| `audit/Issue_Register.md` | Issue tracker with status |
| `source_preserved/` | v1.1.0 manuscript, supplement and key outputs |

## Reproduce

Requires Python 3.10+ (tested with 3.14).

```bash
cd revision
pip install -r requirements.txt
python run_all.py
pytest -q
python src/build_docx.py
```

Runtime is several minutes with 4 000 Monte Carlo draws. All outputs are written to `outputs/`.

## Structure

```
revision/
├── src/
│   ├── model.py              # corrected cohort-component model
│   ├── analysis.py           # calibration, scenarios, MC, sensitivity, figures, tables
│   ├── build_docx.py         # DOCX builder
│   └── fig_flow.py           # supplementary flow diagram
├── tests/
│   ├── test_model.py         # calibration, flow, pipeline, φ, lag, age, hazards
│   └── test_analysis.py      # PRCC helper
├── data/                     # copied input data (unchanged)
├── outputs/
│   ├── figures/              # regenerated PNG + PDF
│   ├── tables/               # generated CSV tables
│   ├── key_numbers.md        # all numbers cited in the manuscript
│   ├── validation_report.md  # automated checks
│   ├── results_summary.json
│   └── environment.txt
├── audit/Issue_Register.md
├── figures/                  # submission-named PDF copies (Fig1–Fig9, FigS1)
├── source_preserved/
├── Manuscript_HRH_Revised.md/.docx
├── Additional_file_1_Revised.md/.docx
├── Scientific_Audit_Report.md
├── Revision_Log.md
├── Figure_Revision_Register.md
├── Reference_Audit.csv
└── Final_QA_Report.md
```

## Key specification

The model separates pipeline non-entry into:

- international pre-entry emigration, \(\phi(1-\sigma)G\);
- domestic non-entry, \((1-\phi)(1-\sigma)G\).

Only international emigration enters the return-eligible pool. The central \(\phi=0.50\) is an assumption, tested from 0 to 1. The training expansion applies to graduate cohorts from 2031; entrants appear after the postgraduate lag.

## Remaining author actions

Complete the funding, competing-interest, contributions and acknowledgements statements; insert the repository DOI; confirm the AI-tool names and Mariem Zribi's ORCID preference.
