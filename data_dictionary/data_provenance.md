# Data provenance and data dictionary

**Model version:** 3.0.0  
**Manuscript:** Retention, return or training? A stock-and-flow simulation of Tunisia's physician workforce under incomplete migration data  
**Last verified:** 24 November 2026

This document records the source, access, transformation, cleaning and limitations of every input used by the model. The processed CSVs are in `data/processed/`; raw source documents are in `data/raw/` for audit verification.

## 1. `tunisia_physician_workforce.csv`

**Source:** Institut National de la Statistique (INS), “Personnel médical”, https://www.ins.tn/statistiques/123 (accessed 24 November 2026); source line: Ministère de la Santé; table updated 3 February 2026. The 2022–2023 Carte sanitaire is used as a cross-check.

**Years:** 2010, 2017–2024. The 2010 value is used only as an initial-condition anchor. The model's historical reconstruction starts in 2008.

**Variables:**

| Column | Definition | Unit | Transformations |
|---|---|---|---|
| `year` | Calendar year | year | — |
| `physicians_total` | Physicians in active practice (public + private) | physicians | 2017–2024: public + private; 2010: WHO/UN estimate |
| `public_sector` | Public-sector physicians | physicians | Used for the public share and the 2020 discontinuity check |
| `private_sector` | Private practitioners | physicians | Used for the total and the 2020 check |
| `definition` | Definition used | text | — |
| `source` | Source | text | — |
| `notes` | Data-quality notes | text | — |

**Cleaning decisions:**

- The total is the sum of public and private counts for 2017–2024. Where the source reports a total that differs by rounding, the public + private sum is used.
- The 2010 value (12 996) is not used in the 2017–2024 fit; it anchors the 2008 initial stock after scaling to 12 600.
- The 2020 public-sector count (6 118) is 725 below 2019 (6 843), while the private count rose by 91. The total fell by 634. This is treated as an unresolved reporting or reclassification discontinuity, not as migration. The model reports fit with and without 2020–2021 and calibrates to 2019/2022 as a sensitivity.

**Known limitations:**

- Public/private classification may change across years.
- The series excludes most residents.
- The 2020–2021 break is not fully explained.
- The 2017–2024 series is a count of practising physicians, not CNOM registration.

**Redistribution:** public aggregate data; can be redistributed with attribution to INS/Ministry of Health. The raw PDFs remain subject to the publisher's terms.

## 2. `tunisia_registration_and_flows.csv`

**Source:** CNOM *Rapport moral 2021–2022*; CNOM *Tableau de l'Ordre*; ITES 2024; La Presse (2022, 2025); Tunisie Numérique (2024); CNOM France *Atlas 2023*; German medical statistics via ITES; OECD DIOC.

**Years:** 2009–2026 (mixed).

**Variables:**

| Indicator | Definition | Unit | Status |
|---|---|---|---|
| `cnom_registered` | Physicians inscribed on the national register (active + inactive) | physicians | Observed |
| `cnom_registered_indexed` | Records indexed in the CNOM public directory | records | Observed directory count, not active practice |
| `new_cnom_registrations` | New inscriptions | physicians | Observed |
| `certificats_bonne_conduite` | Certificates of good conduct issued | certificates | Observed proxy |
| `radiations` | Requests to be removed from the register granted | physicians | Observed proxy |
| `departure_files` | Physicians who prepared a departure file | physicians | Media-reported |
| `emigration_reported` | Physicians reported to have left | physicians | Media-reported |
| `stock_in_france` | Tunisian-diploma physicians registered with the French Order | physicians | Observed destination stock |
| `stock_in_germany` | Tunisian physicians in German medical statistics | physicians | Observed destination stock |
| `stock_in_oecd` | Tunisian-born physicians in OECD countries | physicians | Indirect estimate |

**Cleaning decisions:**

- The indicators are kept separate; they are not combined into a flow series.
- The 2024 departure figure is “près de 1 450” from La Presse (7 January 2025), not 1 400.
- The 2023 figure is 1 325 (Tunisie Numérique, 20 March 2024).
- The 2021 departure-file figure is 975 (La Presse, 10 February 2022).
- Destination stocks use country of diploma (France), country of training/nationality (Germany), and country of birth (OECD); they are lower bounds and not directly comparable.

**Known limitations:**

- Registration is not active practice.
- Media-reported departures are not a validated flow series.
- Destination counts use different definitions and years.
- The 31 804 directory records are a website count, not a practising count.

**Redistribution:** public aggregate data; cite the original sources. Do not redistribute the raw PDFs without permission.

## 3. `population_tunisia.csv`

**Source:** INS RGPH 2024 census; UN World Population Prospects 2024.

**Years:** 2010–2040.

**Variables:**

| Column | Definition | Unit |
|---|---|---|
| `year` | Calendar year | year |
| `population` | Resident population | persons |
| `source` | Source | text |
| `note` | Transformation | text |

**Cleaning decisions:**

- 2024 = 11 972 169 (INS census).
- Other years: WPP 2024 rescaled to the 2024 census by the factor 0.97516.
- 2040 = 12 632 123.
- Population is used only for density denominators (physicians per 1 000 population).

**Known limitations:**

- WPP projections are uncertain.
- The rescaling is a simple proportional adjustment, not a full demographic reconciliation.
- Density is a crude indicator; it does not measure need, access or adequacy.

**Redistribution:** public aggregate data; cite INS and UN WPP.

## 4. Medical doctorates

**Source:** Zehnati A. *L'émigration des médecins, en particulier vers la France, et la desserte médicale au Maghreb*. Belgeo. 2024. doi:10.4000/12ihd.

**Values:**

- 987 doctorates in 2013.
- 1 128 doctorates in 2021.
- Average annual growth 2013–2021: 1.7%.
- 1 305 in 2024: **extrapolated at 5.0% per year** from 2021. This value is not in Zehnati 2024. It reflects the reported acceleration and is an assumption, not an observation.
- Baseline after 2024: constant at 1 305.
- Continued-growth alternative: 1 709 by 2040 (1.7%/year).
- Constant-1 900 alternative: unverified press-reported cohort, stress test only.

**Known limitations:**

- The 2024 value is an assumption; a 1.7%/year extrapolation would give about 1 186.
- The doctorate count is the end of DCEM, not entry into practice.
- The track mix and completion rates are assumptions.

**Redistribution:** the article is open access; cite it. The derived 2024 value is an assumption and should be labelled as such.

## 5. Training pathway

**Sources:** Décret n° 95-2601 (1995); Décret n° 93-1440 (1993); Décret n° 2011-4132 (2011); Décret gouvernemental n° 2019-341 (2019); Arrêté of 10 May 2023; Loi n° 2004-1 (2004).

**Values:**

- PCEM 2 years + DCEM 4 years (including internship) = 6 years.
- TCEM: family medicine 3 years; other specialties 4–5 years.
- National service: 0–1 year.
- Total pathway: 9–12 years from admission to independent practice.
- Cohort-specific lag distributions: pre-2011 GPs 0; 2011–2014 family medicine 2; 2015–2018 family medicine 2–3; 2019+ family medicine 3 and specialists 4–5, with 60% national service.

**Known limitations:**

- Legal durations, not observed progression.
- The track mix, completion and national-service take-up are assumptions.
- The 2016–2019 transition is approximated.

**Redistribution:** legal texts are public; cite the Journal Officiel.

## 6. Initial age distribution

**Source:** CNOM *Rapport moral 2007–2008*, registered physicians by five-year age band.

**Transformation:** bands scaled to a 2008 practising stock of 12 600 (WHO 2010: 12 996). The distribution is spread uniformly within each five-year band. Younger and older two-year shifts are tested.

**Known limitations:**

- Registered, not practising, counts.
- Reconstructed, not observed, practising age structure.
- The 2008 stock is an indirect estimate.

**Redistribution:** public aggregate data; cite CNOM.

## 7. Initial return-eligible pool

**Value:** 4 000 in 2008, illustrative.

**Basis:** OECD DIOC country-of-birth estimate of about 4 000 Tunisian-born physicians in OECD countries in 2015/16; CNOM France and German statistics as cross-checks.

**Known limitations:**

- Country of birth does not identify training, prior practice or eligibility to return.
- The pool is an accounting construct, not a measured diaspora.
- Varied 2 000–8 000.

**Redistribution:** derived assumption; no raw data.

## 8. Cost assumptions

**Unit costs (2025 TND, illustrative):**

- Average public-sector compensation: TND 72 000 per physician-year.
- Remuneration increment: 30%.
- Career development: TND 3 000 per practising physician-year.
- Training: TND 250 000 per additional graduate.
- Return programme: TND 40 000 per additional return migrant.

**Known limitations:**

- Not observed budget data.
- Average, not marginal, costs.
- Training cost counted at graduation, not spread over the years of training.
- Career cost applied to all practising physician-years.
- No infrastructure, demand-side or health-gain costs.
- Not a cost-effectiveness, budget-impact or value-for-money analysis.

**Redistribution:** illustrative assumptions; document them, do not present them as official costs.

## 9. What can and cannot be redistributed

| Item | Can be shared? | Conditions |
|---|---|---|
| Processed aggregate CSVs | Yes | Attribute INS, CNOM, ITES, OECD, UN WPP, Zehnati |
| Model code | Yes | MIT License (confirm) |
| Documentation | Yes | CC-BY-4.0 recommended (confirm) |
| Raw source PDFs | Depends on the publisher | Do not redistribute without permission; provide URLs and access dates |
| Individual-level data | None used | — |
| CNOM directory records | No | Website count; not a dataset for redistribution |
| Media-reported departure figures | Cite only | Not a validated dataset |

## 10. Reproducibility note

The processed CSVs were assembled by hand from the sources listed above. The raw PDFs are retained for verification. No scraping is required to reproduce the analysis. The pipeline uses the processed CSVs and the model code; it does not access the internet.
