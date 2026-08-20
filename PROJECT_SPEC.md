# Project Specification: Physician Exodus from Tunisia

**Title**: Physician Exodus from Tunisia: Workforce Projections, Policy Simulation, and Economic Evaluation to 2050  
**Repository Version**: 0.1.0-alpha  
**Status**: Specification Phase (Pre-Modeling)  
**Projection Horizon**: 2020 (Baseline Calibration) to 2050  

---

## 1. Executive Summary & Research Rationale

The Tunisian health system has historically been recognized for high medical training standards and regional medical leadership. However, escalating physician emigration—driven by macroeconomic deterioration, stagnating public-sector remuneration, worsening hospital working conditions, security concerns, and aggressive recruitment by high-income countries (primarily France, Germany, the Gulf States, and Canada)—poses a structural threat to health system resilience and universal health coverage (UHC).

This study develops an integrated quantitative and health economics framework to:
1. Reconstruct historical and current physician migration trajectories and domestic stock dynamics.
2. Model physician decision-making and retention elasticity using microeconometric choice models.
3. Simulate national and regional physician stock, density, and specialty-mix trajectories through **2050** under baseline and counterfactual policy interventions.
4. Quantify the economic and fiscal consequences of physician flight (public training subsidy loss, replacement costs) and evaluate the cost-effectiveness of targeted retention strategies.

---

## 2. Core Research Questions (RQs)

- **RQ 1 (Workforce & Flow Accounting)**: What has been the absolute and proportional trajectory of physician emigration from Tunisia over the past two decades, disaggregated by specialty, age, sex, and career stage?
- **RQ 2 (Determinant & Preference Econometrics)**: How do macro-level factors (economic crisis, inflation, currency depreciation), meso-level conditions (hospital infrastructure, equipment availability, administrative burden, workplace violence), and micro-level attributes (demographics, specialty, career expectations) interact to shape physician willingness to migrate vs. remain? What is the marginal willingness-to-accept (MWTA) / marginal willingness-to-pay (MWTP) for specific retention package components?
- **RQ 3 (Workforce Trajectory Projections to 2050)**: Under status-quo policies versus alternative counterfactual scenarios (e.g., salary adjustments, workplace enhancements, training quota adjustments, return-of-service reforms), what will be the trajectory of physician density (physicians per 1,000 / 10,000 population) in Tunisia through 2050?
- **RQ 4 (Spatial & Specialty Maldistribution)**: How will physician emigration exacerbate existing regional inequities (coastal vs. interior governorates) and specialty-specific deficits (e.g., anesthesiology, critical care, emergency medicine, oncology)?
- **RQ 5 (Economic Valuation & Policy Cost-Effectiveness)**: What is the fiscal loss in terms of public education investment per emigrating physician? What are the net costs, cost-consequences, and incremental cost-effectiveness ratios (ICERs per physician-year retained) of proposed policy intervention packages?

---

## 3. Theoretical & Conceptual Frameworks

### 3.1. WHO Health Labour Market Framework

The project adopts the World Health Organization (WHO) Health Labour Market Framework (HLMF), which models the entire lifecycle of health personnel:
- **Supply Pipeline**: Secondary education graduates $\rightarrow$ Medical faculty admission quotas $\rightarrow$ Medical school enrollment $\rightarrow$ Internships / Residency (Résidanat) $\rightarrow$ Graduation / Board Certification.
- **Labour Market Entry & Allocation**: Licensure by the Conseil National de l'Ordre des Médecins (CNOM) $\rightarrow$ Sectoral sorting (Public Sector: University Hospitals [CHU], Regional Hospitals, Basic Health Centers; Private Sector: Private clinics, independent practices; Inactivity / Unemployment).
- **Labour Market Dynamics & Attrition**:
  - Domestic mobility (inter-regional migration, public-to-private transfer).
  - Outflow (Emigration, permanent retirement, temporary leave, mortality, profession exit).
  - Inflow (Return migration, foreign-trained returning nationals).
- **Need vs. Demand**: Demographic aging, epidemiological transitions (non-communicable diseases), and healthcare financing driving population health needs versus effective economic demand for services.

```
       +-------------------------------------------------------------+
       |                  Education & Training Pipeline              |
       |  Medical Faculty Entrants -> Interns -> Residents -> Licensure
       +-------------------------------------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |             Health Labour Market Dynamics (Tunisia)         |
       |  +-------------------------------------------------------+  |
       |  | Public Sector (CHU, Regional, Primary Care)           |  |
       |  | Private Sector (Clinics, Solo Practice)               |  |
       |  | Inactive / Non-Clinical                               |  |
       |  +-------------------------------------------------------+  |
       +-------------------------------------------------------------+
                 |                                      ^
                 | Attrition / Emigration               | Return Migration
                 v                                      |
       +-------------------------------------------------------------+
       |             International Labour Market (Exodus)            |
       |  France, Germany, Gulf States, Canada, Other OECD           |
       +-------------------------------------------------------------+
```

### 3.2. Push-Pull Migration Theory

Physician mobility is conceptualized through directional push-pull forces:
- **Push Factors (Tunisia)**:
  - *Macro*: Real wage erosion (TND inflation/devaluation), political instability, social climate.
  - *Meso*: Degradation of public hospital infrastructure, frequent stockouts of essential pharmaceuticals and consumables, legal vulnerability (medical liability law), physical insecurity/violence against healthcare staff, lack of meritocratic career progression.
  - *Micro*: Family obligations, debt, burnout, disillusionment with professional status.
- **Pull Factors (Destination Countries)**:
  - *Macro*: High real incomes, social stability, favorable visa/immigration pathways (e.g., French EVC - Épreuves de Vérification des Connaissances, German Approbation, Gulf tax-free packages).
  - *Meso*: State-of-the-art medical technology, structured continuous medical education, supportive staffing ratios, research funding.
  - *Micro*: International recognition, children's educational opportunities.

### 3.3. Macro-Meso-Micro Determinants Hierarchy

Determinants of the migration decision are structured hierarchically:

| Level | Dimension | Indicators / Variables |
| :--- | :--- | :--- |
| **Macro** | Economic & Structural | Real GDP growth, inflation rate, TND/EUR and TND/USD exchange rates, public health expenditure as % of GDP, national health workforce financing. |
| **Macro** | Policy & Bilateral | International recruitment agreements, destination credentialing regulations, visa policies, mandatory civil service laws. |
| **Meso** | Institutional & Clinical | Hospital category (CHU, Regional, Local), equipment functionality index, drug availability index, security incidents/violence, bed-to-nurse ratio, administrative workload. |
| **Meso** | Remuneration & Benefits | Base salary, on-call compensation (*gardes et astreintes*), remote area allowances, private practice rights (*activité privée complémentaire*). |
| **Micro** | Demographic & Professional | Age, gender, marital status, dependent children, medical specialty, years since thesis defense, current rank (Intern, Resident, Specialist, Hospital-University Assistant, Professor). |
| **Micro** | Attitudinal & Psychological | Burnout score (e.g., Maslach Burnout Inventory), perceived professional fulfillment, intention to migrate score. |

---

## 4. Methodological Blueprint

The methodology is organized into four computational modules:

```
[Module 1: Determinants & RUM/DCE]
  Estimates utility weights (beta), elasticities, and MWTP from empirical choice data.
         |
         v
[Module 2: Dynamic Cohort Workforce Simulation]
  Stock-and-flow Markov model projecting cohorts from 2020 to 2050 by state vector (a, s, k, j, r, m).
         |
         v
[Module 3: Policy Counterfactual Simulation]
  Translates policy levers into modified transition probability matrices P_t(policy).
         |
         v
[Module 4: Economic & Cost-Effectiveness Evaluation]
  Computes fiscal training loss, direct policy costs, cost-consequences, and ICERs.
```

### 4.1. Module 1: Random-Utility & Discrete-Choice Econometrics

Individual physician choice between practicing domestically (public/private/location) versus emigrating is formalized under Random Utility Maximization (RUM):

$$U_{nit} = V_{nit} + \varepsilon_{nit} = \mathbf{x}_{nit}' \boldsymbol{\beta}_n + \mathbf{z}_n' \boldsymbol{\gamma}_i + \varepsilon_{nit}$$

where:
- $U_{nit}$ is the latent utility of alternative $i \in \{ \text{Stay Public Urban}, \text{Stay Public Rural}, \text{Private Practice}, \text{Emigrate to Europe}, \text{Emigrate to Gulf}, \dots \}$ for physician $n$ at time $t$.
- $\mathbf{x}_{nit}$ is a vector of alternative-specific attributes (net earnings, working hours, hospital resource availability, housing/relocation subsidy, career advancement rate).
- $\mathbf{z}_n$ is a vector of individual physician characteristics (age, sex, specialty, family status).
- $\boldsymbol{\beta}_n$ represents preference parameters (fixed or random across physicians in mixed multinomial logit formulations).
- $\varepsilon_{nit}$ is an idiosyncratic error term (Gumbel/Type I extreme value distributed for Logit/Mixed Logit models).

From estimated utility parameters, the Marginal Willingness-to-Pay / Accept for policy attribute $k$ relative to compensation $w$ is derived as:

$$\text{MWTP}_k = -\frac{\beta_k}{\beta_{\text{remuneration}}}$$

### 4.2. Module 2: Dynamic Cohort / State-Transition Stock-and-Flow Simulation (2020–2050)

The core projection engine is a discrete-time Markov state-transition model with annual cycles ($t \in \{2020, 2021, \dots, 2050\}$).

The physician workforce stock $\mathbf{S}_t$ is represented by a multi-dimensional state tensor:

$$\mathbf{S}_t(a, s, k, j, r, m)$$

where:
- $a \in [25, 75]$: Age in single years.
- $s \in \{\text{Male}, \text{Female}\}$: Biological sex.
- $k \in \mathcal{K}$: Specialty category ($\approx 40$ disciplines aggregated into core groups: General Practice, Internal Medicine Subspecialties, Surgical Subspecialties, Anesthesiology & Intensive Care, Emergency Medicine, Pediatrics, Obstetrics & Gynecology, Radiology, Laboratory/Pathology, Psychiatry, Public Health).
- $j \in \mathcal{J}$: Sector / Practice mode ($\text{Public CHU}, \text{Public Regional/District}, \text{Private Clinic}, \text{Private Solo Practice}, \text{Inactive}$).
- $r \in \mathcal{R}$: Geographic Region / Governorate (24 governorates aggregated into 7 planning regions: District of Tunis, North East, North West, Center East, Center West, South East, South West).
- $m \in \mathcal{M}$: Migration status ($\text{Domestic Resident}, \text{Emigrated (Europe)}, \text{Emigrated (Gulf)}, \text{Emigrated (North America)}, \text{Emigrated (Other)}, \text{Returned}$).

The state transition update from $t$ to $t+1$ satisfies the master demographic conservation equation:

$$\mathbf{S}_{t+1} = \mathbf{S}_t \mathbf{T}_t(\boldsymbol{\theta}) + \mathbf{I}_{t+1} - \mathbf{O}_{t+1}$$

where:
- $\mathbf{T}_t(\boldsymbol{\theta})$ is the age- and attribute-dependent transition probability matrix, parameterized by policy and economic vector $\boldsymbol{\theta}$.
- $\mathbf{I}_{t+1}$ is the entry vector (newly certified specialists and licensed general practitioners from the 4 medical faculties: Tunis, Sousse, Monastir, Sfax).
- $\mathbf{O}_{t+1}$ is the natural exit vector (all-cause mortality, age-mandated statutory retirement, early retirement, permanent non-migration disability).

### 4.3. Module 3: Policy Counterfactual Simulation

Policy scenarios modify the transition probability matrix $\mathbf{T}_t(\boldsymbol{\theta})$ via the estimated choice elasticities from Module 1. Candidate policy scenarios to be defined in `ASSUMPTIONS.md` include:
1. **Scenario 0 (Status Quo Baseline)**: Continuation of current trends, real wage trajectories, and destination recruitment pulls.
2. **Scenario 1 (Public Sector Remuneration Enhancement)**: Structural base salary increase and performance-based retention bonuses.
3. **Scenario 2 (Workplace & Infrastructure Modernization)**: Targeted capital investment improving hospital equipment availability and security personnel.
4. **Scenario 3 (Targeted Regional Incentive Package)**: Differentiated financial bonuses, housing provisions, and accelerated promotion for practicing in underserved interior governorates.
5. **Scenario 4 (Medical Training Capacity Adjustment)**: Expansion or contraction of residency (*résidanat*) quotas in shortage specialties.
6. **Scenario 5 (Comprehensive Multi-Component Strategy)**: Synergistic bundle combining compensation, workplace safety, regional incentives, and return-of-service terms.

### 4.4. Module 4: Economic & Cost-Effectiveness Evaluation

#### 4.4.1. Public Education Investment & Human Capital Valuation
The net fiscal loss per emigrating physician is quantified using the Human Capital / Direct Replacement Cost methodology:

$$\text{Loss}_{\text{training}} = \sum_{y=1}^{Y} C_{\text{direct}, y} \cdot (1 + r)^{Y-y} + C_{\text{clinical\_internship}} + C_{\text{residency\_subsidy}}$$

where $C_{\text{direct}, y}$ is the annual public operating expenditure per medical student, $Y$ is duration of medical training (9 to 12 years depending on specialty), and $r$ is the social discount rate.

#### 4.4.2. Cost-Consequence Analysis (CCA)
A disaggregated balance sheet presenting all direct implementation costs (budgetary outlays for salary increases, equipment, infrastructure) alongside multidimensional health system consequences:
- Total physician-years retained domestically (2020–2050).
- Physician density change in underserved interior regions.
- Specialist density preservation in critical shortage specialties (e.g., intensive care, anesthesia).
- Estimated averted service disruption hours.

#### 4.4.3. Cost-Effectiveness Analysis (CEA)
Calculation of the Incremental Cost-Effectiveness Ratio (ICER):

$$\text{ICER}_{A \text{ vs } B} = \frac{\Delta \text{Cost}_{A-B}}{\Delta \text{Physician-Years Retained}_{A-B}}$$

All future costs and outcomes will be discounted at baseline standard rates (3% and 5% annual discount rates tested in sensitivity analysis).

---

## 5. Computational & Software Standards

- **Core Analytical Language**: R ($\ge 4.3.0$).
- **Key Package Ecosystem**:
  - Econometrics / Choice Modeling: `apollo`, `mlogit`, `survival`.
  - Dynamic Simulation & Matrix Algebra: `Rcpp`, `matrixStats`, `data.table`.
  - Sensitivity Analysis & Uncertainty Quantification: `lhs`, `sensitivity`, `purrr`.
  - Validation & Testing: `testthat`, `checkmate`.
- **Reproducibility Rules**:
  - Deterministic random seed management for all Monte Carlo / PSA draws.
  - Configuration-driven parameter ingestion (no hardcoded parameters in simulation scripts).
  - Explicit pipeline orchestration (e.g., `targets` or modular Make/script pipelines).
