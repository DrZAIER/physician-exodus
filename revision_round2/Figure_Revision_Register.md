# Figure Revision Register

**Revision:** 2.1.2
**Original figure files preserved:** `submission/Figures/` (v1.1.0), `revision/figures/` (v2.0.0) and `revision_round2/source_preserved/` (manuscript files). The original PDFs were not overwritten.

All figures were regenerated from the corrected model. PNG and PDF versions are in `revision_round2/outputs/figures/`. The register below records why each figure changed.

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
- Fig. 4: cost panel later removed in v2.1.1; cost ratios moved to Fig. S2.
- Fig. 6: conditional vs marginal associations; calibration-ridge note.
- Fig. 9: 14.5% retention break-even; 62% training match.

## Files

- Regenerated PNG/PDF: `revision/outputs/figures/`
- Submission-named PDFs: `revision/figures/Fig1.pdf` … `Fig9.pdf`, `FigS1.pdf`
- Manuscript figure legends: `revision/Manuscript_HRH_Revised.md`
- Original v1.1.0 figures: `submission/Figures/` (unchanged)

---

## Round 2 updates (v2.1.0)

| Figure | Change | Reason | Status |
|---|---|---|---|
| Fig. 4 | Reduced to panels A–C; cost panel removed | Fiscal and resource costs are not commensurable; cost is exploratory | Regenerated |
| Fig. S1 | Added 15% re-emigration loop back to the pool | Reconcile return accounting and recycling | Regenerated |
| Fig. S2 | New exploratory fiscal/resource cost ratio figure | Keep cost analysis separate from main outcomes | New |
| Fig. 9 | Legend changed from training expansion to graduate-output expansion | Training scenario relabelled | Regenerated |
| All figures | Final 4,000-draw outputs; no central-number changes under recycling | Consistency audit | Regenerated |

Submission-named PDFs are in `revision_round2/figures/`; PNG/PDF source outputs are in `revision_round2/outputs/figures/`. Original v2.0.0 and v1.1.0 figures remain preserved.

## Pre-submission updates (v2.1.1)

| Figure | Change | Reason | Status |
|---|---|---|---|
| Fig. S2 | Rebuilt as two panels: (A) fiscal transfers, (B) resource costs; no stacking or totals. Now embeds in the supplement DOCX | Categories are not commensurable; the earlier stacked bar implied addition, and the figure was silently omitted from the DOCX | Verified |
| Fig. 4 | x-axis labels rotated and wrapped | Category labels overlapped and were unreadable | Regenerated |
| Fig. 6 | Parameter labels replaced with readable names | The figure displayed raw variable names (`initial_diaspora_2008`, `mortality_mult`, `phi`) | Regenerated |
| Fig. 9 | Legend moved below the plot; axis margins added; labels renamed | Legend overlapped contour labels and clipped the 62% annotation | Regenerated |
| Fig. S1 | Return and re-emigration lanes separated; loop label repositioned | Arrows and labels overlapped between the stock and pool boxes | Regenerated |
| Fig. S1 | 15% re-emigration loop matches the exact pool transition | Return accounting corrected | Regenerated |
| All figures | Rebuilt from the final 4 000-draw pipeline; captions cross-checked | Consistency | Regenerated |

## Submission figure manifest

| Figure | File | Caption status |
|---|---|---|
| Fig. 1 | `figures/Fig1.pdf` | Matches manuscript legend |
| Fig. 2 | `figures/Fig2.pdf` | Matches manuscript legend |
| Fig. 3 | `figures/Fig3.pdf` | Matches manuscript legend |
| Fig. 4 | `figures/Fig4.pdf` | Three panels (A–C); cost panel removed |
| Fig. 5 | `figures/Fig5.pdf` | Matches manuscript legend |
| Fig. 6 | `figures/Fig6.pdf` | Matches manuscript legend |
| Fig. 7 | `figures/Fig7.pdf` | Matches manuscript legend |
| Fig. 8 | `figures/Fig8.pdf` | Matches manuscript legend |
| Fig. 9 | `figures/Fig9.pdf` | Graduate-output expansion labels |
| Fig. S1 | `figures/FigS1.pdf` | Matches supplement legend |
| Fig. S2 | `figures/FigS2.pdf` | Exploratory, non-comparable cost categories |
