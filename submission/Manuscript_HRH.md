# Retention, return or training? A stock-and-flow simulation of Tunisia's physician workforce under incomplete migration data

**Authors:** [Author 1]^1, [Author 2]^1, [Author 3]^2

**Affiliations:**
^1 [Department, Institution, City, Country]
^2 [Department, Institution, City, Country]

**Corresponding author:** [Name], [Department, Institution, City, Country]. Email: [email]

**Word count:** 3 220 (abstract and main text; excluding tables, figures, references and additional files)

**Tables:** 5 **Figures:** 8 **Additional files:** 1

---

## Abstract

**Background.** Tunisia trains more physicians than it retains, yet the scale of emigration is unknown: estimates of annual departures range from a few hundred to more than 1 400, and registered, practising and emigrated physicians are routinely conflated. We modelled how retention, return-migration and training policies could affect the practising workforce over 15 years, and what can be established when migration flows are poorly observed.

**Methods.** We built an annual, single-year-of-age cohort-component model of physicians in active practice in Tunisia, calibrated to the national practising stock for 2017–2024. The model represents entry of graduates after a five-year postgraduate lag, emigration before and after entry, return migration, retirement and mortality. We compared business as usual with five scenarios: remuneration and working conditions; career development; return migration; 30% training expansion; and a combined retention and return strategy. Policy effects were explicit, range-tested assumptions. We used 2 000 Monte Carlo draws, alternative effect sizes, and structural scenarios with rising emigration.

**Results.** The practising stock was 15 315 in 2024 (1.28 per 1 000). Under the central baseline it would reach 17 990 by 2040 (90% interval 16 340–19 970; 1.42 per 1 000). A combined retention and return strategy would add 7 350 physicians by 2040 (25 340 in total) and 57 900 physician-years. Remuneration alone would add 3 730; return migration 3 450; career development 1 860; and training expansion only 1 120, because graduates enter after 2031. If emigration intensity rose 3% per year, the baseline would fall to 13 570 while the combined strategy would still reach 22 660. The observed stock path was nearly equally consistent with 675 to 1 839 annual emigrants; the emigration level is not identifiable from aggregate data.

**Conclusions.** Within 15 years, retaining practising physicians and attracting return migrants outperforms training expansion, which is delayed by the training pipeline and partly offset by emigration of new graduates. A combined strategy is robust to plausible escalation of emigration. The results are conditional and mainly structure policy choices and expose data gaps. Tunisia needs cohort-consistent reporting that distinguishes registered, practising and emigrated physicians.

**Keywords:** health workforce; physician migration; brain drain; Tunisia; stock-and-flow model; health policy; uncertainty analysis

---

## Background

Tunisia has expanded medical training rapidly. Four public medical faculties produce roughly 1 100 physicians a year, and the government announced a 30% increase in admissions in 2025 [1]. Yet emigration is prominent: Tunisian-trained physicians are the second-largest group of non-EU-trained doctors in France (1 591 in 2023, up from 266 in 2010) [2], and Germany recorded 881 in 2022 [3]. The medical council and medical unions describe an exodus [4,5].

The debate rests on incomparable numbers. The Tunisian Order of Physicians (Conseil National de l'Ordre des Médecins, CNOM) reported 27 935 registered physicians at the end of 2022 [6] and indexed 31 804 directory records in 2026 [7]. The Ministry of Health and the National Institute of Statistics (INS) report about 15 000 physicians in active practice [8,9]. The gap is not the diaspora: it includes retired, deceased, inactive and administrative physicians, and some physicians abroad who remain registered. Departure indicators range from 187 removal requests in the first half of 2023 [3] to 1 325 in 2023 and about 1 400 in 2024 [4,5,10]. These indicators measure different things.

This matters because it makes the workforce situation appear either catastrophic or exaggerated depending on the number cited, and it prevents a serious comparison of policies. International evidence shows that migration responds to wages, working conditions, career opportunities, stability and diasporic ties, and to destination-country immigration policy [11,12]. In Ghana, a 10% wage increase reduced annual attrition among young health workers by about one percentage point from a mean of eight [13], and a related evaluation found a 10% reduction in the stock of Ghanaian doctors abroad after six years [14]. Return can be substantial: more than half of Hungarian physicians who left during 2003–2011 returned at some point [15]. Tunisian surveys report migration intentions of 38.5% in 2019, 53.6% in 2022 and 68% in 2024 [16–18], but intentions are not flows.

Workforce projection models organise this uncertainty. Cohort-component stock-and-flow models are standard, and the JRC SANDEM model is a recent example [19,20]. Agent-based models can represent individual decisions and heterogeneity; the Portuguese physician workforce model is the closest application [21]. Both need data that Tunisia lacks: age-specific migration rates, reliable annual flows, and a separation of temporary and permanent moves. Reviews emphasise that projections are conditional statements whose credibility depends on transparency, not computational sophistication [22,23].

We therefore built a deliberately simple, age-structured stock-and-flow model to (i) integrate the available Tunisian evidence; (ii) compare retention, return-migration and training policies over 15 years; (iii) quantify parameter and structural uncertainty; and (iv) identify what cannot be estimated. We do not claim that any simulated policy has a proven causal effect in Tunisia.

## Methods

### Design and reporting

We built an annual, single-year-of-age cohort-component model of physicians in active practice in Tunisia, running from 2008 to 2040, with 2017–2024 used for retrospective calibration. The model is supply-only: it excludes demand, vacancies, wages, specialty choice, sector and region. It follows the 30-item reporting guideline of Lee et al. [22] (Additional file 1). It was implemented in Python 3.14 with NumPy, pandas, SciPy and Matplotlib. AI-assisted tools supported code development and language editing; the authors reviewed all design decisions, parameters, interpretations and text and take responsibility for the work.

### Definitions and data

We modelled **practising** physicians: public-sector physicians plus private practitioners recorded in the national health map, calibrated to the INS/Ministry of Health series [8,9]. This is not the same as physicians registered with the CNOM, physicians born in Tunisia, or physicians trained in Tunisia. Table 1 summarises the sources; key parameters and their evidence status are in Table 2.

The practising stock rose from 14 892 in 2017 to 15 426 in 2019, fell to 14 792 in 2020 and reached 15 315 in 2024 [8]. The 2020 fall reflected a 725-physician drop in the public-sector count, probably a reporting change; fit is reported with and without 2020–2021.

Graduates were reconstructed from published estimates: 987 in 2013 and 1 128 in 2021, with 1.7% annual growth [24]; we used 1 305 in 2024 and held output constant thereafter. The announced 30% expansion was treated as a scenario. Population denominators used the 2024 census (11 972 169) and United Nations World Population Prospects 2024, rescaled to the census [25,26].

Emigration is not directly observed. We therefore did not impose an external emigration series; instead we calibrated the post-entry flow to reproduce the 2024 stock and mapped the range of emigration consistent with history.

### Model structure

The model tracks practising physicians by single year of age, N_a(t), and an effective diaspora pool, D(t). Each year:

**Entry.** A cohort graduating in year t − 5 enters in year t:

E(t) = G(t − 5) × σ(t),

where G is the number of graduates and σ is the share who enter Tunisian practice. The remainder, X(t) = G(t − 5) × [1 − σ(t)], is pre-entry emigration. Entrants are spread over ages 29–33. Because residents are not counted in the practising stock, emigration during residency and failure to enter practice are observationally equivalent; σ absorbs both.

**Emigration.** Post-entry emigration is a total annual flow M(t), allocated across ages by a fixed relative profile w_a:

e_a(t) = min{ M(t) w_a / Σ_b N_b(t) w_b, 0.35 }, with M(t) = m(t) × Π(t),

where m is the calibrated flow and Π a scenario multiplier. The profile peaks at 30–34 and declines after 35 (Additional file 1, Table S2); it is an assumption, not an estimated rate.

**Return.** R(t) = ρ(t) D(t), distributed over ages 33–50; D(t + 1) = D(t)[1 − ρ(t)] + M(t) + X(t). The pool is an accounting device, not a diaspora estimate.

**Retirement and mortality.** Hazards reflect Tunisian legal ages (62 in the public sector, 60 in the private sector, 65–70 for hospitalo-university professors): 0 below 60, 0.20 at 60–61, 0.45 at 62, 0.35 at 63–64, 0.45 at 65–69 and 1.00 at 70 and above. Mortality is 0.1% at ages 25–54, 0.4% at 55–64, 1.5% at 65–74 and 5% at 75 and over.

**Ageing.** N_{a+1}(t + 1) = N_a(t)[1 − e_a(t) − r_a − q_a].

The structure follows the supply side of SANDEM [19,20] but is not a re-implementation of it. We did not use an agent-based or multi-state Markov model because the data do not support the behavioural or transition parameters they require.

### Initial conditions

The 2008 age distribution came from the CNOM 2007–2008 report [27], scaled to a practising stock of 12 600 (the WHO estimate for 2010 was 12 996 [28]). The initial diaspora pool was 4 000, consistent with OECD estimates [29]. The sensitivity of the 2040 projection to the initial stock level is reported.

### Calibration and identifiability

For each parameter draw, the post-entry flow m was solved numerically so that the simulated 2024 stock equalled 15 315. The calibration identifies a ridge: a higher σ (more graduates entering practice) requires a higher m to reproduce the same stock. We mapped the fit over σ = 0.30–0.80 and training-output multipliers of 0.85–1.50, recalibrating m at each point. This shows which combinations are consistent with history and what emigration each implies; it does not identify the true σ or m.

### Scenarios

All scenarios start in 2026 and phase in over three years (Table 3): (1) business as usual; (2) remuneration and working conditions (30% reduction in emigration, applied before and after entry); (3) professional development and careers (15% reduction); (4) return migration and diaspora reintegration (return rate 2.0% to 3.5%); (5) expanded training capacity (+30% graduates from 2031); and (6) combined retention and return (35% reduction plus a 3.5% return rate).

Effect sizes are assumptions, not estimates. The 30% reduction is broadly consistent with the Ghanaian evidence [13,14], scaled up for a package that also addresses conditions and security. Low and high effect sizes are reported in Additional file 1, Table S3.

### Uncertainty and sensitivity

We generated 2 000 parameter draws: σ from a Beta distribution (mean 0.55, SD 0.07); the training multiplier from a lognormal distribution (median 1.0, log-SD 0.12); the return rate from a Beta distribution (mean 0.02, SD 0.008); the emigration age tilt from a lognormal distribution (median 1.0, log-SD 0.15); the retirement-age shift from a uniform distribution (±1.5 years); and the initial 2008 stock from a normal distribution (mean 12 600, SD 300). m was recalibrated for each draw, and all scenarios used the same draw. Intervals are 5th–95th percentiles.

Because structural uncertainty dominates, we also ran deterministic scenarios with emigration intensity rising 3%, 5% or 7% per year after 2024. One-at-a-time sensitivity varied each parameter from its 10th to its 90th percentile, and partial rank correlation coefficients (PRCC) were computed from the Monte Carlo sample.

## Results

### Retrospective fit

The model reproduced the 2024 stock and tracked history with a root mean squared error of 258 physicians (1.7% of the mean) and a mean absolute percentage error of 1.5% (Fig. 1). The largest discrepancies were in 2017–2019 (under-prediction) and 2020–2021 (over-prediction after the public-sector count fell). Excluding 2020–2021, the RMSE was 232.

The central calibration implied 601 entries (after 491 pre-entry emigrants), 477 post-entry emigrants, 282 returns and 367 retirements in 2024, a net change of about 14 (Table 4). Total emigration was about 969, roughly half before entry. This is above the administrative proxy (about 374 per year) and below the press estimates (1 300–1 450).

### The emigration level is not identifiable

The fit surface was flat (Fig. 2): across σ = 0.30–0.80 and training multipliers of 0.85–1.50, the RMSE varied only between 252 and 360 (1.6–2.3%), while implied emigration in 2024 varied from 675 to 1 839. The best fit (σ = 0.55, multiplier 0.85) implied 741; the central calibration 969; the highest training output 1 839. All reproduced history almost equally well.

This is the central result. The stock path constrains net flow, not gross flow. A country that trains more and loses more can look like one that trains less and loses less. The model therefore does not estimate the true emigration level; it carries the identified range through the scenarios.

### Baseline projection

With constant emigration intensity, the stock would reach 16 041 in 2030, 17 002 in 2035 and 17 987 in 2040 (90% interval 16 339–19 968; Fig. 1, Fig. 3A). Density would rise from 1.28 to 1.42 per 1 000 (1.29–1.58), still far below the OECD average of 3.9 [30]. Cumulative emigration over 2026–2040 would be about 15 800, offset by about 6 100 returns.

This is not a forecast of collapse. It reflects about 1 300 graduates a year, 55% entering practice, and a relatively young stock. If emigration intensity rises, the picture changes sharply.

### Policy scenarios

All five policies produced higher stocks in 2040 than business as usual (Table 5, Fig. 3A, Fig. 4). The combined strategy performed best: 25 335 in 2040 (+7 348; +41%), or 57 855 physician-years. Remuneration added 3 728 (+21%; 29 468 physician-years); return migration 3 446 (+19%; 26 008); career development 1 861 (+10%; 14 725); and training expansion only 1 124 (+6%; 3 341).

The ranking was stable: combined ranked first in all 2 000 draws; training ranked last in 1 983 (99%). The return scenario had the widest interval (2040 stock 18 204–25 344; physician-years 11 619–44 698); remuneration was narrower (19 299–24 619). Density would reach 2.01 per 1 000 under the combined strategy versus 1.42 under business as usual (Fig. 5).

Training expansion was slow and leaky: its effect appeared only after 2035 (2031 graduates enter in 2036), and it increased cumulative emigration (16 692 vs 15 811) because larger cohorts produce more pre-entry emigrants.

### Sensitivity

The 2040 workforce was most influenced by the implied emigration level (PRCC 0.60), return rate (0.57) and training output (0.53), then initial stock (−0.26), pipeline retention (0.12) and emigration age profile (0.12) (Fig. 6). Retirement age had almost no effect (−0.03) because calibration compensated: later retirement reduced exits but required higher emigration to reproduce the same 2024 stock. This is an identifiability result, not evidence that retirement policy is unimportant.

### Age structure

Under business as usual, the share aged 55–64 rises from 21% in 2024 to 25% in 2040, and the share aged 45–54 falls from 35% to 30% (Fig. 7). The combined strategy produces a younger workforce (38% aged 35–44 vs 34%). These results depend on the reconstructed 2008 distribution and the assumed emigration age profile.

### Structural uncertainty

With emigration intensity rising 3% per year, the baseline peaked at about 15 400 in 2029 and fell to 13 574 by 2040 (1.07 per 1 000; Fig. 3B, Fig. 8). At 5%, it fell to 10 003; at 7%, to 7 592. The policy ranking held: under 3% growth, combined reached 22 662, remuneration 18 591, return 17 367, career 16 077 and training 14 270, all above the baseline.

## Discussion

### Principal findings

Four findings stand out.

First, the level of emigration cannot be identified from aggregate data. The same stock path is nearly equally consistent with 675–1 839 annual emigrants. The range sits above the administrative proxy and overlaps the lower press estimates. The debate about 400 versus 1 400 cannot be settled without independent measurement of entries or exits.

Second, retention and return outperform training within 15 years. Combined added about 7 350 physicians by 2040 versus about 1 120 for a 30% training expansion. Training is slow (five-year lag) and leaky (larger cohorts produce more pre-entry emigrants). This does not make training unimportant — a larger pipeline is needed in the long run — but it is a weak short-run instrument.

Third, the ranking is robust to structural uncertainty. Even with emigration rising 3% per year, combined reaches about 22 700 while the baseline falls to about 13 600.

Fourth, key quantities are weakly identified. Retirement age, the pre-/post-entry split and the emigration age profile can be offset by changes in emigration. Aggregate data cannot tell us which combination is true.

### Interpretation

Retention dominates training because an emigrant is lost for the rest of their working life, while a new graduate takes at least five years to replace them and may also leave. Hungarian evidence that more than half return [15] suggests return can offset some losses, but return is uncertain and slow; our return scenario produces a large effect with the widest interval.

The Ghanaian comparison suggests that a 10% wage increase reduced attrition by about 12.5% relative [13]. A 30% real increase might therefore reduce emigration by roughly a third — our remuneration effect size. But wage gaps remain large, and non-wage drivers are prominent in Tunisian surveys [16–18]. A package addressing conditions and careers may be needed.

The baseline deserves care. Slow growth is not stability: it assumes about 1 300 graduates, 55% entry and constant emigration. The 2020–2021 discontinuity, uncertainty about recent output (1 100 vs 1 900) and possible escalation all imply that the true path could be lower. At 3% annual growth in emigration intensity, the workforce falls 11% by 2040; at 5%, 35%.

### What the model can and cannot establish

It can establish the arithmetic of the stock under explicit assumptions, compare policy consequences, show which parameters matter, and demonstrate that some published combinations are inconsistent. It cannot establish the true emigration level, causal policy effects, demand, specialty or regional shortages, or quality of care. It cannot validate its projections against future data.

### Implications for data and measurement

Tunisia needs an annual, cohort-consistent account distinguishing registered, practising, entering and exiting physicians. Registration data illustrate the gain: 2 073 new CNOM inscriptions in 2021–2022 (about 1 036 per year) versus roughly 1 100–1 300 graduates [6]. If all were new entrants, pipeline retention would be nearer 0.8 than 0.55, shifting emigration from pre- to post-entry. The 2040 projection would change by only about 2%, but the interpretation of when and why physicians leave would change substantially. Linked registration–training–payroll data would resolve part of the ambiguity.

### Policy implications

Retention should be treated as a supply instrument: a 30% reduction in emigration adds more by 2040 than a 30% training expansion, and sooner. Return migration is potentially large but uncertain; it requires qualification recognition, re-entry pathways and a diaspora register. Training expansion should be paired with retention, not substituted for it. None of these results is a forecast; they make trade-offs and data gaps explicit.

### Strengths and limitations

Strengths: transparency, open code and data, explicit parameter status, identifiability analysis, range-tested effects and structural scenarios.

Limitations: aggregate data; no specialty, sector or region; no demand or productivity; fixed emigration age profile and retirement hazards; a reconstructed 2008 age distribution; no separation of temporary and permanent migration (which overstates net losses if circular migration is common); an uncalibrated diaspora pool; a 2020–2021 discontinuity; uncertain training output; and no external validation. The historical comparison is a consistency check, not validation.

## Conclusions

Tunisia's physician workforce is shaped more by retention and return than by training capacity within 15 years. A combined strategy would add substantially more physicians than a 30% training expansion and would remain effective if emigration rises. Training is necessary for the long run but slow and leaky without retention. The fundamental constraint is data: the emigration level cannot be identified from the published stock series, and the debate uses indicators that measure different things. Cohort-consistent accounting is a precondition for credible planning.

## List of abbreviations

CNOM: Conseil National de l'Ordre des Médecins; INS: Institut National de la Statistique; OECD: Organisation for Economic Co-operation and Development; PRCC: partial rank correlation coefficient; RMSE: root mean squared error; SANDEM: Supply ANd DEMand model; SD: standard deviation; WHO: World Health Organization; WPP: World Population Prospects.

## Declarations

### Ethics approval and consent to participate

Not applicable. This study used aggregate, publicly available data and did not involve human participants.

### Consent for publication

Not applicable.

### Availability of data and materials

The datasets generated and analysed during the current study, together with all model code, are available in the [repository name] repository, [persistent identifier and URL]. The source data are publicly available from the sources listed in Table 1.

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

1. La Presse de Tunisie. Facultés de médecine: le nombre d'étudiants augmenté de 30% pour combler le déficit médical. 7 Jul 2025. https://www.lapresse.tn/2025/07/07/facultes-de-medecine-le-nombre-detudiants-augmente-de-30-pour-combler-le-deficit-medical. Accessed 23 Nov 2026.
2. Conseil National de l'Ordre des Médecins. Atlas de la démographie médicale en France: situation au 1er janvier 2023. Paris: CNOM; 2023.
3. Institut Tunisien des Études Stratégiques. La migration des professionnels de santé: défis pour le système de santé tunisien. Tunis: ITES; 2024. https://www.admin.ites.tn/api/uploads/66156d8f285bb65f10309d2d_0.pdf. Accessed 23 Nov 2026.
4. La Presse de Tunisie. Exode des médecins: près de 1 450 médecins ont fui la Tunisie en 2024. 7 Jan 2025. https://www.lapresse.tn/2025/01/07/exode-des-medecins-pres-de-1-450-medecins-ont-fui-la-tunisie-en-2024. Accessed 23 Nov 2026.
5. Tunisie Numérique. Tunisie – Exode des compétences: 1 325 médecins ont quitté le pays en 2023. 20 Mar 2024. https://www.tunisienumerique.com/tunisie-exode-des-competences-1325-medecins-ont-quitte-le-pays-en-2023. Accessed 23 Nov 2026.
6. Conseil National de l'Ordre des Médecins de Tunisie. Rapport moral 2021–2022. Tunis: CNOM; 2022. https://www.ordremedecins-centre.org.tn/fileadmin/contenu/Publications/Rapports_CNOM/Rapport_2021-2022.pdf. Accessed 23 Nov 2026.
7. Conseil National de l'Ordre des Médecins de Tunisie. Tableau de l'Ordre. https://ordremedecins.tn. Accessed 23 Nov 2026.
8. Institut National de la Statistique, Ministère de la Santé. Personnel médical. https://ins.tn. Accessed 23 Nov 2026.
9. Ministère de la Santé. Carte sanitaire 2022–2023: synthèse. Tunis: Direction des études et de la planification; 2024. https://santetunisie.rns.tn/images/Synthese-carte-sanitaire2023.pdf. Accessed 23 Nov 2026.
10. La Presse de Tunisie. 975 médecins ont préparé un dossier de départ en 2021. 10 Feb 2022. https://www.lapresse.tn/2022/02/10/975-medecins-ont-prepare-un-dossier-de-depart-en-2021-de-limpossibilite-de-reformer. Accessed 23 Nov 2026.
11. Adovor E, Czaika M, Docquier F, Moullan Y. Medical brain drain: how many, where and why? J Health Econ. 2021;76:102409.
12. Arah OA. The metrics and correlates of physician migration from Africa. BMC Public Health. 2007;7:83.
13. Antwi J, Phillips DC. Wages and health worker retention: evidence from public sector wage reforms in Ghana. J Dev Econ. 2013;102:101–15.
14. Okeke EN. Do higher salaries lower physician migration? Health Policy Plan. 2014;29(5):603–14.
15. Varga J. Out-migration and attrition of physicians and dentists before and after EU accession (2003 and 2011): the case of Hungary. Eur J Health Econ. 2017;18:1079–93.
16. Ajmi M, Kahloul M, Kacem I, Chouchane A, Ben Mansour S, Slama Y, et al. Immigration projects among young doctors in Tunisia: prevalence, destinations and causes. Eur Psychiatry. 2022;65(Suppl 1):S633–4.
17. Tabib F, Guermazi F, Zouari A, Ben Abdallah M, Hentati S, Baati I, et al. Emigration intentionality among Tunisian interns and residents in medicine. Eur Psychiatry. 2022;65(Suppl 1):S633.
18. Haouari W, Omri S, Labyadh A, Feki R, Gassara I, Charfi N, et al. Factors driving the emigration intentions of young Tunisian medical professionals. Eur Psychiatry. 2024;67(Suppl 1):S829–30.
19. Bernini A, Icardi R, Natale F, Nedee A. Supply AND DEMand model for the healthcare workforce in the EU27: data sources and model structure. Luxembourg: Publications Office of the European Union; 2024.
20. Bernini A, Icardi R, Natale F, Nedee A. Healthcare workforce demand and supply in the EU27. Ispra: Joint Research Centre; 2024.
21. Lopes MA, Almeida ÁS, Almada-Lobo B. Forecasting the medical workforce: a stochastic agent-based simulation approach. Health Care Manag Sci. 2018;21(1):52–75.
22. Lee JT, Crettenden I, Tran M, Miller D, Cormack M, Cahill M, et al. Methods for health workforce projection model: systematic review and recommended good practice reporting guideline. Hum Resour Health. 2024;22:25.
23. World Health Organization. Models and tools for health workforce planning and projections. Geneva: WHO; 2010.
24. Zehnati A. L'émigration des médecins, en particulier vers la France, et la desserte médicale au Maghreb. Belgeo. 2024;(1). doi:10.4000/12ihd.
25. Institut National de la Statistique. Recensement Général de la Population et de l'Habitat 2024: bilan démographique. Tunis: INS; 2025.
26. United Nations. World Population Prospects 2024. New York: UN; 2024. https://population.un.org/wpp/. Accessed 23 Nov 2026.
27. Conseil National de l'Ordre des Médecins de Tunisie. Rapport moral 2007–2008. Tunis: CNOM; 2008. https://www.ordremedecins-centre.org.tn/fileadmin/contenu/Publications/Rapports_CNOM/Rapport_2007-2008.pdf. Accessed 23 Nov 2026.
28. World Health Organization. Global Health Workforce Statistics. https://www.who.int/data/gho/data/themes/topics/health-workforce. Accessed 23 Nov 2026.
29. OECD. Database on Immigrants in OECD Countries (DIOC). https://www.oecd.org/els/mig/dioc.htm. Accessed 23 Nov 2026.
30. OECD. Health at a Glance 2025. Paris: OECD Publishing; 2025.

## Tables

### Table 1. Data sources and definitions

| Quantity | Source | Period | Definition and limitations |
|---|---|---|---|
| Physicians in active practice | INS / Ministry of Health [8]; carte sanitaire [9] | 2017–2024 | Public-sector physicians plus private practitioners; excludes most residents; 2020 public count affected by reporting change |
| Physicians registered with the CNOM | CNOM [6,7] | 2009–2026 | All inscriptions, including inactive, retired, administrative and deceased physicians; not a practising count |
| Medical graduates | Zehnati [24]; ministerial statements [1] | 2013–2025 | Medicine graduates only; series reconstructed; recent values uncertain |
| Emigration proxies | CNOM via ITES [3]; press [4,10] | 2011–2024 | Certificates of good conduct, removal requests, departure files and union/CNOM estimates; not comparable |
| Tunisian physicians in France | CNOM France [2] | 2010–2023 | Registered with the French Order; excludes unregistered physicians |
| Tunisian physicians in Germany | German medical statistics via ITES [3] | 2022 | Country-of-training/nationality definition |
| Tunisian-born physicians in OECD countries | OECD DIOC [29]; ITES [3] | 2010/11, 2015/16 | Country-of-birth estimate; lower bound |
| Population | INS census [25]; UN WPP 2024 [26] | 2010–2040 | 2024 census 11 972 169; WPP rescaled |

### Table 2. Key model parameters and evidence status

| Parameter | Central value | Range or distribution | Status |
|---|---|---|---|
| Practising physicians, 2024 | 15 315 | — | Observed |
| Medical graduates, 2024 | 1 305 | 987 (2013) to 1 900 (2025 statement) | Observed or reconstructed |
| Pipeline retention, σ | 0.55 | Beta (mean 0.55, SD 0.07) | Estimated or assumed |
| Post-entry emigration, 2024, m | 477 | Calibrated per draw | Estimated |
| Total emigration, 2024 | 969 | 675–1 839 across identified set | Estimated |
| Pre-entry share of emigration | 0.45 | 0.20–0.70 | Assumed |
| Return rate, ρ | 0.020 | Beta (mean 0.02, SD 0.008) | Assumed |
| Retirement age | 60–70 | Shift ±1.5 years | Observed (legal) and assumed |
| Initial practising stock, 2008 | 12 600 | Normal (SD 300) | Indirect estimate |
| Initial diaspora pool, 2008 | 4 000 | 3 200–6 000 | Indirect estimate |
| Population, 2024 | 11 972 169 | — | Observed |
| Population growth, 2024–2040 | UN WPP medium | — | Projected |

### Table 3. Policy scenarios and central effect sizes

| Scenario | Emigration multiplier | Reduction in pre-entry emigration | Return-rate multiplier | Training multiplier |
|---|---|---|---|---|
| Business as usual | 1.00 | 0 | 1.00 | 1.00 |
| Remuneration and working conditions | 0.70 | 30% | 1.00 | 1.00 |
| Professional development and careers | 0.85 | 15% | 1.00 | 1.00 |
| Return and diaspora reintegration | 1.00 | 0 | 1.75 | 1.00 |
| Expanded training capacity | 1.00 | 0 | 1.00 | 1.30 (from 2031) |
| Combined retention and return | 0.65 | 35% | 1.75 | 1.00 |

Low and high effect sizes are reported in Additional file 1, Table S3. Effect sizes are assumptions, not estimated causal effects.

### Table 4. Modelled flow decomposition, selected years

| Year | Stock | Entries | Pre-entry emigration | Post-entry emigration | Returns | Retirements | Net change | Density (per 1 000) |
|---|---|---|---|---|---|---|---|---|
| 2017 | 14 716 | 534 | 437 | 286 | 193 | 204 | +215 | 1.30 |
| 2020 | 15 173 | 561 | 459 | 368 | 229 | 285 | +113 | 1.30 |
| 2024 | 15 316 | 601 | 491 | 477 | 282 | 367 | +14 | 1.28 |
| 2030 | 16 041 | 718 | 587 | 477 | 367 | 397 | +184 | 1.30 |
| 2035 | 17 002 | 718 | 587 | 477 | 434 | 428 | +217 | 1.36 |
| 2040 | 17 987 | 718 | 587 | 477 | 495 | 549 | +155 | 1.42 |

Values are rounded. Deaths (22–31 per year) are omitted. The model is calibrated to the observed 2024 stock of 15 315.

### Table 5. Projected workforce and policy outcomes in 2040

| Scenario | Workforce 2040 | Difference from BAU | Density 2040 (per 1 000) | Cumulative emigration 2026–2040 | Physician-years vs BAU | Workforce 2040 if emigration rises 3% per year |
|---|---|---|---|---|---|---|
| Business as usual | 17 987 | — | 1.42 | 15 811 | — | 13 574 |
| Remuneration and conditions | 21 715 | +3 728 | 1.72 | 11 366 | 29 468 | 18 591 |
| Career development | 19 848 | +1 861 | 1.57 | 13 588 | 14 725 | 16 077 |
| Return migration | 21 433 | +3 446 | 1.70 | 15 811 | 26 008 | 17 367 |
| Training expansion | 19 111 | +1 124 | 1.51 | 16 692 | 3 341 | 14 270 |
| Combined strategy | 25 335 | +7 348 | 2.01 | 10 625 | 57 855 | 22 662 |

BAU: business as usual. Physician-years are the undiscounted sum of annual differences from BAU over 2026–2040. Cumulative returns over the same period were 6 084 under BAU and 8 444 under the combined strategy. The final column is a deterministic structural scenario, not a probabilistic interval.

## Figure legends

**Fig. 1 Observed and modelled physician stock, Tunisia, 2010–2040.** Points are observed values from INS/Ministry of Health; the solid line is the retrospective fit (2008–2024); the dashed line is the baseline projection; the shaded area is the 90% uncertainty interval from 2 000 Monte Carlo draws. The vertical dotted line marks the start of the projection.

**Fig. 2 Identifiability of the emigration level.** (A) Root mean squared error of the retrospective fit across pipeline retention (σ) and the training-output multiplier, with the post-entry emigration flow recalibrated at each point. (B) Implied total emigration in 2024 for the same combinations. The fit surface is flat over a wide range, while implied emigration varies more than twofold.

**Fig. 3 Policy scenarios under constant and rising emigration intensity.** (A) Constant emigration intensity; the shaded area is the baseline 90% uncertainty interval. (B) Emigration intensity rising at 3% per year (deterministic structural scenario). All scenarios are phased in from 2026.

**Fig. 4 Workforce, emigration and retention benefits by scenario.** (A) Workforce in 2040; error bars show low and high scenario effect sizes. (B) Cumulative emigration 2026–2040. (C) Physician-years retained relative to business as usual. Dashed lines in A and B show the business-as-usual value.

**Fig. 5 Physician density, 2015–2040.** Density is physicians in practice per 1 000 population, using the 2024 census and UN World Population Prospects 2024 medium-variant projections.

**Fig. 6 Sensitivity of the 2040 workforce.** Bars show the change from the central calibration when each parameter is set to its 10th (blue) or 90th (red) percentile, with the emigration flow recalibrated each time.

**Fig. 7 Age structure of the practising workforce, 2024 and 2040.** Bars show the percentage of practising physicians in each age group under business as usual and under the combined strategy.

**Fig. 8 Structural sensitivity to future emigration intensity.** The baseline assumes constant emigration intensity; the other lines assume annual growth of 3%, 5% or 7% after 2024.

## Additional files

**Additional file 1.** DOCX. Supplementary tables and reporting checklist. Contains model notation, the emigration age profile, scenario effect-size ranges, parameter distributions, full scenario results, the identifiability grid, structural scenarios and the reporting checklist.
