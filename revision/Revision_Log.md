# Revision Log

**Revision:** 2.0
**Date:** 23 November 2026
**Original state preserved:** Git tag `v1.1.0`; `revision/source_preserved/`

---

## 1. Model and code

| Change | File | Reason |
|---|---|---|
| Added φ (share of pipeline non-entry that is international emigration) | `src/model.py` | Stop equating non-entry with emigration |
| Split X into X_pre and X_dom; only X_pre enters pool | `src/model.py` | Conceptual correction |
| Policy pre-entry effect applies to φX, not all X | `src/model.py` | Consistency with corrected definition |
| Training multiplier applied to graduate cohorts from 2031, entrants after lag | `src/model.py` | Correct timing |
| Continuous retirement-age shift by interpolation | `src/model.py` | Fractional shifts distinct |
| Added mortality multiplier | `src/model.py` | Sensitivity |
| Added age-shape alternatives (young/old) | `src/model.py` | Initial age-structure uncertainty |
| Added cap-binding and hazard diagnostics | `src/model.py` | Audit issue A12 |
| MC increased to 4 000 draws | `src/analysis.py` | Stability of percentiles/PRCC |
| Added φ, initial pool and mortality priors | `src/analysis.py` | Cover structural uncertainty |
| δ prior aligned to 0.04–0.12 (mean 0.08) | `src/analysis.py` | Resolve prior/central mismatch |
| Added rank distribution and overlap probabilities | `src/analysis.py` | Policy-ranking uncertainty |
| Added φ, lag, age-shape and retirement sensitivity | `src/analysis.py` | Audit issues A1, A3, A5, A4 |
| Split costs into fiscal transfers and resource costs | `src/analysis.py` | Economic interpretation |
| Added flow/pipeline density/PY validation | `src/analysis.py` | Reproducibility |
| Added 13 model tests | `tests/test_model.py` | Guards against regression |
| Updated tests for φ, pipeline, lag, age shape | `tests/test_model.py` | New specification |

---

## 2. Manuscript

| Change | Reason |
|---|---|
| Exactly two authors: Firas Zaier, Mariem Zribi; correct affiliations, email, ORCID | Task requirement |
| Removed third-author placeholders | Task requirement |
| Added φ-based conceptual framework and equations | Audit issue A1 |
| Revised abstract, Results, Discussion and Conclusions to new estimates | Reanalysis |
| Narrowed policy claim: only combined/remuneration robustly beat training | New ranking |
| Added break-even (14.5%; 62%), φ/lag/age/retirement sensitivity, fiscal/resource costs | Audit issues |
| Clarified admissions vs graduates vs practising physicians; removed 1 900 baseline | Audit issue A6 |
| Labelled destination screen as plausibility, not validation | Audit issue A2 |
| Described 2020–2021 as unresolved discontinuity | Audit issue A24 |
| Retained contributions/funding/competing interests/acknowledgements as placeholders | Do not invent |
| Data availability flagged pending repository DOI | Do not invent |
| Word count reduced to 3 999 including abstract; abstract 347 words | Journal limit |
| 7 tables, 9 figures, 44 references | Updated structure |

---

## 3. Supplementary material

| Change | Reason |
|---|---|
| S1 notation includes φ, X_pre, X_dom | New model |
| S3 effect sizes clarify pre-entry effects apply to φ share | New model |
| S4 priors updated: φ, initial pool, mortality, δ 0.04–0.12, 4 000 draws | New MC |
| S5 deterministic vs MC labelled; new values | Reanalysis |
| S6 identifiability grid includes non-entry, φ=0.5 and φ=1 | New model |
| S7 structural scenarios updated; both margins apply to φ share | New model |
| S8 break-even updated (14.5%; 62%) | Reanalysis |
| S9 diaspora sensitivity updated | Reanalysis |
| S10 lag/age/retirement sensitivity added | Audit issues A3–A5 |
| S11 costs split fiscal/resource | Audit issue A16 |
| S12 validation expanded | Reproducibility |
| S13 item-level 30-item checklist | Audit issue A19 |

---

## 4. Deliverables produced

- `Manuscript_HRH_Revised.docx`
- `Additional_file_1_Revised.docx`
- `Scientific_Audit_Report.md`
- `Revision_Log.md` (this file)
- `Figure_Revision_Register.md`
- `Reference_Audit.csv`
- `Final_QA_Report.md`
- `audit/Issue_Register.md`
- `README.md`
- `src/`, `tests/`, `data/`, `outputs/`

---

## 5. Commands

```bash
cd revision
pip install -r requirements.txt
python run_all.py
pytest -q
python src/build_docx.py
```

The pipeline writes `outputs/key_numbers.md`, `outputs/validation_report.md`, `outputs/results_summary.json`, tables and figures. The DOCX builder writes the two revised manuscript files plus the cover letter.

---

## 6. Remaining author actions

1. Complete funding, competing-interest, contributions and acknowledgements statements.
2. Insert the repository DOI/URL in the data availability statement.
3. Confirm the AI-tool statement names the tools actually used.
4. Confirm that Mariem Zribi's affiliation and email are correct and that no ORCID is to be added.
5. Re-run the pipeline and tests after any further edits; rebuild the DOCX.
