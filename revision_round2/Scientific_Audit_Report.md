# Scientific Audit Report

**Project:** Tunisia physician workforce stock-and-flow model
**Revision:** 2.1.2 (scientific and computational audit)
**Prepared in:** `revision_round2/`
**Original state preserved in:** `revision/`, `revision_round2/source_preserved/`, and Git tags `v1.1.0`, `v2.0.0` and `pre-review-baseline`

---

## 1. Scope and preservation

The audit started from the repository state tagged `v1.1.0` (main branch) and the earlier pre-review baseline tagged `pre-review-baseline`. The following were preserved unchanged in `revision/source_preserved/`:

- `Manuscript_HRH_v1.1.0.md` and `.docx`
- `Additional_file_1_v1.1.0.md` and `.docx`
- `results_summary_v1.1.0.json`
- `key_numbers_v1.1.0.md`
- `validation_report_v1.1.0.md`

The revised analysis is in `revision/src/`, with outputs in `revision/outputs/`. Original source files outside `revision/` were not overwritten.

---

## 2. Baseline reproduction

The v1.1.0 pipeline was inspected and executed before modification. It reproduced the reported central values (BAU 2040 ≈ 16 019, combined ≈ 21 125, training ≈ 17 131) under the v1.1.0 specification. The existing tests passed. The baseline was therefore computationally reproducible; the audit focused on specification and interpretation.

---

## 3. Issue register and findings

### Issue 1 (major): pipeline non-entry was equated with international emigration

**Original specification.** The model defined \(X(t)=G(t-5)[1-\sigma(t)]\) and described it as pre-entry emigration. All of \(X(t)\) entered the return-eligible diaspora pool. This silently assumed that every graduate who did not enter the practising stock had emigrated internationally.

**Why this is wrong.** Non-entry also includes further training, domestic non-clinical employment, temporary inactivity and other reasons. Only international emigrants can return from abroad. Equating the two overstates the diaspora pool, return migration and the return scenario, and it biases the policy comparison.

**Correction.** Introduced an explicit parameter \(\phi\), the share of pipeline non-entry assumed to be international emigration:

\[
X_{pre}(t)=\phi(t)[1-\sigma(t)]G(t-L), \qquad
X_{dom}(t)=[1-\phi(t)][1-\sigma(t)]G(t-L).
\]

Only \(X_{pre}\) enters the return-eligible pool. \(\phi=0.50\) is the central assumption; \(\phi=0,0.25,0.75,1.0\) are reported as structural alternatives. The policy scenarios reduce pre-entry **international** emigration, not all non-entry.

**Consequences.** Under \(\phi=0.50\), 2024 international emigration is 563 (245 pre-entry + 317 post-entry), not 840; the 2024 pool is 4 312, not 6 234; the 2040 baseline is 15 821, not 16 019. The ranking of the weaker instruments changes: training (16 914) exceeds return migration (16 689), and career development (16 953) is only 39 physicians above training. Combined and remuneration still exceed training in all 4 000 draws. At \(\phi=0\), training is close to remuneration and above return; at \(\phi=1\), the earlier ordering returns.

**Status:** corrected, with structural alternatives retained.

---

### Issue 2: destination-stock screen was presented too strongly

**Finding.** The 4 000–10 000 pool band is a plausibility screen based on the OECD country-of-birth lower bound (about 4 000) expanded to allow for non-OECD destinations and unregistered physicians. It is not a statistical identification constraint and does not validate the pool. The screen excludes low-pool combinations that fit the stock equally well.

**Correction.** The manuscript now reports results with and without the screen, labels it a plausibility check, and does not claim destination registration data validate the diaspora pool. Under \(\phi=0.50\), the acceptable set is 262–1 017 international emigrants; the destination-consistent subset is 481–1 017. The upper bound (\(\phi=1\)) is 502–1 540 and 705–1 540, respectively.

**Status:** corrected in text and tables.

---

### Issue 3: postgraduate lag

**Finding.** The central 5-year lag is an assumption, not an empirically validated Tunisian interval. The model applies the training multiplier to graduate cohorts from 2031 and entrants after the lag; the code was made explicit. Lag sensitivity (3–7 years) shows training 2040 from 17 239 (3 years) to 16 535 (7 years), and the retention break-even from 19.3% to 9.2%.

**Correction.** Lag is labelled an assumption; sensitivity table added (Table 7, Table S10). No claim of empirical validation.

**Status:** documented and tested.

---

### Issue 4: retirement and mortality

**Finding.** The original retirement hazard used a discrete shift; +1.5 and +2 years produced identical schedules. Legal ages vary by sector (60 private, 62 public, extensions for professors); actual retirement is behavioural. The model now applies a continuous linear interpolation of the hazard schedule, so fractional shifts are distinct, and reports retirement/mortality sensitivity. Mortality multipliers have small effects; retirement timing moves the baseline from 15 986 (−2 years) to 15 429 (+2 years).

**Correction.** Continuous shift implemented; legal facts separated from behavioural assumptions; sensitivity table added.

**Status:** corrected.

---

### Issue 5: initial age distribution

**Finding.** The 2008 age distribution is reconstructed from CNOM registered physicians by five-year bands, spread uniformly within bands, and scaled to 12 600. It is not observed practising physicians by age. Alternative two-year younger and older shapes move the 2040 baseline from 14 961 to 16 570 and combined from 18 586 to 19 523. This is a material uncertainty.

**Correction.** The reconstruction is labelled; age-shape sensitivity added. The shape is not treated as observed data.

**Status:** documented.

---

### Issue 6: training output and the 1 900 figure

**Finding.** The 30% announcement concerns admissions, not graduates or practising physicians. The 1 900 figure appears in a press report about a graduating cohort, not in official statistics; it could not be verified. The v1.1.0 manuscript called it a ministerial figure, which was inaccurate.

**Correction.** The 1 900 figure is not used in the main analysis. The manuscript states that it is an unverified press report. The training scenario is described as +30% graduate cohorts from 2031, entering after the lag. The continued-growth alternative (1 709 by 2040) is retained.

**Status:** corrected; 1 900 retained only in the audit and optional stress output, not the main tables.

---

### Issue 7: numerical discrepancies

| Discrepancy | Finding | Resolution |
|---|---|---|
| 2017 stock 14 892 vs 14 928 | Methods reported observed 2017; Table 4 reported model-simulated 2017 | Table 4 now states model-simulated stock and notes the 73-physician over-prediction |
| Density 1.26 vs 1.27 | Abstract/Results used a rounded MC median; tables used deterministic density | Deterministic density is 1.25 and MC median 1.25 in the revised model; both are labelled |
| δ = 0.08 vs MC mean 0.095 | Central δ and uniform prior 0.04–0.15 had different means | MC prior changed to uniform 0.04–0.12 (mean 0.08); wider 0.02–0.15 sensitivity retained |
| Deterministic vs MC physician-years | The two were mixed in places | All tables label deterministic vs MC; Table 5 and Table S5 separate them |
| Emigration cap 0.35 | Cap might bind | Maximum simulated hazard is 0.057; the cap never binds centrally |
| Initial pool fixed in MC vs varied in sensitivity | MC held the pool at 4 000 | Initial pool is now a MC prior (lognormal median 4 000, 2 000–8 000); separate sensitivity still varies δ and ρ |
| Flow identity | Should hold under all scenarios | Validated for all scenarios; pipeline identity (entries + non-entry = graduate cohort) also validated |

**Status:** all resolved at source or explicitly documented.

---

## 4. Model modifications

1. Added \(\phi\) and split pipeline non-entry into international pre-entry emigration and domestic non-entry.
2. Only international emigration enters the return-eligible pool.
3. Policy pre-entry effects apply to the \(\phi\) share, not all non-entry.
4. Training multiplier applied to graduate cohorts from 2031, with entrants after the lag.
5. Continuous retirement-age shift by interpolation.
6. Mortality multiplier parameter added.
7. Initial age-shape alternatives added.
8. MC expanded to 4 000 draws; \(\phi\), initial pool and mortality multiplier included as priors; δ prior aligned with central value.
9. Rank distribution and scenario-overlap probabilities added.
10. Costs split into fiscal transfers and real resource costs.
11. Validation expanded to flow, pipeline, age, density, physician-year and hazard checks.

---

## 5. Results affected

| Result | v1.1.0 | Revision 2.0 |
|---|---|---|
| 2024 international emigration | 840 | 563 (φ=0.50); 840 upper bound |
| 2024 return-eligible pool | 6 234 | 4 312 |
| BAU 2040 | 16 019 | 15 821 |
| BAU density 2040 | 1.25 (deterministic) | 1.25 (deterministic and MC median) |
| Combined 2040 | 21 125 | 19 162 |
| Remuneration 2040 | 19 504 | 18 087 |
| Career 2040 | 17 760 | 16 953 |
| Training 2040 | 17 131 | 16 914 |
| Return 2040 | 17 320 | 16 689 |
| Break-even retention | 9.6% | 14.5% |
| Training needed to match 30% retention | 94% | 62% |
| Identified emigration range (φ=0.50) | 582–1 497 (effectively φ=1) | 262–1 017 |
| Upper bound (φ=1) | — | 502–1 540 |

The central qualitative conclusion is narrower than in v1.1.0: combined and remuneration strategies robustly outperform training, but return migration alone does not, and career/training/return overlap. This is reported rather than forcing the original ranking.

---

## 6. Unresolved limitations

- \(\phi\) is not observed; the central 0.50 is a neutral assumption, and the policy ranking depends on it.
- The 2008 age distribution is a reconstruction from registered physicians.
- The 2020–2021 public-sector discontinuity is unresolved.
- Destination stocks use inconsistent definitions (country of birth, training, registration, active practice).
- The model has no demand, specialty, sector or regional dimension.
- The return-eligible pool is an accounting device, not a diaspora estimate.
- Costs are illustrative and undiscounted; remuneration is a transfer, not a resource cost.
- No external validation; the historical comparison is a consistency check.
- The 1 900 press cohort is unverified and not used.

---

## 7. Evidence and decision summary

| Decision | Evidence | Confidence |
|---|---|---|
| Separate non-entry from emigration | Conceptual; Varga shows domestic non-clinical exits; no Tunisian data separate the two | High (conceptual), low (φ value) |
| Central φ = 0.50 | No direct evidence; neutral midpoint; alternatives 0–1 | Assumption |
| Keep 5-year lag as central | Tunisian training pathway; not empirically validated | Assumption |
| Continuous retirement shift | Legal ages vary; discrete shift produced identical 1.5/2-year schedules | High (implementation) |
| Destination screen 4 000–10 000 | OECD lower bound plus allowance for non-OECD/unregistered | Plausibility only |
| 4 000 MC draws | Percentile/PRCC stability; runtime acceptable | High |
| Fiscal/resource cost split | Wages are transfers; training/career/return are resource costs | High (classification), low (unit costs) |

---

## Round 2 revision (v2.1.0–v2.1.2)

### R2.1 Return-pool accounting

The v2.0 model subtracted gross returns ρD, added back the 15% unsuccessful attempts, and applied diaspora attrition. The pool equation was internally coherent, but the manuscript labelled ρ/(ρ+δ) = 20% and 1/(ρ+δ) = 10 years as the eventual successful-return probability and duration. Those quantities ignore the 0.85 retention rate and treat the annual transition as continuous. The corrected metrics are:

- attempt probability: ρ/[1−(1−ρ)(1−δ)] = 20.3%;
- successful-return probability: θρ/[1−(1−θρ)(1−δ)] = 17.8%;
- mean time to exit: 1/[1−(1−θρ)(1−δ)] = 10.5 years.

These are exact discrete-time competing-risk quantities implied by the implemented annual transition D(t+1) = [D(t)+X_pre(t)+M(t)](1−θρ)(1−δ), not continuous-time approximations. The earlier draft used the continuous-time closed forms (20%, 17.5%, 10.3 years); they differed only marginally but did not correspond exactly to the code. A no-recycling sensitivity treats re-emigrants as permanently outside the pool: successful return θρ/[1−(1−ρ)(1−δ)] = 17.3%, mean duration 10.2 years, 2024 pool 4 199 rather than 4 312, and return advantage 828 rather than 868 physicians. The central projections are unchanged under recycling; the no-recycling sensitivity is reported in Table S17.

### R2.2 Policy-ranking claims

At φ = 0, remuneration is 16 671 and training 16 698, so remuneration is 27 below training. The claim that remuneration outperforms training is therefore bounded to the Monte Carlo φ prior (0.25–0.75), where it ranks second in 99.8% of draws. Combined remains above training across φ = 0–1.

### R2.3 Effect-size assumptions

The 30% remuneration, 15% career and 35% combined effects are illustrative. A conservative grid (10% remuneration, 5% career, 1.35× return) gives 16 576, 16 198 and 16 238, all below the 30% graduate-output scenario (16 914). Only the constructed combined package (20% + 1.35×, 17 701) remains above training. The 14.5% break-even is conditional arithmetic.

### R2.4 Training scenario

The training scenario is relabelled a hypothetical 30% graduate-output expansion from 2031, not a simulation of the 2025 admissions announcement. Completion of additional admissions is varied at 80/90/100%, giving 16 695/16 804/16 914 in 2040.

### R2.5 Initial pool

The 4 000 initial pool is an illustrative external anchor, not a lower bound or measured return-eligible population. Country of birth does not identify training, prior practice or eligibility to return. The pool is varied 2 000–8 000 and the return scenario is flagged as especially assumption-dependent.

### R2.6 Historical residual and calibration endpoint

The 2020 public-sector fall of 725 (private +91) could be reclassification, reporting, real exit or a mix; the model cannot distinguish them. Calibrating to 2019 or 2022 gives 2040 baselines of 16 032 and 15 247 versus 15 821 for 2024. The residual is not evidence of migration.

### R2.7 Age structure

The reconstructed 2008 age structure shifts the 2040 baseline from 14 961 to 16 570, larger than the central training effect. This is now stated in the abstract, Results, Discussion and limitations.

### R2.8 PRCC stability and cost framing

Bootstrap 90% intervals from 1 000 resamples are narrow (e.g., future emigration −0.82 to −0.80; φ 0.14–0.20; return retention −0.04 to 0.01). PRCCs are conditional on priors and calibration, not causal. Cost ratios are exploratory and fiscal/resource categories are explicitly non-comparable; the cost column was removed from Table 5. Table 6 and Fig. S2 report fiscal transfers and resource costs in separate columns and panels; they are not summed, stacked or ranked.

### R2.9 Pre-submission corrections (v2.1.1–v2.1.2)

| Item | Correction |
|---|---|
| Table 4 stock status | Second column renamed “Modelled practising stock”; the note states that the 2017 and 2020 values are modelled and gives both observed comparisons (over-prediction of 73 and 538); all flows are labelled model-implied |
| Return transition | Manuscript now writes the implemented annual transition D(t+1) = [D(t)+X_pre(t)+M(t)](1−θρ)(1−δ), defines gross attempts ρD, successful θρD and recycled (1−θ)D, and states that net return-related removal is θρD. Metrics are exact discrete-time competing-risk quantities |
| Table S17 | Updated to the exact discrete-time metrics (0.203 / 0.178 / 10.5; no recycling 0.203 / 0.173 / 10.2) |
| Supplement figures | Image paths corrected so both Fig. S1 and Fig. S2 embed in the DOCX; previously Fig. S2 silently failed to embed |
| Reproducibility | Repository contains processed inputs, data dictionary, parameter definitions, seed, tests and the one-command pipeline; the pipeline regenerates tables, figures, key numbers and validation report. DOCX assembly is a separate documented step |
| Figure package | Nine main and two supplementary PDFs present in `figures/`; captions cross-checked against the manuscript and supplement |
| Cost categories | Removed the summed “total cost” and mixed “cost per additional physician” columns; Table 6 and Fig. S2 now report fiscal transfers and resource costs separately per additional physician-year, with no stacking, summing or ranking. Fig. S2 has two panels |
| Declarations and repository | Funding: none; competing interests: none; contributions: equal with FZ leading technical work; acknowledgements: not applicable; both ORCIDs supplied; public GitHub repository and tag `v2.1.2` inserted |
