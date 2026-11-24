# Release notes — version 3.0.0

**Release date:** 24 November 2026  
**Status:** published as tag `v3.0.0` (and branch `v3.0.0`). The repository's `main` branch contains a separate R-based project; this release preserves the Python model lineage.

## What this release is

Version 3.0.0 is the Round 3 cohort- and track-specific model used for the *Health Care Science* submission. It is distinct from the public `v2.1.2` tag, which contains the Round 2 model.

## Changes from v2.1.2

### Model

- Added cohort- and track-specific post-doctorate lags (3–6 years) and the 6-year undergraduate lag, giving a 9–12-year total pathway.
- Added the separation of pipeline non-entry into pre-entry international emigration (φ) and domestic non-entry.
- Added exact return-pool accounting with recycling and no-recycling variants.
- Added alternative emigration age profiles and historical ramps.
- Added continuous retirement-shift interpolation.
- Added `emig_future_mult` as a projection-only shock.

### Analysis

- 4 000 Monte Carlo draws with exact recalibration of the post-entry flow per draw.
- True rank-residual PRCCs with bootstrap intervals.
- Identifiability grid with full-period and excluding-2020–2021 criteria.
- Destination stock-flow triangulation.
- Structural escalation on post-entry and both margins.
- Break-even analysis.
- Retention-margin, training-timing, age-shape, retirement/mortality and calibration-endpoint sensitivities.
- Fiscal transfers and resource costs separated; 3%/5% discounting.

### Outputs

- Regenerated tables and figures at 300 dpi (PNG) and vector PDF.
- `key_numbers.md`, `results_summary.json`, `validation_report.md`, `environment.txt`.
- 21 automated tests.

### Documentation

- `README.md` updated for version 3.0.0.
- `data_dictionary/data_provenance.md` added.
- `CITATION.cff` updated.
- `VERSION` added.

## Reproduction

```bash
pip install -r requirements.txt
python run_all.py
pytest -q
```

Seed: `20261121`. Environment: Python 3.14.7, NumPy 2.5.2, pandas 3.0.5, SciPy 1.18.1, Matplotlib 3.11.1.

## Validation

All 13 Round 3 numerical targets reproduce exactly. Validation report: PASS. Tests: 21 passed.

## Known limitations

- The 2024 doctorate value (1 305) is an extrapolation, not an observation.
- The central calibration is outside the full-period 2% acceptable-fit set.
- 332 of 4 332 Monte Carlo candidate draws were infeasible and excluded.
- The return hazards are unvalidated.
- The cost unit values are illustrative.
- The model is supply-only; it has no demand, adequacy, specialty, regional or productivity component.

## Release status and remaining steps

The `v3.0.0` tag and branch were pushed to the public repository on 24 November 2026. The release contains the Round 3 cohort-specific model, the 4 000-draw Monte Carlo analysis, 21 tests and the regenerated outputs.

Remaining optional steps:

1. Confirm the license and `CITATION.cff`. The LICENSE uses “Copyright (c) 2026 Firas Zaier and Mariem Zribi”.
2. Review the raw source PDFs and remove them if the publisher's terms do not permit redistribution.
3. Archive the release on Zenodo and obtain a DOI.
4. Add the final manuscript citation when published.
