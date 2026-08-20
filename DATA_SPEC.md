# Data Specification & Governance Protocol

**Project**: Physician Exodus from Tunisia: Workforce Projections, Policy Simulation, and Economic Evaluation to 2050  
**Status**: Specification Phase (Pre-Ingestion)  
**Classification**: Research Data Governance Document  

---

## 1. Core Data Governance Principles

1. **Zero Synthetic / Fabricated Data**: No fabricated, mocked, or artificially generated numerical values may be used in production or analysis. All model inputs must be tied to verified primary or secondary empirical records.
2. **Data Immutability**: All files placed in `data/raw/` are strictly read-only and immutable. No script or investigator may modify raw files in place.
3. **Idempotent & Scripted Processing**: Every transformation from `data/raw/` to `data/processed/` must be executed via automated R scripts in `R/data_processing/`, fully documented and reproducible with checksum logging.
4. **Data Privacy & De-Identification**: Any microdata involving individual physician identifiers (e.g., CNOM registration numbers, names, personal tax IDs) must be de-identified, hashed, or aggregated prior to inclusion in the modeling pipeline.
5. **Schema Conformance**: All datasets ingested into `data/processed/` must conform to the formal data dictionary and type definitions specified below.

---

## 2. Data Flow Architecture

```
[Primary & Secondary Sources]
  ├── CNOM Tunisia (Order of Physicians)
  ├── Ministry of Health (Ministère de la Santé / Carte Sanitaire)
  ├── Ministry of Higher Education & Medical Faculties
  ├── INS Tunisia (Institut National de la Statistique)
  ├── International Registers (DREES/RPPS France, BÄK Germany, GMC UK, OECD)
  └── Survey / DCE Microdata
               │
               v  (Ingestion with SHA-256 Checksumming)
       +---------------+
       |   data/raw/   |  <-- Strictly Read-Only Raw Files
       +---------------+
               │
               v  (R/data_processing/ scripts + Data Validation Tests)
       +--------------------+
       |  data/processed/   |  <-- Harmonized, Cleaned, Tidy Datasets (.parquet / .rds / .csv)
       +--------------------+
               │
               +---> Logged Schemas & Codebooks in `data/metadata/`
               │
               v
       +--------------------+
       |  Modeling Engines  |  (Discrete Choice, Cohort Simulation, Economic Evaluation)
       +--------------------+
```

---

## 3. Data Source Provenance & Inventory

| Source Identifier | Owning Organization / Institution | Description & Coverage | Format / Access Protocol |
| :--- | :--- | :--- | :--- |
| `SRC_CNOM_ANN` | Conseil National de l'Ordre des Médecins (Tunisia) | Annual registry of licensed physicians, specialty, sector of practice, registration date, good-standing certificates (*attestation de bonne conduite* requested for emigration). | Official reports, periodic census bulletins, formal data requests. |
| `SRC_MS_CARTE` | Ministère de la Santé (Direction des Études et de la Planification) | *Carte Sanitaire* annual statistical reports: public sector physician headcount, hospital bed capacity, equipment by governorate and facility tier (CHU, Regional Hospital, District Hospital, CSB). | Published annual statistical yearbooks (PDF/XLSX). |
| `SRC_MES_FAC` | Ministère de l'Enseignement Supérieur / Facultés de Médecine (Tunis, Sousse, Monastir, Sfax) | Annual medical faculty admissions quotas, student enrollment, residency (*résidanat*) positions by specialty, thesis completions. | Official ministerial bulletins, faculty annual reports. |
| `SRC_INS_DEM` | Institut National de la Statistique (INS) | National population censuses, governorate-level population estimates and demographic projections by age and sex to 2050. | Public statistical portal, census microdata extracts. |
| `SRC_BCT_MAC` | Banque Centrale de Tunisie (BCT) & INS | Macroeconomic indicators: annual GDP, CPI inflation, health sector public expenditures, TND/EUR and TND/USD historical exchange rates. | Official statistical bulletins. |
| `SRC_INT_DREES`| DREES & Conseil National de l'Ordre des Médecins (France) | Foreign-trained and foreign-born physicians practicing in France (*praticiens à diplôme hors Union Européenne* - PADHUE, RPPS registry data). | DREES Open Data portal / RPPS annual tables. |
| `SRC_INT_BAK`  | Bundesärztekammer (German Medical Association) | Annual statistics of foreign physicians practicing in Germany disaggregated by nationality and country of medical degree. | Annual BÄK statistical reports (*Ärztestatistik*). |
| `SRC_INT_OECD` | OECD Health Statistics & WHO Global Health Observatory | International migration of health workers, cross-national physician density, Tunisian-trained physicians abroad. | OECD.Stat / WHO NHWA database. |
| `SRC_SURV_DCE` | Primary / Secondary Research Surveys | Microdata on physician emigration intentions, job satisfaction scores, and discrete-choice experiment responses. | De-identified tabular survey microdata. |

---

## 4. Target Schemas & Data Dictionaries

### 4.1. Dataset: `physician_stock_annual.parquet`
Harmonized annual stock of practicing physicians in Tunisia.

### 4.1. Dataset: `physician_stock_annual.parquet`
Harmonized annual stock of active practicing physicians in Tunisia (36-cell cohort tensor).
*Baseline Initialization Protocol*: The 36-cell stock distribution at $t_0 = 2020$ is initialized from INS (national public/private totals) and Ministry of Health *Carte Sanitaire* (governorate public headcounts and specialty clusters) marginal distributions via 2-dimensional **Iterative Proportional Fitting (IPF / raking)**.
*Inactivity Adjustment Timing*: The `active_practice_ratio` ($\alpha = 0.88$) is applied strictly as an **initial baseline stock filter at $t_0$** ($\text{headcount\_active}_0 = \alpha \cdot \text{headcount\_raw}_0$). Subsequent annual evolution ($t > 0$) is governed by dynamic demographic stock-flow transitions.

| Field Name | Type | Allowed Values / Range | Description |
| :--- | :--- | :--- | :--- |
| `year` | Integer | $2015 \le \text{year} \le 2050$ | Reference calendar year. |
| `career_stage` | String | `early_resident` (<35 yrs), `mid_career` (35–54 yrs), `senior` (55+ yrs) | Career stage stratum (3 bins). |
| `sector` | String | `public`, `private` | Sector of practice (2 strata). |
| `geography_macro`| String | `coastal_metro` (District of Tunis, Center East), `interior_underserved` (North West, Center West, South) | Geographic planning stratum (2 strata). |
| `specialty_cluster`| String | `general_medicine`, `medical_specialties`, `surgical_critical_care` | Aggregated specialty cluster (3 strata). |
| `migration_status` | String | `active_domestic`, `cumulative_emigrated` | Domestic vs. Emigrated stock pool. |
| `headcount_raw_admin` | Numeric | $\ge 0$ | Raw administrative registration headcount from INS / MS Carte Sanitaire. |
| `active_practice_ratio` | Numeric | $[0.85, 0.90]$ (base = 0.88) | Baseline-only correction factor eliminating inactive / unpurged registrations. |
| `headcount_active` | Numeric | $\ge 0$ | Active practicing stock ($\text{raw} \times \alpha$ at $t_0$; dynamic stock for $t > 0$). |
| `data_source` | String | `SRC_INS_ANN`, `SRC_MS_CARTE`, `SRC_CNOM_ANN` | Provenance source identifier. |

### 4.2. Dataset: `emigration_flows_annual.parquet`
Annual outflow of physicians by career stage, specialty cluster, and destination region.

| Field Name | Type | Allowed Values / Range | Description |
| :--- | :--- | :--- | :--- |
| `year` | Integer | $2015 \le \text{year} \le 2050$ | Reference calendar year. |
| `career_stage` | String | `early_resident`, `mid_career`, `senior` | Career stage at departure. |
| `specialty_cluster` | String | `general_medicine`, `medical_specialties`, `surgical_critical_care` | Specialty cluster. |
| `destination_region` | String | `france_drees`, `germany_bak`, `gulf_gcc`, `north_america_other` | Destination registry/region. |
| `cnom_certificates_raw` | Integer | $\ge 0$ | Raw *Attestations de bonne conduite* requested from CNOM. |
| `clearance_multiplier` | Numeric | $[0.65, 0.90]$ (base = 0.75) | Realization factor mapping certificate requests to border departures ($\lambda_{\text{exit}}$). |
| `flow_realized_est` | Numeric | $\ge 0$ | Realized annual physical departures ($\text{raw} \times \lambda_{\text{exit}}$). |
| `data_source` | String | `SRC_CNOM_ANN`, `SRC_INT_DREES`, `SRC_INT_BAK` | Source identifier. |

### 4.3. Dataset: `training_pipeline_annual.parquet`
Annual throughput of medical education and specialization.

| Field Name | Type | Allowed Values / Range | Description |
| :--- | :--- | :--- | :--- |
| `academic_year` | String | `YYYY-YYYY` (e.g., `2023-2024`) | Academic cohort year. |
| `faculty_id` | String | `FAC_TUNIS`, `FAC_SOUSSE`, `FAC_MONASTIR`, `FAC_SFAX` | Medical faculty. |
| `stage` | String | `admission`, `pcem1`, `pcem2`, `dcfm1`, `dcfm2`, `dcfm3`, `internship`, `residency_entry`, `thesis_defense`, `board_certification` | Stage in the medical training curriculum. |
| `specialty_code` | String | Specialty code or `GENERAL_MEDICINE` / `PRE_SPECIALIZATION` | Specialty allocated (if residency/board). |
| `quota_authorized` | Integer | $\ge 0$ | Ministerial allocated quota (*numerus clausus*). |
| `enrolled_count` | Integer | $\ge 0$ | Actual enrolled student count. |
| `graduated_count` | Integer | $\ge 0$ | Successfully completed/graduated headcount. |

### 4.4. Dataset: `macro_demographic_series.parquet`
Demographic and macroeconomic background series.

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `year` | Integer | Calendar year ($2000 \le \text{year} \le 2050$). |
| `governorate` | String | Governorate identifier (or `NATIONAL` for aggregate). |
| `population_total` | Numeric | Total resident population. |
| `pop_age_65plus_pct`| Numeric | Proportion of population aged 65 and over. |
| `real_gdp_pc_tnd` | Numeric | Real GDP per capita in constant TND. |
| `inflation_cpi` | Numeric | Consumer Price Index inflation rate (%). |
| `exchange_rate_tnd_eur` | Numeric | Average annual TND to EUR exchange rate. |
| `health_exp_pct_gdp`| Numeric | Total health expenditure as % of GDP. |

### 4.5. Dataset: `dce_survey_microdata.parquet`
Microdata for discrete-choice modeling (de-identified).

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `respondent_id` | String | Anonymized unique physician respondent token. |
| `choice_set_id` | Integer | Choice task index per respondent ($1, \dots, T$). |
| `alternative_id` | Integer | Alternative within choice task ($1, 2, \dots, J$). |
| `choice` | Integer (0/1) | Chosen alternative indicator (1 = chosen, 0 = otherwise). |
| `attr_monthly_net_income_tnd` | Numeric | Net monthly remuneration attribute in TND. |
| `attr_workplace_condition` | Factor | Infrastructure/equipment quality level (Poor, Standard, Advanced). |
| `attr_location_tier` | Factor | Greater Tunis, Coastal City, Interior Governorate, Abroad (Europe/Gulf). |
| `attr_housing_subsidy` | Factor | None, Standard allowance, Free official housing. |
| `attr_career_acceleration` | Factor | Standard progression, 2-year fast-track promotion. |
| `resp_age` | Integer | Respondent age in years. |
| `resp_sex` | Factor | Biological sex (`M`, `F`). |
| `resp_specialty_group` | Factor | Specialty grouping. |
| `resp_current_sector` | Factor | Public / Private / Resident. |

---

## 5. Data Validation & Quality Assurance Rules

All processed datasets must pass programmatic assertion checks in `tests/test_data_integrity.R`:

1. **Uniqueness**: Primary key uniqueness on compound keys (e.g., `{year, governorate, specialty_code, sector, age_group, sex}`).
2. **Non-negativity**: All count and economic value columns must be $\ge 0$.
3. **Conservation**: Total regional physician headcount must sum to national total ($\sum_{r} S_{r,t} = S_{\text{national}, t}$).
4. **Referential Integrity**: All foreign keys (governorate codes, specialty codes, faculty IDs) must resolve to standardized lookup tables in `data/metadata/`.
5. **No Undocumented Imputation**: Missing values must be encoded explicitly as `NA` with imputation protocols logged in `data/metadata/imputation_log.md`.
