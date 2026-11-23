# Figure Revision Register

**Revision:** 2.0
**Original figure files preserved:** `submission/Figures/` (v1.1.0) and `revision/source_preserved/` (manuscript files). The original PDFs were not overwritten.

All figures were regenerated from the corrected model. PNG and PDF versions are in `revision/outputs/figures/`. The register below records why each figure changed.

| Figure | Underlying data affected | Reason for revision | Required change | Status |
|---|---|---|---|---|
| Fig. 1 | Historical fit, baseline, MC interval | φ correction lowers baseline and pool; MC now 4 000 draws | Regenerate observed/fit/projection/fan with new baseline 15 821 and interval 14 407–17 438 | Regenerated |
| Fig. 2 | RMSE surface, emigration, upper bound, pool | φ=0.50 central; φ=1 upper bound; extended grid 0.20–0.80 σ and 0.80–1.60 training | New 2×2 layout: A RMSE, B international emigration φ=0.5, C upper bound φ=1, D pool | Regenerated |
| Fig. 3 | Scenario trajectories | All scenario levels changed; both-margin trend applies to φ share | Regenerate three panels (constant, post-entry +3%, both margins +3%) | Regenerated |
| Fig. 4 | Workforce difference, emigration, PY, costs | Scenario effects smaller; costs split fiscal/resource | Regenerate four panels; panel D stacked fiscal/resource | Regenerated |
| Fig. 5 | Density | Baseline density 1.25; combined 1.52 | Regenerate BAU/combined density and observed points | Regenerated |
| Fig. 6 | Tornado/PRCC | New parameters φ, initial pool, mortality; new PRCC values | Regenerate tornado and PRCC/marginal comparison | Regenerated |
| Fig. 7 | Age structure | New age shares; combined 37.4% aged 35–44 | Regenerate 2024/2040 BAU/2040 combined bars | Regenerated |
| Fig. 8 | Structural escalation | New values; both margins apply to φ share | Regenerate post-entry and both-margin panels | Regenerated |
| Fig. 9 | Break-even | New threshold 14.5%; training match 62% | Regenerate grid, markers and annotation | Regenerated |
| Fig. S1 | Model flow diagram | Pipeline non-entry split into international emigration and domestic non-entry | Rebuild diagram with φ split; only pre-entry international emigration enters pool | Regenerated |

## Figure legends updated

All legends in `Manuscript_HRH_Revised.md` were rewritten to match the revised data, including:

- Fig. 1: 4 000 draws; 2024 calibration endpoint.
- Fig. 2: φ=0.5 and φ=1 panels; grid boundaries; plausibility note.
- Fig. 3: both-margin trend applies to pre-entry international and post-entry margins.
- Fig. 4: stacked fiscal/resource cost.
- Fig. 6: conditional vs marginal associations; calibration-ridge note.
- Fig. 9: 14.5% retention break-even; 62% training match.

## Files

- Regenerated PNG/PDF: `revision/outputs/figures/`
- Submission-named PDFs: `revision/figures/Fig1.pdf` … `Fig9.pdf`, `FigS1.pdf`
- Manuscript figure legends: `revision/Manuscript_HRH_Revised.md`
- Original v1.1.0 figures: `submission/Figures/` (unchanged)
