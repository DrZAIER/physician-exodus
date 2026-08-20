# R/08_policy_scenarios.R
# ==============================================================================
# Pipeline Step 8: Policy Counterfactual Simulation Engine (2020-2050)
# Project: Physician Exodus from Tunisia
# ==============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(purrr)
})

run_all_policy_scenarios <- function(baseline_stock_36, params, years = 2020:2050) {
  message("[08_policy_scenarios] Simulating 6 policy counterfactual scenarios to 2050...")
  
  scenario_results <- list()
  
  # Structural Utility Shifts: Delta_U = -ln(1 - RRR)
  wage_shift <- -log(max(1 - params$scen1_rrr_wage, 1e-4))
  infra_shift <- -log(max(1 - params$scen2_rrr_infra, 1e-4))
  rural_shift <- -log(max(1 - params$scen3_rrr_rural, 1e-4))
  
  # ----------------------------------------------------------------------------
  # SCEN_0: Status Quo (Baseline)
  # ----------------------------------------------------------------------------
  res_scen0 <- run_workforce_simulation(
    baseline_stock_36 = baseline_stock_36,
    params = params,
    years = years
  )
  scenario_results[["SCEN_0"]] <- list(
    scenario_id = "SCEN_0",
    scenario_name = "Status Quo (Baseline)",
    data = res_scen0$summary,
    raw = res_scen0
  )
  
  # ----------------------------------------------------------------------------
  # SCEN_1: Public Sector Remuneration Reform (+30% Wage)
  # ----------------------------------------------------------------------------
  res_scen1 <- run_workforce_simulation(
    baseline_stock_36 = baseline_stock_36,
    params = params,
    years = years,
    policy_modifiers = list(
      wage_utility_shift = wage_shift
    )
  )
  scenario_results[["SCEN_1"]] <- list(
    scenario_id = "SCEN_1",
    scenario_name = "Public Remuneration Reform (+30%)",
    data = res_scen1$summary,
    raw = res_scen1
  )
  
  # ----------------------------------------------------------------------------
  # SCEN_2: Workplace & Hospital Infrastructure Upgrades
  # ----------------------------------------------------------------------------
  res_scen2 <- run_workforce_simulation(
    baseline_stock_36 = baseline_stock_36,
    params = params,
    years = years,
    policy_modifiers = list(
      infra_utility_shift = infra_shift
    )
  )
  scenario_results[["SCEN_2"]] <- list(
    scenario_id = "SCEN_2",
    scenario_name = "Workplace & Infrastructure Upgrades",
    data = res_scen2$summary,
    raw = res_scen2
  )
  
  # ----------------------------------------------------------------------------
  # SCEN_3: Regional Retention & Rural Incentive Package
  # ----------------------------------------------------------------------------
  res_scen3 <- run_workforce_simulation(
    baseline_stock_36 = baseline_stock_36,
    params = params,
    years = years,
    policy_modifiers = list(
      rural_utility_shift = rural_shift
    )
  )
  scenario_results[["SCEN_3"]] <- list(
    scenario_id = "SCEN_3",
    scenario_name = "Regional Retention & Rural Package",
    data = res_scen3$summary,
    raw = res_scen3
  )
  
  # ----------------------------------------------------------------------------
  # SCEN_4: Medical Training Quota & Residency Expansion (+15% Intake)
  # ----------------------------------------------------------------------------
  res_scen4 <- run_workforce_simulation(
    baseline_stock_36 = baseline_stock_36,
    params = params,
    years = years,
    inflow_expansion = params$scen4_quota_exp
  )
  scenario_results[["SCEN_4"]] <- list(
    scenario_id = "SCEN_4",
    scenario_name = "Training Quota Expansion (+15%)",
    data = res_scen4$summary,
    raw = res_scen4
  )
  
  # ----------------------------------------------------------------------------
  # SCEN_5: Comprehensive Synergistic Reform Package
  # ----------------------------------------------------------------------------
  res_scen5 <- run_workforce_simulation(
    baseline_stock_36 = baseline_stock_36,
    params = params,
    years = years,
    policy_modifiers = list(
      wage_utility_shift = wage_shift,
      infra_utility_shift = infra_shift,
      rural_utility_shift = rural_shift
    ),
    inflow_expansion = params$scen4_quota_exp * 0.50 # moderate balanced expansion
  )
  scenario_results[["SCEN_5"]] <- list(
    scenario_id = "SCEN_5",
    scenario_name = "Comprehensive Synergistic Reform",
    data = res_scen5$summary,
    raw = res_scen5
  )
  
  # Combine into comparison dataframe
  combined_df <- map_dfr(scenario_results, function(x) {
    x$data %>% mutate(scenario_id = x$scenario_id, scenario_name = x$scenario_name)
  })
  
  message("[08_policy_scenarios] Completed simulation across all 6 policy counterfactuals.")
  
  list(
    scenario_runs = scenario_results,
    combined_data = combined_df
  )
}
