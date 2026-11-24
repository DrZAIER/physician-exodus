# Physician Exodus — Tunisia physician workforce model

**Version:** 3.0.0  
**Manuscript:** Retention, return or training? A stock-and-flow simulation of Tunisia's physician workforce under incomplete migration data  
**Target journal:** *Health Care Science* (Wiley / Tsinghua University Press), Original Article  
**Public repository:** https://github.com/DrZAIER/physician-exodus  
**Release:** tag and branch `v3.0.0`. The repository's `main` branch currently contains a separate R-based project; the Python model lineage is published under `v3.0.0`, with the earlier model under `v2.1.2`.

## What the model does

The model projects the number of physicians in active practice in Tunisia by single year of age, 2008–2040. Each year, the stock changes through:

- entry of graduates who complete postgraduate training and remain in Tunisia;
- pre-entry international emigration (the φ share of pipeline non-entry);
- domestic non-entry (further training, non-clinical work, inactivity);
- post-entry emigration from the practising stock;
- return migration from a return-eligible accounting pool;
- retirement and mortality.

The model is deliberately parsimonious. It is a **supply-only** national model. It does not estimate demand, adequacy, specialty mix, regional distribution, productivity, quality of care or the causal effect of policy. The return-eligible pool is an accounting construct, not a measured diaspora.

## Key results (central calibration)

| Quantity | Value |
|---|---:|
| Practising physicians, 2024 | 15 315 |
| Baseline 2040 | 17 262 |
| Baseline Monte Carlo median (90% simulation interval) | 17 439 (15 823–19 246) |
| Remuneration and conditions, 2040 | 19 172 (+1 910) |
| Career development, 2040 | 18 216 (+955) |
| Return migration, 2040 | 17 983 (+722) |
| Doctorate-output expansion (+30%), 2040 | 18 498 (+1 237) |
| Combined strategy, 2040 | 20 068 (+2 807) |
| Retention reduction matching 30% training expansion | 19.4% |
| Training expansion matching 30% retention effect | 46.3% |

The ranking is conditional on the unobserved emigration share φ, the assumed policy effect sizes, the age structure and the 9–12-year training pipeline. It is not a forecast or a causal estimate.

## Reproduce

```bash
pip install -r requirements.txt
python run_all.py
pytest -q
```

The pipeline uses 4 000 Monte Carlo draws and the fixed seed `20261121`. It regenerates all tables, figures, `key_numbers.md`, `results_summary.json` and `validation_report.md`.

**Reference environment:** Python 3.14.7; NumPy 2.5.2; pandas 3.0.5; SciPy 1.18.1; Matplotlib 3.11.1; Windows 11. See `outputs/environment.txt`.

## Repository structure

```
.
├── VERSION
├── RELEASE_NOTES.md
├── CITATION.cff
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── run_all.py
├── src/
│   ├── model.py
│   ├── analysis.py
│   ├── build_docx.py
│   └── fig_flow.py
├── data/
│   ├── raw/
│   └── processed/
├── data_dictionary/
│   └── data_provenance.md
├── tests/
│   ├── test_model.py
│   └── test_analysis.py
└── outputs/
    ├── figures/
    ├── tables/
    ├── key_numbers.md
    ├── results_summary.json
    ├── validation_report.md
    └── environment.txt
```

## Data

The processed CSVs are analysis-ready aggregate data. The raw source PDFs are retained for audit verification and remain subject to the original publishers' terms. See `data_dictionary/data_provenance.md` and supplementary Table S2 for sources, access dates, transformations and limitations.

Key data caveats:

- The practising stock is from INS/Ministry of Health; 2024 = 15 315.
- The 2010 WHO estimate (12 996) is an initial-condition anchor only.
- The 2013/2021 doctorate counts are from Zehnati 2024; the 2024 value (1 305) is a 5.0%/year extrapolation, not an observation.
- Destination stocks are lower bounds with different definitions.
- The 2020–2021 public-sector count contains a known discontinuity.
- The return-eligible pool is an accounting construct, not a measured diaspora.

## Tests and validation

`pytest -q` runs 21 tests covering calibration, stock-flow identity, pipeline identity, training lags, age progression, non-negative stocks, return accounting, scenario consistency, PRCC helper, density conversion, discounting and draw reproducibility. `outputs/validation_report.md` reports PASS.

## Version comparison

See `RELEASE_NOTES.md` for the differences from `v2.1.2` (2 000 vs 4 000 draws; baseline 16 019 vs 17 262; combined 21 125 vs 20 068; uniform five-year vs cohort-specific 3–6-year post-doctorate lag; no φ separation vs separated non-entry).

## Release status and remaining steps

The `v3.0.0` tag was created from the Python model lineage on 24 November 2026 and pushed to the public repository. The release contains the Round 3 cohort-specific model, 4 000-draw Monte Carlo analysis, 21 tests and the regenerated outputs.

Remaining optional steps:

1. Confirm the license (`MIT` for code; `CC-BY-4.0` recommended for documentation and derived data).
2. Review the raw source PDFs and remove them if the publisher's terms do not permit redistribution.
3. Archive the release on Zenodo and obtain a DOI.
4. Add the final manuscript citation when published.

## Citation

If you use the model, cite the manuscript and the software release. See `CITATION.cff`.
