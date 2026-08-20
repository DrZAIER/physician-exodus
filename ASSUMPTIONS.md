# Structural Assumptions, Policy Scenarios, and Uncertainty Framework

**Project**: Physician Exodus from Tunisia: Workforce Projections, Policy Simulation, and Economic Evaluation to 2050  
**Status**: Specification Phase (Pre-Calibration)  
**Methodological Role**: Explicit documentation of model assumptions, scenario definitions, and uncertainty analysis protocols.

> [!IMPORTANT]
> **Strict Empirical Grounding Rule**: No numerical parameter values are hardcoded or fabricated in this document. All quantitative parameter distributions must be populated exclusively via empirical data ingestion (`DATA_SPEC.md`) and systematic literature extraction (`LITERATURE_SPEC.md`). This document defines the *structural framework*, *scenario definitions*, and *mathematical boundaries*.

---

## 1. Structural & Model Assumptions

### 1.1. Model Boundary & Population Demarcation
- **Target Population**: All legally licensed physicians registered with the *Conseil National de l'Ordre des Médecins* (CNOM) in Tunisia, plus Tunisian-trained physicians currently residing and practicing abroad.
- **Active Age Range**: Age 25 (minimum theoretical age of residency entry/licensure) to Age 75 (statutory retirement + maximum private practice extension).
- **Time Horizon**: Discrete annual time steps from $t_0 = 2020$ (baseline calibration year) through $t_T = 2050$ (terminal projection year).

### 1.2. State-Transition Topology & Invariants
- **Conservation of Stock**: In every time step $t$, the total national and expatriate physician pool obeys exact conservation:

$$\text{Stock}_{t+1} = \text{Stock}_t + \text{Entries}_{t+1} - \text{Exits}_{\text{mortality}, t+1} - \text{Exits}_{\text{retirement}, t+1}$$

- **State Space**: Each cohort cell is indexed by $(a, s, k, j, r, m)$:
  - Age $a \in [25, 75]$
  - Sex $s \in \{\text{Male}, \text{Female}\}$
  - Specialty cluster $k \in \mathcal{K}$ (11 standardized clusters)
  - Sector of practice $j \in \{\text{Public CHU}, \text{Public Regional/District}, \text{Private Solo}, \text{Private Clinic}, \text{Inactive}\}$
  - Region $r \in \mathcal{R}$ (7 planning regions, 24 governorates)
  - Migration status $m \in \{\text{Domestic}, \text{Emigrated (Europe)}, \text{Emigrated (Gulf)}, \text{Emigrated (North America)}, \text{Emigrated (Other)}, \text{Returned}\}$

- **Transition Rules**:
  - Medical residents cannot transition to private solo practice prior to board certification (*thèse et clinicat/assistanat* validation).
  - Public-sector physicians can transition to private practice, emigration, or statutory retirement.
  - Emigrated physicians have non-zero return probabilities $p_{\text{return}}(a, s, k)$ conditioned on age and years abroad.
  - Age advances deterministically by $+1$ year per simulation step until absorption at maximum retirement age or mortality.

---

## 2. Policy Scenario Matrix (Counterfactual Definitions)

Policy counterfactuals will be simulated against the status-quo baseline from 2025 to 2050:

| Scenario Code | Scenario Name | Policy Levers & Mechanism | Key Parameters Impacted |
| :--- | :--- | :--- | :--- |
| **SCEN_0** | **Status Quo (Baseline)** | Continuation of historical macroeconomic trends, existing salary scales, current public investment trajectories, and foreign recruitment pulls. | Baseline transition probabilities $P_{0}(t)$. |
| **SCEN_1** | **Public Sector Remuneration Reform** | Targeted base wage realignment with inflation, doubling of on-call (*gardes*) compensation, and performance-based clinical allowances. | Public sector retention utility $V_{\text{public}}$, reduces $P_{\text{public}\rightarrow\text{emigrate}}$. |
| **SCEN_2** | **Workplace & Infrastructure Upgrades** | Capital investment targeting equipment availability, continuous drug supply, hospital security personnel, and reduced administrative load. | Institutional quality attribute $\mathbf{x}_{\text{infra}}$, reducing burnout-driven exit. |
| **SCEN_3** | **Regional Retention & Rural Incentive Package** | Differentiated financial hardship allowance (+30–50%), provision of subsidized housing, guaranteed priority transfer to CHU after 3 years in interior governorates. | Spatial utility in interior governorates $V_{\text{interior}}$, mitigating coastal-interior disparity. |
| **SCEN_4** | **Medical Training Quota & Residency Expansion** | Selective expansion of *numerus clausus* in high-deficit specialties (anesthesia, ICU, emergency) coupled with return-of-service commitments. | Inflow vector $\mathbf{I}_{t+1}(k)$ and contractual retention constraints. |
| **SCEN_5** | **Comprehensive Synergistic Reform Package** | Combined implementation of SCEN_1 + SCEN_2 + SCEN_3 + bilateral ethical recruitment agreements with European destination countries. | Full interaction vector $\boldsymbol{\theta}_{\text{comprehensive}}$. |

---

## 3. Economic & Costing Assumptions

### 3.1. Public Investment & Training Valuation
- Direct public educational cost per medical graduate will be estimated using the UNESCO/WHO Human Capital methodology based on Ministry of Higher Education operating expenditures per student across the 4 medical faculties.
- Shadow price of capital and social discount rate: Baseline social discount rate of **3.0%** per annum (tested across 0%, 3%, 5%, and 8% in sensitivity analysis).

### 3.2. Cost-Consequence & Cost-Effectiveness Boundaries
- **Perspective**: Societal and Public Payer (Ministry of Health / National Social Security Funds).
- **Time Horizon for Costs & Consequences**: 2025 to 2050 (30-year analytical horizon).
- **Cost Categories**:
  - Direct policy intervention costs (wage bill expansions, infrastructure capital expenditure, incentive payments).
  - Averted loss of public training investment.
  - Averted service disruption / locum replacement costs.
- **Outcome Metrics**:
  - Domestic physician-years gained ($PYG$).
  - Effective clinical specialist hours delivered in underserved regions.
  - Physician-to-population density achieved relative to WHO UHC benchmarks (e.g., WHO threshold of 4.45 skilled health professionals per 1,000 population).
  - Incremental Cost-Effectiveness Ratio: $\text{ICER} = \frac{\Delta \text{Cost}}{\Delta PYG}$.

---

## 4. Uncertainty & Sensitivity Analysis Protocol

To ensure scientific robustness against parameter uncertainty, the modeling framework implements a three-tier uncertainty protocol:

```
+-----------------------------------------------------------------------------------+
|                        Three-Tier Uncertainty Protocol                            |
+-----------------------------------------------------------------------------------+
                                         |
     +-----------------------------------+-----------------------------------+
     |                                   |                                   |
     v                                   v                                   v
+------------------------+  +------------------------+  +------------------------+
| Tier 1: Deterministic  |  | Tier 2: Probabilistic  |  | Tier 3: Structural     |
| Sensitivity Analysis   |  | Sensitivity Analysis   |  | Scenario Testing       |
| - One-way Tornado plots|  | - Monte Carlo (10,000) |  | - Macroeconomic shocks |
| - Extreme value bounds |  | - Parameter covariance |  | - Border/visa closures |
+------------------------+  +------------------------+  +------------------------+
```

### 4.1. Tier 1: Deterministic Sensitivity Analysis (DSA)
- **One-Way Sensitivity Analysis**: Varying each empirical parameter (e.g., base emigration rate, discrete-choice wage elasticity, discount rate, training unit cost) across its 95% confidence interval or $\pm 25\%$ range to construct Tornado diagrams.
- **Multi-Way / Scenario Extremes**: Best-case versus worst-case compound scenarios.

### 4.2. Tier 2: Probabilistic Sensitivity Analysis (PSA)
- Monte Carlo simulation drawing $N = 10,000$ parameter vectors from empirical joint probability distributions:
  - Transition probabilities: Dirichlet / Beta distributions.
  - Cost parameters: Gamma / Log-normal distributions.
  - Discrete-choice coefficients: Multivariate Normal distribution $\mathcal{N}(\hat{\boldsymbol{\beta}}, \hat{\boldsymbol{\Sigma}}_{\boldsymbol{\beta}})$.
- Output reporting: 95% Credible Intervals (2.5th and 97.5th percentiles) for all stock and cost projections, Cost-Effectiveness Acceptability Curves (CEAC).

### 4.3. Tier 3: Structural & Macroeconomic Stress-Testing
- Simulating macroeconomic shock scenarios:
  - High-inflation / severe currency depreciation shock (accelerated push).
  - Destination country policy shifts (e.g., tightening or expansion of French/German recruitment regulations).
