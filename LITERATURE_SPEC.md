# Literature Review & Evidence Synthesis Protocol

**Project**: Physician Exodus from Tunisia: Workforce Projections, Policy Simulation, and Economic Evaluation to 2050  
**Status**: Protocol Specification (Pre-Synthesis)  
**Taxonomy Target**: `literature/` Subdirectory Hierarchy  

---

## 1. Overview & Objectives

The literature synthesis serves three distinct functions in this research project:
1. **Contextual & Policy Synthesis**: Documenting historical policy reforms, legal statutes (e.g., medical liability laws, mandatory civil service decrees), and institutional structures in Tunisia.
2. **Empirical Parameter Extraction**: Extracting rigorously documented parameter distributions (transition probabilities, attrition rates, training costs, income differentials) without resorting to arbitrary parameter assumptions.
3. **Methodological Calibration**: Grounding the econometric choice models and dynamic Markov simulation in established international best practices.

---

## 2. Literature Directory Taxonomy

The `literature/` folder is partitioned into four dedicated domains:

```
literature/
├── tunisia/          # Country-specific evidence, ministerial reports, CNOM data, national studies
├── north_africa/     # Regional Maghreb & MENA comparative health workforce studies
├── international/    # Global health worker mobility, OECD destination studies, WHO frameworks
└── methods/          # Methodological literature: RUM/DCE, Markov modeling, CEA/CCA
```

### 2.1. `literature/tunisia/`
- **Scope**: Studies specifically examining the Tunisian medical profession, physician emigration trends, public hospital conditions, resident physician satisfaction, medical faculty graduation outputs, and regional distribution across the 24 governorates.
- **Key Document Types**:
  - Peer-reviewed articles in *La Tunisie Médicale*, *Maghreb Médical*, and international journals.
  - Official publications from the Ministère de la Santé (Direction des Études et de la Planification, *Carte Sanitaire*).
  - Official bulletins and statistics from the Conseil National de l'Ordre des Médecins (CNOM).
  - Reports from medical unions and associations (e.g., Syndicat des Médecins, Pharmaciens et Médecins Dentistes de Santé Publique; Organisation Tunisienne des Jeunes Médecins - OTJM).
  - Academic theses (thèses de doctorat en médecine, thèses en sciences économiques/santé publique).

### 2.2. `literature/north_africa/`
- **Scope**: Health workforce and medical migration literature from Algeria, Morocco, Egypt, Lebanon, and Jordan.
- **Purpose**: Provides regional comparative benchmarks for push-pull drivers, rural retention schemes, public-private wage ratios, and remittance patterns across culturally and structurally similar health systems.

### 2.3. `literature/international/`
- **Scope**: Destination country policies, global brain drain dynamics, and multilateral codes of practice.
- **Key Topics**:
  - French integration mechanisms: *Praticiens à diplôme hors Union Européenne* (PADHUE), *Épreuves de Vérification des Connaissances* (EVC), and *Autorisation d'Exercice*.
  - German medical immigration: *Approbation* and *Berufserlaubnis* pathways for non-EU doctors.
  - Gulf Cooperation Council (GCC) recruitment packages and tax-free contracts.
  - OECD health workforce migration monitoring and WHO Global Code of Practice on the International Recruitment of Health Personnel.

### 2.4. `literature/methods/`
- **Scope**: Mathematical, econometric, and epidemiological modeling literature.
- **Key Methodological Areas**:
  - Discrete Choice Experiments (DCE) in health workforce preferences and LMIC meta-analyses (Mandeville et al. 2014, Lancsar, Louviere, Ryan, Lagarde, Blaauw).
  - Random Utility Maximization (RUM) and mixed multinomial logit formulations (Train, Hensher, Greene).
  - Odds Ratio to Relative Risk conversion under high baseline prevalence (Zhang & Yu, *JAMA* 1998).
  - Intention-to-action realization gaps in migration economics (Docquier, Peri, & Ruyssen 2014; Clemens & Mendola 2020; Creighton 2013).
  - Dynamic cohort, stock-and-flow, and Markov state-transition models for health workforce planning (WHO 2021, AAMC/Zhang et al. 2020, Ono et al., Birch et al., Amorim-Lopes et al. 2019).
  - Cost-consequence (CCA) and cost-effectiveness (CEA) methodologies applied to human resources for health (Drummond et al. 2015, Sanders et al. 2016 Second Panel, WHO-CHOICE guidelines).

---

## 3. Systematic Search & Extraction Protocol

### 3.1. Bibliographic Search Strategy
- **Databases**: PubMed/MEDLINE, Embase, Web of Science, Scopus, Cairn.info, Google Scholar, and WHO IRIS.
- **Search Terms (Multilingual: English & French)**:
  - Concept 1 (Population): `("physician*" OR "doctor*" OR "medical specialist*" OR "resident*" OR "médecin*" OR "interne*")`
  - Concept 2 (Migration/Workforce): `("emigration" OR "migration" OR "brain drain" OR "mobility" OR "retention" OR "shortage" OR "maldistribution" OR "exode" OR "fuite des cerveaux")`
  - Concept 3 (Geography): `("Tunisia" OR "Tunisie" OR "North Africa" OR "Maghreb" OR "MENA")`
- **Grey Literature Screening**: Hand-searching official websites of the Tunisian Ministry of Health, CNOM, INS, DREES, Bundesärztekammer, and WHO EMRO.

### 3.2. Evidence & Parameter Extraction Log Template

Every empirical parameter used to inform model structures, initial states, or transition probabilities must be cataloged in `literature/parameter_extraction_matrix.csv` with the following schema:

| Column Name | Description | Example |
| :--- | :--- | :--- |
| `param_id` | Unique parameter identifier | `PAR_MIG_PROB_RES_01` |
| `study_citation` | Full bibliographic citation | Ben Salem et al. (2022) |
| `doi_or_url` | Direct DOI or institutional URL | `10.1016/j.tunmed.2022.04.012` |
| `target_variable` | Specific parameter represented in model | Annual intention/rate to emigrate among residents |
| `stratum_specialty` | Specialty group applicability | General Surgery / Anesthesiology |
| `stratum_sector` | Sector applicability | Public CHU |
| `stratum_experience` | Experience / Career stage | Residents ($<35$ years) |
| `point_estimate` | Empirical mean or median value | `0.65` (65% intention) |
| `ci_lower` | 95% Confidence interval lower bound | `0.58` |
| `ci_upper` | 95% Confidence interval upper bound | `0.72` |
| `distribution_type` | Fitted or reported parametric distribution | Beta($\alpha=32.5, \beta=17.5$) |
| `sample_size` | Empirical sample size ($N$) | `420` |
| `method_type` | Study design (Survey, Administrative Registry, DCE) | Cross-sectional survey |
| `quality_score` | Risk of bias / quality rating (Low, Moderate, High) | Moderate |
| `notes_rationale` | Contextual notes and parameter bounds | Conducted across 4 university hospital centers |

---

## 4. Synthesis Synthesis Outputs

The findings from this protocol will generate two foundational outputs prior to model execution:
1. `literature/evidence_synthesis_summary.md`: Narrative synthesis structured by the Macro-Meso-Micro determinant hierarchy and Push-Pull dynamics.
2. `data/metadata/parameter_dictionary.json`: Machine-readable parameter priors, uncertainty bounds, and distribution families ready for ingestion by the simulation engine in `R/`.
