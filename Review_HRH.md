# Peer review — *Human Resources for Health*

**Manuscript:** “Retention, return or training? A stock-and-flow simulation of Tunisia's physician workforce under incomplete migration data”
**Article type:** Research article
**Reviewer recommendation:** Major revision
**Reviewer expertise:** Health workforce modelling, migration statistics, health economics
**Conflicts of interest:** None

---

## 1. Summary of the submission

The manuscript develops an annual, single-year-of-age cohort-component model of physicians in active practice in Tunisia from 2008 to 2040, calibrated to the 2024 practising stock of 15 315. The model represents entry after a five-year postgraduate lag, emigration before and after entry, return migration from an “effective diaspora pool,” retirement and mortality. It compares business as usual with five scenarios: remuneration and working conditions, career development, return migration, a 30% expansion of training, and a combined retention-and-return strategy. Uncertainty is explored with 2 000 Monte Carlo draws, alternative effect sizes, and deterministic structural scenarios in which emigration intensity rises by 3%, 5% or 7% per year.

The paper makes four claims: (i) the level of emigration is not identifiable from the aggregate stock path, with 675–1 839 annual emigrants nearly equally consistent with the observed history; (ii) retention and return outperform training within 15 years; (iii) a combined strategy remains effective if emigration rises 3% per year; and (iv) Tunisia needs cohort-consistent reporting that distinguishes registered, practising and emigrated physicians.

## 2. Overall assessment

This is a timely, clearly written and unusually transparent paper. The identifiability analysis is the most valuable contribution: it quantifies what the aggregate stock can and cannot tell us, and it has transferable value for other countries with incomplete migration data. The policy scenarios are a useful application, the figures are clean, and the “what the model can and cannot establish” section is candid. The manuscript is a good fit for *Human Resources for Health*.

However, the policy conclusions are presented with more confidence than the model supports, and several of the quantitative claims do not survive a closer check. The most consequential problem is that the structural escalation scenario appears to raise pre-entry emigration as well as post-entry emigration, which drives the headline “collapse” result; a post-entry-only 3% trend leaves the baseline growing to about 16 000, not falling to 13 574. The sensitivity analysis labels marginal Spearman correlations as partial rank correlation coefficients; a true partial correlation reverses the sign of the emigration effect. The diaspora pool used for the return scenario is several times the destination-country stock, and the return scenario’s magnitude depends on it. The Monte Carlo draws do not all reproduce the 2024 calibration target, and the priors do not cover the identified range. The graduate series is internally inconsistent, and the baseline holds output constant without testing the alternative.

These problems are fixable, but they require substantial revision and, in places, a reframing of the paper around the identifiability result rather than the policy ranking. I recommend **major revision**.

## 3. Major comments

### M1. The structural escalation scenario is not described correctly, and it drives the headline result

The Methods say the structural scenarios let “emigration intensity” rise 3%, 5% or 7% per year after 2024. In the model, pre-entry emigration is G(t−5)[1−σ(t)] and post-entry emigration is m(t)Π(t). If the trend applies only to the post-entry flow, the 3% scenario produces a 2040 stock of about **16 000**, not 13 574; the baseline continues to grow. The reported fall to 13 574 requires the trend to also raise the pre-entry share from 45% in 2024 to about **72% in 2040** (and to 90% under 5–7%). That is a much stronger assumption than “emigration intensity rising 3% per year” implies, and it is not stated in the Methods, Results or Fig. 8 legend.

Please (i) state explicitly which margin is trended; (ii) justify applying the trend to the pre-entry share, if that is intended; (iii) show both the post-entry-only and the combined-margin versions; and (iv) revise the abstract, Results, Discussion and Fig. 8 accordingly. This is the single most consequential issue because the “collapse” narrative, the “not a forecast of collapse” framing, and the claim that the combined strategy is “robust to plausible escalation” all depend on it.

### M2. The reported “PRCC” values are marginal Spearman correlations, and the emigration coefficient has the wrong sign

The Sensitivity section reports “partial rank correlation coefficients (PRCC)” of 0.60 for the implied emigration level, 0.57 for the return rate and 0.53 for training output. The underlying table labels the Spearman correlations as PRCC. A true partial rank correlation, controlling for the other parameters, gives approximately: return rate **0.65**, training output **0.60**, pipeline retention **0.37**, initial stock **−0.37**, emigration **−0.31**, age profile **0.24**, retirement **0.05**.

The marginal +0.60 for emigration is an artefact of the calibration ridge: draws with higher σ or training output require higher m to match the 2024 stock, and also produce a larger 2040 stock. Conditional on the other parameters, higher emigration lowers the 2040 workforce, as expected. The current text therefore reverses the sign and misranks the drivers. Please recompute true PRCCs (or relabel the values as Spearman correlations and stop interpreting them as independent effects), align the text with Fig. 6 and the sensitivity table, and explain the calibration-induced confounding. This is a substantive statistical error, not a wording issue.

### M3. The diaspora pool is unvalidated and determines the return scenario

The model’s “effective diaspora pool” reaches about **13 800 in 2024** and **24 200 in 2040**, while the OECD estimate cited in Table 1 is about **4 000** (2015/16) and the France + Germany stock is about **2 500**. The return rate (2% baseline, 3.5% scenario) is applied to this pool, so the return scenario’s 3 446 additional physicians by 2040 is proportional to an unvalidated stock. The manuscript calls the pool “an accounting device, not a diaspora estimate,” but the return scenario treats it as a population at risk.

Please (i) reconcile the pool with destination-country stocks, including non-OECD destinations; (ii) add deaths abroad and re-emigration of return migrants; (iii) provide a sensitivity analysis over the initial pool (e.g., 2 000–8 000) and the return rate (0.5–4%); and (iv) temper the return conclusion if it is not robust. The Hungarian evidence (>50% return at some point) is also difficult to reconcile with a 2% annual baseline return rate, which implies a mean duration abroad of 50 years; please discuss.

### M4. The Monte Carlo draws do not reproduce the calibration target and do not cover the identified range

The 90% interval for the 2024 stock in the Monte Carlo output is about **14 810–15 802**, so many draws are not calibrated to 15 315. The Methods say m was recalibrated for each draw; Table S4 also includes a lognormal “calibration residual on m” (log-SD 0.06). If that residual multiplies the annual flow over the whole 2008–2024 period, it compounds over 17 years and produces the observed spread.

Please clarify how the residual is applied, calibrate exactly (or report the calibration error), and ensure the Monte Carlo priors cover the identified range. The Monte Carlo 5th–95th percentile of m is about **209–895**, while the identifiability grid is **675–1 839**; the claim that the model “carries the identified range through the scenarios” is therefore not accurate. Either widen the priors or present the policy results across the full grid.

### M5. The graduate series is internally inconsistent, and the baseline output assumption is not tested

The Methods say graduates were reconstructed as 987 in 2013 and 1 128 in 2021, “with 1.7% annual growth,” and 1 305 in 2024. A 1.7% extrapolation from 1 128 in 2021 gives about **1 188** in 2024, not 1 305; the implied growth 2021–2024 is about **5% per year**. The 2025 cohort is reported as **1 900** in Table 2. The baseline then holds 1 305 constant after 2024.

These are not minor discrepancies: a continued 1.7% growth gives about 1 700 graduates by 2040 and a baseline of about **18 900**; a constant 1 900 gives about **22 600**. Please (i) state the actual graduate series and justify the 2021–2024 acceleration; (ii) reconcile the 1 100, 1 305 and 1 900 figures; and (iii) add at least one alternative-output baseline (continued historical growth, and/or 1 900 constant). The policy ranking may survive, but the magnitudes and the “slow growth” framing will change. The training scenario also applies +30% to 1 305; if the 2025 cohort is 1 900, the scenario should apply +30% to 1 900, or the 1 305 figure needs a clear justification. The Methods also say all scenarios start in 2026, while the training scenario starts in 2031; clarify the timing.

### M6. The policy ranking is largely arithmetic; add a break-even/threshold analysis

The finding that retention beats training within 15 years follows from the assumed flows: a 30% reduction in about 969 emigrants versus a 30% expansion of about 1 305 graduates with a five-year lag and 55% entry. The paper should show how small the retention effect (or how large the training effect) would need to be to change the ranking. A simple linear approximation suggests that a reduction of roughly **9–10%** in emigration would match the 30% training expansion in 2040. If that is correct, the conclusion is robust but should be presented as a threshold result, not an empirical discovery.

A break-even figure (x-axis: retention effect; y-axis: training effect; iso-lines of 2040 stock) would make the paper much more useful to policy-makers and would pre-empt the criticism that the ranking is built into the assumptions.

### M7. Cost is absent from a policy comparison that includes a remuneration scenario

The paper compares a remuneration/conditions package with training expansion but does not model costs. A 30% real wage increase for public physicians is likely very expensive; a 30% training expansion also has costs (faculty, infrastructure, clinical training). Without cost, the ranking is about supply effects per unit of assumed effect, not per dollar.

At minimum, add a cost caveat and a simple cost-per-additional-physician-year calculation; ideally, discuss fiscal affordability and the public/private financing mix. The current policy implications (“Retention should be treated as a supply instrument”) read as cost-free advice, which is not warranted.

### M8. The 30-item reporting checklist is incomplete

Additional file 1, Table S8 has **19 domain rows**, but the Lee et al. guideline has **30 items**, including demand-side, gap, budgetary, regional and distribution items. The note says these are “not applicable,” but they are not listed or marked by item number. Please provide an item-by-item checklist (1–30) with locations and NA justifications. This matters because the paper claims to follow the guideline and because the journal’s readers will use the checklist to assess transparency.

### M9. The calibration is to a single year, not 2017–2024

The Methods say m was solved so that the simulated 2024 stock equalled 15 315. The abstract says the model was “calibrated to the national practising stock for 2017–2024.” The 2017–2024 series is a post-hoc fit, not a calibration target. Please correct the wording in the abstract and Methods, explain why a single endpoint was chosen (the 2020–2021 discontinuity is a good reason), and report the calibration error and the fit excluding 2020–2021. This is a transparency issue, not a fatal flaw, but it matters for the paper’s central claim about what the data can identify.

### M10. The identifiability range is conditional and could be narrowed with the data already in Table 1

The identifiability point is close to an accounting identity: one stock observation cannot identify two gross flows. The paper’s contribution is the quantification and the policy application, not the identity itself, and the framing should reflect that. The 675–1 839 range comes from a two-dimensional grid over σ and the training multiplier, holding the return rate, initial stock, retirement age and age profile at their central values. The grid’s low corner (675) attributes almost all emigration to the pre-entry margin (about 650 of 675), while the high corner (1 839) implies a diaspora of roughly 20 000–25 000, several times the OECD estimate. Both are extreme combinations, and the paper lists the destination-country stocks in Table 1 but does not use them as constraints.

Please (i) describe the range as conditional on the other parameters; (ii) define a consistency threshold rather than relying on the visual flatness of the RMSE surface; and (iii) add a stock–flow consistency check against the destination-country data. This could narrow the range substantially and would strengthen the paper’s main contribution.

## 4. Minor comments

**m1. Numerical inconsistencies between the abstract, results and tables.** The abstract reports 17 990 and 16 340–19 970; the Results and tables report 17 987 and 16 339–19 968. The abstract reports 25 340, 57 900, 3 730, 3 450 and 1 120; the Results report 25 335, 57 855, 3 728, 3 446 and 1 124. The abstract says training effects appear “after 2031”; the Results say “2031 graduates enter in 2036.” The abstract says “calibrated … for 2017–2024”; the Methods say the calibration target is 2024 only. Please harmonise and state whether each value is deterministic or a Monte Carlo median.

**m2. Table 2’s “pre-entry share of emigration 0.45” is not the share of total emigration.** It is 1−σ. The realised central share is 491/(491+477) = 0.51. Please distinguish the pipeline non-entry share from the pre-entry share of total emigration, and correct the table.

**m3. “Remuneration alone” is not a single lever.** The remuneration scenario also reduces pre-entry emigration by 30%, so it is a package. Say “remuneration and conditions package” rather than “remuneration alone.”

**m4. The ageing equation is written incorrectly.** It subtracts e_a, r_a and q_a simultaneously. At 70+, r_a = 1.00 and q_a = 0.05, giving a negative survival factor. The implementation appears to apply mortality to survivors after retirement; write the equation accordingly, or combine the hazards as competing risks, and state the treatment of the 75+ open-ended group.

**m5. The historical emigration trend is not described in the manuscript.** The model appears to impose a linear rise from 60% of the 2024 value in 2017 to 100% in 2024. This affects the hindcast and the diaspora pool. Add it to the Methods and Table 2, and justify it.

**m6. Fig. 1’s 2010 point is from WHO, not INS/Ministry of Health.** The legend says “Observed (INS / Ministry of Health).” Clarify the source or remove the 2010 point. Also explain why the model line in Fig. 1 starts in 2010 while the model starts in 2008.

**m7. Fig. 6 does not match the sensitivity table and the text.** The retirement-age bar appears to have the 10th/90th percentile effects reversed, and the magnitudes differ (Fig. 6 roughly −140/+30; the sensitivity table +28/−213). The text says “retirement age had almost no effect (−0.03)” while the figure shows a non-trivial bar. Regenerate Fig. 6 from the final sensitivity run and check the sign convention.

**m8. “The return scenario had the widest interval” is true only among single policies.** The combined scenario’s interval is wider in absolute terms (21 546–30 112, width 8 566) than the return scenario’s (18 204–25 344, width 7 140). Say “among the single-policy scenarios.”

**m9. The migration-intention surveys are conference abstracts with small, non-representative samples.** The 38.5% figure comes from 182 young doctors in Sousse; the 53.6% figure from 56 interns/residents recruited via Facebook. Add sample sizes and caution, and note that the 38.5→53.6→68 comparison is across different samples, not a time series.

**m10. The Ghana evidence is about attrition from the public payroll, not international emigration.** The 12.5% relative reduction is at the low end of the reported 0.9–1.8 percentage-point range; the linear extrapolation to a 30% wage increase is an assumption. Soften “suggests” and state the outcome mismatch.

**m11. The Varga evidence also shows a large flow of physicians to domestic non-clinical jobs.** The model does not represent this exit route. Discuss it as a limitation, especially given the registered-versus-practising gap.

**m12. The 266→1 591 France figures should be checked.** Please confirm that 266 is a stock on the same definition as 1 591, and that the comparison is not affected by a change in the CNOM France counting method.

**m13. Reference 8 is a bare INS homepage.** Give the specific “Personnel médical” table URL and access date. References 28 and 29 are also bare dataset homepages; give the specific dataset and version.

**m14. The data availability statement and title-page details are placeholders.** The paper’s transparency and reproducibility claims cannot be assessed without the repository DOI and a public code/data archive. Complete these before resubmission. The submission checklist’s “Met” status for the data availability statement and reporting guideline should be revised accordingly.

**m15. The Additional file uses commas in numbers (12,600; 17,987) while the main text uses spaces (12 600; 17 987).** The submission checklist says spaces are used. Harmonise.

**m16. The AI-use statement is generic.** Specify the tools and the tasks (code development, language editing) in line with the journal’s policy.

**m17. The 2020–2021 discontinuity is attributed to a reporting change without evidence.** The public-sector count fell by 725 in 2020 and the total by 634, while the private sector grew by 91. This could be a real shift from public to private, a COVID-related exit, or a reporting change. Please justify the “probably a reporting change” claim or treat the alternative as a scenario.

## 5. Comments on figures and tables

- **Fig. 1** is clear and well labelled. The 2010 point source issue (m6) should be fixed. Consider adding a note that the shaded interval is a simulation interval under the assumed priors, not a confidence interval.
- **Fig. 2** is the most important figure. The RMSE surface is described as “flat,” but it varies from 252 to 360 (a 43% range). Add a contour or threshold that defines “consistent,” mark the best-fit and central points, and state that the grid is a two-dimensional slice.
- **Fig. 3** is clear. Panel B needs a note on whether the trend applies to pre-entry as well as post-entry emigration (M1). The training-expansion line is hard to distinguish from the baseline in panel A before 2036; consider a difference panel or a broken axis.
- **Fig. 4** is informative, but the zero-based y-axis in panel A compresses the differences. Consider a difference plot or a secondary panel. The error bars in panel C are very wide for the combined strategy; this is honest but deserves a comment in the legend.
- **Fig. 5** is clear. The density dip around 2024–2026 is plausible but unexplained; a note would help.
- **Fig. 6** needs to be regenerated to match the sensitivity table (m7). The sign convention for the retirement-age bar is the main problem.
- **Fig. 7** is clear. The age groups sum to about 99%; note rounding. The 65+ group is very small; consider combining it with 55–64 or noting the small numbers.
- **Fig. 8** is clear, but the legend and caption should state the pre-entry assumption (M1).

**Table 1** is useful. The “Tunisian physicians in Germany” row should clarify whether the 881 is based on country of training or nationality. The “Tunisian-born physicians in OECD countries” row should state that 4 000 is a lower bound and a 2015/16 estimate, not a 2008 stock.

**Table 2** needs the pre-entry share correction (m2) and a clearer label for the 675–1 839 range (deterministic grid, conditional on other parameters). The “1 900 (2025 statement)” entry needs a source and a definition.

**Table 3** is clear, but the “combined” scenario is not the sum of the individual scenarios; add a note.

**Table 4** is internally consistent (the net-change identity works with deaths of 22–32 per year). The 2024 stock is 15 316 versus the stated 15 315; this is rounding but should be harmonised.

**Table 5** is clear. The final column is correctly labelled as a deterministic structural scenario. The “difference from BAU” and “physician-years” values are deterministic; the Monte Carlo medians in Table S5 differ. State which is which.

**Table S5** is useful, but the deterministic and median columns should be labelled more prominently. The combined interval is wider than the return interval, contrary to the text (m8).

**Table S6** is useful, but the grid boundaries should be stated; the 675 lower bound is at the edge of the grid, so the true range could be wider.

**Table S8** is incomplete (M8).

## 6. Comments on reporting, data availability and format

1. The manuscript is within the journal’s word limit and the abstract is within 350 words. The structure, keywords and reference numbering are appropriate.
2. The data availability statement is a placeholder. For a paper whose main selling point is transparency, this is a significant gap. Provide the repository DOI and ensure the code, processed data and README are public.
3. The title page and author details are placeholders. Complete them before submission, or confirm that the journal’s review model allows anonymisation.
4. The reporting checklist should be item-level (1–30) and should mark the demand, gap, budgetary and regional items as not applicable with reasons.
5. The Additional file’s number formatting should match the main text (spaces, not commas).
6. The AI-use statement should be expanded to name the tools and the tasks.
7. The cover letter’s claim that the manuscript “offers a transferable methodological approach” is fair, but it would be stronger if the abstract foregrounded the identifiability result rather than the policy ranking.
8. The abbreviation list omits BAU (business as usual), which is used in Table 5 and the figure legends. Add it.

## 7. Confidential comments to the editor

**Recommendation: major revision.** The manuscript addresses an important question, and the identifiability analysis is a genuine contribution. However, the policy ranking is presented with more confidence than the model supports. The structural escalation scenario appears to apply the emigration trend to pre-entry emigration as well as post-entry emigration, which drives the “collapse” result; the sensitivity analysis labels marginal Spearman correlations as PRCCs, reversing the sign of the emigration effect; and the diaspora pool used for the return scenario is several times the destination-country stock. These are fixable but substantive. I would be willing to review a revised version. I have no conflicts of interest.

## 8. Suggested revision checklist

| # | Issue | Required action | Priority |
|---|---|---|---|
| 1 | Structural scenario applies trend to pre-entry emigration | State the assumption; show post-entry-only and combined versions; revise abstract, Results, Fig. 8 | Essential |
| 2 | “PRCC” values are marginal Spearman correlations | Recompute true PRCCs or relabel; correct the sign and ranking of emigration | Essential |
| 3 | Diaspora pool 3.5× destination stocks | Reconcile with OECD/France/Germany data; add mortality/re-emigration; sensitivity on initial pool | Essential |
| 4 | Monte Carlo does not reproduce 2024 stock; priors narrower than identified range | Clarify residual; calibrate exactly; widen priors or use full grid | Essential |
| 5 | Graduate series 1 305 vs 1 188 vs 1 900 | State actual series; justify acceleration; add alternative-output baselines | Essential |
| 6 | Policy ranking is arithmetic | Add break-even/threshold analysis | High |
| 7 | No cost analysis | Add cost caveat and simple cost-per-physician-year calculation | High |
| 8 | 30-item checklist incomplete | Provide item-level checklist (1–30) with NA justifications | High |
| 9 | Calibration described as 2017–2024 | Correct to 2024 endpoint; explain; report calibration error | Moderate |
| 10 | Identifiability range conditional | Describe as conditional; add destination-stock consistency check | Moderate |
| 11 | Numerical inconsistencies | Harmonise abstract, Results, tables | Moderate |
| 12 | Fig. 6/sensitivity-table mismatch | Regenerate figure; check sign convention | Moderate |
| 13 | Data availability/title page placeholders | Complete repository DOI and author details | Moderate |
| 14 | Minor data/reference issues | Fix pre-entry share, France 266 definition, migration-survey caveats, reference URLs | Minor |

---

*Reviewer’s note: I inspected the manuscript, supplementary files, figures and the supplied model outputs. The comments above are based on the reported numbers and the model description; where I refer to a specific numerical result, it can be reproduced from the reported parameters and tables.*
