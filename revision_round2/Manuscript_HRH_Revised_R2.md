# Retention, return or training? A stock-and-flow simulation of Tunisia's physician workforce under incomplete migration data

**Authors:** Firas Zaier^1, Mariem Zribi^1,2

**Affiliations:**
^1 Faculty of Medicine of Tunis, University of Tunis El Manar, Tunis, Tunisia
^2 National Health Institute, Republic of Tunisia Ministry of Public Health, Tunis, Tunisia

**Corresponding author:** Firas Zaier, Faculty of Medicine of Tunis, University of Tunis El Manar, Tunis, Tunisia. Email: dr.firas.zaier@gmail.com. ORCID: https://orcid.org/0009-0006-4887-1819

**Co-author:** Mariem Zribi. Email: mariem.zribi@fmt.utm.tn. ORCID: https://orcid.org/0009-0004-5917-984X

**Word count:** 3 996 (abstract and main text; excluding tables, figures, references and additional files)

**Tables:** 8 **Figures:** 9 **Additional files:** 1

---

## Abstract

**Background.** Tunisia faces substantial uncertainty about the relationship between physician training, entry into domestic practice and international emigration. Registered, practising and emigrated physicians are conflated; non-entry is often treated as emigration. We separated non-entry from international emigration and asked what aggregate data can identify and how retention, return and training compare.

**Methods.** We built an annual, single-year-of-age cohort-component model of practising physicians in Tunisia (2008–2040), calibrated to the 2024 stock. Pipeline non-entry is split into international pre-entry emigration (φ = 0.50 central) and domestic non-entry; only international emigration enters a return-eligible pool with attrition. We compared business as usual with remuneration and working conditions, career development, return migration, 30% graduate-output expansion and a combined strategy. We used 4 000 Monte Carlo draws, true partial rank correlations, structural escalation, break-even analysis and return-accounting checks.

**Results.** The 2024 stock was 15 315 (1.28/1 000). The baseline reaches 15 821 in 2040 (median 15 830; 90% interval 14 407–17 438; density 1.25/1 000), but the reconstructed 2008 age structure shifts it to 14 961–16 570. The stock path is consistent with 262–1 017 international emigrants (φ = 0.50), or 502–1 540 if all non-entry were emigration. Combined adds 3 341 physicians (19 162; 26 085 physician-years); remuneration adds 2 266, career development 1 132, expansion 1 092 and return migration 868. A 14.5% emigration reduction matches a 30% graduate-output expansion; 62% expansion matches 30% retention. In the φ prior (0.25–0.75), combined ranked first in all draws and remuneration second in 99.8%; at φ = 0, remuneration 27 below the expansion. Career, expansion and return overlap. With post-entry emigration rising 3% a year, the baseline reaches 14 461 and combined 18 315; if both margins rise, 13 184 and 17 519.

**Conclusions.** Under the central assumptions, reducing international emigration produces larger 15-year gains than 30% graduate-output expansion, but the ranking is conditional on φ, the assumed policy effects, the age structure and the postgraduate lag. The model does not identify Tunisia's true gross emigration flow; its main implication is the need for linked, cohort-consistent data distinguishing registration, practice, entry, domestic non-entry and international migration.

**Keywords:** health workforce; physician migration; brain drain; Tunisia; stock-and-flow model; health policy; uncertainty analysis

---

## Background

Health systems depend on the size, skills and distribution of their workforce. The World Health Organization estimates that substantially more health workers will be needed to reach universal health coverage and the Sustainable Development Goals, with shortages concentrated in low- and middle-income countries [1,2,35]. International migration is one of several flows that shape a national workforce, but it is the most contested: sending countries lose training investments and service capacity, while destination countries gain ready-trained staff [3,4,33]; distribution across regions and sectors is a separate problem [32,34].

Measuring migration is harder than measuring the stock. Destination-country registers capture physicians who are registered abroad, but not those who are unregistered, in non-OECD destinations, or in temporary or circular movement; source-country registers capture inscriptions, not active practice [4–7,42]. Cross-country comparisons therefore produce different totals depending on whether they use country of birth, country of training, nationality, registration or active practice [5–7]. The same problem appears within countries when registration, payroll and survey counts are used interchangeably.

Tunisia illustrates both the policy urgency and the measurement problem. Four public medical faculties graduate roughly 1 100 physicians a year [37], and the government announced a 30% increase in admissions in 2025 [9]. Tunisian-trained physicians are a large and growing group in France (1 591 registered in 2023, up from 266 in 2010) [10] and Germany (881 in 2022) [11]. The Tunisian Order of Physicians (Conseil National de l'Ordre des Médecins, CNOM) reported 27 935 registered physicians at the end of 2022 [14] and indexed 31 804 directory records in 2026 [15]. The Ministry of Health and the National Institute of Statistics (INS) report about 15 000 physicians in active practice [16,17]. The gap includes retired, inactive and administrative physicians, and some physicians abroad who remain registered. Departure indicators range from 187 removal requests in the first half of 2023 [11] to 1 325 in 2023 [13] and about 1 400 in 2024 [12], with 975 departure files prepared in 2021 [18]. These indicators measure different things: intentions, administrative requests, certificates and reported departures.

International evidence shows that migration responds to wages, working conditions, career opportunities, security, diasporic ties and destination-country immigration policy [3,4,19–21]. In Ghana, a public-sector wage reform that raised pay by about 10% reduced annual attrition among young health workers by about one percentage point from a mean of eight [19]. A related evaluation found lower emigration after salary increases [20]. The Ghanaian outcome is payroll attrition, not necessarily international emigration, and the effect sizes are uncertain. Return can be substantial: more than half of Hungarian physicians who left during 2003–2011 returned at some point [21], although the same evidence shows a large flow into domestic non-clinical jobs. Tunisian surveys report migration intentions of 38.5% in 2019 (182 young doctors in Sousse), 53.6% in 2022 (56 interns and residents recruited through social media) and 68% in 2024 [22–24]. These are small, non-representative samples; the comparison is across samples, not a time series, and intentions are not flows.

A conceptual problem runs through this literature. Graduates who do not enter the practising workforce are often treated as emigrants, but non-entry also includes further training, domestic non-clinical employment, temporary inactivity and other reasons. The share of non-entry that is international emigration is not observed. The distinction matters because only emigrants can return from abroad, and because retention policies may affect emigration and domestic non-entry differently.

Workforce projection models organise this uncertainty. Cohort-component stock-and-flow models are standard, and the JRC SANDEM model is a recent example [25,26]. Health labour market analysis treats migration as one adjustment mechanism among several [36]. Agent-based models can represent individual decisions and heterogeneity; the Portuguese physician workforce model is the closest application [27]. All of these approaches need data that Tunisia lacks: age-specific migration rates, reliable annual flows and a separation of temporary and permanent moves. Reviews emphasise that projections are conditional statements whose credibility depends on transparency, explicit assumptions and validation, not computational sophistication [28–31].

We built a parsimonious, age-structured model to integrate the Tunisian evidence, separate non-entry from emigration, compare retention, return and training over 15 years, quantify uncertainty, and express the trade-off as a break-even threshold and illustrative cost. We do not claim causal policy effects.

## Methods

### Design and reporting

We built an annual, single-year-of-age cohort-component model of physicians in active practice in Tunisia from 2008 to 2040, with 2017–2024 for retrospective comparison and 2024 as the calibration endpoint. The model is supply-only. It follows the 30-item reporting guideline of Lee et al. [28] (Additional file 1) and was implemented in Python 3.14 with NumPy, pandas, SciPy and Matplotlib. Code, data and a one-command pipeline are in the repository. AI-assisted tools (OpenAI ChatGPT and OpenCode) supported code development, numerical checks and language editing; the authors reviewed all decisions and text.

### Definitions and data

We modelled practising physicians: public-sector physicians plus private practitioners in the national health map, calibrated to the INS/Ministry of Health series [16,17]. This is not CNOM registration, country of birth or country of training. Table 1 summarises sources; Table 2 gives parameters and evidence status.

The stock rose from 14 892 in 2017 to 15 426 in 2019, fell to 14 792 in 2020 and reached 15 315 in 2024 [16]; the 2020 fall reflected a 725-physician drop in the public sector while the private sector grew by 91. We calibrate to 2024 and report fit with and without 2020–2021. Graduates were reconstructed from 987 in 2013, 1 128 in 2021 and 1 305 in 2024 [37]; baseline output is constant at 1 305 after 2024, with a continued-growth alternative (1 709 by 2040). The 30% expansion is a hypothetical graduate-output shock from 2031, not a simulation of the announced admissions policy; 80–100% completion is tested. Population denominators use the 2024 census and UN WPP 2024 [38,39].

### Model structure

The model tracks practising physicians by age, N_a(t), and a return-eligible pool, D(t) (Fig. S1). A graduate cohort G(t−L) reaches the labour market after lag L (central 5 years). A share σ enters practice. Pipeline non-entry is split:

X_pre(t) = φ(t)[1 − σ(t)]G(t−L),

X_dom(t) = [1 − φ(t)][1 − σ(t)]G(t−L),

E(t) = G(t−L) − X_pre(t) − X_dom(t).

φ is the share of non-entry assumed to be international emigration; it is unobserved, with central 0.50 and alternatives 0–1. Only X_pre enters D. Post-entry emigration is M(t), allocated by age profile w_a: e_a = min{M w_a / ΣN_b w_b, 0.35}, M = mΠε. A projection-only shock ε applies after 2024. Post-entry intensity rises linearly from 60% of its 2024 value in 2017 to 100% in 2024; this is an assumption.

Return attempts are ρ times the pool including current-year inflows. θ = 0.85 succeed and enter practice; (1−θ)ρ re-emigrate and, under central recycling, rejoin D immediately. The exact annual transition is D(t+1) = [D(t) + X_pre(t) + M(t)](1−θρ)(1−δ): gross attempts ρD, successful θρD, unsuccessful (1−θ)ρD returned, so the net return-related reduction is θρD, then attrition δ. With δ = 0.08 and ρ = 0.02, the exact discrete-time attempt probability is 20.3%, successful return 17.8%, and mean time to exit 10.5 years. A no-recycling sensitivity makes re-emigrants permanently ineligible; success is 17.3% and duration 10.2 years. The pool is an accounting stock, not a diaspora estimate.

Retirement hazards approximate Tunisian legal ages (60 private, 62 public, extensions for professors): 0 below 60, 0.20 at 60–61, 0.45 at 62, 0.35 at 63–64, 0.45 at 65–69, 1.00 at 70+. Mortality is 0.1% at 25–54, 0.4% at 55–64, 1.5% at 65–74 and 5% at 75+. Mortality is applied first, then retirement among survivors; ages advance one year. The 75+ group is open-ended.

The 2008 age distribution is reconstructed from CNOM 2007–2008 [40], scaled to 12 600 (WHO 2010: 12 996 [41]); it is not observed practising physicians by age, and two-year younger/older shapes are tested. The initial pool is an illustrative anchor of 4 000 with reference to OECD country-of-birth estimates [42]; country of birth does not identify training, prior practice or eligibility to return. It is varied 2 000–8 000.

### Calibration and identifiability

m was solved so that the 2024 stock equalled 15 315 (error <0.2). Calibration is a fitting condition, not validation. The calibration identifies a ridge: higher σ requires higher m. We mapped fit over σ = 0.20–0.80 and training multipliers 0.80–1.60, with acceptable fit RMSE ≤2% of mean stock (about 302) and strict fit ≤1.10× best. We screened the 2024 pool against destination stocks (4 000–10 000), a plausibility check, not identification. Calibration to 2019 and 2022 is a sensitivity to the 2020–2021 discontinuity.

### Scenarios

Scenarios start in 2026 and phase in over three years (Table 3): business as usual; remuneration (30% reduction in pre-entry international and post-entry emigration); career development (15%); return migration (return rate 2.0–3.5%); hypothetical +30% graduate output from 2031; and combined (35% reduction plus 3.5% return rate). The combined package is constructed, not estimated. Effect sizes are illustrative; low/high and conservative alternatives are in Tables S3 and 8.

### Uncertainty and sensitivity

We generated 4 000 draws from the priors in Table S4: σ Beta (mean 0.55, SD 0.12), φ uniform (0.25–0.75), training lognormal (median 1.0, log-SD 0.20), ρ Beta (mean 0.02, SD 0.01), δ uniform (0.04–0.12), return retention uniform (0.75–0.95), initial pool lognormal (median 4 000, log-SD 0.30), mortality multiplier uniform (0.8–1.2), and a projection-only emigration shock lognormal (median 1.0, log-SD 0.10). m was recalibrated exactly for each draw; all scenarios used the same draw. Intervals are 5th–95th percentiles.

We explored post-entry emigration rising 3–7% per year and both margins. One-at-a-time sensitivity varied parameters from the 10th to 90th percentile; true PRCCs were computed by rank-residualising the 2040 stock and each parameter on all others. PRCCs are conditional on priors and calibration, not causal; bootstrap 90% intervals are reported. We varied φ (0–1), lag (3–7 years), age shape, retirement/mortality, computed a break-even grid, and tested return recycling.

### Illustrative costs

We attached illustrative 2025 TND unit costs: 30% increment on an assumed public-sector compensation of TND 72 000 per physician-year; TND 3 000 per practising physician-year for career development; TND 250 000 per additional graduate; TND 40 000 per additional return migrant. Fiscal transfers and resource costs are separated and not commensurable. Costs are undiscounted, exclude infrastructure and demand-side costs, and are not a cost-effectiveness analysis.

## Results

### Retrospective fit and calibration

The model reproduced the 2024 stock (error −0.10) and tracked 2017–2024 with RMSE 284 (1.5%) and MAPE 1.5% (Fig. 1). It over-predicted 2020–2023 by 232–519 after the public-sector drop; excluding 2020–2021, RMSE was 189. The public count fell 725 while private grew 91; this could be reclassification, reporting, real exit or a mix, and the residual is not migration evidence. Calibrating to 2019 or 2022 gives 2040 baselines of 16 032 and 15 247 (Table 8); the endpoint matters. This is a consistency check, not validation.

The calibration implies 600 entries, 491 pipeline non-entrants (245 international emigrants and 245 domestic non-entrants), 317 post-entry emigrants, 81 successful returns and 367 retirements in 2024 (Table 4). Model-implied international emigration was about 563, with 44% before entry. The 600 entrants come from the 2019 graduate cohort (1 091), not the 2024 cohort (1 305), which enters from 2029.

### What the stock path can identify

The fit surface is a ridge (Fig. 2). RMSE ranges 238–559. The best fit (σ = 0.20, training 1.55) implies 1 353 non-entrants, 678 international emigrants under φ = 0.50, and a pool of 5 509; it lies at the grid boundaries. Acceptable set: non-entry 240–1 396, international emigration 262–1 017, φ = 1 upper bound 502–1 540. The destination screen narrows these to 481–1 017 and 705–1 540, pools 4 015–7 304; it is a plausibility check, not identification. The range is conditional, not a confidence interval. The stock path constrains net flow; the earlier 582–1 497 is the φ = 1 upper bound.

### Return accounting

Under central recycling, the probability of at least one return attempt is 20.3%, eventual successful return is 17.8%, and mean time to exit is 10.5 years. Without recycling, successful return is 17.3%, duration 10.2 years, the 2024 pool is 4 199 rather than 4 312, and the return advantage is 828 rather than 868 physicians (Table S9). The qualitative conclusion is unchanged.

### Baseline projection

The stock reaches 15 821 in 2040 (median 15 830; 90% interval 14 407–17 438; Fig. 1, Fig. 3A). Density falls from 1.28 to 1.25 per 1 000 (1.14–1.38), below the OECD average of 3.9 [8] (Fig. 5). This is a plateau, not a collapse: it reflects about 1 300 graduates, 55% entry and constant emigration, with retirements rising from 367 to 542. The reconstructed 2008 age structure shifts the baseline to 14 961–16 570, a range larger than the training effect.

### Policy scenarios and the ranking

All five policies produce higher stocks than business as usual (Table 5, Fig. 3A, Fig. 4). Combined: 19 162 (+3 341; 26 085 physician-years). Remuneration: 18 087 (+2 266; 17 530); career: 16 953 (+1 132; 8 762); training: 16 914 (+1 092; 3 269); return: 16 689 (+868; 6 656).

Within the Monte Carlo φ prior (0.25–0.75), combined ranks first in all draws and remuneration second in 99.8%. At φ = 0, remuneration is 16 671 and training 16 698, so remuneration 27 below the expansion. Career, training and return overlap: career beats training in 65% of draws, training beats return in 68%, and return is last in 66%. The central order is combined > remuneration > career > training > return, but career and training differ by 39. The remuneration advantage is bounded to the Monte Carlo prior.

Training is slow and leaky: it increases cumulative emigration (9 520 vs 9 079) because larger cohorts produce more non-entrants, half of whom are assumed to emigrate. With 80% completion of additional admissions, the 2040 effect is 16 695 rather than 16 914.

### Break-even

A 14.5% reduction in emigration matches the hypothetical 30% graduate-output expansion; training would need to rise 62% to match a 30% retention effect (Fig. 9). A 10% retention effect gives 16 576, 338 below training. The threshold is conditional arithmetic, not an empirical policy estimate.

### Specification sensitivity

φ is the key specification (Table 7). At φ = 0, baseline 15 625; remuneration/training/return 16 671/16 698/16 060; threshold 30.8%. At φ = 1, baseline 16 019; 19 504/17 320/17 131; threshold 9.6%. Combined is above training across φ = 0–1; remuneration only for φ ≥ 0.25.

At lag 3/7 years, training is 17 239/16 535 and combined 19 229/19 033; the threshold is 19.3/9.2%. Age shapes shift the baseline to 14 961–16 570 and combined to 18 586–19 523. Retirement −2/+2 shifts baseline to 15 986/15 345 and combined to 18 909/19 169; mortality effects are small (Table S10).

Conservative effects confirm the caveat (Table 8): 10% remuneration 16 576, 5% career 16 198, 1.35× return 16 238, all below training (16 914); only combined 20% + 1.35× remains above, at 17 701.

### Structural uncertainty

With post-entry emigration rising 3% per year, the baseline reaches 14 461 and combined 18 315 (Fig. 3B, Fig. 8A). With both margins rising 3%, the baseline falls to 13 184 and combined reaches 17 519 (Fig. 3C, Fig. 8B). At 5%/7% both, baseline 10 917/8 216 and combined 16 105/14 364. Combined remains above business as usual, but the level depends on which margin is trended; the “collapse” narrative requires the stronger both-margin assumption.

### Sensitivity

The 2040 workforce is most strongly associated with future emigration intensity (PRCC −0.81), initial stock (−0.78), pipeline retention (0.55), training output (0.51), initial pool (−0.50), retirement age (−0.35), return rate (−0.30), age profile (0.28), diaspora attrition (−0.25) and φ (0.17) (Fig. 6). Marginal Spearman correlations are smaller; the calibration ridge links higher retention or training output to higher emigration. PRCCs are conditional on the priors and calibration design, not causal effects; bootstrap intervals are in Table S16.

### Age structure

Under business as usual, the share aged 55–64 rises from 20.7% in 2024 to 26.2% in 2040, and the share aged 45–54 falls from 34.0% to 26.0% (Fig. 7). Combined produces a younger workforce (37.4% aged 35–44 vs 33.9%).

### Illustrative costs

Costs are exploratory and not commensurable (Table 6; Fig. S2). Remuneration is a fiscal transfer of TND 2.18 billion over 2026–2040 (TND 124 176 per additional physician-year). Combined involves TND 2.63 billion in transfers and TND 18 million in resource costs. Career, return and training cost TND 83 443, 5 346 and 299 443 per additional physician-year. Categories are not ranked; this is not an economic evaluation.


## Discussion

### Principal findings

Four findings. First, the emigration level is not identified: 262–1 017 under φ = 0.50, or 502–1 540 if all non-entry is emigration. The annualised 374 proxy lies inside the central range; press estimates (1 300–1 450) lie near the φ = 1 upper bound, not the central range. Second, the baseline is a plateau: about 500 more physicians over 16 years, falling density, and an age reconstruction that shifts 2040 by about 1 600. Third, under the central assumptions combined and remuneration exceed 30% graduate-output expansion, but the threshold is 14.5%; conservative 10% remuneration, 5% career and 1.35× return effects fall below the expansion. Fourth, return alone is smaller; accounting changes the advantage only from 868 to 828, and the career/expansion/return ranking is unstable.

### Interpretation

Under the central assumptions, reducing international emigration yields earlier and larger gains than 30% graduate output, because graduates enter after the lag. Size and ranking depend on φ, effects and age structure. A 30% expansion increases non-entry by 30%, half assumed emigration. Return is smaller because only international emigrants enter the pool and attrition applies. Hungarian evidence that more than half return [21] suggests attrition may be pessimistic, but return is often temporary and many move to domestic non-clinical jobs.

A 10% wage increase in Ghana reduced attrition by about 12.5% relative [19]. If that relative effect transferred to international emigration, a 30% real increase would correspond to about a one-third reduction, our illustrative remuneration effect. This is an assumption, not an estimate: the Ghanaian outcome is payroll attrition, wage gaps remain large, and non-wage drivers are prominent in Tunisian surveys [22–24]. The conservative 10% effect is below the expansion, so the policy conclusion depends on effect size.

Slow growth is not stability: the baseline assumes about 1 300 graduates, 55% entry, φ = 0.50 and constant emigration. The 2020–2021 discontinuity, uncertain output, the age reconstruction and possible escalation imply that the true path could be lower or higher; calibrating to 2019 or 2022 gives 2040 baselines of 16 032 and 15 247. At 3% annual growth in post-entry emigration, the workforce falls 9% below the baseline by 2040; if both margins rise, it falls 16% below it. This is a major structural assumption.

### What the model can and cannot establish

It can establish the arithmetic of the stock under explicit assumptions, compare policy consequences, show which parameters matter, and demonstrate that published combinations are inconsistent. It cannot establish the true emigration level, causal policy effects, demand, specialty or regional shortages, or quality of care, and it cannot validate its projections against future data. The historical comparison, destination screen and calibration checks are consistency checks, not validation.

### Implications for data and measurement

Tunisia needs an annual, cohort-consistent account distinguishing registered, practising, entering, non-entering and emigrated physicians. Registration data illustrate the gain: 2 073 new CNOM inscriptions in 2021–2022 (about 1 036 per year) versus roughly 1 100–1 300 graduates [14]. If all were new entrants, retention would be nearer 0.8 than 0.55, shifting emigration from pre- to post-entry. Linked registration–training–payroll and destination data with consistent definitions would resolve part of the ambiguity. Until then, φ is a scenario parameter, not an estimate.

### Policy implications

Under the central assumptions, retention is a supply instrument: a 30% reduction in emigration adds more by 2040 than 30% graduate output. But the threshold is 14.5%, and a 10% remuneration effect is below training. The cost is mostly a fiscal transfer: a 30% public-sector increment costs about TND 2.18 billion over 2026–2040 on illustrative assumptions. Return is uncertain and smaller than training under the central φ; it requires qualification recognition, re-entry pathways and a diaspora register [43,44], and the pool is an accounting anchor, not a measured target. Training should be paired with retention, not substituted for it. These are conditional scenario results, not forecasts.

### Strengths and limitations

Strengths: transparency, open code and data, exact calibration, explicit separation of non-entry and emigration, parameter-status labelling, identifiability thresholds and a destination-stock screen, range-tested effects, separate escalation margins, true PRCCs with bootstrap intervals, break-even analysis, return-accounting sensitivity and specification sensitivity.

Limitations: aggregate data; φ unobserved; no specialty, sector or region; no demand or productivity; fixed emigration age profile and retirement hazards; a reconstructed 2008 age distribution that shifts 2040 by about 1 600 physicians; no temporary/permanent separation; a return-eligible pool that is an accounting anchor; return-accounting conventions that change the advantage modestly; a 2020–2021 discontinuity only partly addressed by 2019/2022 calibration; uncertain training output and completion; PRCCs conditional on priors and calibration; and illustrative costs. The model cannot distinguish reporting changes from real exits.


## Conclusions

Under the central model assumptions, reducing international emigration produces larger 15-year workforce gains than a 30% increase in graduate output. This comparison is conditional on the assumed share of pipeline non-entry attributable to international emigration, the assumed effects of retention interventions, the reconstructed age structure and the postgraduate lag. Combined retention and return remains above training across the tested φ range; remuneration does so within the Monte Carlo prior but not at φ = 0. The model does not identify Tunisia's true gross emigration flow. Its principal implication is the need for linked, cohort-consistent data that distinguish registration, practice, entry, domestic non-entry and international migration.

## List of abbreviations

BAU: business as usual; CNOM: Conseil National de l'Ordre des Médecins; INS: Institut National de la Statistique; OECD: Organisation for Economic Co-operation and Development; PRCC: partial rank correlation coefficient; RMSE: root mean squared error; SANDEM: Supply ANd DEMand model; SD: standard deviation; TND: Tunisian dinar; WHO: World Health Organization; WPP: World Population Prospects.

## Declarations

### Ethics approval and consent to participate

Not applicable. This study used aggregate, publicly available data and did not involve human participants.

### Consent for publication

Not applicable.

### Availability of data and materials

The datasets generated and analysed during the current study, together with all model code, tests and a one-command reproduction pipeline, are available in the GitHub repository at https://github.com/DrZAIER/physician-exodus (tag v2.1.2). The source data are publicly available from the sources listed in Table 1.

### Competing interests

The authors declare that they have no competing interests.

### Funding

This research received no specific grant from any funding agency in the public, commercial or not-for-profit sectors.

### Authors' contributions

FZ and MZ contributed equally to the conception and design of the study and to the interpretation of the results. FZ led the computational modelling, software development, data curation, formal analysis and visualisation. MZ contributed to the epidemiological and policy interpretation, literature synthesis, validation and critical revision of the manuscript. Both authors read and approved the final manuscript.

### Acknowledgements

Not applicable.

### Use of artificial intelligence

[To be completed by the authors: names of any generative AI tools used, their purpose (for example, code assistance or language editing) and the extent of use.]

### Authors' information

Firas Zaier is at the Faculty of Medicine of Tunis, University of Tunis El Manar. Mariem Zribi is at the Faculty of Medicine of Tunis, University of Tunis El Manar, and the National Health Institute, Republic of Tunisia Ministry of Public Health.

## References

1. World Health Organization. Global strategy on human resources for health: workforce 2030. Geneva: WHO; 2016.
2. Liu JX, Goryakin Y, Maeda A, Cheung T, Van Lerberghe W. Global health workforce labor market projections for 2030. Hum Resour Health. 2017;15:11.
3. Adovor E, Czaika M, Docquier F, Moullan Y. Medical brain drain: how many, where and why? J Health Econ. 2021;76:102409.
4. Arah OA. The metrics and correlates of physician migration from Africa. BMC Public Health. 2007;7:83.
5. Clemens M, Pettersson G. New data on African health professionals abroad. Hum Resour Health. 2008;6:1.
6. Mullan F. The metrics of the physician brain drain. N Engl J Med. 2005;353:1810–8.
7. Duvivier RJ, Burch VC, Boulet JR. A comparison of physician emigration from Africa to the United States of America between 2005 and 2015. Hum Resour Health. 2017;15:41.
8. OECD. Health at a Glance 2025. Paris: OECD Publishing; 2025.
9. La Presse de Tunisie. Facultés de médecine: le nombre d'étudiants augmenté de 30% pour combler le déficit médical. 7 Jul 2025. https://www.lapresse.tn/2025/07/07/facultes-de-medecine-le-nombre-detudiants-augmente-de-30-pour-combler-le-deficit-medical. Accessed 23 Nov 2026.
10. Conseil National de l'Ordre des Médecins. Atlas de la démographie médicale en France: situation au 1er janvier 2023. Paris: CNOM; 2023.
11. Institut Tunisien des Études Stratégiques. La migration des professionnels de santé: défis pour le système de santé tunisien. Tunis: ITES; 2024. https://www.admin.ites.tn/api/uploads/66156d8f285bb65f10309d2d_0.pdf. Accessed 23 Nov 2026.
12. La Presse de Tunisie. Exode des médecins: près de 1 450 médecins ont fui la Tunisie en 2024. 7 Jan 2025. https://www.lapresse.tn/2025/01/07/exode-des-medecins-pres-de-1-450-medecins-ont-fui-la-tunisie-en-2024. Accessed 23 Nov 2026.
13. Tunisie Numérique. Tunisie – Exode des compétences: 1 325 médecins ont quitté le pays en 2023. 20 Mar 2024. https://www.tunisienumerique.com/tunisie-exode-des-competences-1325-medecins-ont-quitte-le-pays-en-2023. Accessed 23 Nov 2026.
14. Conseil National de l'Ordre des Médecins de Tunisie. Rapport moral 2021–2022. Tunis: CNOM; 2022. https://www.ordremedecins-centre.org.tn/fileadmin/contenu/Publications/Rapports_CNOM/Rapport_2021-2022.pdf. Accessed 23 Nov 2026.
15. Conseil National de l'Ordre des Médecins de Tunisie. Tableau de l'Ordre. https://ordremedecins.tn. Accessed 23 Nov 2026.
16. Institut National de la Statistique, Ministère de la Santé. Personnel médical. https://ins.tn. Accessed 23 Nov 2026.
17. Ministère de la Santé. Carte sanitaire 2022–2023: synthèse. Tunis: Direction des études et de la planification; 2024. https://santetunisie.rns.tn/images/Synthese-carte-sanitaire2023.pdf. Accessed 23 Nov 2026.
18. La Presse de Tunisie. 975 médecins ont préparé un dossier de départ en 2021. 10 Feb 2022. https://www.lapresse.tn/2022/02/10/975-medecins-ont-prepare-un-dossier-de-depart-en-2021-de-limpossibilite-de-reformer. Accessed 23 Nov 2026.
19. Antwi J, Phillips DC. Wages and health worker retention: evidence from public sector wage reforms in Ghana. J Dev Econ. 2013;102:101–15.
20. Okeke EN. Do higher salaries lower physician migration? Health Policy Plan. 2014;29(5):603–14.
21. Varga J. Out-migration and attrition of physicians and dentists before and after EU accession (2003 and 2011): the case of Hungary. Eur J Health Econ. 2017;18:1079–93.
22. Ajmi M, Kahloul M, Kacem I, Chouchane A, Ben Mansour S, Slama Y, et al. Immigration projects among young doctors in Tunisia: prevalence, destinations and causes. Eur Psychiatry. 2022;65(Suppl 1):S633–4.
23. Tabib F, Guermazi F, Zouari A, Ben Abdallah M, Hentati S, Baati I, et al. Emigration intentionality among Tunisian interns and residents in medicine. Eur Psychiatry. 2022;65(Suppl 1):S633.
24. Haouari W, Omri S, Labyadh A, Feki R, Gassara I, Charfi N, et al. Factors driving the emigration intentions of young Tunisian medical professionals. Eur Psychiatry. 2024;67(Suppl 1):S829–30.
25. Bernini A, Icardi R, Natale F, Nedee A. Supply AND DEMand model for the healthcare workforce in the EU27: data sources and model structure. Luxembourg: Publications Office of the European Union; 2024.
26. Bernini A, Icardi R, Natale F, Nedee A. Healthcare workforce demand and supply in the EU27. Ispra: Joint Research Centre; 2024.
27. Lopes MA, Almeida ÁS, Almada-Lobo B. Forecasting the medical workforce: a stochastic agent-based simulation approach. Health Care Manag Sci. 2018;21(1):52–75.
28. Lee JT, Crettenden I, Tran M, Miller D, Cormack M, Cahill M, et al. Methods for health workforce projection model: systematic review and recommended good practice reporting guideline. Hum Resour Health. 2024;22:25.
29. World Health Organization. Models and tools for health workforce planning and projections. Geneva: WHO; 2010.
30. Roberfroid D, Leonard C, Stordeur S. Physician supply forecast: better than peering in a crystal ball? Hum Resour Health. 2009;7:10.
31. Ono T, Lafortune G, Schoenstein M. Health workforce planning in OECD countries: a review of 26 projection models from 18 countries. OECD Health Working Papers No. 62. Paris: OECD; 2013.
32. Dussault G, Franceschini MC. Not enough there, too many here: understanding geographical imbalances in the distribution of the health workforce. Hum Resour Health. 2006;4:12.
33. Aluttis C, Bishaw T, Frank MW. The workforce for health in a globalized context – global shortages and international migration. Glob Health Action. 2014;7:23611.
34. Crettenden I, Poz MD, Buchan J. Right time, right place: improving access to health service through effective retention and distribution of health workers. Hum Resour Health. 2013;11:60.
35. Cometto G, Scheffler R, Liu J, Maeda A, Tomblin Murphy G, Tani K, et al. Health workforce requirements for universal health coverage and the Sustainable Development Goals. Hum Resour Health. 2016;14(Suppl 1):46.
36. Scheffler RM, Herbst CH, Lemiere C, Campbell J. Health labor market analyses in low- and middle-income countries: an evidence-based approach. Washington DC: World Bank; 2016.
37. Zehnati A. L'émigration des médecins, en particulier vers la France, et la desserte médicale au Maghreb. Belgeo. 2024;(1). doi:10.4000/12ihd.
38. Institut National de la Statistique. Recensement Général de la Population et de l'Habitat 2024: bilan démographique. Tunis: INS; 2025.
39. United Nations. World Population Prospects 2024. New York: UN; 2024. https://population.un.org/wpp/. Accessed 23 Nov 2026.
40. Conseil National de l'Ordre des Médecins de Tunisie. Rapport moral 2007–2008. Tunis: CNOM; 2008. https://www.ordremedecins-centre.org.tn/fileadmin/contenu/Publications/Rapports_CNOM/Rapport_2007-2008.pdf. Accessed 23 Nov 2026.
41. World Health Organization. Global Health Workforce Statistics. https://www.who.int/data/gho/data/themes/topics/health-workforce. Accessed 23 Nov 2026.
42. OECD. Database on Immigrants in OECD Countries (DIOC). https://www.oecd.org/els/mig/dioc.htm. Accessed 23 Nov 2026.
43. Frehywot S, Mullan F, Payne PW, Ross H. Compulsory service programmes for recruiting health workers in remote and rural areas: do they work? Bull World Health Organ. 2010;88:364–70.
44. Barnighausen T, Bloom DE. Financial incentives for return of service in underserved areas: a systematic review. BMC Health Serv Res. 2009;9:86.

## Tables

### Table 1. Data sources and definitions

| Quantity | Source | Period | Definition and limitations |
|---|---|---|---|
| Physicians in active practice | INS / Ministry of Health [16]; carte sanitaire [17] | 2017–2024 | Public-sector physicians plus private practitioners; excludes most residents; 2020 public count affected by an unresolved reporting or reclassification discontinuity |
| Physicians in active practice, 2010 | WHO Global Health Workforce Statistics [41] | 2010 | Used only as an initial-condition anchor; different definition from the 2017–2024 series |
| Physicians registered with the CNOM | CNOM [14,15] | 2009–2026 | All inscriptions, including inactive, retired, administrative and deceased physicians; not a practising count |
| Medical graduates | Zehnati [37]; ministerial statements [9] | 2013–2025 | Medicine graduates only; 2013 and 2021 anchored; 2024 reconstructed; post-2024 assumptions tested |
| Emigration proxies | CNOM via ITES [11]; press [12,18] | 2011–2024 | Certificates of good conduct, removal requests, departure files and union/CNOM estimates; not comparable |
| Tunisian physicians in France | CNOM France [10] | 2010–2023 | Registered with the French Order; the 266 (2010) and 1 591 (2023) figures are not guaranteed to use the same counting method |
| Tunisian physicians in Germany | German medical statistics via ITES [11] | 2022 | Country-of-training/nationality definition; 881 |
| Tunisian-born physicians in OECD countries | OECD DIOC [42]; ITES [11] | 2010/11, 2015/16 | Country-of-birth estimate; about 4 000 in 2015/16; lower bound |
| Population | INS 2024 census [38]; UN WPP 2024 [39] | 2010–2040 | 2024 census 11 972 169; WPP rescaled to the census |

### Table 2. Key model parameters and evidence status

| Parameter | Central value | Range or distribution | Status |
|---|---|---|---|
| Practising physicians, 2024 | 15 315 | — | Observed |
| Medical graduates, 2013 / 2021 / 2024 | 987 / 1 128 / 1 305 | 987–1 900 (1 900 unverified) | Observed or reconstructed |
| Pipeline retention, σ | 0.55 | Beta (mean 0.55, SD 0.12), 0.30–0.80 | Estimated (weakly identified) |
| Share of non-entry that is emigration, φ | 0.50 | 0–1 (structural); Uniform 0.25–0.75 (MC) | Assumption (not observed) |
| Post-entry emigration, 2024, m | 317 | Calibrated per draw | Estimated (weakly identified) |
| Pipeline non-entry, 2024 | 491 | 240–1 396 (acceptable set) | Derived |
| International emigration, 2024 | 563 | 262–1 017 (acceptable, φ=0.50); 502–1 540 (φ=1) | Estimated (conditional) |
| Pre-entry share of international emigration, 2024 | 0.44 | Varies with σ, φ and training | Derived |
| Return rate, ρ | 0.020 | Beta (mean 0.02, SD 0.01), 0.005–0.050 | Assumption |
| Diaspora attrition, δ | 0.08 | Uniform 0.04–0.12 (MC); 0.02–0.15 (sensitivity) | Assumption |
| Return retention | 0.85 | Uniform 0.75–0.95 | Assumption |
| Postgraduate lag, L | 5 years | 3–7 years | Assumption |
| Retirement age | 60–70 | Shift ±2 years | Observed (legal) and assumed |
| Initial practising stock, 2008 | 12 600 | Normal (SD 400) | Indirect estimate |
| Initial return-eligible pool, 2008 | 4 000 | 2 000–8 000 | Indirect estimate |
| Population, 2024 | 11 972 169 | — | Observed |
| Population growth, 2024–2040 | 0.33%/yr | UN WPP medium | Projected |

### Table 3. Policy scenarios and central effect sizes

| Scenario | Post-entry emigration multiplier | Reduction in pre-entry international emigration | Return-rate multiplier | Training multiplier | Timing |
|---|---|---|---|---|---|
| Business as usual | 1.00 | 0 | 1.00 | 1.00 | — |
| Remuneration and working conditions | 0.70 | 30% | 1.00 | 1.00 | 2026, 3-year ramp |
| Professional development and careers | 0.85 | 15% | 1.00 | 1.00 | 2026, 3-year ramp |
| Return and diaspora reintegration | 1.00 | 0 | 1.75 | 1.00 | 2026, 3-year ramp |
| Hypothetical graduate-output expansion | 1.00 | 0 | 1.00 | 1.30 | Graduate cohorts from 2031; entrants after the lag; not the announced admissions policy |
| Combined retention and return | 0.65 | 35% | 1.75 | 1.00 | 2026, 3-year ramp |

Low and high effect sizes are in Additional file 1, Table S3. Effect sizes are assumptions, not estimated causal effects. The combined scenario is not the arithmetic sum of the single scenarios. Pre-entry reductions apply to the φ share of pipeline non-entry, not to all non-entry.

### Table 4. Modelled flow decomposition, selected years

| Year | Modelled practising stock | Entries | Pipeline non-entry | Pre-entry emigration | Domestic non-entry | Post-entry emigration | Returns | Retirements | Deaths | Net change | Density (per 1 000) | Return-eligible pool |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2017 | 14 965 | 534 | 437 | 218 | 218 | 190 | 72 | 205 | 23 | +188 | 1.32 | 3 837 |
| 2020 | 15 330 | 561 | 459 | 230 | 230 | 245 | 74 | 285 | 25 | +80 | 1.31 | 3 955 |
| 2024 | 15 315 | 600 | 491 | 245 | 245 | 317 | 81 | 367 | 26 | −29 | 1.28 | 4 312 |
| 2030 | 15 547 | 718 | 587 | 294 | 294 | 317 | 92 | 391 | 28 | +74 | 1.26 | 4 898 |
| 2035 | 15 808 | 718 | 587 | 294 | 294 | 317 | 99 | 410 | 30 | +59 | 1.27 | 5 244 |
| 2040 | 15 821 | 718 | 587 | 294 | 294 | 317 | 103 | 542 | 31 | −70 | 1.25 | 5 454 |

Values are rounded. The table reports model-simulated stocks, not the observed series: over-prediction is 73 in 2017 and 538 in 2020. All flows are model-implied. The 600 entries in 2024 are from the 2019 graduate cohort (1 091), not the 2024 cohort (1 305), which enters from 2029. Pipeline non-entry is split into pre-entry international emigration and domestic non-entry; only pre-entry emigration enters the return-eligible pool.

### Table 5. Projected workforce and policy outcomes in 2040

| Scenario | Workforce 2040 | Difference from BAU | Density 2040 (per 1 000) | Cumulative emigration 2026–2040 | Cumulative returns 2026–2040 | Physician-years vs BAU | Workforce 2040, MC median (90% interval) | Workforce 2040, post-entry +3%/yr | Workforce 2040, both margins +3%/yr |
|---|---|---|---|---|---|---|---|---|---|
| Business as usual | 15 821 | — | 1.25 | 9 079 | 1 429 | — | 15 830 (14 407–17 438) | 14 461 | 13 184 |
| Remuneration and conditions | 18 087 | +2 266 | 1.43 | 6 528 | 1 207 | 17 530 | 18 403 (16 522–20 838) | 17 125 | 16 222 |
| Career development | 16 953 | +1 132 | 1.34 | 7 804 | 1 318 | 8 762 | 17 115 (15 586–19 043) | 15 792 | 14 701 |
| Return migration | 16 689 | +868 | 1.32 | 9 079 | 2 318 | 6 656 | 16 749 (15 354–18 877) | 15 401 | 14 191 |
| Hypothetical graduate-output expansion | 16 914 | +1 092 | 1.34 | 9 520 | 1 448 | 3 269 | 16 980 (15 425–18 878) | 15 553 | 14 059 |
| Combined strategy | 19 162 | +3 341 | 1.52 | 6 103 | 1 885 | 26 085 | 19 577 (17 328–22 784) | 18 315 | 17 519 |

BAU: business as usual; MC: Monte Carlo. Deterministic values are from the central calibration; MC medians and intervals are from 4 000 draws with exact calibration. Physician-years are the undiscounted sum of annual differences from BAU over 2026–2040. The last two columns are deterministic structural scenarios, not probabilistic intervals. Costs are exploratory and reported separately in Table 6.

### Table 6. Exploratory fiscal and resource cost ratios, 2026–2040

| Scenario | Fiscal transfer (TND million) | Real resource cost (TND million) | Fiscal transfer per additional physician-year (TND) | Resource cost per additional physician-year (TND) | Additional physicians 2040 |
|---|---|---|---|---|---|
| Remuneration and conditions | 2 177 | 0 | 124 176 | 0 | 2 266 |
| Career development | 0 | 731 | 0 | 83 443 | 1 132 |
| Return migration | 0 | 36 | 0 | 5 346 | 868 |
| Hypothetical graduate-output expansion | 0 | 979 | 0 | 299 443 | 1 092 |
| Combined strategy | 2 626 | 18 | 100 658 | 700 | 3 341 |

Assumptions: 30% increment on an average public-sector compensation of TND 72 000 per physician-year; TND 3 000 per practising physician-year for career development; TND 250 000 per additional graduate; TND 40 000 per additional return migrant. Fiscal transfers are payments; resource costs are training, career-development and return-programme costs. Costs are undiscounted 2025 TND; ratios use physician-years relative to business as usual. They exclude infrastructure, demand-side costs and health gains. Fiscal transfers and real resource costs are not commensurable, are reported separately and are not summed. The combined package is costed as a 35% public-sector increment plus return-programme costs; no separate career-development line is added. Unit-cost ranges (0.5–2.0×) are shown in Fig. S2. This is not a cost-effectiveness, budget-impact or value-for-money analysis.

### Table 7. Specification sensitivity

| Specification | BAU 2040 | Remuneration 2040 | Return 2040 | Training 2040 | Combined 2040 | Retention match for 30% training |
|---|---|---|---|---|---|---|
| φ = 0 | 15 625 | 16 671 | 16 060 | 16 698 | 17 200 | 30.8% |
| φ = 0.25 | 15 723 | 17 379 | 16 375 | 16 806 | 18 181 | 19.6% |
| φ = 0.50 (central) | 15 821 | 18 087 | 16 689 | 16 914 | 19 162 | 14.5% |
| φ = 0.75 | 15 920 | 18 796 | 17 005 | 17 022 | 20 143 | 11.5% |
| φ = 1.00 | 16 019 | 19 504 | 17 320 | 17 131 | 21 125 | 9.6% |
| Lag 3 years | 15 705 | — | — | 17 239 | 19 229 | 19.3% |
| Lag 4 years | 15 771 | — | — | 17 084 | 19 204 | 16.9% |
| Lag 5 years (central) | 15 821 | — | — | 16 914 | 19 162 | 14.5% |
| Lag 6 years | 15 859 | — | — | 16 731 | 19 105 | 11.9% |
| Lag 7 years | 15 882 | — | — | 16 535 | 19 033 | 9.2% |
| Younger initial age shape | 14 961 | — | — | 16 053 | 18 586 | 13.3% |
| Older initial age shape | 16 570 | — | — | 17 663 | 19 523 | 16.4% |

φ is the share of pipeline non-entry assumed to be international emigration. The lag is the interval between graduation and entry into practice. The younger and older age shapes shift the reconstructed 2008 distribution by two years. All values are deterministic central-calibration projections; the retention match is the reduction in emigration needed to equal the 30% graduate-output expansion in 2040. At φ = 0, remuneration (16 671) is 27 below training (16 698); the remuneration advantage is therefore bounded to φ ≥ 0.25. The age-shape range (14 961–16 570) exceeds the central training effect. Retirement and mortality sensitivity is in Additional file 1, Table S10.

### Table 8. Conservative effects, expansion implementation and calibration endpoints

| Scenario or specification | Workforce 2040 | Difference from central BAU | Difference from 30% graduate-output expansion | Above 30% expansion? |
|---|---|---|---|---|
| Remuneration, 10% reduction | 16 576 | +755 | −338 | No |
| Career development, 5% reduction | 16 198 | +377 | −715 | No |
| Return migration, 1.35× | 16 238 | +417 | −676 | No |
| Combined, 20% reduction + 1.35× return | 17 701 | +1 880 | +787 | Yes |
| Graduate-output expansion, +30% (current) | 16 914 | +1 092 | 0 | — |
| Graduate-output expansion, +27% (90% completion) | 16 804 | +983 | −109 | No |
| Graduate-output expansion, +24% (80% completion) | 16 695 | +874 | −219 | No |
| Calibration endpoint 2019 (BAU) | 16 032 | +211 | — | — |
| Calibration endpoint 2022 (BAU) | 15 247 | −574 | — | — |

The conservative rows show that small retention and return effects do not beat the 30% graduate-output expansion. Only the constructed combined package does. The calibration endpoints show that the 2020–2021 discontinuity and endpoint choice shift the 2040 baseline by several hundred physicians. All values are deterministic central-calibration projections.

## Figure legends

**Fig. 1 Observed and modelled physician stock, Tunisia, 2010–2040.** Filled points are observed values from INS/Ministry of Health (2017–2024); the open point is the 2010 WHO estimate used only as an initial-condition anchor. The solid line is the retrospective fit (2008–2024); the dashed line is the baseline projection; the shaded area is the 90% simulation interval from 4 000 Monte Carlo draws. The vertical dotted line marks 2024, the calibration endpoint.

**Fig. 2 Identifiability of emigration and the return-eligible pool.** (A) Root mean squared error across pipeline retention (σ) and the training-output multiplier, with the post-entry flow recalibrated at each point. White cells cannot reproduce the 2024 stock even with zero post-entry emigration; the dashed contour is the acceptable-fit threshold (RMSE 302); the star is the best fit and the circle the central calibration. (B) Implied international emigration in 2024 under φ = 0.50. (C) Upper bound if all pipeline non-entry were international emigration (φ = 1). (D) Implied return-eligible pool in 2024; dashed lines mark 4 000 (OECD country-of-birth lower bound) and 10 000. The grid is a two-dimensional slice conditional on the other parameters.

**Fig. 3 Policy scenarios under constant and rising emigration intensity.** (A) Constant emigration intensity; the shaded area is the baseline 90% simulation interval. (B) Post-entry emigration intensity rising 3% per year. (C) Both pre-entry international and post-entry margins rising 3% per year. Retention and return scenarios phase in from 2026; the graduate-output expansion affects graduate cohorts from 2031 and entrants after the postgraduate lag.

**Fig. 4 Workforce, emigration and retention benefit by scenario.** (A) Difference from business as usual in 2040; error bars show low and high scenario effect sizes. (B) Cumulative emigration 2026–2040; the dashed line is business as usual. (C) Physician-years retained relative to business as usual; error bars show low and high effect sizes. Values are deterministic central-calibration estimates. Cost ratios are exploratory and shown separately in Fig. S2.

**Fig. 5 Physician density, 2015–2040.** Density is physicians in practice per 1 000 population, using the 2024 census and UN World Population Prospects 2024 medium-variant projections. The vertical dotted line marks the start of policy phase-in in 2026. The dip around 2024–2026 reflects population growth while the stock is flat.

**Fig. 6 Sensitivity of the 2040 workforce.** (A) One-at-a-time tornado: change from the central calibration when each parameter is set to its 10th (blue) or 90th (red) percentile, with the emigration flow recalibrated each time. The calibrated emigration flow is omitted because its structural effect would compress the scale; it is reported in Additional file 1. (B) True partial rank correlations (dark) controlling for all other parameters, compared with marginal Spearman correlations (orange). The conditional emigration effect is negative; marginal associations can be positive because of the calibration ridge.

**Fig. 7 Age structure of the practising workforce, 2024 and 2040.** Bars show the percentage of practising physicians in each age group under business as usual and under the combined strategy. Percentages may not sum to 100 because of rounding; the 65+ group is small.

**Fig. 8 Structural sensitivity to future emigration intensity.** (A) The trend applies to post-entry emigration only. (B) The trend applies to both pre-entry international and post-entry emigration. Lines show constant intensity and annual growth of 3%, 5% or 7% after 2024. The dotted line is the 2024 stock. The two panels are different assumptions, not uncertainty intervals.

**Fig. 9 Break-even between retention and graduate-output expansion.** Iso-lines show the 2040 workforce over reductions in emigration (x-axis) and graduate-output expansion (y-axis). Markers show +30% graduate output only, retention −30% only, and the expansion needed to match a 30% retention effect (62%). The vertical dashed line is the retention reduction that matches a 30% expansion (14.5%). The grid is deterministic and conditional on the central calibration.

**Fig. S1 Model flow diagram.** Pipeline non-entry is split into pre-entry international emigration and domestic non-entry. Only international emigration enters the return-eligible pool. Return attempts occur at rate ρD; 85% are successful and 15% re-emigrate. Under the central recycling assumption, re-emigrants rejoin the pool immediately; the no-recycling sensitivity removes them permanently. The diagram is illustrative, not to scale.

**Fig. S2 Exploratory fiscal and resource cost ratios, 2026–2040.** (A) Fiscal transfers and (B) real resource costs per additional physician-year relative to business as usual; error bars show 0.5–2.0× unit-cost assumptions. The panels are separate, the bars are not stacked and no total is formed. Fiscal and resource costs are not commensurable; this is not a cost-effectiveness or budget-impact analysis.

## Additional files

**Additional file 1.** DOCX. Supplementary tables and reporting checklist. Contains model notation, the flow diagram, the emigration age profile, scenario effect-size ranges, parameter distributions, full scenario and uncertainty results, the identifiability grid, structural scenarios, the break-even grid, diaspora and graduate-output sensitivity, φ/lag/age/retirement sensitivity, cost assumptions, validation checks and the item-level 30-item reporting checklist.
