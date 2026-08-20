You are acting as a senior health economist, health workforce modeller, migration researcher, and biostatistician preparing a manuscript for peer review.

Your task is to redesign and fully implement a publishable study on physician emigration from Tunisia.

Do NOT optimise for computational novelty. Optimise for methodological credibility, reproducibility, policy relevance, empirical anchoring, and publication quality.

The final study should be understandable to a health economist, health workforce researcher, epidemiologist, or Tunisian health policy researcher without requiring expertise in agent-based modelling.

============================================================
1. CORE RESEARCH QUESTION
============================================================

Primary research question:

"What are the long-term workforce and economic consequences of physician emigration in Tunisia, and which feasible retention, training, and return-migration policies provide the greatest gain in physician-years retained by 2050?"

Secondary questions:

1. How does continued physician emigration affect the size, sectoral composition, specialty composition, and geographic distribution of Tunisia's physician workforce through 2050?

2. How do established macro, meso, and micro determinants of physician migration identified in the literature translate into simulated migration propensity?

3. How do alternative retention, medical-training, geographic-retention, and return-migration policies affect total and public-sector physician-years retained?

4. What is the incremental cost per additional physician-year retained for each policy strategy?

5. How robust are the projected workforce and policy rankings to uncertainty in migration determinants, baseline migration trajectories, and intervention effectiveness?

============================================================
2. CENTRAL METHODOLOGICAL PRINCIPLE
============================================================

Do NOT invent a novel behavioural theory.

Do NOT use a complicated ABM merely because ABM is interesting.

Do NOT make salary the dominant or exclusive determinant of migration.

Do NOT assign arbitrary behavioural weights such as "salary = 0.1, quality of life = 0.2" unless there is a defensible empirical basis.

Anchor the model explicitly in established frameworks:

A. WHO Health Labour Market Framework
B. Push-pull migration theory
C. Macro-meso-micro framework for health-worker migration determinants
D. Random-utility/discrete-choice modelling of migration decisions
E. Cohort/state-transition/stock-flow modelling of health workforce supply
F. Standard health-economic cost-consequence and cost-effectiveness analysis

The methodological lineage should be explicit in the manuscript.

The intended conceptual chain is:

Established migration determinants
        ↓
Physician migration propensity
        ↓
Annual migration flows
        ↓
Dynamic physician workforce stock
        ↓
Sector/specialty/geographic distribution
        ↓
Policy counterfactuals
        ↓
Physician-years retained
        ↓
Economic evaluation

============================================================
3. ESTABLISHED LITERATURE THAT MUST ANCHOR THE MODEL
============================================================

Use and verify these sources rather than replacing them with invented frameworks.

WHO health labour market framework:

World Health Organization. A labour market approach to investing in health and social care workforce development.

WHO has explicitly conceptualised health workforce dynamics through education, labour-market entry, employment, migration, return migration, and workforce exit.

Source:
https://iris.who.int/bitstream/handle/10665/348069/9789240035546-eng.pdf

Also use:

Sousa A, et al. A comprehensive review of the health workforce literature on migration determinants.

Systematic review covering 107 studies and explicitly synthesising health-worker migration using push-pull theory and the macro-meso-micro framework.

Source:
https://pmc.ncbi.nlm.nih.gov/articles/PMC10174016/

The review identifies determinants including:

Macro:
- remuneration
- economic conditions
- political/security environment
- health-system conditions

Meso:
- working conditions
- workload
- job satisfaction
- career prospects
- training
- management
- professional environment

Micro:
- family
- personal circumstances
- quality of life
- individual preferences

Use this framework as the conceptual taxonomy for model variables.

Discrete-choice health workforce literature:

Use the systematic review of discrete-choice experiments in health-worker recruitment and retention:

https://pmc.ncbi.nlm.nih.gov/articles/PMC4161911/

The manuscript should explain why a random-utility/discrete-choice formulation is an established way to translate multidimensional employment and migration preferences into probabilities.

Physician-emigration modelling precedent:

Amorim-Lopes M, Almeida A, Almada-Lobo B.
"Physician Emigration: Should They Stay or Should They Go? A Policy Analysis."
Computational Economics. 2019;54:905-931.
doi:10.1007/s10614-018-9854-1

Source:
https://ciencia.ucp.pt/en/publications/physician-emigration-should-they-stay-or-should-they-go-a-policy-/

Use this as precedent that dynamic physician migration policy simulation is legitimate.

Do NOT copy its architecture unnecessarily.

Dynamic physician workforce modelling precedent:

Use AAMC-style physician workforce stock-flow modelling as precedent for dynamic physician supply projection.

PubMed:
https://pubmed.ncbi.nlm.nih.gov/33913440/

============================================================
4. TUNISIAN EMPIRICAL LITERATURE
============================================================

The model MUST be anchored in actual Tunisian evidence.

Use and verify:

Ben Romdhane et al. Study of immigration projects among young Tunisian physicians.

Source:
https://pmc.ncbi.nlm.nih.gov/articles/PMC9567516/

Important empirical findings include migration intention and associations with:

- dissatisfaction
- underpayment
- workload
- difficult working conditions
- insufficient training
- economic instability
- lack of clear health-system strategy
- influence of physicians who already emigrated
- specialty
- marital/family factors
- career stage

Do not treat these as causal coefficients unless the original study actually supports causal estimation.

Use the more recent Tunisian resident migration-intention study:

https://pmc.ncbi.nlm.nih.gov/articles/PMC11862060/

Extract and verify:

- working conditions
- workplace safety
- salary
- workload
- supervision
- training
- political conditions
- social security
- quality of life
- career prospects

Also consider the Tunisian workplace-incivility study linking organisational/workplace factors with intention to expatriate:

https://www.sciencedirect.com/org/science/article/abs/pii/S2049879924000160

Search for additional peer-reviewed Tunisian and Moroccan physician migration-intention studies.

The model should distinguish:

1. Variables with Tunisian physician-level evidence.
2. Variables with North African evidence.
3. Variables supported by broader LMIC/international evidence.
4. Variables included only as sensitivity parameters.

Never pretend that international evidence is Tunisian causal evidence.

============================================================
5. TUNISIAN WORKFORCE DATA FOR CALIBRATION
============================================================

Use real observed data.

Do not generate synthetic calibration data.

Do not interpolate historical values unless explicitly documented and justified.

Do not silently combine incompatible definitions.

Primary national workforce data:

Institut National de la Statistique (INS), Tunisia.

Source:
https://ins.tn/en/statistiques/123

Relevant observed series include:

2024:
Total physicians = 15,315
Public-sector physicians = 6,113
Private-sector physicians = 9,202

Use the complete available annual series from INS, not just 2024.

Obtain the underlying table and preserve:

- year
- total physicians
- public physicians
- private physicians
- source
- source URL
- extraction date
- exact table definition

Regional workforce:

Tunisia Ministry of Health, Carte Sanitaire 2023.

Source:
https://santetunisie.rns.tn/images/carte-sanitaire-2023.pdf

Use the governorate-level physician counts.

Do not invent missing values.

Population:

INS governorate population data.

Source:
https://www.ins.tn/statistiques/111

Use the appropriate population year and document whether physician density and population are contemporaneous.

Calculate:

Physician density =
physicians / population × 100,000.

Use regional distribution to evaluate whether national physician retention translates into equitable distribution.

============================================================
6. PHYSICIAN EMIGRATION DATA
============================================================

Use real reported migration observations.

A reported 2024 estimate of approximately 1,450 physicians leaving Tunisia was reported by the National Council of Physicians.

Source:
https://www.tunisie-tribune.com/2025/01/07/1450-medecins-ont-quitte-la-tunisie-en-2024/

Other reported national estimates include approximately:

2015–2020:
~3,300 physician departures

2021–2024:
~6,000 physician departures

These figures have been reported in Tunisian media and should be traced back to the original professional/institutional source whenever possible.

Do NOT automatically equate reported annual departures with:

N_t - N_(t+1)

because administrative workforce stocks and reported migration counts have different definitions, coverage, and timing.

Instead create an explicit observation model with an Administrative Clearance Multiplier:

Observed reported departures_t = (1 / λ_exit) × True physical emigration flow_t

where λ_exit ~ Uniform[0.65, 0.90] (base-case λ_exit = 0.75) represents the proportion of CNOM certificate requests that translate into realized border departures, validated against destination registry intakes (French DREES/RPPS and German Bundesärztekammer).

The migration series may be used for:

- validation
- calibration of migration regimes
- sensitivity analysis

depending on the quality and comparability of each observation.

============================================================
7. MEDICAL GRADUATE INPUT
============================================================

Use actual Tunisian medical graduate/medical-school intake data.

Search for and verify:

- annual number of medical graduates
- number of residency positions if relevant
- public/private medical schools
- historical changes in graduate output
- specialty training capacity where data exist

Use Ministry of Higher Education, Ministry of Health, university, WHO, UNESCO, or official Tunisian sources.

Do not fabricate annual graduate counts.

If only a range is available, represent it probabilistically.

============================================================
8. MODEL STRUCTURE
============================================================

Prefer a cohort/state-transition stock-flow model over an ABM.

Represent the physician workforce using a parsimonious 36-cell state tensor:

N_(a,s,r,k,t)

where:

a = career stage (3 strata: Resident/Early-career <35 yrs, Mid-career 35–54 yrs, Senior 55+ yrs)
s = sector (2 strata: Public sector [hospital/primary], Private sector [clinic/solo])
r = geography (2 strata: Coastal/Metropolitan [Greater Tunis, Center East], Interior/Underserved [North West, Center West, South])
k = specialty group (3 strata: General Medicine, Medical Specialties, Surgical/Anesthesia/Critical Care Specialties)
t = year (2020–2050)

Total active domestic state space: 3 × 2 × 2 × 3 = 36 cells.
Multiplied by 2 migration statuses: Active Domestic Practicing vs. Cumulative Emigrated.

Baseline tensor initialization (Iterative Proportional Fitting):
Initialize the 36-cell active domestic stock tensor at baseline (t0 = 2020) using standard 2-dimensional Iterative Proportional Fitting (IPF / raking) to match published marginal distributions from INS (national public/private totals) and Ministry of Health Carte Sanitaire (governorate public headcounts and specialty clusters) exactly.

Administrative stock correction timing:
Apply the Active Practice Ratio (α ~ Uniform[0.85, 0.90], base-case α = 0.88) strictly as an initial baseline filter at t0 (N0 = α × N_raw,0) to eliminate unpurged "ghost registrations". For all subsequent simulation steps (t > 0), workforce changes are governed exclusively by dynamic demographic stock-flow transitions (mortality, retirement, realized emigration) rather than repeating α annually.

Annual workforce transition equation:

N_(t+1) = N_t + Graduates_(t+1) + Returns_(t+1) - Emigrants_(t+1) - Retirements_(t+1) - OtherExits_(t+1)

The migration flow is:

M_t = Σ_i N_(i,t) × P(Emigration_(i,t))

where the physical emigration probability incorporates the Intention-to-Action Realization Factor (κ ~ Uniform[0.25, 0.45], base-case κ = 0.35, drawing on Clemens & Mendola, 2020; Docquier et al., 2014):

P(Emigration_(i,t)) = κ × logit^(-1)(ΔV_(i,t))

and the relative utility index is structured as a static baseline plus discrete policy/regime shifts:

ΔV_(i,t) = β0 + Δβ_regime(t) + β_macro X_macro,i + β_meso X_meso,i + β_micro X_micro,i + β_pull X_pull,i + β_peer X_peer,i(t)

where:

MACRO: baseline economic, institutional, and health system environment
MESO: remuneration, workload, infrastructure, career prospects, supervision
MICRO: family commitments, career stage baseline utility
PULL: destination income and credentialing attractiveness
PEER: aggregate cohort/sectoral migration feedback loop (cumulative emigration proportion of cohort in preceding 2 years)

Do not overparameterise. Relative weights (β) are anchored in established DCE literature, avoiding dynamic unidentifiable micro-attribute forecasting.

============================================================
9. PARAMETER IDENTIFICATION
============================================================

This is critical.

Do NOT claim that all behavioural coefficients are estimated from Tunisian data.

Create a parameter provenance table with columns:

parameter
meaning
estimate/distribution
source
country
population
study design
identification status
base-case value
lower bound
upper bound
justification

Classify every parameter:

A = directly estimated from Tunisian data
B = estimated from North African evidence
C = estimated from international physician/health-worker evidence
D = expert/structural assumption
E = scenario parameter

Only A and B parameters should be described as empirically Tunisian/North African.

For C/D/E parameters, explicitly state uncertainty.

If a Tunisian study reports odds ratios (OR) for migration intention, convert them into conservative Relative Risks (RR) using the Zhang & Yu (JAMA 1998) transformation before using them in policy response functions:

RR = OR / ((1 - p0) + (p0 × OR))

where p0 is the baseline intention prevalence in the reference group (e.g., p0 ≈ 0.75 for residents).
Do not convert cross-sectional odds ratios directly into causal elasticities.

============================================================
10. BASELINE MODEL
============================================================

The baseline should represent continuation of observed/pre-intervention migration conditions.

Use historical data to calibrate:

- workforce stock (adjusted by active ratio α = 0.88)
- public/private distribution
- migration regime (with post-2021 structural shift)
- graduate entry
- retirement

Where the post-2021 migration acceleration is clearly documented, allow structural regime changes.

Do not force the model to explain a sudden national migration shock using salary alone.

Formulation:

pre-2021 regime (2015–2021)
post-2021 regime (2022–2024+)

Estimate regime intercepts while retaining the literature-based determinant structure.

============================================================
11. CALIBRATION & IDENTIFICATION
============================================================

Use a transparent, low-dimensional calibration procedure avoiding overparameterisation.

Identification strategy:
1. Fix standardized relative choice attribute weights using pooled LMIC health workforce DCE meta-analyses (Mandeville et al., 2014, Class C).
2. Calibrate only TWO global scalar parameters to historical Tunisian macro series (2015–2021):
   - Baseline migration scale parameter (β0)
   - Post-2021 structural regime shift (Δβ_2021+)

The calibration objective reproduces:
1. total active practicing physician stock
2. public physician stock
3. private physician stock
4. historical realized migration flows (CNOM certificate series adjusted by λ_exit = 0.75)
5. graduate entry throughput

Use standard OLS / Maximum Likelihood count loss:

L(θ) = Σ_k w_k Σ_t [(Y_k,t^sim - Y_k,t^obs)^2 / σ_k^2]

Temporal validation split:
- Calibration period: 2015–2021
- Out-of-sample temporal validation: 2022–2024
- External directional validation check: Annual influx of Tunisian physicians registered in French DREES/RPPS and German Bundesärztekammer databases.

============================================================
12. MODEL VALIDATION
============================================================

Report:

- MAE
- RMSE
- MAPE only where mathematically appropriate
- calibration plots
- observed vs simulated trajectories
- coverage of uncertainty intervals
- migration-flow validation
- workforce-stock validation

Figures should show observed data as points/lines and model median + uncertainty ribbon.

Do not show meaningless model-only curves.

============================================================
13. ABLATION / STRUCTURAL ANALYSIS
============================================================

Ablation should answer scientifically meaningful questions.

Run:

A. Full model

B. No migration-determinant heterogeneity
   Constant migration propensity.

C. Financial-only model
   Only remuneration.

D. Meso-only model
   Working conditions/career/training.

E. Macro + meso + micro model.

F. No peer effect.

G. No return migration.

H. No public/private mobility if the data support testing it.

Compare:

- historical fit
- validation fit
- 2050 workforce projection
- migration flows
- policy ranking

The purpose is to determine whether the multifactorial framework adds explanatory or policy value.

Do NOT call these "machine-learning ablations".

============================================================
14. SENSITIVITY ANALYSIS
============================================================

Perform:

1. One-way sensitivity analysis.

2. Probabilistic sensitivity analysis.

3. Structural sensitivity analysis.

4. Scenario sensitivity.

Parameters requiring uncertainty include:

- migration coefficients
- baseline migration regime
- return probability
- graduate output
- retirement
- intervention effectiveness
- intervention costs
- observation/definition factor for reported migration data

Use Monte Carlo sampling.

At least 1,000 simulations for final PSA unless computational cost is demonstrably unnecessary.

Report parameter distributions and sources.

============================================================
15. POLICY SCENARIOS
============================================================

Use realistic interventions.

At minimum:

1. Status quo.

2. Salary increase.

3. Working-condition intervention.

4. Career/training intervention.

5. Institutional/security intervention.

6. Geographic retention incentive.

7. Increased medical-school output.

8. Return-migration programme.

9. Integrated retention package.

10. Integrated retention + return-migration package.

Do not invent arbitrary intervention effects.

Each intervention must specify:

- mechanism
- target population
- parameter affected
- magnitude
- evidence source
- uncertainty range
- cost

If no empirical estimate exists, make it an explicit scenario assumption and run wide sensitivity analysis.

Multiplicative bounding for compound reform packages (Scenario 5, 9, 10):
When simulating multi-component interventions combining salary, infrastructure, and rural allowances, calculate composite Relative Risk Reductions (RRR) multiplicatively rather than additively:
RRR_package = 1 - Π_k (1 - RRR_k)  <=>  RR_package = Π_k RR_k
This guarantees diminishing marginal returns across bundled policy levers and prevents retention probabilities from exceeding theoretical bounds [0, 1).

============================================================
16. ECONOMIC EVALUATION
============================================================

Keep this deliberately simple, reproducible, and economically rigorous.

Primary perspective:
Tunisian public payer / government perspective (Ministry of Health and Ministry of Finance).

Costing methodology:
1. Public Sector Wage Bill Expansion (Inframarginal costing):
   For any salary adjustment policy, calculate the full budgetary cost across all practicing public physicians:
   ΔCost_salary,t = N_public,t × Δw_t
   (Do not cost only for marginal retained physicians).

2. Net Training Investment Loss Valuation:
   Net Training Cost = Gross University Educational Outlay - (Years of Residency × Imputed Value of Resident Clinical Labor)
   (Baseline assumes a 40% resident labor value offset).

Primary economic presentation:
Cost-Consequence Analysis (CCA) and Budget Impact Analysis (BIA) reporting milestone outcomes at 2030, 2040, and 2050.

Calculate:
ΔC = C_policy - C_statusquo (discounted at 3% baseline, tested at 0%, 5%, 8%)
ΔE = PhysicianYears_policy - PhysicianYears_statusquo

Primary and disaggregated secondary ICERs:
- ICER_total = ΔC / ΔPhysicianYears_retained
- ICER_public = ΔC / ΔPublicPhysicianYears_retained
- ICER_interior = ΔC / ΔInteriorPhysicianYears_retained

Also report:
- Annual and cumulative Budget Impact (2025–2050) as % of national health budget
- Net training investment preserved domestically
- Cost-Effectiveness Acceptability Curves (CEAC) from 1,000-draw Monte Carlo PSA

Do NOT calculate QALYs or DALYs unless a defensible Tunisian physician-density-to-health-outcome relationship is identified.

============================================================
17. 2050 HORIZON & UNCERTAINTY MANAGEMENT
============================================================

The final projection horizon is:
2025–2050 (mandatory 25-year investment horizon).

Epistemic framing:
All 2025–2050 results are formally defined as CONDITIONAL POLICY COUNTERFACTUALS under explicit demographic/economic baseline assumptions, not unconditional point forecasts.

Report milestone outcomes:
- 2030 (Short-term / immediate post-graduation impact)
- 2040 (Medium-term / mid-career cohort progression)
- 2050 (Long-term / structural workforce equilibrium)

Run a standard 1,000-draw Monte Carlo Probabilistic Sensitivity Analysis (PSA) drawing from bounded parametric distributions for realization factor (κ), clearance multiplier (λ_exit), policy effect sizes, and discount rates, reporting 95% Credible Intervals for all milestone outcomes.

============================================================
18. PUBLICATION-READY OUTPUTS
============================================================

The figures must be designed as manuscript figures, not exploratory plots.

Every figure must answer a substantive question.

Minimum figures:

FIGURE 1
Conceptual framework.

Show:

migration determinants
→ migration probability
→ physician flows
→ workforce stock
→ geographic/sector consequences
→ policy
→ economic outcomes

FIGURE 2
Model architecture.

Show:

entry
→ domestic practice
→ public/private transition
→ emigration
→ return
→ retirement

with agent/cohort states and transitions.

FIGURE 3
Historical calibration.

Panel A:
total physician workforce

Panel B:
public/private workforce

Panel C:
reported physician departures

Observed data must be visually distinguished from model output.

FIGURE 4
Model validation.

Observed vs simulated outcomes with uncertainty intervals.

FIGURE 5
Baseline projection 2025–2050.

Show total physicians and public-sector physicians.

Include 2030, 2040, 2050.

FIGURE 6
Policy comparison.

Show absolute incremental physician-years retained for each intervention.

Rank policies.

Use confidence/credible intervals.

FIGURE 7
Policy trajectories.

Show the most policy-relevant 4–5 scenarios through 2050.

FIGURE 8
Cost-effectiveness.

Cost vs physician-years retained.

Show dominance and frontier.

FIGURE 9
Regional distribution.

Show physician density by governorate.

Use actual 2023 data.

If policy scenarios support geographic redistribution, show before/after.

FIGURE 10
Sensitivity analysis.

Tornado plot or probabilistic ranking of the parameters that most influence 2050 physician workforce.

Do NOT create ten figures just to satisfy a number.

If two figures can be combined without loss of information, combine them.

============================================================
19. PUBLICATION-READY TABLES
============================================================

At minimum:

TABLE 1
Model agents/cohorts/states and operational definitions.

TABLE 2
Model parameters, definitions, values, distributions, evidence source, and provenance classification.

TABLE 3
Historical calibration targets and observed data sources.

TABLE 4
Calibration and validation performance.

TABLE 5
Policy scenarios, mechanism, target population, assumed effectiveness, cost, and evidence basis.

TABLE 6
2050 workforce outcomes under all policy scenarios.

TABLE 7
Economic evaluation.

Columns:

strategy
incremental cost
incremental physician-years
incremental public physician-years
ICER
dominance status

TABLE 8
Sensitivity analysis.

Do not generate tables containing redundant numbers already obvious from figures.

============================================================
20. FIGURE DESIGN REQUIREMENTS
============================================================

Use R.

Primary packages:

tidyverse
data.table
ggplot2
patchwork
scales
ggrepel
survival
hesim or BCEA only if actually needed

Use a restrained journal-style design.

Do NOT create:

- rainbow plots
- unnecessary 3D graphics
- decorative dashboards
- giant legends
- meaningless heatmaps
- plots with 30 overlapping lines
- "ROI" charts that merely rank arbitrary assumptions
- figures that contain no observed data or policy interpretation

Every figure must have:

- informative title
- clear x-axis
- clear y-axis
- units
- source note where appropriate
- concise legend
- uncertainty interval where relevant
- publication-safe typography
- grayscale-friendly distinction where possible

Save:

PDF
SVG
PNG at 300–600 dpi

Use consistent dimensions.

============================================================
21. R CODE REQUIREMENTS
============================================================

The R project must be fully reproducible.

Use:

renv

for package version control.

Structure:

project/
├── README.md
├── renv.lock
├── data/
│   ├── raw/
│   ├── processed/
│   └── metadata/
├── R/
│   ├── 01_import_data.R
│   ├── 02_clean_data.R
│   ├── 03_parameter_registry.R
│   ├── 04_migration_model.R
│   ├── 05_workforce_model.R
│   ├── 06_calibration.R
│   ├── 07_validation.R
│   ├── 08_policy_scenarios.R
│   ├── 09_economic_evaluation.R
│   ├── 10_sensitivity.R
│   └── 11_figures_tables.R
├── tests/
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── results/
└── manuscript/
    ├── methods.tex
    ├── results.tex
    └── references.bib

There must be one command:

Rscript run_analysis.R

that regenerates:

- calibration
- validation
- all simulations
- all tables
- all figures
- all numerical result files

No manually entered final numbers.

Every number appearing in the manuscript must be traceable to an output file.

============================================================
22. DATA PROVENANCE
============================================================

Create:

data/metadata/data_dictionary.csv

and:

data/metadata/source_registry.csv

Each variable must have:

variable
definition
source
URL
country
year
unit
extraction date
original table
transformation
missingness
license/redistribution status

Never fabricate a missing observation.

If a source is unavailable, stop and report it.

Do not silently replace real data with synthetic values.

============================================================
23. REFERENCE MANAGEMENT
============================================================

Create a complete references.bib.

Verify every reference.

Do not invent DOI numbers.

Do not invent page numbers.

Do not cite secondary summaries when the primary source is available.

Separate:

- conceptual framework references
- Tunisian empirical studies
- North African studies
- international evidence
- workforce modelling methods
- economic evaluation methods
- data sources

Every parameter must have a traceable source or be explicitly marked as an assumption.

============================================================
24. METHODS SECTION
============================================================

Write a complete manuscript-ready Methods section.

It must contain:

2.1 Study design and conceptual framework

2.2 Data sources

2.3 Physician population and workforce representation

2.4 Migration determinants and operational definitions

2.5 Discrete-choice migration model

2.6 Workforce stock-flow model

2.7 Entry, retirement, emigration and return migration

2.8 Public/private and geographic distribution

2.9 Calibration

2.10 Temporal validation

2.11 Policy scenarios

2.12 Economic evaluation

2.13 Sensitivity and uncertainty analysis

2.14 Model verification and reproducibility

For every mathematical equation:

- define every symbol
- explain the rationale
- state parameter source
- explain assumptions

Do not introduce equations merely to make the manuscript look mathematical.

============================================================
25. WHAT SUCCESS LOOKS LIKE
============================================================

The final study should pass these tests.

Scientific:

- Every major model component has an established conceptual or methodological precedent.
- No arbitrary behavioural theory.
- No claim that salary alone drives migration.
- No causal interpretation of cross-sectional migration-intention studies.
- No fabricated data.
- No unsupported coefficients.
- Historical data are separated from counterfactual assumptions.
- Calibration and validation are separate.
- Migration observation definitions are explicitly addressed.

Computational:

- Runs on an ordinary laptop.
- Uses standard R packages.
- No GPU.
- No deep learning.
- No complex ABM infrastructure.
- Reproducible from a single command.
- Full tests included.

Policy:

A policymaker should be able to answer:

"How many physician-years does this intervention preserve by 2050?"

"How much does it cost?"

"How much does it preserve in the public sector?"

"Does it improve geographic distribution?"

"Is it better value than increasing medical-school output?"

"How robust is that conclusion?"

Publication:

The paper should look like a serious health workforce / health economics / health policy study, not a computer-science demonstration.

The computational method should be almost invisible to the reader.

The substantive result should be the focus.

============================================================
26. IMPORTANT NEGATIVE INSTRUCTIONS
============================================================

Do NOT:

- invent datasets
- generate synthetic calibration observations
- fabricate Tunisian coefficients
- fabricate intervention effectiveness
- make salary the dominant migration determinant without evidence
- use an ABM simply for novelty
- use machine learning
- use neural networks
- use arbitrary agent psychology
- claim causal effects from migration-intention studies
- equate reported emigration counts with workforce-stock changes without checking definitions
- use QALYs merely because health economics papers normally do
- project to only 2040
- create decorative figures
- create "ROI" plots that obscure the actual policy outcome
- report a single deterministic forecast as if it were certain
- hide assumptions inside code
- hard-code manuscript results
- manually edit final figures after analysis

============================================================
27. DELIVERABLES
============================================================

Produce all of the following.

1. Complete manuscript-ready Methods section in LaTeX.

2. Complete mathematical specification.

3. Operational-definition table.

4. Parameter registry with evidence provenance.

5. Complete references.bib.

6. Complete R project.

7. Real-data ingestion scripts.

8. Data validation tests.

9. Calibration code.

10. Validation code.

11. Workforce projection code to 2050.

12. Policy simulation code.

13. Economic evaluation code.

14. Probabilistic sensitivity analysis.

15. Publication-ready figures.

16. Publication-ready tables.

17. README explaining how to reproduce the study.

18. Data dictionary.

19. Source registry.

20. A final machine-readable results file.

21. A manuscript-ready Results skeleton whose numerical values are automatically populated from the generated results.

============================================================
28. FINAL QUALITY CONTROL
============================================================

Before declaring the study complete, independently audit:

A. Is every empirical input real?

B. Can every input be traced to a source?

C. Are Tunisian evidence and international evidence clearly distinguished?

D. Are migration-intention associations incorrectly being treated as causal?

E. Is the migration model actually identifiable?

F. Are calibration and validation separated?

G. Does the model reproduce observed workforce trajectories?

H. Does it reproduce migration observations without violating stock accounting?

I. Are intervention effects assumptions rather than disguised facts?

J. Are economic costs transparent?

K. Does the model reach 2050?

L. Can another researcher reproduce every figure and table from raw/processed data?

M. Do the figures actually answer the research questions?

N. Does the paper have a clear health-policy hook?

O. Is the computational complexity justified by the scientific question?

If any answer is "no", fix the problem before presenting the study as complete.

The objective is not to build the most sophisticated model.

The objective is to build the simplest empirically defensible model that can produce a publishable, policy-relevant answer to the question:

"Given what we know about why Tunisian physicians migrate, what happens to Tunisia's physician workforce by 2050, and which realistic policies provide the best workforce benefit for their cost?"