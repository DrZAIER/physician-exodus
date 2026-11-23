# Retention, return or training? A stock-and-flow simulation of Tunisia's physician workforce under incomplete migration data

**Authors:** [Author names and affiliations to be completed]

**Corresponding author:** [Name, address, email]

**Running title:** Modelling Tunisia's physician workforce

**Keywords:** health workforce; physician migration; brain drain; Tunisia; stock-and-flow model; health policy; uncertainty analysis

---

## Abstract

**Background.** Tunisia trains more physicians than it retains, yet the scale of emigration is unknown: estimates of annual departures range from a few hundred to more than 1,400, and registered, practising and emigrated physicians are routinely conflated. We modelled how retention, return-migration and training policies could affect the practising workforce over 15 years, and what can and cannot be established when migration flows are poorly observed.

**Methods.** We built an annual, single-year-of-age cohort-component model of physicians in active practice in Tunisia, calibrated to the national practising stock for 2017–2024. The model represents entry of graduates after a five-year postgraduate lag, emigration before and after entry, return migration, retirement and mortality. We compared business as usual with five scenarios: remuneration and working conditions; career development; return migration; 30% training expansion; and a combined retention and return strategy. Policy effects were explicit, range-tested assumptions, not estimated causal effects. We used 2,000 Monte Carlo draws, alternative effect sizes, and structural scenarios with rising emigration.

**Results.** The practising stock was 15,315 in 2024 (1.28 per 1,000). Under the central baseline it would reach 17,990 by 2040 (90% interval 16,340–19,970; 1.42 per 1,000). A combined retention and return strategy would add 7,350 physicians by 2040 (25,340 in total) and 57,900 physician-years. Remuneration alone would add 3,730; return migration 3,450; career development 1,860; and training expansion only 1,120, because graduates enter after 2031. If emigration intensity rose 3% per year, the baseline would fall to 13,570 while the combined strategy would still reach 22,660. The observed stock path was nearly equally consistent with 675 to 1,839 annual emigrants; the emigration level is not identifiable from aggregate data.

**Conclusions.** Within 15 years, retaining practising physicians and attracting return migrants outperforms training expansion, which is delayed by the training pipeline and partly offset by emigration of new graduates. A combined strategy is robust to plausible escalation of emigration. The results are conditional on assumed effect sizes and mainly structure policy choices and expose data gaps. Tunisia needs cohort-consistent reporting that distinguishes registered, practising and emigrated physicians.

---

## Background

Tunisia has expanded medical training rapidly over the past decade. Four public medical faculties train roughly 1,100 physicians a year, and the government announced a further 30% increase in admissions in 2025 [1]. Yet the country also has a prominent physician emigration problem. Tunisian-trained physicians are the second-largest group of non-EU-trained doctors in France, after Algerians, and their number rose from 266 in 2010 to 1,591 in 2023 [2]. Germany recorded 881 Tunisian physicians at the end of 2022, 7.8% more than the previous year [3]. The national medical council and medical unions have described the situation as an exodus [8,9].

The policy debate, however, rests on numbers that are not comparable. The Tunisian Order of Physicians (Conseil National de l'Ordre des Médecins, CNOM) reported 27,935 registered physicians at the end of 2022 [4], and its public directory indexed 31,804 records in 2026 [5]. The Ministry of Health and the National Institute of Statistics (INS), by contrast, report about 15,000 physicians in active practice in the public and private sectors [6,7]. The difference is not a measure of the diaspora: it includes retired, deceased, inactive and administrative physicians, and some physicians working abroad who remain on the register. Meanwhile, indicators of departure range from 187 removal requests in the first half of 2023 [3] to 1,325 in 2023 and about 1,400 in 2024 [8,9]. These figures use different definitions, different reference populations and different methods of collection.

This definitional confusion has consequences. It makes the workforce crisis appear either catastrophic or exaggerated, depending on which number is cited. It complicates international comparisons. And it prevents a serious assessment of which policies — higher pay, better working conditions, career reform, diaspora engagement or expanded training — are most likely to change the trajectory of the workforce.

The international literature offers general guidance but not a Tunisian answer. Physician migration responds to wage differentials, working conditions, career opportunities, political stability and diasporic networks, and is shaped by destination-country immigration policy [10,11]. The causal evidence on retention is thin but consistent: in Ghana, a 10% public-sector wage increase reduced annual attrition among young health workers by about one percentage point, from a mean of eight percentage points [12], and a related evaluation found that the reform reduced the stock of Ghanaian doctors abroad by about 10% after six years [13]. Return migration can be substantial; in Hungary, more than half of the physicians who left during 2003–2011 returned at some point [14]. But the magnitude of these effects in Tunisia is unknown, and surveys of migration intention — 38.5% in Sousse in 2019, 53.6% among interns and residents in 2022, and 68% among residents in 2024 [15–17] — do not translate directly into flows.

Health workforce projection models provide a way to organise this uncertainty. Cohort-component stock-and-flow models are the standard tool, and the JRC's SANDEM model is a recent, well documented example for the European Union [18,19]. Agent-based models can represent individual decisions and heterogeneity; the Portuguese physician workforce model is the most relevant application [20]. Both approaches, however, require data that Tunisia does not have: age-specific migration rates, reliable annual flows, and a clear separation between temporary and permanent moves. Reviews of workforce projection methods emphasise that projections are conditional statements whose credibility depends on transparency about structure, data and assumptions, not on computational sophistication [21,22].

We therefore developed a deliberately simple, age-structured stock-and-flow model of the Tunisian physician workforce. Our objectives were: (i) to integrate the available Tunisian evidence into a transparent and reproducible projection framework; (ii) to examine how alternative retention, return-migration and training policies could affect the practising workforce over 15 years; (iii) to quantify the relative importance of parameter and structural uncertainty; and (iv) to identify which quantities cannot be estimated from currently available data. We were not trying to predict the future, and we do not claim that any of the simulated policies has a proven causal effect in Tunisia. The model is a tool for comparing plausible consequences and for exposing the data that would be needed to do better.

## Methods

### Study design and reporting

We developed a deterministic, annual, single-year-of-age cohort-component model of the supply of physicians in active practice in Tunisia, running from 2008 to 2040. The historical period 2017–2024 was used for retrospective calibration; the projection begins in 2024. The model is supply-only and does not include demand, vacancies, wages, specialty choice, public/private allocation or regional distribution.

The study follows the 30-item good practice reporting guideline for health workforce projection models proposed by Lee et al. [21]; the mapping is provided in Additional file 1. The model was implemented in Python 3.14 with NumPy, pandas, SciPy and Matplotlib. All code, data and parameter files are publicly available (see Declarations).

### Definitions and data

We modelled **physicians in active practice in Tunisia**, defined as public-sector physicians plus private practitioners recorded in the national health map, and calibrated to the INS/Ministry of Health series [6,7]. This is not the same as physicians registered with the CNOM, physicians born in Tunisia, or physicians trained in Tunisia. Table 1 summarises the data sources and their definitions.

The practising stock rose from 14,892 in 2017 to 15,426 in 2019, fell to 14,792 in 2020, and recovered to 15,315 in 2024 [6]. The 2020 fall was driven by a 725-physician drop in the public-sector count, which is too large to be a real retirement or emigration effect and probably reflects a change in establishment reporting. We retained the observed series but report goodness of fit with and without 2020–2021.

Training output was reconstructed from published estimates: 987 medical graduates in 2013 and 1,128 in 2021, with 1.7% annual growth over that period [23]. We used 1,305 graduates in 2024, reflecting the reported acceleration towards 1,300, and held output constant after 2024 in the baseline. The announced 30% expansion of admissions was treated as a policy scenario, with graduates affected from 2031.

Emigration is not directly observed. We therefore did not impose an external emigration series. Instead, we calibrated the post-entry emigration flow so that the model reproduced the observed 2024 stock, and we mapped the range of emigration levels consistent with the same history (see below). This is a deliberate departure from the common practice of plugging a press estimate into a projection model.

Population denominators were taken from the 2024 census (11,972,169) and from the United Nations World Population Prospects 2024 medium variant, rescaled to the census for all years [24,25].

### Model structure

The model has two state variables: the number of practising physicians by single year of age, \(N_a(t)\), for ages 25 to 75 and over; and an "effective diaspora pool", \(D(t)\), used to generate return migration. Each year, the stock is updated through five flows.

The structure follows the supply side of the SANDEM cohort-component framework [18,19], but it is not a re-implementation of SANDEM: the parameters, data and migration treatment are Tunisian. We did not use an agent-based or multi-state Markov model because the data do not support the behavioural or transition parameters such models require. A simpler model keeps the assumptions visible and the uncertainty auditable.

We model **practising** physicians only. Physicians born in Tunisia, trained in Tunisia, or registered with the CNOM who practise abroad are not counted in the stock; they enter the model only through emigration and return flows. This distinction is essential because the four quantities are often used interchangeably in policy debate. Because temporary and permanent moves cannot be separated in the available data, all emigration is treated as an exit from the practising stock, with returns modelled separately; if circular migration is common, this overstates net losses.

**Entry.** A cohort graduating in year \(t-5\) enters practice in year \(t\), after internship and residency:

\[
E(t)=G(t-5)\,\sigma(t),
\]

where \(G\) is the number of graduates and \(\sigma\) is the share who enter Tunisian practice. The remaining graduates,

\[
X(t)=G(t-5)\,[1-\sigma(t)],
\]

are pre-entry emigrants: they leave during or immediately after training and never enter the Tunisian practising stock. Entrants are distributed over ages 29–33. This formulation reflects an important measurement problem: because residents are not counted in the practising stock, emigration during residency and failure to enter practice are observationally equivalent in aggregate data. The parameter \(\sigma\) absorbs both.

**Emigration from practice.** Post-entry emigration is modelled as a total annual flow \(M(t)\), allocated across ages using a fixed relative profile \(w_a\):

\[
e_a(t)=\min\left(\frac{M(t)\,w_a}{\sum_b N_b(t)\,w_b},\;0.35\right),\qquad M(t)=m(t)\,\Pi(t),
\]

where \(m(t)\) is the calibrated baseline flow and \(\Pi(t)\) is a scenario or trend multiplier. The age profile peaks at 30–34, is about 60% of peak at 35–39, and declines to near zero after 55 (Additional file 1, Table S2). The profile is an assumption informed by the repeated finding that most Tunisian emigrants are young physicians [15–17]; the model does not estimate age-specific emigration rates.

**Return migration.** Returns are \(R(t)=\rho(t)D(t)\), distributed over ages 33–50, and the diaspora pool evolves as \(D(t+1)=D(t)[1-\rho(t)]+M(t)+X(t)\). The pool is an accounting device, not a diaspora estimate.

**Retirement and mortality.** Retirement hazards are consistent with Tunisian legal ages: 62 in the public sector since Law 2019-37, 60 in the private sector, and 65–70 for hospitalo-university professors. Hazards are 0 below 60, 0.20 at 60–61, 0.45 at 62, 0.35 at 63–64, 0.45 at 65–69 and 1.00 at 70 and above. Mortality and other exits are 0.1% per year at ages 25–54, 0.4% at 55–64, 1.5% at 65–74 and 5% at 75 and over.

**Ageing.** Survivors move to the next single year of age; the 75+ group is open-ended.

### Initial conditions

The 2008 age distribution was taken from the CNOM 2007–2008 report, which tabulates physicians by age group [26]. The distribution was spread uniformly within five-year bands and scaled to a 2008 practising stock of 12,600; the WHO estimate for 2010 was 12,996 [27]. This is the best available age structure, but it is old and refers to registered rather than strictly practising physicians. Its influence decays as the initial cohorts retire; the sensitivity of the 2040 projection to the initial stock level is reported.

### Calibration and identifiability

The free parameter is the post-entry emigration flow \(m\). For each parameter draw, \(m\) was solved numerically so that the simulated 2024 stock equalled the observed 15,315. The calibration identifies a ridge rather than a point: a higher \(\sigma\) (more graduates entering practice) requires a higher \(m\) to reproduce the same stock. We therefore mapped the fit surface over \(\sigma=0.30\)–0.80 and a training-output multiplier of 0.85–1.50, recalibrating \(m\) at each point. This analysis shows which combinations of assumptions are consistent with the observed history and what emigration level each implies. It does not identify the true \(\sigma\) or \(m\).

### Scenarios

All scenarios begin in 2026 and are phased in linearly over three years. The central effect sizes are shown in Table 3.

1. **Business as usual.** No change in emigration intensity, return rate or training capacity.
2. **Remuneration and working conditions.** A 30% reduction in emigration, applied to both pre-entry and post-entry emigration.
3. **Professional development and career pathways.** A 15% reduction in emigration.
4. **Return migration and diaspora reintegration.** The annual return rate rises from 2.0% to 3.5% of the diaspora pool.
5. **Expanded training capacity.** A 30% increase in graduates from 2031, corresponding to the announced 2025 expansion of admissions.
6. **Combined retention and return.** A 35% reduction in emigration plus a return rate of 3.5%.

The effect sizes are assumptions, not estimates. The 30% reduction in the remuneration scenario is broadly consistent with the Ghanaian evidence that a 10% wage increase reduced annual attrition by about 12.5% relative [12,13], scaled up for a package that also addresses conditions and security. Each scenario was also run with low and high effect sizes (15% and 45% reductions for remuneration; 8% and 25% for career development; return-rate multipliers of 1.35 and 2.50; training multipliers of 1.15 and 1.50).

### Uncertainty and sensitivity

We generated 2,000 parameter draws. \(\sigma\) was drawn from a Beta distribution with mean 0.55 and standard deviation 0.07; the training-output multiplier from a lognormal distribution with median 1.0 and log-SD 0.12; the return rate from a Beta distribution with mean 0.02 and SD 0.008; the emigration age tilt from a lognormal distribution with median 1.0 and log-SD 0.15; the retirement-age shift from a uniform distribution of ±1.5 years; and the initial 2008 stock from a normal distribution with mean 12,600 and SD 300. For each draw, \(m\) was recalibrated and all scenarios were run with the same draw, so that scenario differences are not confounded with parameter draws. Intervals are 5th–95th percentiles.

Because the most consequential uncertainty is structural, we also ran deterministic scenarios in which emigration intensity grew at 3%, 5% or 7% per year after 2024. These are not probability statements; they represent plausible continuations of the recent trend.

Deterministic one-at-a-time sensitivity varied each parameter from its 10th to its 90th percentile, recalibrating \(m\) each time. Partial rank correlation coefficients (PRCC) were computed from the Monte Carlo sample.

### Patient and public involvement

No patients or members of the public were involved in this modelling study.

## Results

### Retrospective fit

The calibrated model reproduced the 2024 practising stock and tracked the historical series with a root mean squared error of 258 physicians (1.7% of the observed mean) and a mean absolute percentage error of 1.5% (Fig. 1). The largest discrepancies were in 2017–2019, when the model slightly under-predicted the observed stock, and in 2020–2021, when the observed public-sector count fell sharply. Excluding 2020–2021, the RMSE was 232 physicians.

The central calibration implied 601 entries (after 491 graduates had already emigrated before entry), 477 post-entry emigrants, 282 returns and 367 retirements in 2024, for a net change of about 14 physicians (Table 4). Total emigration was therefore about 969 per year, of which roughly half occurred before entry into the practising stock. This is higher than the administrative proxy of 187 removal requests in the first half of 2023 (about 374 per year) and lower than the 1,300–1,450 departures reported in the press for 2023–2024.

### The emigration level is not identifiable

The fit surface was remarkably flat (Fig. 2). Across \(\sigma=0.30\)–0.80 and training-output multipliers of 0.85–1.50, the RMSE varied only between 252 and 360 physicians (1.6–2.3%), while implied total emigration in 2024 varied from 675 to 1,839 per year. The best-fitting combination (\(\sigma=0.55\), training multiplier 0.85) implied 741 emigrants; the central calibration implied 969; and the combination consistent with the highest reported training output implied 1,839. All of these reproduced the observed stock path almost equally well.

This is the central methodological finding. The observed stock path constrains the **net** flow, not the gross flow. A country that trains more physicians and loses more of them can look exactly like a country that trains fewer and loses fewer. Without independent data on entries or emigration, the two cannot be distinguished. The model therefore does not claim to estimate the true emigration level; it carries the identified range through the scenario analysis and shows how conclusions depend on it.

### Baseline projection

Under the central calibration and constant emigration intensity, the practising stock would rise from 15,315 in 2024 to 16,041 in 2030, 17,002 in 2035 and 17,987 in 2040 (90% interval 16,339–19,968) (Fig. 1, Fig. 3A). Density would rise from 1.28 to 1.42 physicians per 1,000 population (90% interval 1.29–1.58), still far below the OECD average of 3.9 per 1,000 in 2023 [28]. Cumulative emigration over 2026–2040 would be about 15,800 physicians, partly offset by about 6,100 returns.

This baseline is not a prediction of crisis. It reflects the arithmetic of a training system that produces about 1,300 graduates a year, of whom roughly 55% enter Tunisian practice, and a practising stock that is still relatively young. The baseline grows slowly because entries exceed retirements and because emigration is held constant in absolute terms. If emigration intensity continues to rise, the picture changes sharply (see below).

### Policy scenarios

All five policy scenarios produced higher workforce levels than business as usual by 2040 (Table 5, Fig. 3A, Fig. 4). The combined retention and return strategy performed best: 25,335 physicians in 2040, or 7,348 more than the baseline (+41%), equivalent to 57,855 additional physician-years over 2026–2040. Remuneration and working conditions alone added 3,728 physicians (+21%; 29,468 physician-years); return migration alone added 3,446 (+19%; 26,008 physician-years); career development added 1,861 (+10%; 14,725 physician-years); and training expansion added only 1,124 (+6%; 3,341 physician-years).

The ranking was stable across the Monte Carlo draws: the combined strategy was ranked first in all 2,000 draws, and training expansion was ranked last in 1,983 (99%). The uncertainty around the return-migration scenario was the widest (2040 stock 18,204–25,344; physician-years 11,619–44,698), reflecting the absence of Tunisian evidence on return behaviour. The remuneration scenario was more precisely bounded (19,299–24,619).

Training expansion had two distinctive features. First, its effect appeared only after 2035, because graduates from the 2031 cohort enter practice in 2036. Second, it increased cumulative emigration rather than reducing it (16,692 versus 15,811 in the baseline), because a larger graduate cohort produces more pre-entry emigrants. Expanding training without improving retention therefore partly finances emigration.

### Structural uncertainty: rising emigration intensity

When emigration intensity was allowed to grow at 3% per year after 2024, the baseline reversed: the stock peaked at about 15,400 in 2029 and fell to 13,574 by 2040 (1.07 per 1,000) (Fig. 3B, Fig. 8). At 5% annual growth, it fell to 10,003; at 7%, to 7,592. These scenarios are consistent with the reported increase in departures after 2019 and with continued demand from ageing high-income health systems.

The policy ranking, however, was robust. Under 3% annual growth in emigration intensity, the combined strategy still reached 22,662 physicians in 2040, remuneration reached 18,591, return migration 17,367, career development 16,077 and training expansion 14,270 — all above the baseline of 13,574. Retention and return policies therefore dominated the structural trend, while training expansion alone did not.

### Sensitivity

The parameters that most influenced the 2040 workforce were the implied emigration level (PRCC 0.60), the return rate (0.57) and training output (0.53) (Fig. 6). Pipeline retention (\(\sigma\), 0.12), the age profile of emigration (0.12) and the initial 2008 stock (−0.26) were less influential. Retirement age had almost no effect (−0.03), because the calibration compensated for it: a later retirement age reduced exits but also required a higher emigration flow to reproduce the same 2024 stock. This is an identifiability result, not evidence that retirement policy is unimportant; it means that retirement effects cannot be separated from emigration effects using aggregate stock data alone.

In the one-at-a-time analysis, varying training output and the return rate from their 10th to 90th percentiles changed the 2040 workforce by about ±800 physicians each, while varying retirement age changed it by less than 250 (Fig. 6).

### Age structure

The model projects a gradual ageing of the practising stock under business as usual, with the share aged 55–64 rising from 21% in 2024 to 25% in 2040, and the share aged 45–54 falling from 35% to 30% (Fig. 7). The combined strategy produces a younger workforce, with a larger share aged 35–44 (38% versus 34% under business as usual), because it retains more early-career physicians and attracts return migrants. These age-structure results are indicative: they depend on the reconstructed 2008 age distribution and on the assumed age profile of emigration.

## Discussion

### Principal findings

We developed a transparent, reproducible model of the Tunisian physician workforce and used it to compare retention, return-migration and training policies under explicit uncertainty. Four findings stand out.

First, the level of physician emigration from Tunisia cannot be identified from aggregate data. The same observed stock path is nearly equally consistent with 675 to 1,839 annual emigrants, depending on how many graduates enter Tunisian practice. This range sits above the administrative proxy (about 374 removal requests per year), which is expected because many emigrants never request removal, and overlaps the lower part of the press estimates (1,300–1,450). The debate about whether Tunisia is losing 400 or 1,400 physicians a year cannot be settled with the data currently published; it requires independent measurement of entries or exits.

Second, within a 15-year horizon, policies that retain practising physicians and attract return migrants outperform training expansion. The combined strategy added about 7,350 physicians by 2040, compared with about 1,120 for a 30% expansion of training. The training effect is small for two reasons: the five-year postgraduate lag delays entry until 2036, and a larger graduate cohort produces more pre-entry emigrants. This does not mean that training is unimportant — a larger pipeline is necessary for long-run growth — but it means that training alone is a slow and leaky instrument.

Third, the policy ranking is robust to structural uncertainty about migration. Even if emigration intensity rises at 3% per year, the combined strategy reaches about 22,700 physicians in 2040, while the baseline falls to about 13,600. Retention and return policies are therefore not merely optimistic add-ons; they are the difference between a shrinking and a growing workforce under plausible future conditions.

Fourth, the model shows what cannot be estimated. Retirement age, the split between pre-entry and post-entry emigration, and the age profile of emigration are all weakly identified. Their effects on the historical stock can be offset by changes in emigration, so aggregate data cannot tell us which combination is true. This should temper claims about the effectiveness of specific policies and should redirect attention to data collection.

### Interpretation

The finding that retention dominates training in the medium run is consistent with the structure of the physician labour market. A physician who emigrates is lost not only for the year of departure but for the remaining working life; a new graduate takes at least five years to replace them, and may also emigrate. The Hungarian evidence that more than half of emigrants return [14] suggests that return migration can partly offset these losses, but return is uncertain and slow. Our return scenario, which raises the return rate by 75%, produces a large effect (3,446 physicians by 2040) but with the widest uncertainty interval of any scenario. This is an argument for investing in diaspora engagement and in the data systems needed to evaluate it, not for assuming that returns will happen.

The comparison with Ghana is instructive. A 10% wage increase reduced annual attrition by about one percentage point from a mean of eight [12], implying a relative reduction of about 12.5%. If a similar elasticity applied in Tunisia, a 30% real wage increase might reduce emigration by roughly a third — the effect size we used in the remuneration scenario. But wage gaps with destination countries remain large, and the non-wage drivers (security, workload, career prospects, political stability) are prominent in Tunisian surveys [15–17]. A pure wage strategy may therefore have less effect than a package that also addresses working conditions and career pathways. Our scenario structure cannot distinguish these channels; it only shows that a combined effect of 30–35% would be substantial.

The baseline projection deserves careful interpretation. It suggests slow growth, not collapse, if emigration intensity remains constant. That is not a prediction of stability. The baseline assumes that Tunisia continues to train about 1,300 physicians a year, that 55% of them enter practice, and that emigration does not increase. Each of these assumptions is fragile. The 2020–2021 administrative discontinuity, the uncertainty about recent training output (1,100 versus 1,900), and the possibility of continued escalation all imply that the true trajectory could be much lower. The structural scenarios make this explicit: at 3% annual growth in emigration intensity, the workforce declines by 11% from 2024 to 2040; at 5%, by 35%.

### What the model can and cannot establish

The model can establish the **arithmetic** of the workforce: given a set of entry, exit and migration assumptions, what follows for the stock, its age structure and density. It can compare the relative consequences of different policy assumptions. It can show which parameters matter and which are weakly identified. It can demonstrate that some combinations of published numbers are mutually inconsistent.

It cannot establish the true level of emigration, the causal effect of any policy, the demand for physicians, the specialty or regional distribution of shortages, or the quality of care. It cannot tell whether a 30% reduction in emigration is achievable, or at what fiscal cost. It cannot validate its projections against future data. These limitations are inherent to the available evidence, not to the choice of software.

### Comparison with other models

SANDEM projects the EU workforce with a cohort-component model and holds migration flows constant [18,19]. Our model follows the same logic but adapts it to a data-poor setting: instead of imposing an external migration flow, we calibrate the flow to the observed stock and map the range of flows consistent with it. This is a modest methodological contribution, but it is important for countries where migration statistics are incomplete.

The Portuguese agent-based model [20] shows that small errors in emigration or dropout rates can produce divergent long-run forecasts. Our results point in the same direction, but they also show that the divergence is driven as much by **structural** assumptions (whether emigration escalates) as by parameter uncertainty. A complex model with poorly identified parameters would not resolve this; it would only make the assumptions harder to see.

### Implications for data and measurement

The most important implication is not a policy recommendation but a measurement one. Tunisia needs an annual, cohort-consistent workforce account that distinguishes:

- physicians registered with the CNOM;
- physicians in active practice, by sector, age and specialty;
- entries from training, including residents;
- exits by retirement, death and emigration;
- returns from abroad.

The CNOM registration database could provide much of this if it were linked to the Ministry of Health payroll and the carte sanitaire, and if registration status were updated when physicians leave. Destination-country data (France, Germany, Canada, Gulf states) could be used to triangulate emigration, but only if definitions (country of birth versus country of training versus nationality) are harmonised. Until then, projections will remain conditional and the policy debate will continue to cite incompatible numbers.

Registration data already illustrate how the ambiguity could be reduced. In 2021–2022, the CNOM recorded 2,073 new inscriptions, about 1,036 per year, compared with roughly 1,100–1,300 graduates [4]. If these inscriptions were all new entrants, pipeline retention would be closer to 0.8 than the 0.55 used in the central calibration. For the same total emigration, that would imply a smaller pre-entry and a larger post-entry component. The 2040 workforce projection would change by only about 2%, but the interpretation of when and why physicians leave would change substantially. A linked registration–training–payroll dataset would resolve part of this ambiguity; aggregate stock data cannot.

### Policy implications

Three implications follow.

First, retention should be treated as a workforce supply instrument, not only as a labour-rights issue. A package that reduces emigration by 30% would add more physicians by 2040 than a 30% expansion of training, and it would do so sooner. The package needs to address pay, security, workload and career progression; the evidence does not allow us to say how much weight each component should receive.

Second, return migration is a potentially large but uncertain lever. Tunisia has a large diaspora and a strong linguistic and professional link to France. A serious return policy would require recognition of foreign-acquired qualifications, flexible re-entry pathways, and a register of Tunisian physicians abroad. Our scenario suggests that a 75% increase in the return rate would add about 3,450 physicians by 2040, but the uncertainty around this estimate is wider than for any other scenario.

Third, training expansion should be paired with retention. On its own, it is slow and leaky: it adds physicians only after 2035 and increases the number of graduates who emigrate before entry. This does not argue against expansion — Tunisia's density remains far below OECD levels — but it argues against treating expansion as a substitute for retention.

Finally, the results should not be read as a forecast of crisis or of success. They are conditional statements. Their value is to make the trade-offs explicit, to show which assumptions drive the conclusions, and to identify the data that would reduce uncertainty.

## Strengths and limitations

The main strengths of this study are its transparency and its treatment of uncertainty. The model is simple enough to be audited, all parameters are documented with their sources and status, the code and data are open, and the identifiability analysis makes explicit what the data can and cannot support. The scenario analysis tests alternative effect sizes rather than asserting a single causal effect, and the structural scenarios show how conclusions change when the migration trend changes.

The limitations are substantial. The model uses aggregate national data and cannot distinguish specialties, sectors or regions. It treats all physicians as equivalent and ignores differences in productivity, hours and case mix. It does not model demand, so it cannot say whether the projected workforce is adequate; density comparisons with OECD countries are descriptive, not normative. It assumes a fixed age profile of emigration and a fixed retirement hazard, and it uses a reconstructed 2008 age distribution. It does not distinguish temporary from permanent migration; if circular migration is common, the model overstates net losses. The diaspora pool is not calibrated to a reliable stock, so the return scenario should be read as an illustration rather than an estimate. The 2020–2021 data contain an administrative discontinuity, and the training-output series is uncertain. Most importantly, the model is not externally validated: the historical comparison is a consistency check, and the projections have not been tested against future observations.

These limitations do not invalidate the comparative conclusions, which are driven by the structure of the flows rather than by precise parameter values, but they do limit the precision of the numbers. The model should be used to structure debate, not to set targets.

## Conclusions

Tunisia's physician workforce is shaped more by retention and return than by training capacity within a 15-year horizon. A combined retention and return strategy would add substantially more physicians by 2040 than a 30% expansion of training, and it would remain effective even if emigration continues to rise. Training expansion is necessary for the long run but is slow and partly self-defeating without retention. The most fundamental constraint, however, is data: the level of emigration cannot be identified from the published stock series, and the policy debate is conducted with indicators that measure different things. Better cohort-consistent workforce accounting — distinguishing registered, practising and emigrated physicians — is a precondition for credible planning.

---

## Declarations

**Ethics approval and consent to participate.** This study used aggregate published data and did not involve human participants. Ethical approval was not required.

**Consent for publication.** Not applicable.

**Availability of data and materials.** All data used are publicly available from the sources listed in Table 1. The analysis-ready datasets, model code and scripts are available in the project repository [repository URL to be inserted]. The repository includes a README with reproduction instructions.

**Competing interests.** The authors declare no competing interests.

**Funding.** This research received no specific grant from any funding agency in the public, commercial or not-for-profit sectors.

**Authors' contributions.** [To be completed.]

**Acknowledgements.** [To be completed.]

---

## Tables

### Table 1. Data sources and definitions

| Quantity | Source | Period | Definition and limitations |
|---|---|---|---|
| Physicians in active practice | INS / Ministry of Health [6]; carte sanitaire [7] | 2017–2024 | Public-sector physicians plus private practitioners; excludes most residents; 2020 public count affected by reporting change |
| Physicians registered with the CNOM | CNOM [4,5] | 2009–2026 | All inscriptions, including inactive, retired, administrative and deceased physicians; not a practising count |
| Medical graduates | Zehnati [23]; ministerial statements [1] | 2013–2025 | Medicine graduates only; series reconstructed; recent values uncertain |
| Emigration proxies | CNOM via ITES [3]; press [8,29] | 2011–2024 | Certificates of good conduct, removal requests, departure files and union/CNOM estimates; not comparable |
| Tunisian physicians in France | CNOM France [2] | 2010–2023 | Registered with the French Order; excludes unregistered physicians |
| Tunisian physicians in Germany | German medical statistics via ITES [3] | 2022 | Country-of-training/nationality definition |
| Tunisian-born physicians in OECD countries | OECD DIOC [30]; ITES [3] | 2010/11, 2015/16 | Country-of-birth estimate; lower bound |
| Population | INS census [24]; UN WPP 2024 [25] | 2010–2040 | 2024 census 11,972,169; WPP rescaled |

### Table 2. Key model parameters

| Parameter | Central value | Range / distribution | Status |
|---|---|---|---|
| Practising physicians, 2024 | 15,315 | — | Observed |
| Medical graduates, 2024 | 1,305 | 987 (2013) – 1,900 (2025 statement) | Observed / reconstructed |
| Pipeline retention, \(\sigma\) | 0.55 | Beta(mean 0.55, SD 0.07) | Estimated / assumed |
| Post-entry emigration, 2024, \(m\) | 477 | Calibrated per draw | Estimated |
| Total emigration, 2024 | 969 | 675–1,839 across identified set | Estimated |
| Pre-entry share of emigration | 0.45 | 0.20–0.70 | Assumed |
| Return rate, \(\rho\) | 0.020 | Beta(mean 0.02, SD 0.008) | Assumed |
| Retirement age | 60–70 | Shift ±1.5 years | Observed (legal) + assumed |
| Initial practising stock, 2008 | 12,600 | Normal(SD 300) | Indirect estimate |
| Initial diaspora pool, 2008 | 4,000 | 3,200–6,000 | Indirect estimate |
| Population, 2024 | 11,972,169 | — | Observed |
| Population growth, 2024–2040 | UN WPP medium | — | Projected |

### Table 3. Scenario definitions and effect sizes

| Scenario | Emigration multiplier | Reduction in pre-entry emigration | Return-rate multiplier | Training multiplier |
|---|---|---|---|---|
| Business as usual | 1.00 | 0 | 1.00 | 1.00 |
| Remuneration and working conditions | 0.70 | 30% | 1.00 | 1.00 |
| Professional development and careers | 0.85 | 15% | 1.00 | 1.00 |
| Return and diaspora reintegration | 1.00 | 0 | 1.75 | 1.00 |
| Expanded training capacity | 1.00 | 0 | 1.00 | 1.30 (from 2031) |
| Combined retention and return | 0.65 | 35% | 1.75 | 1.00 |

Low and high effect sizes used in the scenario uncertainty analysis are reported in Additional file 1, Table S3.

### Table 4. Modelled flow decomposition, selected years

| Year | Stock | Entries | Pre-entry emigration | Post-entry emigration | Returns | Retirements | Deaths | Net change | Density (/1,000) |
|---|---|---|---|---|---|---|---|---|---|
| 2017 | 14,716 | 534 | 437 | 286 | 193 | 204 | 22 | +215 | 1.30 |
| 2020 | 15,173 | 561 | 459 | 368 | 229 | 285 | 24 | +113 | 1.30 |
| 2024 | 15,316 | 601 | 491 | 477 | 282 | 367 | 24 | +14 | 1.28 |
| 2030 | 16,041 | 718 | 587 | 477 | 367 | 397 | 26 | +184 | 1.30 |
| 2035 | 17,002 | 718 | 587 | 477 | 434 | 428 | 29 | +217 | 1.36 |
| 2040 | 17,987 | 718 | 587 | 477 | 495 | 549 | 31 | +155 | 1.42 |

Values are rounded; the model is calibrated to the 2024 observed stock of 15,315.

### Table 5. Projected workforce and policy outcomes, 2040

| Scenario | Workforce 2040 | Difference from BAU | Density 2040 (/1,000) | Cumulative emigration 2026–2040 | Cumulative returns 2026–2040 | Physician-years vs BAU | Workforce 2040 if emigration rises 3%/yr |
|---|---|---|---|---|---|---|---|
| Business as usual | 17,987 | — | 1.42 | 15,811 | 6,084 | — | 13,574 |
| Remuneration and conditions | 21,715 | +3,728 | 1.72 | 11,366 | 5,473 | 29,468 | 18,591 |
| Career development | 19,848 | +1,861 | 1.57 | 13,588 | 5,778 | 14,725 | 16,077 |
| Return migration | 21,433 | +3,446 | 1.70 | 15,811 | 9,614 | 26,008 | 17,367 |
| Training expansion | 19,111 | +1,124 | 1.51 | 16,692 | 6,135 | 3,341 | 14,270 |
| Combined strategy | 25,335 | +7,348 | 2.01 | 10,625 | 8,444 | 57,855 | 22,662 |

Physician-years are the undiscounted sum of annual differences from business as usual over 2026–2040. The final column is a deterministic structural scenario, not a probabilistic interval.

## Figure legends

**Fig. 1** Observed and modelled practising physician stock, Tunisia, 2010–2040. Points are observed values from INS/Ministry of Health; the solid line is the retrospective fit (2008–2024); the dashed line is the baseline projection; the shaded area is the 90% uncertainty interval from 2,000 Monte Carlo draws. The vertical dotted line marks the start of the projection.

**Fig. 2** Identifiability of the emigration level. (A) Root mean squared error of the retrospective fit across pipeline retention (\(\sigma\)) and the training-output multiplier, with the post-entry emigration flow recalibrated at each point. (B) Implied total emigration in 2024 for the same combinations. The fit surface is flat over a wide range, while implied emigration varies more than twofold.

**Fig. 3** Policy scenarios, 2024–2040. (A) Constant emigration intensity; the shaded area is the baseline 90% uncertainty interval. (B) Emigration intensity rising at 3% per year (deterministic structural scenario). All scenarios are phased in from 2026.

**Fig. 4** Policy outcomes. (A) Workforce in 2040; error bars show low and high scenario effect sizes. (B) Cumulative emigration 2026–2040. (C) Physician-years retained relative to business as usual. Dashed lines in A and B show the business-as-usual value.

**Fig. 5** Physician density, 2015–2040. Density is physicians in practice per 1,000 population, using the 2024 census and UN WPP 2024 medium-variant projections.

**Fig. 6** Sensitivity of the 2040 workforce. Bars show the change from the central calibration when each parameter is set to its 10th (blue) or 90th (red) percentile, with the emigration flow recalibrated each time.

**Fig. 7** Age structure of the practising workforce, 2024 and 2040. Bars show the percentage of practising physicians in each age group under business as usual and under the combined strategy.

**Fig. 8** Structural sensitivity to the future path of emigration. The baseline assumes constant emigration intensity; the other lines assume annual growth of 3%, 5% or 7% after 2024.

## Additional file 1

Supplementary tables: reporting checklist, emigration age profile, scenario effect-size ranges, and full parameter distributions. Available with the online version.

## References

1. Ministère de l'Enseignement Supérieur et de la Recherche Scientifique. Annonce d'une hausse de 30% des admissions en médecine. Tunis; 2025.
2. Conseil National de l'Ordre des Médecins (France). *Atlas de la démographie médicale en France: situation au 1er janvier 2023.* Paris: CNOM; 2023.
3. Institut Tunisien des Études Stratégiques. *La migration des professionnels de santé: défis pour le système de santé tunisien.* Tunis: ITES; 2024.
4. Conseil National de l'Ordre des Médecins de Tunisie. *Rapport moral 2021–2022.* Tunis: CNOM; 2022.
5. Conseil National de l'Ordre des Médecins de Tunisie. Tableau de l'Ordre [website]. Tunis; 2026. https://ordremedecins.tn
6. Institut National de la Statistique / Ministère de la Santé. Personnel médical [database]. Tunis: INS; 2026. https://ins.tn
7. Ministère de la Santé. *Carte sanitaire 2022–2023: synthèse.* Tunis: Direction des études et de la planification; 2024.
8. La Presse de Tunisie. Exode des médecins: près de 1.450 médecins ont fui la Tunisie en 2024. 7 January 2025.
9. Tunisie Numérique. Tunisie – Exode des compétences: 1,325 médecins ont quitté le pays en 2023. 20 March 2024.
10. Adovor E, Czaika M, Docquier F, Moullan Y. Medical brain drain: how many, where and why? *J Health Econ.* 2021;76:102409. doi:10.1016/j.jhealeco.2020.102409
11. Arah OA. The metrics and correlates of physician migration from Africa. *BMC Public Health.* 2007;7:83. doi:10.1186/1471-2458-7-83
12. Antwi J, Phillips DC. Wages and health worker retention: evidence from public sector wage reforms in Ghana. *J Dev Econ.* 2013;102:101–115. doi:10.1016/j.jdeveco.2012.10.004
13. Okeke EN. Do higher salaries lower physician migration? *Health Policy Plan.* 2014;29(5):603–614. doi:10.1093/heapol/czt046
14. Varga J. Out-migration and attrition of physicians and dentists before and after EU accession (2003 and 2011): the case of Hungary. *Eur J Health Econ.* 2017;18:1079–1093. doi:10.1007/s10198-016-0854-6
15. Ajmi M, Kahloul M, Kacem I, Chouchane A, Ben Mansour S, Slama Y, et al. Immigration projects among young doctors in Tunisia: prevalence, destinations and causes. *Eur Psychiatry.* 2022;65(S1):S633–S634. doi:10.1192/j.eurpsy.2022.1624
16. Tabib F, Guermazi F, Zouari A, Ben Abdallah M, Hentati S, Baati I, et al. Emigration intentionality among Tunisian interns and residents in medicine. *Eur Psychiatry.* 2022;65(S1):S633. doi:10.1192/j.eurpsy.2022.564
17. Haouari W, Omri S, Labyadh A, Feki R, Gassara I, Charfi N, et al. Factors driving the emigration intentions of young Tunisian medical professionals. *Eur Psychiatry.* 2024;67(S1):S829–S830. doi:10.1192/j.eurpsy.2024.1731
18. Bernini A, Icardi R, Natale F, Nedee A. *Supply AND DEMand Model for the Healthcare Workforce in the EU27: Data Sources and Model Structure.* Luxembourg: Publications Office of the European Union; 2024. doi:10.2760/957386
19. Bernini A, Icardi R, Natale F, Nedee A. *Healthcare Workforce Demand and Supply in the EU27.* Ispra: Joint Research Centre; 2024. doi:10.2760/1683259
20. Lopes MA, Almeida ÁS, Almada-Lobo B. Forecasting the medical workforce: a stochastic agent-based simulation approach. *Health Care Manag Sci.* 2018;21(1):52–75. doi:10.1007/s10729-016-9379-x
21. Lee JT, Crettenden I, Tran M, Miller D, Cormack M, Cahill M, et al. Methods for health workforce projection model: systematic review and recommended good practice reporting guideline. *Hum Resour Health.* 2024;22:25. doi:10.1186/s12960-024-00895-z
22. World Health Organization. *Models and Tools for Health Workforce Planning and Projections.* Human Resources for Health Observer No. 3. Geneva: WHO; 2010.
23. Zehnati A. L'émigration des médecins, en particulier vers la France, et la desserte médicale au Maghreb. *Belgeo.* 2024;(1). doi:10.4000/12ihd
24. Institut National de la Statistique. *Recensement Général de la Population et de l'Habitat 2024: bilan démographique.* Tunis: INS; 2025.
25. United Nations. *World Population Prospects 2024.* New York: UN; 2024.
26. Conseil National de l'Ordre des Médecins de Tunisie. *Rapport moral 2007–2008.* Tunis: CNOM; 2008.
27. World Health Organization. Global Health Workforce Statistics [database]. Geneva: WHO; 2024.
28. OECD. *Health at a Glance 2025.* Paris: OECD Publishing; 2025.
29. La Presse de Tunisie. 975 médecins ont préparé un dossier de départ en 2021. 10 February 2022.
30. OECD. Database on Immigrants in OECD Countries (DIOC), 2010/11 and 2015/16. Paris: OECD; 2018.
