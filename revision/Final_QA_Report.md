# Final QA Report

**Revision:** 2.0
**Date:** 23 November 2026
**Pipeline:** `revision/run_all.py`
**Seed:** 20261121
**Monte Carlo draws:** 4 000

---

## 1. Execution status

| Check | Result |
|---|---|
| Full pipeline executed | Pass (exit 0) |
| Tests (`pytest -q`) | Pass (13 tests) |
| Validation report | Pass (all checks) |
| DOCX manuscript | Generated (`Manuscript_HRH_Revised.docx`, 7 tables, 187 paragraphs) |
| DOCX supplement | Generated (`Additional_file_1_Revised.docx`, 13 tables, 43 paragraphs) |
| Figures | Regenerated (9 main + Fig. S1; PNG and PDF) |
| Word count | 3 999 including abstract; 3 652 main text |
| Abstract | 347 words |
| References | 44, all cited in text |
| Tables | 7 main tables |
| Figures | 9 main figures + Fig. S1 |

---

## 2. Numerical integrity checks

| Check | Result |
|---|---|
| 2024 calibration error | −0.098 physicians |
| Maximum Monte Carlo calibration error | 0.137 physicians |
| Workforce flow identity, all scenarios | Pass |
| Graduate pipeline identity, all scenarios | Pass |
| Age distributions non-negative | Pass |
| Density calculation | Pass |
| Physician-year calculation | Pass |
| Emigration hazard cap | Does not bind; maximum simulated hazard 0.057 |
| Hazards in [0, 1] | Pass |
| Monte Carlo intervals ordered | Pass |
| PRCCs in [−1, 1] | Pass |
| Combined ranks first in 2040 | Pass in all 4 000 draws |
| Remuneration ranks second | 99.8% of draws |

---

## 3. Key numerical results

| Result | Value |
|---|---|
| 2024 practising stock | 15 315 |
| 2024 total international emigration (φ=0.50) | 563 (245 pre-entry + 317 post-entry) |
| 2024 pipeline non-entry | 491 (245 international + 245 domestic) |
| 2024 return-eligible pool | 4 312 |
| BAU 2040 | 15 821 (MC median 15 830; 90% interval 14 407–17 438) |
| BAU density 2040 | 1.25 per 1 000 (MC 1.25; 1.14–1.38) |
| Combined 2040 | 19 162 (+3 341; 26 085 physician-years) |
| Remuneration 2040 | 18 087 (+2 266; 17 530) |
| Career 2040 | 16 953 (+1 132; 8 762) |
| Training 2040 | 16 914 (+1 092; 3 269) |
| Return 2040 | 16 689 (+868; 6 656) |
| Identified international emigration (φ=0.50) | 262–1 017 |
| Upper bound (φ=1) | 502–1 540 |
| Destination-consistent (φ=0.50) | 481–1 017 |
| Break-even retention | 14.5% |
| Training needed to match 30% retention | 62% |
| Post-entry +3%/yr baseline / combined | 14 461 / 18 315 |
| Both margins +3%/yr baseline / combined | 13 184 / 17 519 |

---

## 4. Manuscript consistency checks

| Check | Result |
|---|---|
| Two authors only | Pass (Firas Zaier, Mariem Zribi) |
| Affiliations, email, ORCID | Applied exactly as specified |
| No third-author placeholder | Pass |
| Abstract ≤350 words | Pass (347) |
| Main text ≤4 000 words | Pass (3 652 main; 3 999 including abstract) |
| Tables cited in order | Pass |
| Figures cited in order | Pass (all 1–9 cited) |
| Table 4 note distinguishes observed 2017 (14 892) from modelled 2017 (14 965) | Pass |
| Deterministic vs Monte Carlo values labelled | Pass |
| Density discrepancy resolved | Pass (both 1.25) |
| δ prior mean matches central 0.08 | Pass (uniform 0.04–0.12) |
| Initial pool varies in MC | Pass (lognormal 2 000–8 000) |
| Emigration cap diagnostic reported | Pass |
| Cost table separates fiscal transfer/resource cost | Pass |
| Reporting checklist item-level (1–30) | Pass (Table S13) |
| All references cited | Pass (44/44) |
| 1 900 figure not used as baseline | Pass (flagged unverified) |

---

## 5. Remaining unresolved issues

| Issue | Status | Action required |
|---|---|---|
| Funding statement | Placeholder | Author completion |
| Competing interests | Placeholder | Author completion |
| Authors' contributions | Placeholder | Author completion |
| Acknowledgements | Placeholder | Author completion |
| Repository DOI/URL | Placeholder | Author completion |
| AI-tool statement | Present, but tool names should be confirmed | Author confirmation |
| Mariem Zribi ORCID | Not supplied; not invented | Author confirmation if desired |
| 1 900 press cohort | Unverified | Not used in main analysis; flagged |
| φ = 0.50 | Assumption, not observed | Presented with 0–1 sensitivity |
| 2008 age distribution | Reconstruction | Age-shape sensitivity reported |
| Destination stocks | Inconsistent definitions | Plausibility screen only |
| External validation | Not possible | Explicitly stated |
| Temporary/permanent migration | Not separated | Limitation stated |

---

## 6. Output locations

- Manuscript: `revision/Manuscript_HRH_Revised.docx` and `.md`
- Supplement: `revision/Additional_file_1_Revised.docx` and `.md`
- Audit: `revision/Scientific_Audit_Report.md`
- Change log: `revision/Revision_Log.md`
- Figure register: `revision/Figure_Revision_Register.md`
- Reference audit: `revision/Reference_Audit.csv`
- Issue register: `revision/audit/Issue_Register.md`
- Key numbers: `revision/outputs/key_numbers.md`
- Validation: `revision/outputs/validation_report.md`
- Tables: `revision/outputs/tables/`
- Figures: `revision/outputs/figures/`

---

## 7. Reproducibility statement

The pipeline runs from `revision/` with:

```bash
pip install -r requirements.txt
python run_all.py
pytest -q
python src/build_docx.py
```

The random seed is fixed. The pipeline regenerates every table, figure, key number and validation report. The manuscript DOCX is built from the markdown source; no manual numerical corrections are applied to the DOCX.
