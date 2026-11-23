# Revision 2.1.1 workspace (Round 2)

This directory contains the Round-2 scientific and computational revision. The v2.0.0 and earlier materials are preserved in `revision/` and in Git tags; this workspace does not overwrite them.

## Deliverables

| File | Purpose |
|---|---|
| `Manuscript_HRH_Revised_R2.docx` / `.md` | Revised manuscript, two authors |
| `Additional_file_1_Revised_R2.docx` / `.md` | Revised supplement (Tables S1–S17) |
| `Scientific_Audit_Report.md` | Audit, including Round-2 corrections |
| `Revision_Log.md` | Change log |
| `Figure_Revision_Register.md` | Figure-by-figure update register |
| `Reference_Audit.csv` | Reference verification register |
| `Final_QA_Report.md` | Final QA |
| `Submission_Readiness_Checklist.md` | Journal requirements, verified items and remaining author actions |
| `audit/Issue_Register.md` | Issue tracker |
| `figures/` | Submission-named PDFs (Fig1–Fig9, FigS1–FigS2) |
| `outputs/` | Generated tables, figures, key numbers, validation report |
| `source_preserved/` | Earlier manuscript artefacts |

## Reproduce

```bash
cd revision_round2
pip install -r requirements.txt
python run_all.py
pytest -q
python src/build_docx.py
```

The pipeline uses 4 000 Monte Carlo draws, fixed seed 20261121. `run_all.py` regenerates every table, every main and supplementary figure (including Fig. S1), `key_numbers.md` and the validation report. `src/build_docx.py` then assembles the DOCX files from the markdown sources; it applies no numerical edits. Runtime is several minutes.

## Key specification in this revision

- Pipeline non-entry is split into international pre-entry emigration (φ) and domestic non-entry. Only international emigration enters the return-eligible pool.
- Return attempts occur at ρD; 85% succeed and enter practice, 15% re-emigrate. The central specification recycles re-emigrants into the pool immediately. A no-recycling sensitivity is reported.
- Return metrics are exact discrete-time competing-risk quantities: 20.3% attempt probability, 17.8% successful-return probability, 10.5-year mean time to exit. The no-recycling sensitivity gives 17.3% and 10.2 years.
- The policy ranking is bounded to the Monte Carlo φ prior; at φ=0 remuneration is slightly below training.
- Training is a hypothetical 30% graduate-output expansion, not the announced admissions policy.
- The initial return-eligible pool is an illustrative anchor, not a measured population.
- Costs are exploratory; fiscal transfers and resource costs are reported separately per additional physician-year and are neither summed nor ranked.

## Remaining author actions

Complete funding, competing-interest, contributions and acknowledgements statements; insert the repository DOI; confirm AI-tool names and Mariem Zribi's ORCID preference. The package is not submission-ready until these are completed.
