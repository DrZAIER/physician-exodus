# Retention, return or training? A stock-and-flow simulation of Tunisia's physician workforce under incomplete migration data

**Authors:** [Author 1]^1, [Author 2]^1, [Author 3]^2

**Affiliations:**
^1 [Department, Institution, City, Country]
^2 [Department, Institution, City, Country]

**Corresponding author:** [Name], [Department, Institution, City, Country]. Email: [email]

**Word count:** 4 000 (abstract and main text; excluding tables, figures, references and additional files)

**Tables:** 7 **Figures:** 9 **Additional files:** 1

---

## Abstract

**Background.** Tunisia trains more physicians than it retains, but the scale of emigration is contested: estimates range from a few hundred to about 1 400 departures a year, and registered, practising and emigrated physicians are routinely conflated. We quantified what aggregate workforce data can identify and compared retention, return migration and training policies over 15 years.

**Methods.** We built an annual, single-year-of-age stock-and-flow model of physicians in active practice in Tunisia, calibrated exactly to the 2024 practising stock. The model represents entry after a five-year postgraduate lag, emigration before and after entry, return migration from a return-eligible diaspora pool with attrition, retirement and mortality. We compared business as usual with remuneration and working conditions, career development, return migration, 30% training expansion and a combined strategy. We used 2 000 Monte Carlo draws, true partial rank correlations, structural escalation on one or both emigration margins, break-even analysis and illustrative costs.

**Results.** The stock was 15 315 in 2024 (1.28 per 1 000). The baseline reaches 16 019 by 2040 (90% interval 14 514–17 565; 1.26 per 1 000), a plateau, not growth. The observed stock path is consistent with 582–1 497 annual emigrants; a destination-stock check narrows this to 582–1 405. The combined strategy adds 5 106 physicians by 2040 (21 125; 39 692 physician-years); remuneration adds 3 485, career development 1 741, return migration 1 301 and training 1 112. A 9.6% reduction in emigration matches a 30% training expansion, whereas training would need to rise 94% to match a 30% retention effect. With post-entry emigration rising 3% a year, the baseline reaches 14 520 and the combined strategy 20 190; if both margins rise, 11 969 and 18 599. Illustrative cost per physician-year is TND 5 400 for return, 70 600 for combined, 84 500 for remuneration and 295 200 for training.

**Conclusions.** Retention dominates training within 15 years, but the advantage is a modest arithmetic threshold, and return alone is uncertain. The larger problem is measurement: cohort-consistent reporting is needed to distinguish registered, practising and emigrated physicians.

**Keywords:** health workforce; physician migration; brain drain; Tunisia; stock-and-flow model; health policy; uncertainty analysis

---

## Background

Health systems depend on the size, skills and distribution of their workforce. The World Health Organization estimates that the world will need substantially more health workers to reach universal health coverage and the Sustainable Development Goals, and that shortages are concentrated in low- and middle-income countries [1,2,35]. International migration is only one of several flows that shape a national workforce, but it is the most contested: sending countries lose training investments and service capacity, while destination countries gain ready-trained staff [3,4,33]; distribution across regions and sectors is a separate policy problem [32,34].

Measuring those flows is harder than measuring the stock. Destination-country registers capture physicians who are registered abroad, but not those who are unregistered, in non-OECD destinations, or in temporary or circular movement; source-country registers capture inscriptions, not active practice [4–7,42]. Studies that compare stocks across countries therefore produce different totals depending on the definition: country of birth, country of training, nationality, registration, or active practice [5–7]. The same problem appears within countries when registration, payroll and survey counts are used interchangeably.

Tunisia illustrates both the policy urgency and the measurement problem. Four public medical faculties produce roughly 1 100 physicians a year, and the government announced a 30% increase in admissions in 2025 [9]. Tunisian-trained physicians are a large and growing group in France (1 591 registered in 2023, up from 266 in 2010) [10] and Germany (881 in 2022) [11]. The medical council and medical unions describe an exodus [11–13]. The Tunisian Order of Physicians (Conseil National de l'Ordre des Médecins, CNOM) reported 27 935 registered physicians at the end of 2022 [14] and indexed 31 804 directory records in 2026 [15]. The Ministry of Health and the National Institute of Statistics (INS) report about 15 000 physicians in active practice [16,17]. The gap is not the diaspora: it includes retired, deceased, inactive and administrative physicians, and some physicians abroad who remain registered. Departure indicators range from 187 removal requests in the first half of 2023 [11] to 1 325 in 2023 [13] and about 1 400 in 2024 [12], with 975 departure files prepared in 2021 [18]. These indicators measure different things: intentions, administrative requests, certificates, and reported departures.

The drivers are similarly multi-dimensional. International evidence shows that migration responds to wages, working conditions, career opportunities, security, diasporic ties and destination-country immigration policy [3,4,19–21]. In Ghana, a public-sector wage reform that raised pay by about 10% reduced annual attrition among young health workers by about one percentage point from a mean of eight [19]. A related evaluation found that higher salaries reduced the stock of Ghanaian doctors abroad after six years [20]. These are important but narrow results: the Ghanaian outcome is attrition from the public payroll, not necessarily international emigration, and the effect sizes are uncertain. Return can be substantial: more than half of Hungarian physicians who left during 2003–2011 returned at some point [21], although the same evidence shows a large flow into domestic non-clinical jobs, which our model does not represent. Tunisian surveys report migration intentions of 38.5% in 2019 (182 young doctors in Sousse), 53.6% in 2022 (56 interns and residents recruited through social media) and 68% in 2024 [22–24]. These are small, non-representative samples, and the comparison is across samples, not a time series; intentions are not flows.

Workforce projection models organise this uncertainty. Cohort-component stock-and-flow models are standard, and the JRC SANDEM model is a recent example [25,26]. Health labour market analysis treats migration as one adjustment mechanism among several [36]. Agent-based models can represent individual decisions and heterogeneity; the Portuguese physician workforce model is the closest application [27]. All of these approaches need data that Tunisia lacks: age-specific migration rates, reliable annual flows, and a separation of temporary and permanent moves. Reviews emphasise that projections are conditional statements whose credibility depends on transparency, explicit assumptions and validation, not computational sophistication [28–31].

We therefore built a deliberately simple, age-structured stock-and-flow model to (i) integrate the available Tunisian evidence; (ii) compare retention, return-migration and training policies over 15 years; (iii) quantify parameter and structural uncertainty; (iv) identify what cannot be estimated from aggregate data; and (v) express the policy trade-off as a break-even threshold and an illustrative cost per physician-year. We do not claim that any simulated policy has a proven causal effect in Tunisia.

## Methods

### Design and reporting

We built an annual, single-year-of-age cohort-component model of physicians in active practice in Tunisia from 2008 to 2040, with 2017–2024 used for retrospective comparison and 2024 as the calibration endpoint. The model is supply-only. It follows the 30-item reporting guideline of Lee et al. [28] (Additional file 1) and was implemented in Python 3.14 with NumPy, pandas, SciPy and Matplotlib. Code, processed data and a one-command pipeline are in the repository. AI-assisted tools (OpenAI ChatGPT and OpenCode) supported code development, numerical checks and language editing; the authors reviewed all decisions and text.

### Definitions and data

We modelled **practising** physicians: public-sector physicians plus private practitioners in the national health map, calibrated to the INS/Ministry of Health series [16,17]. This is not the same as CNOM registration, country of birth, or country of training. Table 1 summarises the sources; Table 2 gives parameters and evidence status.

The practising stock rose from 14 892 in 2017 to 15 426 in 2019, fell to 14 792 in 2020 and reached 15 315 in 2024 [16]. The 2020 fall reflected a 725-physician drop in the public-sector count while the private sector grew by 91. This is consistent with a reporting or reclassification change, but we cannot distinguish that from a real exit; we calibrate to 2024 and report fit with and without 2020–2021.

Graduates were reconstructed from 987 in 2013 and 1 128 in 2021, with about 1.7% annual growth over that period [37]. The 2024 value is 1 305, implying 5.0% annual growth from 2021 to 2024. The baseline holds output at 1 305 after 2024; alternatives are continued 1.7% growth (1 709 by 2040) and a constant 1 900. The announced 30% expansion is a scenario applied to graduates from 2031. Population denominators use the 2024 census (11 972 169) and UN WPP 2024, rescaled to the census [38,39].

### Model structure

The model tracks practising physicians by single year of age, N_a(t), and a return-eligible diaspora pool, D(t). Each year:

**Entry.** A cohort graduating in year t−5 enters in year t: E(t) = G(t−5) × σ(t), where G is graduates and σ the share entering Tunisian practice. The remainder, X(t) = G(t−5) × [1 − σ(t)], is pre-entry emigration. Entrants are spread over ages 29–33. Because residents are not counted in the practising stock, emigration during residency and failure to enter practice are observationally equivalent; σ absorbs both.

**Emigration.** Post-entry emigration is a total annual flow M(t), allocated by a fixed relative age profile w_a: e_a(t) = min{M(t) w_a / Σ_b N_b(t) w_b, 0.35}, with M(t) = m(t) × Π(t). The profile peaks at 30–34 and declines after 35 (Additional file 1, Table S2); it is an assumption. A projection-only shock, ε, multiplies M after 2024 and represents uncertainty about future intensity without disturbing the 2024 calibration.

**Return.** R(t) = ρ(t) D(t), distributed over ages 33–50. The pool evolves as D(t+1) = D(t)[1 − ρ(t) − δ] + M(t) + X(t) + re-emigration, where δ captures death abroad, onward migration and permanent settlement. Return migrants remain in practice with probability 0.85; the remainder rejoin the pool. The pool is a return-eligible stock, not a diaspora estimate. With δ = 0.08 and ρ = 0.02, mean duration is about 10 years and eventual return probability about 20%; both are varied in sensitivity analysis.

**Retirement and mortality.** Hazards reflect Tunisian legal ages: 0 below 60, 0.20 at 60–61, 0.45 at 62, 0.35 at 63–64, 0.45 at 65–69, 1.00 at 70+. Mortality is 0.1% at 25–54, 0.4% at 55–64, 1.5% at 65–74 and 5% at 75+. Mortality is applied first, then retirement among survivors: N_{a+1}(t+1) = N_a(t)(1 − q_a)(1 − r_a)(1 − e_a). The 75+ group is open-ended.

**Initial conditions.** The 2008 age distribution came from the CNOM 2007–2008 report [40], scaled to 12 600 practising physicians (WHO 2010: 12 996 [41]). The initial return-eligible pool was 4 000, consistent with OECD country-of-birth estimates [42]. Sensitivity to both is reported.

### Calibration and identifiability

For each draw, m was solved so that the simulated 2024 stock equalled 15 315; the calibration error is below 0.2 physicians. The calibration identifies a ridge: higher σ requires higher m to reproduce the same stock. We mapped fit over σ = 0.30–0.80 and training multipliers 0.85–1.50, recalibrating m at each point. We defined an acceptable fit (RMSE ≤2% of mean observed stock, about 302) and a strict fit (RMSE ≤1.10 × best). We screened the implied 2024 pool against destination stocks, treating 4 000–10 000 as a plausible band allowing for non-OECD destinations and unregistered physicians.

### Scenarios

Retention and return scenarios start in 2026 and phase in over three years (Table 3): business as usual; remuneration and working conditions (30% reduction in pre- and post-entry emigration); career development (15% reduction); return migration (return rate 2.0% to 3.5%); training expansion (+30% graduates from 2031, entering from 2036); and combined retention and return (35% reduction plus a 3.5% return rate). The combined scenario is not the sum of the single scenarios. Effect sizes are assumptions; low and high values are in Additional file 1, Table S3.

### Uncertainty and sensitivity

We generated 2 000 draws from the priors in Additional file 1, Table S4. Key priors were σ Beta (mean 0.55, SD 0.12, 0.30–0.80), training multiplier lognormal (median 1.0, log-SD 0.20, 0.85–1.50), return rate Beta (mean 0.02, SD 0.01), and a projection-only emigration shock lognormal (median 1.0, log-SD 0.10); the remaining distributions are in Table S4. m was recalibrated exactly for each draw; all scenarios used the same draw. Intervals are 5th–95th percentiles.

Structural uncertainty was explored with post-entry emigration intensity rising 3%, 5% or 7% per year after 2024, and separately with both margins rising. One-at-a-time sensitivity varied each parameter from its 10th to its 90th percentile; true PRCCs were computed by rank-residualising the 2040 stock and each parameter on all other parameters. We also computed a break-even grid and a diaspora sensitivity over δ, the initial pool and ρ.

### Illustrative costs

We attached illustrative 2025 Tunisian dinar (TND) unit costs: a 30% increment on an assumed average public-sector compensation of TND 72 000 per physician-year; TND 3 000 per practising physician-year for career development; TND 250 000 per additional graduate; and TND 40 000 per additional return migrant. Costs are undiscounted, exclude infrastructure and demand-side costs, and treat wages as transfers.

## Results

### Retrospective fit and calibration

The model reproduced the 2024 stock exactly (calibration error 0.04 physicians) and tracked the 2017–2024 series with an RMSE of 277 physicians (1.8% of the mean stock) and a mean absolute percentage error of 1.4% (Fig. 1). The largest discrepancies were in 2020–2023, when the model over-predicted the observed stock by 234–527 physicians after the 2020 public-sector drop; excluding 2020–2021, the RMSE was 188, and the 2017–2019 RMSE was 120.

The central calibration implies 600 entries, 491 pre-entry emigrants, 349 post-entry emigrants, 117 returns, 367 retirements and 26 deaths in 2024, a net change of −25 (Table 4). Total emigration was about 841, with 59% before entry, above the administrative proxy (about 374) and below press estimates (1 300–1 450).

### What the stock path can identify

The fit surface is a ridge, not a point (Fig. 2). Across σ = 0.30–0.80 and training multipliers of 0.85–1.50, the RMSE ranges from 238 to 515. The best fit (σ = 0.38, multiplier 0.85) implies 582 emigrants in 2024; the central calibration implies 841. Under the acceptable fit threshold (RMSE ≤302), the implied range is 582–1 497 annual emigrants; under the strict threshold (RMSE ≤262), it is 582–1 450. A destination-stock check narrows the range to 582–1 405, because the higher-output combinations imply a return-eligible pool of 10 000 or more, about 2.5 times the OECD country-of-birth lower bound. The range is conditional on the other parameters and is not a confidence interval.

This is the central result. The stock path constrains net flow, not gross flow. A country that trains more and loses more can look like one that trains less and loses less. The model therefore does not estimate the true emigration level; it carries the identified range through the scenarios.

### Baseline projection

With constant emigration intensity, the stock would reach 16 019 in 2040 (90% interval 14 514–17 565; Fig. 1, Fig. 3A), after peaking at about 16 084 in 2038. Density would fall from 1.28 to 1.26 per 1 000 (1.15–1.39; Fig. 5), below the OECD average of 3.9 [8]. Cumulative emigration over 2026–2040 would be about 13 900, offset by about 2 100 returns. It is a plateau, not a collapse. It reflects about 1 300 graduates, 55% entry and constant emigration, with retirements rising from 367 to 542.

### Policy scenarios

All five policies produced higher stocks in 2040 than business as usual (Table 5, Fig. 3A, Fig. 4). The combined strategy performed best: 21 125 in 2040 (+5 106; +32%), or 39 692 physician-years. Remuneration added 3 485 (+22%; 26 866 physician-years); career development 1 741 (+11%; 13 427); return migration 1 301 (+8%; 9 910); and training expansion 1 112 (+7%; 3 316).

Combined ranked first in all 2 000 draws; training ranked last in 54% and return exceeded training in 55%.

Training expansion was slow and leaky: its effect appeared only after 2035, and it increased cumulative emigration (14 768 vs 13 887) because larger cohorts produce more pre-entry emigrants. The combined strategy reduced cumulative emigration to 9 330.

### Break-even

The policy ranking is largely arithmetic. A 9.6% reduction in emigration (applied to both margins) matches the 30% training expansion by 2040; conversely, training output would need to rise by 94% to match a 30% retention effect (Fig. 9). The ranking is robust to plausible effect sizes but is not an empirical discovery: a retention effect below about 10% would not beat the 30% training expansion within 15 years.

### Sensitivity

The 2040 workforce was most strongly associated with future emigration intensity (PRCC −0.84), initial stock (−0.79), training output (0.55), diaspora attrition (−0.50), pipeline retention (0.42) and retirement age (−0.41), followed by the emigration age profile (0.30), return rate (−0.17) and return retention (−0.03) (Fig. 6). Marginal Spearman correlations were smaller: the calibration ridge links higher retention or training output to higher emigration, so a marginal association can be positive when the conditional effect is negative. Conditional on the other parameters, higher future emigration lowers the 2040 workforce. Parameters that raise the historical stock require more emigration to reproduce 2024, so their conditional associations can be negative; this is an identifiability result.

### Age structure

Under business as usual, the share aged 55–64 rises from 20.8% in 2024 to 26.1% in 2040, and the share aged 45–54 falls from 34.2% to 26.6% (Fig. 7). The combined strategy produces a younger workforce (39.1% aged 35–44 vs 33.7%). These results depend on the reconstructed 2008 distribution and the assumed emigration age profile.

### Structural uncertainty

With post-entry emigration intensity rising 3% per year, the baseline reaches 14 520 in 2040 (1.15 per 1 000), and the combined strategy reaches 20 190 (Fig. 3B, Fig. 8A). With both pre- and post-entry margins rising 3% per year, the baseline falls to 11 969 (0.95 per 1 000) and the combined strategy reaches 18 599 (Fig. 3C, Fig. 8B). At 5% and 7% on both margins, the baseline falls to 8 563 and 6 034, while the combined strategy reaches 16 424 and 13 751. The combined strategy remains above business as usual in every case, but the absolute level depends heavily on which margin is trended. The "collapse" narrative requires the stronger both-margin assumption.

### Return and diaspora sensitivity

The central return-eligible pool is 6 234 in 2024, about 1.6 times the OECD country-of-birth lower bound, and 8 275 in 2040. Across δ = 0.02–0.15, initial pool 2 000–8 000 and ρ = 0.005–0.04, the 2024 pool ranges from 3 441 to 13 983 and the return scenario's 2040 advantage ranges from 210 to 4 755 physicians. The eventual return probability ranges from 3% to 67%. The central assumptions imply 20%, below the Hungarian evidence of more than 50% [21]; if that evidence applies, the return scenario would be larger but would require a larger pool or lower attrition. Return alone is therefore not a reliable substitute for retention.

### Training-output baselines

Continued 1.7% growth would raise the baseline to 16 907; constant 1 900 would raise it to 19 807 (Table 7). The ranking is unchanged.

### Illustrative costs

Illustrative cost per physician-year ranges from TND 5 400 for return migration to 295 200 for training (Table 6, Fig. 4D). These are orders of magnitude, not a fiscal appraisal.

## Discussion

### Principal findings

Four findings stand out. First, the level of emigration cannot be identified from aggregate data: the same stock path is consistent with 582–1 497 annual emigrants, or 582–1 405 after a destination-stock check. Second, the baseline is a plateau: the stock grows by about 700 physicians over 16 years while population grows faster, so density falls slightly. Third, retention and return outperform training within 15 years, but the advantage is a modest arithmetic threshold: a 9.6% reduction in emigration matches a 30% training expansion, and training would need to rise 94% to match a 30% retention effect. Fourth, the ranking is robust to parameter uncertainty but not to structural assumptions about which emigration margin rises; the "collapse" scenario requires both pre- and post-entry emigration to escalate.

### Interpretation

Retention dominates training because an emigrant is lost for the rest of their working life, while a new graduate takes at least five years to replace them and may also leave. The training pipeline is also leaky: a 30% expansion increases pre-entry emigration by about 30%, so a substantial share of the additional graduates never enters the Tunisian stock. The return scenario is smaller because the pool is modest once attrition is accounted for. Hungarian evidence that more than half return at some point [21] suggests our attrition assumption may be too pessimistic, but return is often temporary and many physicians move to domestic non-clinical jobs.

A 10% wage increase in Ghana reduced attrition by about 12.5% relative [19]. A 30% real increase might therefore reduce emigration by roughly a third, our remuneration effect size. But the Ghanaian outcome is payroll attrition, not international emigration; wage gaps remain large; and non-wage drivers are prominent in Tunisian surveys [22–24]. A broader package may be needed, and its effect is uncertain.

Slow growth is not stability: the baseline assumes about 1 300 graduates, 55% entry and constant emigration. The 2020–2021 discontinuity, uncertainty about recent output (1 305 vs 1 900) and possible escalation all imply that the true path could be lower. At 3% annual growth in post-entry emigration, the workforce falls 5% from 2024 by 2040; if both margins rise, it falls 22%. This is the most consequential structural assumption.

### What the model can and cannot establish

It can establish the arithmetic of the stock under explicit assumptions, compare policy consequences, show which parameters matter, and demonstrate that some published combinations are inconsistent. It cannot establish the true emigration level, causal policy effects, demand, specialty or regional shortages, or quality of care, and it cannot validate its projections against future data.

### Implications for data and measurement

Tunisia needs an annual, cohort-consistent account distinguishing registered, practising, entering and exiting physicians. Registration data illustrate the gain: 2 073 new CNOM inscriptions in 2021–2022 (about 1 036 per year) versus roughly 1 100–1 300 graduates [14]. If all were new entrants, pipeline retention would be nearer 0.8 than 0.55, shifting emigration from pre- to post-entry. The 2040 projection would change by only a few per cent, but the interpretation of when and why physicians leave would change substantially. Linked registration–training–payroll data, and destination-country data with a consistent definition, would resolve part of the ambiguity.

### Policy implications

Retention should be treated as a supply instrument: a 30% reduction in emigration adds more by 2040 than a 30% training expansion, and sooner. But the threshold is modest, and the cost is not trivial: a 30% public-sector pay increment costs about TND 2.3 billion over 2026–2040 on our illustrative assumptions, or TND 84 500 per additional physician-year. Return migration is potentially cheaper per physician-year but uncertain and dependent on the pool; it requires qualification recognition, re-entry pathways and a diaspora register [43,44]. Training expansion should be paired with retention, not substituted for it; it is necessary for the long run but slow and leaky.

### Strengths and limitations

Strengths: transparency, open code and data, exact calibration, explicit parameter status, an identifiability analysis with two thresholds and a destination-stock check, range-tested effects, separate escalation margins, true PRCCs, break-even analysis and illustrative costs.

Limitations: aggregate data; no specialty, sector or region; no demand or productivity; a fixed emigration age profile and retirement hazards; a reconstructed 2008 age distribution; no separation of temporary and permanent migration; a return-eligible pool that is not a diaspora estimate; a 2020–2021 discontinuity; uncertain training output; illustrative rather than audited costs; and no external validation.

## Conclusions

Tunisia's physician workforce is shaped more by retention and return than by training capacity within 15 years. A combined strategy would add substantially more physicians than a 30% training expansion and would remain effective if emigration rises, but the advantage is a modest arithmetic threshold and return alone is uncertain. Training is necessary for the long run but slow and leaky without retention. The fundamental constraint is data: the emigration level cannot be identified from the published stock series, and the debate uses indicators that measure different things. Cohort-consistent accounting is a precondition for credible planning.

## List of abbreviations

BAU: business as usual; CNOM: Conseil National de l'Ordre des Médecins; INS: Institut National de la Statistique; OECD: Organisation for Economic Co-operation and Development; PRCC: partial rank correlation coefficient; RMSE: root mean squared error; SANDEM: Supply ANd DEMand model; SD: standard deviation; TND: Tunisian dinar; WHO: World Health Organization; WPP: World Population Prospects.

## Declarations

### Ethics approval and consent to participate

Not applicable. This study used aggregate, publicly available data and did not involve human participants.

### Consent for publication

Not applicable.

### Availability of data and materials

The datasets generated and analysed during the current study, together with all model code, tests and a one-command reproduction pipeline, are available in the [repository name] repository, [persistent identifier and URL]. The source data are publicly available from the sources listed in Table 1.

### Competing interests

The authors declare that they have no competing interests.

### Funding

This research received no specific grant from any funding agency in the public, commercial or not-for-profit sectors.

### Authors' contributions

[Author 1] designed the study, developed the model, analysed the data and drafted the manuscript. [Author 2] contributed to data collection and interpretation. [Author 3] contributed to the policy analysis and revised the manuscript. All authors read and approved the final manuscript.

### Acknowledgements

Not applicable.

### Authors' information

[Optional: relevant qualifications, positions or background.]

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
| Physicians in active practice | INS / Ministry of Health [16]; carte sanitaire [17] | 2017–2024 | Public-sector physicians plus private practitioners; excludes most residents; 2020 public count affected by a reporting or reclassification change |
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
| Medical graduates, 2013 / 2021 / 2024 | 987 / 1 128 / 1 305 | 987–1 900 | Observed or reconstructed |
| Pipeline retention, σ | 0.55 | Beta (mean 0.55, SD 0.12), 0.30–0.80 | Estimated (weakly identified) |
| Post-entry emigration, 2024, m | 349 | Calibrated per draw | Estimated (weakly identified) |
| Total emigration, 2024 | 841 | 582–1 497 (acceptable); 582–1 405 (destination-consistent) | Estimated (conditional) |
| Pipeline non-entry share, 1−σ | 0.45 | 0.20–0.70 | Assumption (implied by σ) |
| Pre-entry share of total emigration, 2024 | 0.59 | Varies with σ and training output | Derived |
| Return rate, ρ | 0.020 | Beta (mean 0.02, SD 0.01), 0.005–0.050 | Assumption |
| Diaspora attrition, δ | 0.08 | Uniform, 0.04–0.15 | Assumption |
| Return retention | 0.85 | Uniform, 0.75–0.95 | Assumption |
| Retirement age | 60–70 | Shift ±1.5 years | Observed (legal) and assumed |
| Initial practising stock, 2008 | 12 600 | Normal (SD 400) | Indirect estimate |
| Initial return-eligible pool, 2008 | 4 000 | 2 000–8 000 | Indirect estimate |
| Population, 2024 | 11 972 169 | — | Observed |
| Population growth, 2024–2040 | 0.33%/yr | UN WPP medium | Projected |

### Table 3. Policy scenarios and central effect sizes

| Scenario | Post-entry emigration multiplier | Reduction in pre-entry emigration | Return-rate multiplier | Training multiplier | Timing |
|---|---|---|---|---|---|
| Business as usual | 1.00 | 0 | 1.00 | 1.00 | — |
| Remuneration and working conditions | 0.70 | 30% | 1.00 | 1.00 | 2026, 3-year ramp |
| Professional development and careers | 0.85 | 15% | 1.00 | 1.00 | 2026, 3-year ramp |
| Return and diaspora reintegration | 1.00 | 0 | 1.75 | 1.00 | 2026, 3-year ramp |
| Expanded training capacity | 1.00 | 0 | 1.00 | 1.30 | Graduates from 2031; entrants from 2036 |
| Combined retention and return | 0.65 | 35% | 1.75 | 1.00 | 2026, 3-year ramp |

Low and high effect sizes are in Additional file 1, Table S3. Effect sizes are assumptions, not estimated causal effects. The combined scenario is not the arithmetic sum of the single scenarios. Retention and return effects are applied to both pre- and post-entry emigration.

### Table 4. Modelled flow decomposition, selected years

| Year | Stock | Entries | Pre-entry emigration | Post-entry emigration | Returns | Retirements | Deaths | Net change | Density (per 1 000) | Return-eligible pool |
|---|---|---|---|---|---|---|---|---|---|---|
| 2017 | 14 928 | 534 | 437 | 210 | 97 | 204 | 23 | +194 | 1.31 | 5 186 |
| 2020 | 15 311 | 561 | 459 | 269 | 105 | 285 | 25 | +86 | 1.31 | 5 566 |
| 2024 | 15 315 | 600 | 491 | 349 | 117 | 367 | 26 | −25 | 1.28 | 6 234 |
| 2030 | 15 595 | 718 | 587 | 349 | 137 | 392 | 28 | +85 | 1.27 | 7 268 |
| 2035 | 15 921 | 718 | 587 | 349 | 148 | 414 | 30 | +73 | 1.27 | 7 896 |
| 2040 | 16 019 | 718 | 587 | 349 | 156 | 542 | 31 | −49 | 1.27 | 8 275 |

Values are rounded. The model is calibrated to the observed 2024 stock of 15 315; the 2024 net change is the difference from 2023. Deaths (23–31 per year) are included in the identity. Entries exclude pre-entry emigrants.

### Table 5. Projected workforce and policy outcomes in 2040

| Scenario | Workforce 2040 | Difference from BAU | Density 2040 (per 1 000) | Cumulative emigration 2026–2040 | Cumulative returns 2026–2040 | Physician-years vs BAU | Workforce 2040, MC median (90% interval) | Workforce 2040, post-entry +3%/yr | Workforce 2040, both margins +3%/yr | Cost per physician-year (TND) |
|---|---|---|---|---|---|---|---|---|---|---|
| Business as usual | 16 019 | — | 1.27 | 13 887 | 2 136 | — | 15 933 (14 514–17 565) | 14 520 | 11 969 | — |
| Remuneration and conditions | 19 504 | +3 485 | 1.54 | 9 981 | 1 796 | 26 866 | 19 755 (18 089–22 367) | 18 443 | 16 638 | 84 500 |
| Career development | 17 760 | +1 741 | 1.41 | 11 934 | 1 966 | 13 427 | 17 838 (16 405–19 839) | 16 479 | 14 300 | 55 800 |
| Return migration | 17 320 | +1 301 | 1.37 | 13 887 | 3 469 | 9 910 | 17 155 (15 622–19 790) | 15 901 | 13 483 | 5 400 |
| Training expansion | 17 131 | +1 112 | 1.36 | 14 768 | 2 176 | 3 316 | 17 087 (15 588–19 032) | 15 632 | 12 648 | 295 200 |
| Combined strategy | 21 125 | +5 106 | 1.67 | 9 330 | 2 807 | 39 692 | 21 454 (19 347–25 172) | 20 190 | 18 599 | 70 600 |

BAU: business as usual; MC: Monte Carlo; TND: Tunisian dinar. Deterministic values are from the central calibration; MC medians and intervals are from 2 000 draws with exact calibration. Physician-years are the undiscounted sum of annual differences from BAU over 2026–2040. The last three columns are deterministic structural or costing scenarios, not probabilistic intervals. Costs are illustrative; see Table 6.

### Table 6. Illustrative resource costs, 2026–2040

| Scenario | Total cost (TND million) | Cost per physician-year (TND) | Cost per physician-year, low unit costs | Cost per physician-year, high unit costs | Cost per additional physician in 2040 (TND) |
|---|---|---|---|---|---|
| Remuneration and conditions | 2 269 | 84 500 | 42 200 | 169 000 | 651 000 |
| Career development | 749 | 55 800 | 27 900 | 111 700 | 431 000 |
| Return migration | 53 | 5 400 | 2 700 | 10 800 | 41 000 |
| Training expansion | 979 | 295 200 | 147 600 | 590 300 | 880 000 |
| Combined strategy | 2 803 | 70 600 | 35 300 | 141 300 | 549 000 |

Assumptions: 30% increment on an average public-sector compensation of TND 72 000 per physician-year; TND 3 000 per practising physician-year for career development; TND 250 000 per additional graduate; TND 40 000 per additional return migrant. Costs are undiscounted 2025 TND and exclude infrastructure, demand-side costs and health gains. Wages are transfers, not resource costs; the training estimate is the most resource-like. Low and high columns multiply all unit costs by 0.5 and 2.0.

### Table 7. Robustness to graduate output and structural escalation

| Assumption | BAU 2040 | Training 2040 | Combined 2040 | Training physician-years | Combined physician-years |
|---|---|---|---|---|---|
| Baseline graduates, constant 1 305 | 16 019 | 17 131 | 21 125 | 3 316 | 39 692 |
| Continued 1.7% growth (1 709 by 2040) | 16 907 | 18 201 | 22 261 | 3 817 | 40 742 |
| Constant 1 900 graduates | 19 807 | 21 427 | 25 965 | 4 829 | 45 970 |
| Post-entry emigration +3%/yr | 14 520 | 15 632 | 20 190 | — | — |
| Both margins +3%/yr | 11 969 | 12 648 | 18 599 | — | — |
| Both margins +5%/yr | 8 563 | 8 851 | 16 424 | — | — |
| Both margins +7%/yr | 6 034 | 6 215 | 13 751 | — | — |

BAU: business as usual. The first three rows vary the post-2024 graduate path; the remaining rows apply a deterministic annual growth rate to emigration intensity after 2024, either to the post-entry margin only or to both the pre- and post-entry margins. All values are deterministic central-calibration projections.

## Figure legends

**Fig. 1 Observed and modelled physician stock, Tunisia, 2010–2040.** Filled points are observed values from INS/Ministry of Health (2017–2024); the open point is the 2010 WHO estimate used only as an initial-condition anchor. The solid line is the retrospective fit (2008–2024); the dashed line is the baseline projection; the shaded area is the 90% simulation interval from 2 000 Monte Carlo draws. The vertical dotted line marks 2024, the calibration endpoint.

**Fig. 2 Identifiability of the emigration level.** (A) Root mean squared error of the retrospective fit across pipeline retention (σ) and the training-output multiplier, with the post-entry emigration flow recalibrated at each point. White cells cannot reproduce the 2024 stock even with zero post-entry emigration. The dashed contour is the acceptable-fit threshold (RMSE 302); the star is the best fit and the circle is the central calibration. (B) Implied total emigration in 2024. (C) Implied return-eligible pool in 2024; dashed lines mark 4 000 (OECD country-of-birth lower bound) and 10 000. The grid is a two-dimensional slice conditional on the other parameters.

**Fig. 3 Policy scenarios under constant and rising emigration intensity.** (A) Constant emigration intensity; the shaded area is the baseline 90% simulation interval. (B) Post-entry emigration intensity rising 3% per year. (C) Both pre- and post-entry margins rising 3% per year. All retention and return scenarios are phased in from 2026; the training expansion affects graduates from 2031 and entrants from 2036.

**Fig. 4 Workforce, emigration, retention benefit and illustrative cost by scenario.** (A) Difference from business as usual in 2040; error bars show low and high scenario effect sizes. (B) Cumulative emigration 2026–2040; the dashed line is business as usual. (C) Physician-years retained relative to business as usual; error bars show low and high effect sizes. (D) Illustrative cost per additional physician-year; error bars show low and high unit costs. Values are deterministic central-calibration estimates.

**Fig. 5 Physician density, 2015–2040.** Density is physicians in practice per 1 000 population, using the 2024 census and UN World Population Prospects 2024 medium-variant projections. The vertical dotted line marks the start of policy phase-in in 2026. The dip around 2024–2026 reflects population growth while the stock is flat.

**Fig. 6 Sensitivity of the 2040 workforce.** (A) One-at-a-time tornado: change from the central calibration when each parameter is set to its 10th (blue) or 90th (red) percentile, with the emigration flow recalibrated each time. The calibrated emigration flow is omitted because its structural effect (+3 960/−7 594) would compress the scale; it is reported in Table 7 and Additional file 1. (B) True partial rank correlations (dark) controlling for all other parameters, compared with marginal Spearman correlations (orange). The conditional emigration effect is negative; the marginal positive association in the earlier analysis was a calibration-ridge artefact.

**Fig. 7 Age structure of the practising workforce, 2024 and 2040.** Bars show the percentage of practising physicians in each age group under business as usual and under the combined strategy. Percentages may not sum to 100 because of rounding; the 65+ group is small.

**Fig. 8 Structural sensitivity to future emigration intensity.** (A) The trend applies to post-entry emigration only. (B) The trend applies to both pre- and post-entry emigration. Lines show constant intensity and annual growth of 3%, 5% or 7% after 2024. The dotted line is the 2024 stock. The two panels are different assumptions, not uncertainty intervals.

**Fig. 9 Break-even between retention and training.** Iso-lines show the 2040 workforce over reductions in emigration (x-axis) and training expansion (y-axis). Markers show training +30% only, retention −30% only, and the training expansion needed to match a 30% retention effect (94%). The vertical dashed line is the retention reduction that matches a 30% training expansion (9.6%). The grid is deterministic and conditional on the central calibration.

## Additional files

**Additional file 1.** DOCX. Supplementary tables and reporting checklist. Contains model notation, the flow diagram, the emigration age profile, scenario effect-size ranges, parameter distributions, full scenario and uncertainty results, the identifiability grid, structural scenarios, the break-even grid, diaspora and graduate-output sensitivity, cost assumptions, validation checks and the item-level 30-item reporting checklist.
