# Evidence and data assessment

## 1. Scope and approach

This document summarises the evidence used to design and parameterise a
supply-side projection model of Tunisia's physician workforce. It focuses on
four questions:

1. What is known about the drivers and policy responsiveness of physician
   migration and retention?
2. Which projection methods are appropriate when migration flows are poorly
   observed?
3. What Tunisian data exist, with which definitions and limitations?
4. Which quantities can be estimated from those data, and which cannot?

The review prioritises peer-reviewed research, official statistics and
methodological publications. Grey literature and press reports are used only
where they are the sole source (notably annual emigration estimates), and are
labelled as such.

## 2. International evidence on physician migration and retention

Physician migration is driven by wage differentials, working conditions,
career and training opportunities, political and economic stability, and
linguistic and diasporic ties. A 25-year database covering 192 origin and 22
destination countries shows that migration is strongly shaped by origin and
destination income, by bilateral ties, and by destination-country immigration
policy (visa rules, diploma recognition, points systems, permanent residence)
[1]. This matters for Tunisia because France and Germany — its two largest
recorded destinations — have both expanded active recruitment and
regularisation pathways for non-EU-trained physicians.

The causal evidence on retention is modest but consistent. In Ghana, a 10%
increase in public-sector wages reduced annual attrition among young health
workers from about 8% to about 7% — a 12.5% relative reduction — with the
effect concentrated among 20–35-year-olds in migrating occupations [2]. A
separate evaluation found that the Ghanaian wage reform reduced the stock of
Ghanaian doctors abroad by about 10% six years later [3]. These estimates imply
that pay matters, but that even substantial pay increases do not eliminate
emigration. Working conditions, security, workload and career progression are
consistently ranked as important in surveys, but credible quantitative
estimates of their independent effects are scarce [4].

Return migration is common enough to matter. In Hungary, more than half of the
doctors who left during 2003–2011 returned at some point [5]. Return is
influenced by relative wages, family circumstances and opportunities at home.
There is, however, almost no quantitative evidence on return to Tunisia, and
no reliable diaspora register that would allow return flows to be measured.

The WHO Global Code of Practice on the International Recruitment of Health
Personnel provides the normative framework, but it is voluntary and has not
prevented active recruitment from Tunisia [6].

## 3. Health workforce projection methods

Three families of models are relevant.

**Cohort-component stock-and-flow models.** The workforce is represented as a
stock by age (and sometimes sex), updated annually or quinquennially by
entries, exits and migration. This is the dominant approach in national and
international workforce planning. The JRC SANDEM model is a recent, well
documented example: it projects practising doctors and nurses by five-year age
group for EU member states, holds migration flows at their base-year level,
and explicitly acknowledges that outflows (emigration, dropout, retirement) are
the weakest data component [7,8]. SANDEM combines the supply model with a
demand model, but its supply side is a conventional cohort projection.

**System dynamics models.** These add feedback between supply, demand, wages
and training capacity. They are useful for long-run policy analysis but require
behavioural parameters that are unavailable for Tunisia.

**Agent-based models.** These simulate individual physicians' decisions and can
represent heterogeneity and emergent dynamics. The Portuguese physician
workforce model is the most directly relevant example [9]. It is a stochastic
agent-based simulation calibrated to the Portuguese health system, and its
Monte Carlo analysis shows that small errors in emigration or dropout rates can
produce widely divergent long-run forecasts. That finding is directly relevant
to Tunisia: parameter uncertainty, not model complexity, is the binding
constraint.

A systematic review of health workforce projection models identified eight
model types and seven statistical approaches, and proposed a 30-item good
practice reporting guideline covering model structure, data, assumptions,
uncertainty and validation [10]. We follow that guideline (see
`03_reporting_checklist.md`). WHO's operational guidance makes the same point
in simpler terms: projections are conditional statements, not forecasts, and
their value depends on the transparency of their assumptions [11,12].

## 4. Reusable models and code availability — verified

We checked whether the two most relevant models could be adapted directly.

- **SANDEM (JRC).** The model is documented in two technical reports with a
  full description of data sources and structure [7,8]. We searched GitHub for
  repositories matching "SANDEM healthcare workforce" and found none, and the
  JRC reports do not link to a public code repository. The model is therefore
  **documented but not publicly available as code**.
- **Portuguese physician ABM.** The model is described in a peer-reviewed
  article [9] and a working paper. We found no public code repository linked to
  either. It is therefore **not reusable as software**.

We consequently implemented a transparent cohort-component model from published
mathematical structures rather than adapting either model. Resemblance to
SANDEM's architecture is a methodological choice, not a validation: the
Tunisian model is not SANDEM, has different parameters and data, and has not
been externally validated.

Other open-source workforce tools exist (for example, WHO's Workload
Indicators of Staffing Needs and various national models), but they either
require service-level data that Tunisia does not publish or model demand rather
than the migration question of interest here.

## 5. Tunisian data: sources, definitions and limitations

### 5.1 The central definitional problem

Four different quantities circulate in policy debate:

| Quantity | 2021–2024 magnitude | What it counts |
|---|---|---|
| Physicians **born** in Tunisia | Not directly observed | Country of birth, regardless of training or practice |
| Physicians **trained** in Tunisia | Not directly observed as a stock | Graduates of Tunisian medical schools, wherever they practise |
| Physicians **registered** with the CNOM | 27,097 (2021); 27,935 (2022); 31,804 directory records (2026) | All inscriptions, including inactive, retired, administrative and deceased physicians, and some physicians practising abroad |
| Physicians **in active practice** in Tunisia | 15,315 (2024) | Public-sector posts plus private practitioners recorded in the carte sanitaire |

The gap between 27,935 registrations and 15,315 practising physicians is
**not** an estimate of the diaspora. It includes physicians who have retired,
died, left clinical work for administration, or never practised, as well as
possible double counting. Conversely, the practising count may exclude some
private practitioners and residents. The ITES report makes this point
explicitly, noting that the CNOM registered 27,097 physicians in 2021 while the
carte sanitaire recorded 16,199 in exercise, and attributing the difference to
inactive and administrative physicians [13].

### 5.2 Stock data

The INS publishes an annual series of "médecins" compiled by the Ministry of
Health, split into public-sector and private-sector physicians:

| Year | Total | Public | Private |
|---|---|---|---|
| 2017 | 14,892 | 6,753 | 8,139 |
| 2018 | 15,136 | 6,783 | 8,353 |
| 2019 | 15,426 | 6,843 | 8,583 |
| 2020 | 14,792 | 6,118 | 8,674 |
| 2021 | 14,981 | 6,252 | 8,729 |
| 2022 | 15,013 | 6,116 | 8,897 |
| 2023 | 15,108 | 5,911 | 9,197 |
| 2024 | 15,315 | 6,113 | 9,202 |

Source: INS / Ministry of Public Health [14]; 2023 values also in the carte
sanitaire [15].

The series is the best available measure of the practising stock, but it has
three limitations. First, the 2020 public-sector count falls by 725 in one year,
which is too large to be a real retirement or emigration effect and probably
reflects a reporting or establishment-count change. Second, the private-sector
count is based on CNOM records and may lag actual entry. Third, the series does
not distinguish generalists from specialists or residents; the 2023 carte
sanitaire reports 5,674 generalists and 9,434 specialists [15].

For 2023, the carte sanitaire reports 5,911 public and 9,197 private physicians,
with 2,396 public generalists, 3,515 public specialists, 3,278 private
generalists and 5,919 private specialists [15].

### 5.3 Training output

Tunisia has four public medical faculties (Tunis, Sousse, Monastir, Sfax). In
2021/22, 9,946 students were enrolled in doctorate programmes in medicine,
dentistry and pharmacy, and 1,675 graduated across the three fields [13]. The
number of medical graduates alone is not published as a clean annual series.
Zehnati, using official data, estimates 987 medical graduates in 2013 and 1,128
in 2021, an average of 1,087 per year [16]. More recent ministerial statements
cite 1,300–1,900 graduates per year, and the government announced a 30%
increase in medical-school admissions in 2025 [17,18].

The number of residency posts opened each year has risen from 200–250 in the
1980s to about 550 in 2015 and more than 2,000 today, including family-medicine
posts [13]. This is consistent with a graduate cohort in the low thousands and
with a large share of graduates entering postgraduate training.

### 5.4 Emigration flows

No official annual emigration series exists. The available indicators are
heterogeneous:

| Indicator | Period | Value | Interpretation |
|---|---|---|---|
| Certificates of good conduct issued | 2011 | 749 | Proxy for intent to work abroad; also required for other purposes |
| Certificates of good conduct issued | 2022 | 1,110 | Same |
| Certificates of good conduct issued | H1 2023 | 732 | Same |
| Requests for removal from the CNOM register | H1 2023 | 187 | Closest administrative proxy for permanent exit, but many emigrants do not request removal |
| Physicians who prepared a departure file | 2021 | 975 | Media-reported; definition unclear |
| Reported departures | 2023 | 1,325 | Trade-union estimate |
| Reported departures | 2024 | ~1,400 (range 1,300–1,450) | CNOM statement |
| Reported cumulative departures | 2020–2023 | ~4,000 | CNOM statement; 80% described as young physicians |
| Reported cumulative departures | 2017–2021 | ~3,100 | CNOM statement |

Sources: CNOM via ITES [13]; press reports [19,20].

These indicators are not interchangeable. Certificates of good conduct are
issued for many purposes and do not prove departure. Removal from the register
is a legal act that many emigrants never complete. Trade-union and CNOM figures
are not based on a published, reproducible flow series. The 1,300–1,450 annual
figures are widely cited but cannot be reconciled with the observed stock path
unless training output is at the top of its plausible range or emigration is
offset by large return flows. This tension is central to the modelling
strategy and is analysed explicitly rather than resolved by assumption.

### 5.5 Migration intentions

Survey evidence consistently finds high intention to emigrate among young
doctors:

- 38.5% of young doctors in Sousse university hospitals reported an immigration
  project in 2019 [21].
- 53.6% of interns and residents in a 2022 online survey reported plans to
  immigrate [22].
- 68% of residents in a 2024 survey expressed intention to emigrate [23].
- A 2025 survey by the Tunisian Organisation of Young Doctors is reported to
  have found 90% intention, but this figure is not peer-reviewed and is based
  on a self-selected sample [24].

Intentions are not flows. They are useful for understanding motives and for
designing policy, but they cannot be converted into emigration rates without
strong and untestable assumptions. We therefore do not use intention prevalence
to calibrate emigration.

### 5.6 Policy context

The main recent policy is a 30% expansion of medical-school admissions,
announced in 2025 [17]. Other proposals include salary increases, reform of the
internship and residency status, limits on working hours, and bilateral
agreements. None has been evaluated with a credible counterfactual. This is why
the model treats policy effects as explicit, range-tested assumptions rather
than estimated causal parameters.

## 6. Destination-country data

Recorded stocks of Tunisian-trained physicians abroad are incomplete but
informative:

- **France:** 266 in 2010 and 1,591 in 2023, or 10.4% of physicians in France
  with a non-EU diploma [25]. This excludes Tunisian physicians working in
  France without CNOM registration (for example, some assistants associés and
  PADHUE in precarious status).
- **Germany:** 881 Tunisian physicians recorded at 31 December 2022, up 7.8%
  year-on-year [13].
- **OECD total:** approximately 4,000 Tunisian-born physicians in OECD
  countries in 2015/16, up from about 3,200 in 2010/11 [13,26]. This is a
  country-of-birth estimate, excludes Gulf states and other non-OECD
  destinations, and may undercount recent graduates.

Destination stocks are therefore **lower bounds** on the diaspora, and cannot
be used to derive annual flows without information on return and mortality.

## 7. What can and cannot be estimated

The data support a credible projection of the **total practising stock** under
explicit assumptions. They do not support estimation of:

- the true annual emigration flow;
- age-specific emigration rates;
- the split between temporary and permanent emigration;
- return migration rates;
- specialty-specific or public/private flows;
- the causal effect of any policy.

The fundamental identification problem is simple. With an observed stock
series, only the **net** change is observed:

> ΔN(t) = entries(t) − emigration(t) − retirements(t) + returns(t)

Entries depend on the number of graduates and on how many enter Tunisian
practice; emigration is unobserved. Different combinations of training output,
pipeline retention and emigration reproduce the same stock path equally well.
The model therefore fixes training output from external evidence, calibrates
the emigration level to the 2024 stock, and represents the remaining ambiguity
through an explicit identifiability analysis and probabilistic sensitivity
analysis.

## 8. Implications for the modelling strategy

The evidence supports a parsimonious, age-structured stock-and-flow model with:

- a single practising-physician stock, calibrated to the INS/MoH series;
- entry from graduates after a five-year postgraduate lag;
- emigration represented as a total annual flow allocated by an assumed age
  profile, with a separately parameterised pre-entry component;
- retirement at legally plausible ages;
- return migration from a diaspora pool;
- explicit separation of observed, estimated and assumed parameters;
- probabilistic uncertainty analysis and structural sensitivity analysis;
- no demand side, no wages and no behavioural optimisation.

This design is appropriate for incomplete national data: it contains few
parameters, each of which can be linked to a source or explicitly labelled as
an assumption.

## References

1. Adovor E, Czaika M, Docquier F, Moullan Y. Medical brain drain: how many,
   where and why? *J Health Econ.* 2021;76:102409.
   doi:10.1016/j.jhealeco.2020.102409
2. Antwi J, Phillips DC. Wages and health worker retention: evidence from
   public sector wage reforms in Ghana. *J Dev Econ.* 2013;102:101–115.
   doi:10.1016/j.jdeveco.2012.10.004
3. Okeke EN. Do higher salaries lower physician migration? *Health Policy
   Plan.* 2014;29(5):603–614. doi:10.1093/heapol/czt046
4. Labonté R, Sanders D, Mathole T, Crush J, Chikanda A, Dambisya Y, et al.
   Health worker migration from South Africa: causes, consequences and policy
   responses. *Hum Resour Health.* 2015;13:92.
   doi:10.1186/s12960-015-0091-6
5. Varga J. Out-migration and attrition of physicians and dentists before and
   after EU accession (2003 and 2011): the case of Hungary. *Eur J Health
   Econ.* 2017;18:1079–1093. doi:10.1007/s10198-016-0854-6
6. World Health Organization. *WHO Global Code of Practice on the
   International Recruitment of Health Personnel.* Geneva: WHO; 2010.
7. Bernini A, Icardi R, Natale F, Nedee A. *Supply AND DEMand Model for the
   Healthcare Workforce in the EU27: Data Sources and Model Structure.*
   Luxembourg: Publications Office of the European Union; 2024.
   doi:10.2760/957386
8. Bernini A, Icardi R, Natale F, Nedee A. *Healthcare Workforce Demand and
   Supply in the EU27.* Ispra: Joint Research Centre; 2024.
   doi:10.2760/1683259
9. Lopes MA, Almeida ÁS, Almada-Lobo B. Forecasting the medical workforce: a
   stochastic agent-based simulation approach. *Health Care Manag Sci.*
   2018;21(1):52–75. doi:10.1007/s10729-016-9379-x
10. Lee JT, Crettenden I, Tran M, Miller D, Cormack M, Cahill M, et al. Methods
    for health workforce projection model: systematic review and recommended
    good practice reporting guideline. *Hum Resour Health.* 2024;22:25.
    doi:10.1186/s12960-024-00895-z
11. World Health Organization. *Models and Tools for Health Workforce Planning
    and Projections.* Human Resources for Health Observer No. 3. Geneva: WHO;
    2010.
12. World Health Organization. *National Health Workforce Accounts: A
    Handbook.* 2nd ed. Geneva: WHO; 2023.
13. Institut Tunisien des Études Stratégiques. *La migration des professionnels
    de santé: défis pour le système de santé tunisien.* Tunis: ITES; 2024.
14. Institut National de la Statistique / Ministère de la Santé. Personnel
    médical [database]. Tunis: INS; 2026.
15. Ministère de la Santé. *Carte sanitaire 2022–2023: synthèse.* Tunis:
    Direction des études et de la planification; 2024.
16. Zehnati A. L'émigration des médecins, en particulier vers la France, et la
    desserte médicale au Maghreb. *Belgeo.* 2024;(1). doi:10.4000/12ihd
17. Ministère de l'Enseignement Supérieur et de la Recherche Scientifique.
    Annonce d'une hausse de 30% des admissions en médecine. Tunis; 2025.
    (Reported in national press, July 2025.)
18. Kapitalis. La Tunisie, pays du «million» de médecins. 21 February 2026.
19. La Presse de Tunisie. Exode des médecins: près de 1.450 médecins ont fui la
    Tunisie en 2024. 7 January 2025.
20. La Presse de Tunisie. 975 médecins ont préparé un dossier de départ en
    2021. 10 February 2022.
21. Ajmi M, Kahloul M, Kacem I, Chouchane A, Ben Mansour S, Slama Y, et al.
    Immigration projects among young doctors in Tunisia: prevalence,
    destinations and causes. *Eur Psychiatry.* 2022;65(S1):S633–S634.
    doi:10.1192/j.eurpsy.2022.1624
22. Tabib F, Guermazi F, Zouari A, Ben Abdallah M, Hentati S, Baati I, et al.
    Emigration intentionality among Tunisian interns and residents in
    medicine. *Eur Psychiatry.* 2022;65(S1):S633.
    doi:10.1192/j.eurpsy.2022.564
23. Haouari W, Omri S, Labyadh A, Feki R, Gassara I, Charfi N, et al. Factors
    driving the emigration intentions of young Tunisian medical professionals.
    *Eur Psychiatry.* 2024;67(S1):S829–S830.
    doi:10.1192/j.eurpsy.2024.1731
24. Dalhoumi L. *Working Conditions for Junior Doctors in Tunisia: A Priority
    for the Public Health Sector.* Public Policy Paper 2025/20. Tunis: Al
    Bawsala; 2025.
25. Conseil National de l'Ordre des Médecins (France). *Atlas de la démographie
    médicale en France: situation au 1er janvier 2023.* Paris: CNOM; 2023.
26. OECD. Database on Immigrants in OECD Countries (DIOC), 2010/11 and
    2015/16. Paris: OECD; 2018.
27. Arah OA. The metrics and correlates of physician migration from Africa.
    *BMC Public Health.* 2007;7:83. doi:10.1186/1471-2458-7-83
28. Mills EJ, Kanters S, Hagopian A, Bansback N, Nachega J, Alberton M, et al.
    The financial cost of doctors emigrating from sub-Saharan Africa: human
    capital analysis. *BMJ.* 2011;343:d7031. doi:10.1136/bmj.d7031
