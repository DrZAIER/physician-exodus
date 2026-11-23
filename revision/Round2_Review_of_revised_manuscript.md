# Independent manuscript review

**Manuscript:** *Retention, return or training? A stock-and-flow simulation of Tunisia's physician workforce under incomplete migration data*  
**Version reviewed:** Revision 2.0, 23 November 2026  
**Materials reviewed:** Revised manuscript (`Manuscript_HRH_Revised(1).md`), revised supplementary file (`Additional_file_1_Revised.md`), Scientific Audit Report, Final QA Report and Figure Revision Register.

## Overall assessment

**Recommendation: major revision before submission.** The manuscript has improved materially and now presents a potentially publishable modelling study. Its strongest contribution is not a precise estimate of Tunisian physician emigration. It is the demonstration that aggregate workforce stocks cannot identify gross migration flows when domestic non-entry, international pre-entry emigration and post-entry emigration are not separately observed.

The revision corrects the most consequential conceptual error in the previous version: it no longer treats every graduate who does not enter the practising workforce as an international emigrant. It introduces the parameter φ, separates domestic non-entry from pre-entry international emigration, and restricts the return-eligible pool to people assumed to have emigrated. This is a substantial improvement in construct validity and policy interpretation.

The revised manuscript is more transparent about assumptions, structural uncertainty, calibration, historical misfit and the limits of its policy scenarios. The supplement is broadly aligned with the revised manuscript, and the QA report documents a successful pipeline execution, 4,000 Monte Carlo draws, passing tests and internal numerical checks.

Nevertheless, the revision is not yet submission-ready. There is a material inconsistency in the return-pool accounting and its reported eventual return probability. There are also claims of robustness that are stronger than the manuscript's own sensitivity results support, and several important assumptions remain insufficiently justified. These are not cosmetic issues. They affect the interpretation of return migration, the policy ranking and the strength of the conclusions.

This review assesses the supplied documents. I did not independently execute the model code, inspect its raw inputs, verify every cited source against the original publication, or inspect the regenerated figure files. The QA report is evidence that the reported pipeline ran and passed its programmed checks; it is not independent confirmation that the model specification is correct.

## 1. Major strengths

### 1.1 The central conceptual correction is appropriate

The split

\[
X_{\mathrm{pre}}(t)=\phi(t)[1-\sigma(t)]G(t-L)
\]

and

\[
X_{\mathrm{dom}}(t)=[1-\phi(t)][1-\sigma(t)]G(t-L)
\]

is the most important improvement. It distinguishes international emigration from domestic non-entry and prevents the model from automatically treating all non-entrants as potential return migrants.

The manuscript correctly identifies φ as unobserved and treats 0.50 as a scenario assumption rather than an empirical estimate. It also distinguishes the central Monte Carlo range (0.25–0.75) from the wider structural range (0–1). This is a defensible way to expose the data limitation, provided the conditional nature of the results remains prominent.

### 1.2 The paper now makes a more useful contribution about identifiability

The calibration ridge and the distinction between stock information and gross flows are central to the paper's value. The manuscript explains why different combinations of pipeline retention, training output and emigration can reproduce a similar observed stock. The destination-stock screen is now described as a plausibility check rather than validation or statistical identification.

This is stronger than presenting a single migration estimate from incompatible administrative indicators. The paper should foreground this as its principal methodological contribution.

### 1.3 Uncertainty and scenario reporting have improved

The revision separates deterministic central estimates from Monte Carlo medians and intervals, uses common random numbers across scenarios, reports the calibration error, and adds structural escalation scenarios for post-entry migration alone and for both international margins. It also reports the overlap between career development, training and return scenarios rather than forcing a definitive ranking among them.

The 4,000-draw analysis, true PRCC description, sensitivity to φ and the initial pool, and the explicit distinction between internal consistency and external validation are positive features.

### 1.4 The revised supplement is substantially better aligned

The supplied revised supplement reports the same central 2040 workforce estimates, 4,000 Monte Carlo draws, φ specification, break-even thresholds and scenario ordering as the manuscript. This resolves the major version mismatch identified in the previous review. The QA report also records regenerated DOCX files, tables and figures.

## 2. Major issues requiring resolution

### Major issue 1: Return-pool accounting and eventual return probability are internally inconsistent

This is the most important remaining technical issue.

The manuscript states that:

- returns occur at rate \(R(t)=\rho(t)D(t)\);
- 85% of return migrants remain in practice;
- the remaining 15% rejoin the return-eligible pool; and
- the pool evolves as \(D(t+1)=D(t)[1-\rho(t)-\delta]+X_{\mathrm{pre}}(t)+M(t)+\text{re-emigration}\).

If the 15% who re-emigrate are added back to the pool, then the net annual removal from the pool through the return pathway is not \(\rho D\), but \(0.85\rho D\). Ignoring new inflows for the purpose of calculating eventual absorption, the effective competing exits are therefore successful return at \(0.85\rho\) and diaspora attrition at \(\delta\).

At the stated central values \(\rho=0.02\) and \(\delta=0.08\), this gives an eventual successful-return probability of:

\[
\frac{0.85\rho}{0.85\rho+\delta}
=\frac{0.017}{0.097}
\approx 0.175.
\]

That is not the reported 20% if the stated calculation is \(\rho/(\rho+\delta)\). More importantly, the supplement reports an eventual return probability of 0.20 and a mean duration of about 10 years, which appear to use the unadjusted competing-risk rates while the pool equation also recycles 15% of returns.

The authors must reconcile the equation, the treatment of re-emigration, the definition of “eventual return”, the reported probability and the mean duration. There are at least two possible coherent specifications:
1. Treat \(\rho D\) as a successful return flow and do not return the unsuccessful fraction to the pool; or
2. Keep the 15% re-emigration loop and calculate the eventual probability and duration using the effective transition structure.

The model code and all affected outputs must then be rerun. This may change the return scenario, the pool size, the return sensitivity table and cost-effectiveness-style ratios. The current return result should not be accepted until this is resolved.

### Major issue 2: The claim that remuneration robustly outperforms training is too broad

The manuscript states that combined and remuneration strategies robustly outperform training. The Monte Carlo analysis supports remuneration outperforming training within the selected φ distribution of 0.25–0.75, and the QA report says remuneration ranks second in 99.8% of draws. But the structural sensitivity table extends φ to 0.

At φ = 0, Table 7 reports:
- Remuneration: 16,671 physicians in 2040.
- Training: 16,698 physicians in 2040.

Thus, remuneration is slightly below training at this structural endpoint. The statement that remuneration is robustly better than training is true only within the specified Monte Carlo prior support, not across the full structural range examined by the paper.

Revise the abstract, discussion and conclusion to say that remuneration outperforms training across the Monte Carlo draws under the selected φ prior, while the ordering is not universal across the full structural range. The combined strategy appears to remain above training in the reported φ scenarios, but that conclusion should also be stated as conditional on the scenario assumptions.

### Major issue 3: Policy effect sizes are assumptions, not empirically identified effects

The remuneration scenario assumes a 30% reduction in both pre-entry international and post-entry emigration. Career development assumes a 15% reduction in both margins. The combined scenario assumes a 35% reduction and a higher return rate. These assumptions drive the ranking.

The Ghana evidence cited in the manuscript concerns payroll attrition and does not directly identify the effect of a 30% pay increase on international emigration among Tunisian physicians. The manuscript acknowledges this distinction, but the numerical translation remains speculative. Similarly, the evidence for career development reducing both pre-entry and post-entry emigration by 15% is not sufficiently established in the text.

The authors should:
- label these as illustrative scenario effect sizes throughout;
- explain why the same intervention is assumed to affect both international margins;
- distinguish evidence for general workforce retention from evidence for international migration specifically;
- avoid language implying that a 30% salary increase is expected to cause a one-third reduction in emigration; and
- show whether the policy ranking changes under a wider and more conservative range of effects, including zero or small effects.

The break-even result is useful arithmetic, not an empirically established policy threshold. A 14.5% reduction in emigration matches the 30% training scenario only under the central model specification and the chosen effect definitions.

### Major issue 4: The training expansion scenario does not yet operationalise the announced policy

The manuscript correctly notes that the 2025 announcement concerns a 30% increase in admissions, not a 30% increase in graduates. However, the model applies a 30% multiplier to graduate cohorts from 2031. The link between admissions, completion, graduation and entry into practice is not modelled.

This is a material distinction because an admissions increase will affect graduate output only after the medical education and postgraduate training pathway, and the additional cohort may not have the same completion or entry rates as the baseline. The authors should either:
- model the admissions increase with an explicit education and postgraduate lag and completion assumptions; or
- clearly relabel the scenario as a hypothetical 30% increase in graduate output, not a simulation of the announced admissions policy.

The current wording risks implying that the model evaluates the actual government announcement when it evaluates a simplified graduate-output shock.

### Major issue 5: The initial return-eligible pool is not empirically established

The manuscript uses an initial pool of 4,000, citing an OECD estimate of Tunisian-born physicians in OECD countries. This is not equivalent to Tunisian-trained physicians who previously practised in Tunisia and are eligible to return to the Tunisian workforce.

The manuscript now calls the pool a return-eligible accounting stock rather than a diaspora estimate, which is appropriate. However, the use of the OECD figure as its central initial value remains weakly grounded. Country of birth does not identify country of training, previous practice in Tunisia or current willingness and eligibility to return. It may include physicians who never trained or worked in Tunisia and exclude Tunisian-trained physicians born elsewhere.

The paper should not call 4,000 a lower bound for the return-eligible pool without qualification. It should describe it as an external reference used to anchor an illustrative initial pool. The return scenario should be presented as especially assumption-dependent, and the manuscript should avoid policy claims based on its cost per physician-year as if the pool were a measured target population.

### Major issue 6: Historical fit and the 2020–2023 residual need more careful interpretation

The model is calibrated to the 2024 endpoint and has an RMSE of 284 over 2017–2024. It overpredicts the observed stock by 232–519 physicians in 2020–2023 after the public-sector discontinuity. Excluding 2020–2021 improves the RMSE.

The manuscript appropriately calls this a consistency check rather than validation. However, the unexplained residual is large enough to affect confidence in the reconstructed flows and the calibration ridge. The paper should not implicitly treat this residual as evidence of migration or as a solved reporting discontinuity.

The authors should add a concise explanation of what is known and unknown about the public-sector count change, and state explicitly that the model cannot distinguish actual exits from reporting or classification changes. A sensitivity excluding the discontinuity is useful, but it does not resolve its cause.

### Major issue 7: The initial age structure materially affects the projection

The 2008 age structure is reconstructed from CNOM registrations, spread uniformly within five-year bands and scaled to an estimated practising stock. The manuscript now identifies this as a reconstruction and reports age-shape sensitivity. That is good practice.

However, the reported shift in 2040 baseline from 14,961 to 16,570 under the younger and older age profiles is large enough to deserve more prominence. The main results are not simply determined by the 2024 endpoint calibration; they also depend on the age distribution used to project retirement and mortality.

The authors should make this uncertainty more visible in the abstract or principal limitations and avoid treating the central age profile as a reliable observed distribution.

## 3. Additional technical and interpretive issues

### 3.1 The administrative and press migration indicators are not directly comparable

The discussion says that an administrative proxy of about 374 lies inside the central range and that press estimates of 1,300–1,450 lie near the upper bound. These indicators refer to different administrative events and may differ in year, population and definition. The 1,300–1,450 values are near the φ = 1 upper-bound range, not the central φ = 0.50 range.

Clarify the year and definition of the approximately 374 indicator, avoid presenting it as a direct annual migration count, and specify that the press estimates are near the upper-bound scenario only. The paper's central message is that these figures are not interchangeable; the discussion should not inadvertently compare them as though they were.

### 3.2 The 2024 international emigration estimate is conditional, not directly observed

The estimate of 563 (245 pre-entry and 317 post-entry) is a model-derived central estimate. The manuscript generally labels it correctly, but some phrasing could still be read as an observed annual flow. Consistently use “model-implied” or “under the central specification” when presenting it.

### 3.3 The cost analysis is illustrative and should not be framed as economic evaluation

The manuscript appropriately separates fiscal transfers from real resource costs and states that it is not a cost-effectiveness analysis. Retain that restraint. The assumed compensation, training, career-development and return-programme unit costs are not demonstrated to be audited national costs. Cost per physician-year is a scenario ratio, not a full economic evaluation, budget-impact analysis or value-for-money result.

The remuneration cost is a fiscal transfer and should not be compared directly with the real resource costs of training or return as though the categories were economically equivalent. Consider moving the cost analysis to a clearly labelled exploratory subsection or supplement if the journal's word limit requires prioritisation.

### 3.4 The “retention dominates training” language needs qualification

The manuscript's interpretation says retention dominates training because an emigrant is lost for the rest of their working life. This is too categorical. The model includes return migration, and not all pipeline non-entry is emigration. The statement also overstates what a scenario model with assumed intervention effects can establish.

A more defensible formulation is:

> Under the central assumptions, reducing international emigration produces earlier and larger workforce gains than a 30% increase in graduate output, because the latter enters the practising stock only after the postgraduate lag. The size and ranking of these gains depend on the assumed share of non-entry attributable to emigration and on the assumed policy effects.

### 3.5 The policy scenario effects may be correlated in practice

The model treats intervention effects as scenario multipliers. In reality, remuneration, working conditions, career development and return incentives may interact. The combined strategy is described as non-additive, but the assumed 35% reduction and 1.75 return-rate multiplier still need a clearer rationale. The manuscript should state that this is a constructed package scenario, not an empirically estimated combined effect.

### 3.6 The return scenario's “eventual return probability” needs a precise definition

Apart from the accounting inconsistency noted above, clarify whether “return” means:
- at least one return to Tunisia;
- a return that results in sustained practice;
- a permanent return; or
- a return attempt before subsequent re-emigration.

These are distinct outcomes. The model's 85% retention parameter suggests that the distinction is important.

### 3.7 The 2024 flow decomposition needs a clear interpretation

The 2024 table reports 600 entrants, 491 pipeline non-entrants, 317 post-entry emigrants, 81 returns, 367 retirements and 26 deaths. This is useful, but the 600 entrants and 491 non-entrants imply a graduate cohort of approximately 1,091, which differs from the 1,305 graduates cited for 2024. The five-year lag means these are not necessarily the same calendar-year cohort, but the table should make the cohort year explicit to prevent readers from assuming that the flow decomposition uses 2024 graduates.

### 3.8 The 2024 calibration endpoint is not independent validation

Exact calibration to 15,315 is a fitting condition. It should not be described as a validation result. The QA report's exact calibration check confirms that the calibration procedure works as programmed; it does not validate the model's historical or future predictive accuracy.

### 3.9 The PRCC interpretation should remain conditional on the calibration design

The manuscript's explanation of marginal versus conditional associations along the calibration ridge is thoughtful. However, readers may find a positive PRCC for φ surprising. Explain that the PRCCs describe the selected joint parameterisation and calibration procedure, not causal effects or general population-level associations. State whether PRCC estimates were stable across seeds or resampling; the QA report does not document such stability.

### 3.10 The age-specific emigration profile remains a strong assumption

The age profile is specified as relative weights and varied through a lognormal tilt. There is no direct Tunisian age-specific migration flow dataset. The paper should consistently call this an assumed profile and avoid implying that the age distribution of emigration is empirically estimated.

## 4. Abstract, discussion and conclusion

The abstract is within the reported 350-word limit, but its opening sentence, “Tunisia trains more physicians than it retains,” is stronger than the data support. The model does not observe how many graduates are retained in domestic practice, and φ is not identified.

Suggested replacement:

> Tunisia faces substantial uncertainty about the relationship between physician training, entry into domestic practice and international emigration.

The abstract should also make clear that the policy comparisons are conditional scenario results. In particular, the statement that combined exceeds remuneration in 99.8% of draws should be checked against the intended rank statistic and worded unambiguously. The QA report says remuneration ranks second in 99.8% of draws; the manuscript should state the same result in the same terms.

The conclusion currently says that the workforce is shaped more by retention than by training capacity within 15 years. This is too broad for a model whose central migration share and policy effects are assumptions.

Suggested replacement:

> Under the central model assumptions, reducing international emigration produces larger 15-year workforce gains than a 30% increase in graduate output. This comparison is conditional on the assumed share of pipeline non-entry attributable to international emigration, the assumed effects of retention interventions and the postgraduate lag. The model does not identify Tunisia's true gross emigration flow. Its principal implication is the need for linked, cohort-consistent data that distinguish registration, practice, entry, domestic non-entry and international migration.

The conclusion should avoid calling the policy ranking robust unless it specifies the uncertainty domain over which robustness was tested.

## 5. Supplementary material and reporting

The revised supplement is materially improved and appears numerically aligned with the manuscript for the main reported scenario values. It includes model notation, parameter distributions, scenario results, the identifiability grid, structural scenarios, break-even analysis, diaspora sensitivity, specification sensitivity, costs, validation checks and the 30-item reporting checklist.

Before submission, the authors should still:

1. Correct and rerun the return-pool accounting and eventual return calculations.
2. Confirm that every supplementary table is generated from the same final model run and that all reported values match the final manuscript.
3. Ensure that the repository contains every file referenced by the supplement, including the full identifiability grid and sensitivity CSV files.
4. Check that the flow diagram accurately represents the return/re-emigration loop after the return-pool correction.
5. Ensure that figure legends and figure files correspond to the final outputs. The figure register records regeneration, but the actual figures were not available for visual inspection in the reviewed materials.
6. Retain the distinction between internal validation checks, retrospective fit and external validation. These are not interchangeable.

The reporting checklist should not be treated as proof that every item is substantively satisfied. For example, an item marked “reported” may still rely on weakly supported assumptions or a limited supply-only scope.

## 6. Editorial and submission readiness

The manuscript is clearly structured and has a coherent narrative. The two-author metadata and the two stated affiliations are internally consistent in the supplied version. The manuscript reports 3,652 main-text words and 347 abstract words in the QA report.

The declarations are not complete. Before submission, the authors must finalise:
- data and code repository URL and persistent identifier;
- funding statement;
- competing interests;
- author contributions;
- acknowledgements, if applicable;
- confirmation of the AI-tool statement and the journal's required disclosure format;
- Mariem Zribi's ORCID only if available and desired.

The manuscript should not be submitted with bracketed placeholders. The authors should also verify the journal's current instructions for abstract structure, word count, reference style, data availability and AI disclosure immediately before submission.

## 7. Priority revision plan

### Essential before submission

1. **Resolve the return-pool equation and probability inconsistency.** Reconcile the 85% return retention, re-emigration loop, 20% eventual return probability and 10-year mean duration. Rerun all affected analyses.
2. **Reconcile the policy-ranking language.** Acknowledge that remuneration is not above training at φ = 0, despite outperforming training in the selected Monte Carlo draws.
3. **Clarify the training scenario.** Either model admissions and completion explicitly or call it a hypothetical increase in graduate output.
4. **Reframe the return-pool anchor.** Describe the OECD country-of-birth estimate as an external reference, not a validated count or lower bound of return-eligible Tunisian-trained physicians.
5. **Qualify causal and policy language.** Make clear that effect sizes are assumptions and break-even thresholds are conditional arithmetic.
6. **Complete the declarations and repository details.**
7. **Run a final manuscript–supplement–code–figure consistency audit after all model changes.**

### Important but potentially manageable in the same revision

8. Clarify the year and definition of the administrative migration proxy and distinguish it from press estimates.
9. Make the 2020–2023 historical residual and the reconstructed initial age profile more prominent limitations.
10. Clarify the cohort year represented by the 2024 graduate pipeline decomposition.
11. State that PRCCs are conditional on the chosen priors and calibration procedure.
12. Verify all references and the current journal submission requirements.

## 8. Final verdict

This is now a serious and potentially publishable health workforce modelling paper. The conceptual correction around φ materially improves the model, and the revised manuscript is more honest about what aggregate data can and cannot identify. The strongest contribution is the demonstration that published stock data and heterogeneous migration indicators do not identify gross emigration, together with a transparent framework for showing how policy comparisons depend on that uncertainty.

The paper is not yet ready for submission because the return-pool formulation appears inconsistent with its reported eventual return probability and duration. That issue needs to be resolved in the model, not merely explained away in the prose. The claims about remuneration outperforming training also need to be bounded to the uncertainty range actually tested. The admissions-versus-graduates distinction and the initial return-eligible pool require clearer treatment.

**Recommendation: major revision before submission, not rejection.** I would retain the overall modelling approach and the paper's central identifiability message. I would not accept the current return-migration results or the broadest policy-ranking claims until the specified corrections have been made and the full pipeline rerun.

---

*Review limitation: this is a document-based scientific review of the supplied revision package. It is not an independent replication of the code, source-data verification, reference-by-reference audit, or visual review of the regenerated figures.*
