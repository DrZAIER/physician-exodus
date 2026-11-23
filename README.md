# Physician emigration and retention policies in Tunisia

A reproducible stock-and-flow model of Tunisia's physician workforce, with policy
scenarios for retention, return migration and training expansion (2024–2040).

This repository accompanies a manuscript prepared for *Human Resources for Health*.
The revision responds to a major-revision review: it separates the pre- and
post-entry emigration margins, uses exact calibration and true partial rank
correlations, reconciles the return-eligible diaspora pool with destination-country
stocks, adds a break-even analysis and illustrative costs, and provides an
item-level 30-item reporting checklist.

---

## What the model does

The model projects the number of **physicians in active practice in Tunisia** by
single year of age. Each year, the stock changes through:

- entry of graduates who complete postgraduate training and remain in Tunisia;
- emigration before entry (during or immediately after training);
- emigration from the practising stock;
- return migration from a return-eligible diaspora pool with attrition;
- retirement and mortality.

The model is deliberately parsimonious. It does **not** estimate demand, specialty
mix, public/private allocation or wages. It is a supply-side cohort-component
model in the tradition of the JRC SANDEM framework, adapted to a setting where
age-specific migration flows are not observed.

## Key results

| Quantity | Central estimate |
|---|---|
| Practising physicians, 2024 | 15 315 (1.28 per 1 000) |
| Baseline, 2040 | 16 019 (90% interval 14 514–17 565; 1.26 per 1 000) |
| Combined retention and return, 2040 | 21 125 (+5 106; 39 692 physician-years) |
| Remuneration and conditions, 2040 | 19 504 (+3 485; 26 866 physician-years) |
| Career development, 2040 | 17 760 (+1 741; 13 427 physician-years) |
| Return migration, 2040 | 17 320 (+1 301; 9 910 physician-years) |
| Training expansion (+30%), 2040 | 17 131 (+1 112; 3 316 physician-years) |
| Identified annual emigration, 2024 | 582–1 497 (582–1 405 after destination-stock check) |
| Retention effect matching 30% training | 9.6% reduction in emigration |
| Training expansion matching 30% retention | 94% |

The baseline is a plateau, not a collapse. Retention and return outperform
training within 15 years, but the advantage is a modest arithmetic threshold.
The level of emigration is not identifiable from the aggregate stock path.

## Key data caveats

Three different quantities are often conflated in Tunisian policy debate:

| Concept | Approximate magnitude | Source |
|---|---|---|
| Physicians **registered** with the Ordre (CNOM) | 27 935 (2022); 31 804 directory records (2026) | CNOM |
| Physicians **in active practice** (public + private) | 15 315 (2024) | INS / Ministry of Health |
| Physicians **trained in Tunisia** practising abroad | ≥2 500 in France and Germany alone; ~4 000 in OECD countries (2015/16) | CNOM France; German statistics; OECD |

The model is calibrated to the **practising** stock, not to registrations. Annual
emigration is **not directly observed**; it is inferred from the stock path
conditional on training output and retirement. The repository includes an
explicit identifiability analysis showing which combinations of parameters are
consistent with the same observed history.

The return-eligible diaspora pool is **not** a diaspora estimate. It is an
accounting device with an explicit attrition hazard (death abroad, onward
migration and permanent settlement), calibrated to remain within the range
implied by destination-country stocks. Return migrants are assumed to remain in
practice with probability 0.85.

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
│   ├── build_docx.py            # submission DOCX builder
│   └── fig_flow.py              # supplementary flow diagram
├── tests/
│   ├── test_model.py            # calibration, flow identity, hazards, scenarios
│   └── test_analysis.py         # PRCC helper
├── outputs/
│   ├── figures/                 # publication figures (PNG + PDF)
│   ├── tables/                  # parameter, scenario, results, sensitivity, cost tables
│   ├── key_numbers.md           # all numbers cited in the manuscript
│   ├── validation_report.md     # automated consistency checks
│   ├── results_summary.json     # machine-readable summary
│   └── environment.txt          # Python and package versions
├── docs/
│   ├── 01_evidence_and_data_assessment.md
│   ├── 02_model_methodology.md
│   └── 03_reporting_checklist.md
├── manuscript/
│   ├── manuscript.md            # editable copy of the submission manuscript
│   └── additional_file_1.md
├── submission/
│   ├── Manuscript_HRH.md / .docx
│   ├── Additional_file_1.md / .docx
│   ├── Title_page.md
│   ├── Cover_letter.md / .docx
│   ├── Submission_checklist.md
│   └── Figures/Fig1.pdf … Fig9.pdf, FigS1.pdf
├── .github/workflows/ci.yml
├── run_all.py
├── requirements.txt
└── README.md
```

## Reproducing the analysis

Requires Python 3.10+ (tested with 3.14).

```bash
pip install -r requirements.txt
python run_all.py
pytest -q
```

Runtime is about 2–4 minutes on a laptop. All outputs are written to `outputs/`.
The random seed is fixed (`20261121`) so results are exactly reproducible.

The pipeline writes:

- `outputs/key_numbers.md` — every number cited in the manuscript;
- `outputs/validation_report.md` — calibration, flow-identity and ranking checks;
- `outputs/results_summary.json` — machine-readable results;
- `outputs/tables/` — CSV versions of all tables and sensitivity grids;
- `outputs/figures/` — PNG and PDF versions of all figures.

To rebuild the Word files after editing the markdown:

```bash
python src/build_docx.py
```

## Model parameters

All parameters, their plausible ranges and their evidence status (observed,
estimated, assumed) are documented in `docs/02_model_methodology.md`,
`outputs/tables/table2_parameters.csv` and Additional file 1, Table S4.

The Monte Carlo priors are chosen to cover the identified range of σ and
training output. The post-entry emigration flow `m` is recalibrated exactly for
every draw; the maximum absolute calibration error is 0.14 physicians across
2 000 draws.

## What the model cannot establish

- It does not identify the true level of emigration. The observed stock path is
  consistent with 582–1 497 annual emigrants depending on how many graduates
  enter practice; a destination-stock check narrows this to 582–1 405.
- It does not estimate causal effects of policies. Scenario effects are
  **assumed effect sizes**, tested across plausible ranges.
- It does not model demand, vacancies, regional maldistribution, specialty mix
  or quality of care.
- It does not model temporary or circular migration explicitly; return migrants
  are assumed to remain in practice with probability 0.85.
- It is not externally validated. The historical comparison is a retrospective
  consistency check (hindcast), not validation against independent data.
- The cost figures are illustrative, undiscounted and exclude infrastructure and
  demand-side costs. Wages are transfers, not resource costs.

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
| `Additional_file_1.docx` / `.md` | Supplementary tables and item-level 30-item reporting checklist |
| `Figures/Fig1.pdf` … `Fig9.pdf`, `FigS1.pdf` | Figure files, renamed for submission |
| `Submission_checklist.md` | Requirement-by-requirement checklist and author actions |

Current length: 3 646 words (Background–Conclusions) and 339 words (abstract),
i.e. 3 985 words including the abstract, within the 4 000-word limit.

## Round 2 revision

The Round-2 scientific revision (v2.1.1) is in `revision_round2/`. It corrects the return-pool accounting, bounds the policy-ranking claims, adds conservative-effect, training-completion, calibration-endpoint and PRCC-stability analyses, separates fiscal from resource costs, and includes the revised manuscript and supplement. See `revision_round2/README.md`.

## Version control

The repository is initialised with Git. `main` holds the current revision; the
pre-revision baseline is commit `3f40cfb`, tagged `pre-review-baseline`.
`revision` is the development branch used for the peer-review response. To
publish it on GitHub:

```bash
git remote add origin https://github.com/<owner>/physician-exodus.git
git push -u origin main
git push -u origin revision
git push --tags
```

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs the test suite on
every push and pull request. The `gh` command-line tool was not available in the
authoring environment, so the remote must be created in the GitHub web interface
or with an authenticated `gh` installation.

## Licence and citation

Code: MIT licence. Derived data tables: CC BY 4.0, with attribution to the
original sources listed in each file.

If you use this work, please cite the accompanying manuscript (see
`submission/Manuscript_HRH.md`).
