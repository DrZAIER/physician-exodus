# Model methodology

## 1. Overview

The model is a deterministic, annual, single-year-of-age cohort-component model
of the supply of physicians in active practice in Tunisia. It is implemented in
`src/model.py` and calibrated in `src/analysis.py`.

It has three state variables:

- \(N_a(t)\): number of practising physicians aged \(a\) at the end of year
  \(t\), for \(a = 25,\ldots,75\) (75 = 75 and over);
- \(D(t)\): the **return-eligible pool** of Tunisian-trained physicians abroad;
- the flow accounts (entries, emigration, returns, retirements, deaths).

The model runs from 2008 (initial condition) to 2040. The 2017–2024 series is a
retrospective comparison; the **calibration endpoint is 2024**. The projection
begins after 2024.

The model is supply-only. It does not include demand, vacancies, wages,
specialty choice, public/private allocation or regional distribution.

## 2. State transitions

For each year \(t\):

### 2.1 Entry

A cohort graduating in year \(t-L\) enters the practising stock in year \(t\),
where \(L=5\) years represents internship and residency. The number of entrants
is

\[
E(t) = G(t-L)\,\sigma(t),
\]

where \(G\) is the number of medical graduates and \(\sigma(t)\) is the share of
graduates who enter Tunisian practice. The complement,

\[
X(t) = G(t-L)\,[1-\sigma(t)],
\]

is **pre-entry emigration**: graduates who emigrate during or immediately after
training and never enter the Tunisian practising stock. Entrants are distributed
over ages 29–33 with weights \((0.15, 0.30, 0.30, 0.15, 0.10)\).

This formulation is deliberate. Because residents are not enumerated in the
practising stock, emigration during residency and non-entry are
observationally equivalent in aggregate data. \(\sigma\) absorbs both.

### 2.2 Emigration from the practising stock

Post-entry emigration is modelled as a total annual flow \(M(t)\), allocated
across ages using a fixed relative age profile \(w_a\):

\[
e_a(t) = \min\left(\frac{M(t)\,w_a}{\sum_b N_b(t)\,w_b},\; \bar e\right),
\qquad M(t)=m(t)\,\Pi(t)\,\varepsilon(t),
\]

where \(m(t)\) is the calibrated baseline flow, \(\Pi(t)\) is a scenario and
trend multiplier, \(\varepsilon(t)\) is a projection-only shock (1 before 2025),
and \(\bar e=0.35\) prevents implausible single-year hazards.

The age profile \(w_a\) is highest at 30–34, about 60% of peak at 35–39, and
declines to near zero after 55:

| Age | 25–29 | 30–34 | 35–39 | 40–44 | 45–49 | 50–54 | 55–59 | 60+ |
|---|---|---|---|---|---|---|---|---|
| Relative weight | 0.85 | 1.00 | 0.60 | 0.35 | 0.20 | 0.10 | 0.04 | 0.01 |

The profile is an assumption informed by the repeated finding that most
Tunisian emigrants are young physicians [1–3]. It is varied in sensitivity
analysis (`emig_tilt`). The model does **not** estimate age-specific emigration
rates from data.

### 2.3 Return migration and the return-eligible pool

\[
R(t) = \rho(t)\,D(t),
\]

with returns distributed over ages 33–50 (peak 38–41). Return migrants enter the
practising stock with probability 0.85 (return retention); the remainder rejoin
the pool. The pool evolves as

\[
D(t+1) = D(t)\,[1-\rho(t)-\delta] + M(t) + X(t) + (1-\theta)R(t),
\]

where \(\delta\) is an attrition hazard (death abroad, onward migration and
permanent settlement) and \(\theta=0.85\) is return retention. The pool is not a
diaspora estimate. With \(\delta=0.08\) and \(\rho=0.02\), the mean duration in
the pool is about 10 years and the eventual return probability is about 20%.
Both are varied in sensitivity analysis.

### 2.4 Retirement and mortality

Retirement is applied through age-specific hazards \(r_a\) consistent with
Tunisian legal ages (62 in the public sector since Law 2019-37; 60 in the
private sector; 65–70 for hospitalo-university professors):

| Age | <60 | 60–61 | 62 | 63–64 | 65–69 | 70+ |
|---|---|---|---|---|---|---|
| Annual retirement hazard | 0 | 0.20 | 0.45 | 0.35 | 0.45 | 1.00 |

Mortality hazards \(q_a\) are 0.001 at ages 25–54, 0.004 at 55–64, 0.015 at
65–74 and 0.05 at 75+.

Mortality is applied first, then retirement among survivors:

\[
N_{a+1}(t+1) = N_a(t)\,(1-q_a)(1-r_a)(1-e_a), \qquad a=25,\ldots,74,
\]

with the open-ended 75+ group absorbing survivors. This ordering keeps the
survival factor non-negative at all ages (the earlier draft subtracted the
hazards simultaneously, which was incorrect at 70+).

## 3. Initial conditions

The 2008 age distribution is taken from the CNOM 2007–2008 report, which
reports physicians by age group (25–30: 2 000; 30–35: 2 109; 35–40: 2 468;
40–45: 1 946; 45–50: 2 041; 50–55: 1 241; 55–60: 535; 60–65: 144; 65+: 132).
The distribution is spread uniformly within five-year bands and scaled to a
2008 practising stock of 12 600 (WHO estimated 12 996 physicians in 2010).

The initial return-eligible pool is 4 000, consistent with OECD country-of-birth
estimates of about 4 000 in 2015/16 plus non-OECD destinations. The sensitivity
of the 2040 projection to the initial stock and pool is reported.

## 4. Exogenous series

### 4.1 Graduates

The graduate series is anchored on published estimates:

- 987 graduates in 2013 and 1 128 in 2021, with exact geometric growth of about
  1.68% per year between the two anchors [4];
- 1 305 in 2024, a geometric interpolation from 2021 (5.0% per year);
- constant at 1 305 after 2024 in the baseline.

The 2021–2024 acceleration is explicit and uncertain. Two alternatives are
tested: continued 1.7% growth after 2024 (1 709 by 2040) and a constant 1 900
(an upper-bound ministerial statement). Training expansion is implemented as a
multiplier applied to graduates from 2031; those graduates enter practice from
2036.

### 4.2 Historical emigration trend

Post-entry emigration intensity rises linearly from 60% of its 2024 value in
2017 to 100% in 2024, reflecting the reported acceleration. After 2024 it is
held constant in the baseline. Structural sensitivity lets post-entry emigration
grow at 3%, 5% or 7% per year, and separately lets both pre- and post-entry
margins grow at the same rate. These are distinct assumptions.

## 5. Calibration

The free parameter is the post-entry emigration flow \(m\). For each parameter
draw, \(m\) is solved numerically so that the simulated 2024 stock equals the
observed 15 315. This is a one-dimensional root-finding problem; the stock is
monotone decreasing in \(m\). The calibration is exact: the maximum absolute
error across 2 000 accepted draws is 0.14 physicians. There is no calibration
residual multiplying the historical flow.

Calibration targets the 2024 endpoint rather than minimising the error over the
whole 2017–2024 series because the 2020–2021 observations contain an unresolved
administrative discontinuity (the public-sector count fell by 725 in 2020 while
the private sector grew by 91). Goodness of fit is nevertheless reported for the
full series and for the series excluding 2020–2021.

The calibration does **not** identify \(m\) and \(\sigma\) separately. It
identifies a ridge: a higher \(\sigma\) (more graduates entering practice)
requires a higher \(m\) to reproduce the same stock. This ridge is mapped in
Figure 2 and in `outputs/tables/identifiability_grid.csv`. Two thresholds are
reported:

- an **acceptable fit** of RMSE ≤2% of the mean observed stock (about 302
  physicians);
- a **strict fit** of RMSE ≤1.10 times the best RMSE.

The implied 2024 return-eligible pool is also screened against destination
stocks: 4 000–10 000 is treated as a plausible band, allowing for non-OECD
destinations and unregistered physicians.

## 6. Parameter table

| Parameter | Symbol | Central value | Range / distribution | Status | Basis |
|---|---|---|---|---|---|
| Practising physicians, 2024 | \(N(2024)\) | 15 315 | — | Observed | INS / MoH |
| Medical graduates, 2013 / 2021 / 2024 | \(G\) | 987 / 1 128 / 1 305 | 987–1 900 | Observed / reconstructed | Zehnati 2024; ministerial statements |
| Pipeline retention | \(\sigma\) | 0.55 | Beta, mean 0.55, SD 0.12 (0.30–0.80) | Estimated / assumed | Calibration; no direct data |
| Post-entry emigration, 2024 | \(m\) | 349 | Calibrated per draw | Estimated | Calibration |
| Total emigration, 2024 | \(M+X\) | 841 | 582–1 497 acceptable; 582–1 405 destination-consistent | Estimated | Derived |
| Pipeline non-entry share | \(1-\sigma\) | 0.45 | 0.20–0.70 | Assumed | Model structure |
| Pre-entry share of total emigration, 2024 | \(X/(X+M)\) | 0.59 | Varies | Derived | Model output |
| Return rate | \(\rho\) | 0.020 | Beta, mean 0.02, SD 0.01 (0.005–0.05) | Assumed | No Tunisian data; informed by Varga 2017 |
| Diaspora attrition | \(\delta\) | 0.08 | Uniform, 0.04–0.15 | Assumed | Reconciliation with destination stocks |
| Return retention | \(\theta\) | 0.85 | Uniform, 0.75–0.95 | Assumed | Re-emigration and non-practice |
| Emigration age profile | \(w_a\) | See §2.2 | Lognormal tilt, median 1.0, log-SD 0.15 | Assumed | Survey evidence on young emigrants |
| Retirement age | \(r_a\) | 60–70 | Shift ±1.5 years | Observed (legal) + assumed | Law 2019-37; CNRPS/CNSS |
| Initial stock, 2008 | \(N(2008)\) | 12 600 | Normal, SD 400 | Indirect estimate | WHO 2010; CNOM 2008 |
| Initial return-eligible pool, 2008 | \(D(2008)\) | 4 000 | 2 000–8 000 | Indirect estimate | OECD; CNOM France; German statistics |
| Population, 2024 | — | 11 972 169 | — | Observed | INS 2024 census |
| Population growth | — | UN WPP medium | — | Projected | UN WPP 2024, rescaled |

## 7. Scenarios

All retention and return scenarios begin in 2026 and are phased in linearly over
three years. The central effect sizes are deliberately moderate and are varied
in the scenario uncertainty analysis.

| Scenario | Emigration multiplier | Reduction in pre-entry emigration | Return-rate multiplier | Training multiplier |
|---|---|---|---|---|
| Business as usual | 1.00 | 0 | 1.00 | 1.00 |
| Remuneration and working conditions | 0.70 | 30% | 1.00 | 1.00 |
| Professional development and careers | 0.85 | 15% | 1.00 | 1.00 |
| Return and diaspora reintegration | 1.00 | 0 | 1.75 | 1.00 |
| Expanded training capacity | 1.00 | 0 | 1.00 | 1.30 (from 2031) |
| Combined retention and return | 0.65 | 35% | 1.75 | 1.00 |

The 30% emigration reduction in the remuneration scenario is an assumption, not
an estimate. It is broadly consistent with the Ghanaian evidence that a 10%
wage increase reduced annual attrition by about 12.5% relative [5,6], scaled up
for a package that also addresses conditions and security. The low and high
effect sizes (15% and 45% reductions) bracket a plausible range.

The return scenario raises the annual return rate from 2.0% to 3.5% of the
return-eligible pool, a 75% increase. This is a policy assumption; there is no
Tunisian estimate of return responsiveness.

The training scenario implements the announced 30% expansion of admissions,
with graduates affected from 2031 and entrants from 2036.

## 8. Uncertainty analysis

### 8.1 Probabilistic

Two thousand parameter draws are generated from the distributions in Table S4.
For each draw, \(m\) is recalibrated exactly to the 2024 stock, and all scenarios
are simulated with the same draw (common random numbers). This separates
scenario differences from parameter uncertainty.

Reported intervals are 5th–95th percentiles. They represent uncertainty in
**parameters**, conditional on the model structure. They do not represent
uncertainty about the structure itself.

### 8.2 Structural

Because the most consequential uncertainty is structural — the future path of
emigration — the model is also run with post-entry emigration intensity growing
at 3%, 5% and 7% per year after 2024, and separately with both pre- and
post-entry margins growing. These are deterministic scenarios, not probability
statements. The earlier draft applied the trend to both margins without saying
so; the revision separates the two.

### 8.3 Sensitivity

Deterministic one-at-a-time sensitivity varies each parameter from its 10th to
its 90th percentile, recalibrating \(m\) each time, and records the change in the
2040 workforce. True partial rank correlation coefficients (PRCC) are computed
by rank-residualising the 2040 stock and each parameter on all other parameters.
Marginal Spearman correlations are reported for comparison. The calibrated
emigration flow is not an independent parameter; its structural effect is
reported separately (±20% change: +3 960/−7 595 physicians in 2040).

### 8.4 Break-even and costs

A two-dimensional grid varies the retention effect (0–50% reduction in
emigration) and the training effect (0–100% expansion of graduates). A 9.6%
retention effect matches a 30% training expansion; a 94% training expansion is
needed to match a 30% retention effect. Illustrative costs attach unit costs to
each scenario; they are undiscounted, exclude infrastructure and demand-side
costs, and treat wages as transfers. See §9 of the manuscript and Table S11.

## 9. Key structural assumptions

1. **Single occupational stock.** All practising physicians are treated as
   equivalent. No specialty, sector or regional disaggregation.
2. **Exogenous training.** Graduate numbers are not affected by labour-market
   conditions or emigration.
3. **Exogenous emigration.** Emigration responds to policy only through the
   assumed scenario multipliers; there is no wage or queueing mechanism.
4. **Fixed age profile of emigration.** The level, not the shape, is varied.
5. **No temporary migration.** Emigration is treated as an exit from the
   practising stock; returns are modelled from the return-eligible pool. This
   overstates net losses if circular migration is common.
6. **No demand constraint.** The model does not ask whether the health system
   can employ the projected physicians.
7. **No external validation.** The historical comparison is a consistency
   check, not validation.

## 10. Software and reproducibility

The model uses NumPy, pandas, SciPy and Matplotlib. The random seed is
`20261121`. Running `python run_all.py` regenerates every figure, table and
number in the manuscript. `pytest -q` runs the model and analysis tests. All
parameter values and data are in `data/processed/` and `src/`.

## References

1. Ajmi M, Kahloul M, Kacem I, Chouchane A, Ben Mansour S, Slama Y, et al.
   Immigration projects among young doctors in Tunisia. *Eur Psychiatry.*
   2022;65(S1):S633–S634.
2. Tabib F, Guermazi F, Zouari A, Ben Abdallah M, Hentati S, Baati I, et al.
   Emigration intentionality among Tunisian interns and residents in medicine.
   *Eur Psychiatry.* 2022;65(S1):S633.
3. Haouari W, Omri S, Labyadh A, Feki R, Gassara I, Charfi N, et al. Factors
   driving the emigration intentions of young Tunisian medical professionals.
   *Eur Psychiatry.* 2024;67(S1):S829–S830.
4. Zehnati A. L'émigration des médecins, en particulier vers la France, et la
   desserte médicale au Maghreb. *Belgeo.* 2024;(1). doi:10.4000/12ihd
5. Antwi J, Phillips DC. Wages and health worker retention: evidence from
   public sector wage reforms in Ghana. *J Dev Econ.* 2013;102:101–115.
6. Okeke EN. Do higher salaries lower physician migration? *Health Policy
   Plan.* 2014;29(5):603–614.
