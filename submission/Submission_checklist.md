# Submission checklist — Human Resources for Health (BMC)

**Article type:** Research article
**Title:** Retention, return or training? A stock-and-flow simulation of Tunisia's physician workforce under incomplete migration data

## Journal requirements

| Requirement | Status | Where / note |
|---|---|---|
| Maximum 4 000 words (excluding tables, figures, additional files) | Met | 3 959 words including abstract (3 620 words Background–Conclusions) |
| Abstract ≤350 words, structured (Background, Methods, Results, Conclusions) | Met | 339 words |
| No references in abstract | Met | — |
| 3–10 keywords | Met | 7 keywords |
| Title page with authors, institutional addresses, corresponding author | Included | `Title_page.md`; author details remain placeholders |
| Structured main text (Background, Methods, Results, Discussion, Conclusions) | Met | — |
| List of abbreviations | Included | Before Declarations; includes BAU and TND |
| Declarations with all required subheadings | Included | Ethics; Consent; Availability; Competing interests; Funding; Contributions; Acknowledgements; Authors' information |
| Vancouver references, numbered in citation order | Met | 44 references, sequential; NLM journal abbreviations; up to 6 authors then et al. |
| Tables as editable table objects, numbered, cited in order | Met | 7 tables; Word table objects |
| Table titles ≤15 words, legends ≤300 words | Met | Titles 4–8 words |
| No commas in numerical values in tables | Met | Spaces used as thousands separators |
| No colour or shading in tables | Met | Table Grid only |
| Figures numbered and cited in order, separate files | Met | 9 main figures + FigS1; `submission/Figures/` |
| Figure titles ≤15 words, legends ≤300 words | Met | Titles 3–9 words; legends <100 words |
| Figures ≤10 MB each, 300 dpi or vector | Met | Vector PDF files |
| Additional file named, cited, described (name, format, title, description) | Met | Additional file 1, DOCX; Tables S1–S13 and Figure S1 |
| Page numbers | Met | Footer field in DOCX |
| Double line spacing | Met | Normal style, 2.0 |
| Line numbering | Met | Continuous line numbering in DOCX |
| Data availability statement in journal format | Pending author action | Repository DOI/URL placeholder must be completed before submission |
| Cover letter with required declarations | Included | `Cover_letter.docx`; update numbers if the manuscript changes |
| Reporting guideline followed | Met | Item-level 30-item checklist in Additional file 1, Table S13 |
| AI use documented in Methods | Met | Tools, tasks and author responsibility stated; confirm tool names before submission |
| Ethics statement | Met | Not applicable (aggregate data) |

## Files in this package

| File | Purpose |
|---|---|
| `Manuscript_HRH.docx` | Main manuscript, submission-formatted |
| `Manuscript_HRH.md` | Editable markdown source |
| `Title_page.md` | Standalone title page |
| `Cover_letter.docx` / `.md` | Cover letter |
| `Additional_file_1.docx` / `.md` | Supplementary tables and item-level reporting checklist |
| `Figures/Fig1.pdf` … `Fig9.pdf` | Main figures |
| `Figures/FigS1.pdf` | Supplementary flow diagram |
| `Submission_checklist.md` | This file |

## Author actions before submission

1. Replace author names, affiliations, ORCID iDs and corresponding-author details in the manuscript and title page.
2. Insert the repository name and persistent identifier/URL in the Data availability statement. The repository must contain the code, processed data, tests and a README. Do not mark this item "Met" until the DOI resolves.
3. Confirm funding and competing-interest statements.
4. Complete authors' contributions with initials.
5. Add institutional emails for suggested reviewers in the cover letter, or remove the reviewer suggestion.
6. Confirm the AI-use statement names the tools actually used and the tasks performed.
7. Verify that all authors approve the final version.
8. Rebuild the DOCX after any edit: `python src/build_docx.py`.
9. Re-run the pipeline and checks before submission: `python run_all.py` and `pytest -q`.
10. Optionally add a non-English abstract (French), ≤350 words, after the English abstract.
11. Rebuild the canonical DOCX with `python src/build_docx.py` after any further edits; the current file has been rebuilt (7 tables, 9 figure legends).

## Notes on journal style

- The journal allows either CC BY or CC BY-NC-ND; choose at submission.
- The APC is £2 490 / $3 390 / €2 790 (at the time of checking); waiver/discount requests must be made at submission.
- The journal uses transparent peer review: reviewer reports are published if the article is accepted.
- The manuscript is supplied as DOCX (editable), as required for production.

## Revision notes (response to review)

The revision addresses the reviewer's essential and high-priority points:

- Structural escalation is now reported separately for the post-entry margin and for both margins; the "collapse" result is explicitly tied to the both-margin assumption.
- Sensitivity uses true partial rank correlations, with marginal Spearman correlations shown for comparison; the conditional emigration effect is negative.
- The diaspora pool is a return-eligible pool with an explicit attrition hazard and return retention; it is reconciled with destination-country stocks and tested over a wide sensitivity range.
- Monte Carlo draws are calibrated exactly (maximum error 0.14 physicians), and the priors cover the identified range.
- The graduate series is explicit and piecewise; alternative output baselines are reported.
- A break-even analysis and illustrative cost-per-physician-year analysis are included.
- The reporting checklist is item-level (1–30) with NA justifications.
- Calibration is described as a 2024 endpoint with a 2017–2024 retrospective comparison.
- The 2020–2021 discontinuity is treated as an unresolved reporting or reclassification change, not asserted to be a reporting artefact.
- Numbers are harmonised across the abstract, results, tables and figures.
