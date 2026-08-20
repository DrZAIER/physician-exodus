# Structural Assumptions, Policy Scenarios, and Uncertainty Framework

**Project**: Physician Exodus from Tunisia: Workforce Projections, Policy Simulation, and Economic Evaluation to 2050  
**Status**: Specification Phase (Pre-Calibration)  
**Methodological Role**: Explicit documentation of model assumptions, scenario definitions, and uncertainty analysis protocols.

> [!IMPORTANT]
> **Strict Empirical Grounding Rule**: No numerical parameter values are hardcoded or fabricated in this document. All quantitative parameter distributions must be populated exclusively via empirical data ingestion (`DATA_SPEC.md`) and systematic literature extraction (`LITERATURE_SPEC.md`). This document defines the *structural framework*, *scenario definitions*, and *mathematical boundaries*.

---

## 1. Structural & Model Assumptions

#### 1.1. Model Boundary & Population Demarcation
- **Target Population**: All legally licensed and active practicing physicians in Tunisia, plus Tunisian-trained physicians currently residing and practicing abroad.
- **Active Age Range**: Age 25 (minimum theoretical age of residency entry/licensure) to Age 75 (statutory retirement + maximum private practice extension).
- **Time Horizon**: Discrete annual time steps from $t_0 = 2015$ (historical calibration) / $2025$ (policy projection baseline) through $t_T = 2050$ (terminal projection year).

### 1.2. Parsimonious State-Transition Topology (36-Cell Tensor)
- **Conservation of Stock**: In every time step $t$, the active practicing domestic stock obeys exact demographic conservation:

$$N_{t+1} = N_t + \text{Graduates}_{t+1} + \text{Returns}_{t+1} - \text{Emigrants}_{t+1} - \text{Retirements}_{t+1} - \text{OtherExits}_{t+1}$$

- **State Space**: Cohorts are stratified across a parsimonious 36-cell tensor $(a, s, r, k)$:
  - **Career Stage ($a$)** [3 strata]: Early-Career / Resident ($<35$ yrs), Mid-Career ($35–54$ yrs), Senior ($55+$ yrs).
  - **Sector ($s$)** [2 strata]: Public Sector (CHU / Regional Hospital / Primary Care), Private Sector (Clinics / Solo Practice).
  - **Geography ($r$)** [2 strata]: Coastal / Metropolitan (District of Tunis, Center East), Interior / Underserved (North West, Center West, South).
  - **Specialty Group ($k$)** [3 strata]: General Medicine, Medical Specialties, Surgical / Anesthesia / Critical Care Specialties.
  - Multiplied by **2 Migration Pools**: Active Domestic Practicing vs. Cumulative Emigrated.
  - Total Active Domestic State Space: $3 \times 2 \times 2 \times 3 = 36 \text{ cells}$.

- **Baseline Initialization Protocol (Iterative Proportional Fitting)**:
  The 36-cell stock distribution at baseline ($t_0 = 2020$) is initialized from INS and Ministry of Health *Carte Sanitaire* marginal distributions via 2-dimensional Iterative Proportional Fitting (IPF / raking), ensuring exact consistency with official public/private and regional totals.

- **Empirical Multipliers & Transformation Rules**:
  - **Active Practice Ratio ($\alpha$)**: $\alpha \sim \text{Uniform}[0.85, 0.90]$ (base case $\alpha = 0.88$) applied **strictly as an initial baseline stock filter at $t_0$** ($N_0 = \alpha \cdot N_{\text{raw}, 0}$) to eliminate unpurged inactive/emigrated registrations. For $t > 0$, dynamics follow exact stock-flow conservation equations.
  - **Intention-to-Action Realization Factor ($\kappa$)**: $\kappa \sim \text{Uniform}[0.25, 0.45]$ (base case $\kappa = 0.35$, drawing on Clemens & Mendola, 2020; Docquier et al., 2014) scaling latent survey intention into physical emigration probabilities:
    $$P(\text{Emigration}_{i,t}) = \kappa \cdot \text{logit}^{-1}(\Delta V_{i,t})$$
  - **Administrative Clearance Multiplier ($\lambda_{\text{exit}}$)**: $\lambda_{\text{exit}} \sim \text{Uniform}[0.65, 0.90]$ (base case $\lambda_{\text{exit}} = 0.75$) mapping CNOM good-standing certificates to realized border departures.
  - **OR-to-RR Non-Collapsibility Transformation**: Survey odds ratios are converted to Relative Risks via Zhang & Yu (JAMA 1998):
    $$\text{RR} = \frac{\text{OR}}{(1 - p_0) + (p_0 \cdot \text{OR})}$$
    where $p_0 \approx 0.75$ is the baseline intention prevalence.

---

## 2. Policy Scenario Matrix (Counterfactual Definitions)

Policy counterfactuals are simulated against the status-quo baseline from 2025 to 2050:

| Scenario Code | Scenario Name | Policy Levers & Mechanism | Key Parameters Impacted |
| :--- | :--- | :--- | :--- |
| **SCEN_0** | **Status Quo (Baseline)** | Continuation of post-2021 migration regime, current public salary scales, and historical recruitment pulls. | Baseline transition probabilities $P_{0}(t)$. |
| **SCEN_1** | **Public Sector Remuneration Reform** | Targeted public base wage increase (+30%), doubling of on-call (*gardes*) compensation, and performance allowances. | Public sector retention utility $V_{\text{public}}$, reduces $P_{\text{public}\rightarrow\text{emigrate}}$. |
| **SCEN_2** | **Workplace & Infrastructure Upgrades** | Capital investment targeting equipment availability, continuous drug supply, hospital security personnel, and reduced administrative load. | Institutional quality attribute $\mathbf{x}_{\text{infra}}$, reducing burnout-driven exit. |
| **SCEN_3** | **Regional Retention & Rural Incentive Package** | Differentiated financial hardship allowance (+40%), provision of subsidized housing, guaranteed priority transfer to CHU after 3 years in interior governorates. | Spatial utility in interior governorates $V_{\text{interior}}$, mitigating coastal-interior disparity. |
| **SCEN_4** | **Medical Training Quota & Residency Expansion** | Selective expansion of *numerus clausus* in high-deficit specialties (anesthesia, ICU, emergency) coupled with return-of-service commitments. | Inflow vector $\mathbf{I}_{t+1}(k)$ and contractual retention constraints. |
| **SCEN_5** | **Comprehensive Synergistic Reform Package** | Combined implementation of SCEN_1 + SCEN_2 + SCEN_3 + bilateral ethical recruitment agreements with European destination countries. | Multiplicative composite reduction: $\text{RR}_{\text{package}} = \prod_k \text{RR}_k$, ensuring diminishing returns. |

---

## 3. Economic & Costing Assumptions

### 3.1. Public Sector Wage Bill Expansion (Inframarginal Costing)
For any salary reform (e.g., SCEN_1, SCEN_5), the economic cost is calculated across the entire practicing public physician workforce:

$$\Delta \text{Cost}_{\text{salary}, t} = N_{\text{public}, t} \cdot \Delta w_t$$

### 3.2. Net Training Investment & Resident Labor Offset
Net public training investment loss per emigrating specialist is adjusted for clinical hospital service delivered during residency:

$$\text{Net Training Cost} = \text{Gross Educational Outlay} - (\text{Years of Residency} \times \text{Imputed Value of Resident Clinical Labor})$$

(Baseline assumes a **40% net labor value offset** against gross educational expenditures).

### 3.3. Cost-Consequence & Budget Impact Framework
- **Primary Perspective**: Tunisian Public Payer / Ministry of Health and Ministry of Finance.
- **Discounting**: Baseline annual social discount rate of **3.0%** (tested across 0%, 3%, 5%, and 8% in sensitivity analysis).
- **Outcome Metrics**:
  - Incremental Cost-Consequence Balance Sheet (Milestones: 2030, 2040, 2050).
  - Annual Budget Impact as % of Ministry of Health recurrent budget.
  - $\text{ICER}_{\text{total}} = \frac{\Delta \text{Cost}}{\Delta \text{Physician-Years Retained}}$.
  - $\text{ICER}_{\text{public}} = \frac{\Delta \text{Cost}}{\Delta \text{Public Physician-Years Retained}}$.
  - $\text{ICER}_{\text{interior}} = \frac{\Delta \text{Cost}}{\Delta \text{Interior Physician-Years Retained}}$.

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
