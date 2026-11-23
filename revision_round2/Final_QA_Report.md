# Final QA Report — Round 2

**Revision:** 2.1.1
**Date:** 23 November 2026
**Pipeline:** `revision_round2/run_all.py`
**Seed:** 20261121
**Monte Carlo draws:** 4 000

---

## 1. Execution status

| Check | Result |
|---|---|
| Full pipeline executed | Pass (exit 0) |
| Tests (`pytest -q`) | Pass (14 tests) |
| Validation report | Pass (all checks) |
| Manuscript DOCX | `Manuscript_HRH_Revised_R2.docx` (8 tables, 192 paragraphs) |
| Supplement DOCX | `Additional_file_1_Revised_R2.docx` (17 tables, 61 paragraphs) |
| Figures | 9 main + Fig. S1 + Fig. S2; PNG and PDF |
| Word count | 3 996 including abstract; 3 646 main text |
| Abstract | 350 words |
| References | 44, all cited |
| Tables | 8 main tables |
| Figures | 9 main figures + 2 supplementary |

---

## 2. Numerical integrity checks

| Check | Result |
|---|---|
| 2024 calibration error | −0.098 physicians |
| Maximum Monte Carlo calibration error | 0.137 physicians |
| Workforce flow identity, all scenarios | Pass |
| Graduate pipeline identity, all scenarios | Pass |
| Return flow components additive | Pass |
| Return retention matches flow | Pass (0.850) |
| Return probabilities ordered | Pass (attempt 0.203, success 0.178, duration 10.5) |
| No-recycling flow identity | Pass |
| Age distributions non-negative | Pass |
| Density calculation | Pass |
| Physician-year calculation | Pass |
| Emigration hazard cap | Does not bind; maximum hazard 0.057 |
| Hazards in [0, 1] | Pass |
| Monte Carlo intervals ordered | Pass |
| PRCCs in [−1, 1] | Pass |
| Combined ranks first in 2040 | Pass in all 4 000 draws |
| Remuneration ranks second | 99.8% of draws |

---

## 3. Round-2 corrections

| Issue | Resolution |
|---|---|
| Return-pool accounting | Metrics corrected to exact discrete-time: 20.3% attempt, 17.8% successful return, 10.5 years; no-recycling 17.3%, 10.2 years, advantage 828 vs 868 |
| Remuneration “robustly” beats training | Bounded to Monte Carlo φ prior; at φ=0 remuneration 16 671 vs training 16 698 |
| Policy effects too confident | Conservative grid: 10% remuneration 16 576; 5% career 16 198; 1.35× return 16 238; all below training 16 914; combined 20% + 1.35× 17 701 |
| Training scenario | Relabelled hypothetical graduate-output expansion; completion 80/90/100% gives 16 695/16 804/16 914 |
| Initial pool | Reframed as illustrative anchor, not lower bound/measured population |
| Historical residual | Described as unresolved; calibration endpoints 2019/2022 give 16 032/15 247 vs 15 821 |
| Age structure | 14 961–16 570 range added to Abstract, Results, Discussion, limitations |
| Administrative/press indicators | 374 defined as annualised H1 2023 removal requests; press estimates near φ=1 upper bound only |
| Cost framing | Removed from abstract/Table 5; Fig. 4D moved to Fig. S2; categories non-comparable |
| PRCC stability | Bootstrap 90% intervals: future emigration −0.82 to −0.80; φ 0.14–0.20; return retention −0.04 to 0.01 |
| Cohort year | 2024 entries from 2019 cohort (1 091); 2024 cohort (1 305) enters 2029 |

---

## 4. Manuscript consistency checks

| Check | Result |
|---|---|
| Two authors only | Pass (Firas Zaier, Mariem Zribi) |
| Affiliations, email, ORCID | Applied exactly as specified |
| No third-author placeholder | Pass |
| Abstract ≤350 words | Pass (350) |
| Main text ≤4 000 words | Pass (3 646 main; 3 996 including abstract) |
| Tables cited in order | Pass (1–8) |
| Figures cited in order | Pass (1–9; S1–S2 in supplement) |
| Table 4 stock column labelled modelled | Pass |
| Table 4 observed 2017/2020 comparisons | Pass (73 / 538 over-prediction) |
| Table 4 cohort-year note | Pass |
| Return transition equation matches code | Pass (recycling and no-recycling forms) |
| Supplement figures embedded | Pass (S1 and S2) |
| Figure manifest complete | Pass (11 PDFs) |
| Deterministic vs Monte Carlo values labelled | Pass |
| Density values consistent | Pass (1.25 deterministic and MC median) |
| δ prior mean matches central 0.08 | Pass |
| Initial pool varies in MC | Pass (2 000–8 000) |
| Emigration cap diagnostic | Pass |
| Cost table exploratory and separate | Pass |
| Fiscal and resource costs not summed or stacked | Pass (Table 6 and Fig. S2 report separately) |
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
| AI-tool statement | Present; tool names should be confirmed | Author confirmation |
| Mariem Zribi ORCID | Not supplied; not invented | Author confirmation if desired |
| 1 900 press cohort | Unverified | Not used; flagged |
| φ = 0.50 | Assumption, not observed | Reported with 0–1 sensitivity |
| 2008 age distribution | Reconstruction | 1 600-physician range reported |
| Destination stocks | Inconsistent definitions | Plausibility screen only |
| External validation | Not possible | Explicitly stated |
| Temporary/permanent migration | Not separated | Limitation stated |
| Return-accounting convention | Recycling central; no-recycling sensitivity | Reported |

---

## 6. Output locations

- Manuscript: `revision_round2/Manuscript_HRH_Revised_R2.docx` / `.md`
- Supplement: `revision_round2/Additional_file_1_Revised_R2.docx` / `.md`
- Audit: `revision_round2/Scientific_Audit_Report.md`
- Change log: `revision_round2/Revision_Log.md`
- Figure register: `revision_round2/Figure_Revision_Register.md`
- Reference audit: `revision_round2/Reference_Audit.csv`
- Issue register: `revision_round2/audit/Issue_Register.md`
- Submission checklist: `revision_round2/Submission_Readiness_Checklist.md`
- Key numbers: `revision_round2/outputs/key_numbers.md`
- Validation: `revision_round2/outputs/validation_report.md`
- Tables: `revision_round2/outputs/tables/`
- Figures: `revision_round2/outputs/figures/` and `revision_round2/figures/`

---

## 7. Reproducibility statement

```bash
cd revision_round2
pip install -r requirements.txt
python run_all.py
pytest -q
python src/build_docx.py
```

The seed is fixed. `run_all.py` regenerates every table, every main and supplementary figure (including the flow diagram), key numbers and the validation report. The DOCX is built from the markdown source; no manual numerical corrections are applied to the DOCX. Calibration checks confirm the numerical procedure, not predictive validity.
