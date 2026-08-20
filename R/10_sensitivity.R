# R/10_sensitivity.R
# ==============================================================================
# Pipeline Step 10: Deterministic Tornado & 1,000-Draw Monte Carlo PSA Engine
# Project: Physician Exodus from Tunisia
# ==============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(purrr)
})

run_one_way_sensitivity <- function(baseline_stock_36, base_params) {
  message("[10_sensitivity] Running One-Way Deterministic Sensitivity Analysis (Tornado)...")
  
  param_ranges <- list(
    realization_kappa_base = c(low = 0.25, high = 0.45),
    scen1_rrr_wage = c(low = 0.08, high = 0.18),
    scen2_rrr_infra = c(low = 0.06, high = 0.16),
    scen3_rrr_rural = c(low = 0.12, high = 0.26),
    policy_decay_annual = c(low = 0.02, high = 0.06),
    retire_senior_rate = c(low = 0.09, high = 0.16),
    geo_internal_trans_rate = c(low = 0.03, high = 0.065),
    discount_rate = c(low = 0.00, high = 0.08),
    net_train_cost = c(low = 39000, high = 66000),
    active_ratio = c(low = 0.85, high = 0.90)
  )
  
  # Base run under SCEN_5
  base_runs <- run_all_policy_scenarios(baseline_stock_36, base_params)
  base_eval <- evaluate_economic_impact(base_runs$scenario_runs, base_params)$cca_summary %>%
    filter(scenario_id == "SCEN_5")
  base_retained <- base_eval$discounted_public_phys_years
  base_cost <- base_eval$discounted_net_cost_million_tnd
  
  tornado_results <- list()
  
  for (p_name in names(param_ranges)) {
    # Low run
    p_low <- base_params
    p_low[[p_name]] <- param_ranges[[p_name]]["low"]
    
    # Dynamic stock scaling for active_ratio
    stock_low <- baseline_stock_36
    if (p_name == "active_ratio") {
      stock_low$headcount_2020 <- stock_low$headcount_2020 * (p_low$active_ratio / base_params$active_ratio)
    }
    
    runs_low <- run_all_policy_scenarios(stock_low, p_low)
    eval_low <- evaluate_economic_impact(runs_low$scenario_runs, p_low)$cca_summary %>%
      filter(scenario_id == "SCEN_5")
    
    # High run
    p_high <- base_params
    p_high[[p_name]] <- param_ranges[[p_name]]["high"]
    
    stock_high <- baseline_stock_36
    if (p_name == "active_ratio") {
      stock_high$headcount_2020 <- stock_high$headcount_2020 * (p_high$active_ratio / base_params$active_ratio)
    }
    
    runs_high <- run_all_policy_scenarios(stock_high, p_high)
    eval_high <- evaluate_economic_impact(runs_high$scenario_runs, p_high)$cca_summary %>%
      filter(scenario_id == "SCEN_5")
    
    swing_ret <- abs(eval_high$discounted_public_phys_years - eval_low$discounted_public_phys_years)
    swing_c <- abs(eval_high$discounted_net_cost_million_tnd - eval_low$discounted_net_cost_million_tnd)
    
    tornado_results[[p_name]] <- tibble(
      parameter = p_name,
      base_value = base_params[[p_name]],
      low_val = param_ranges[[p_name]]["low"],
      high_val = param_ranges[[p_name]]["high"],
      retained_low = eval_low$discounted_public_phys_years,
      retained_high = eval_high$discounted_public_phys_years,
      cost_low = eval_low$discounted_net_cost_million_tnd,
      cost_high = eval_high$discounted_net_cost_million_tnd,
      swing_retained = swing_ret,
      swing_cost_million_tnd = swing_c
    )
  }
  
  tornado_df <- bind_rows(tornado_results) %>% arrange(desc(swing_retained))
  message("[10_sensitivity] Completed One-Way Sensitivity Analysis.")
  tornado_df
}

run_probabilistic_sensitivity <- function(baseline_stock_36, 
                                          base_params, 
                                          psa_params_list = NULL,
                                          n_draws = 1000) {
  if (is.null(psa_params_list)) {
    psa_sampled <- sample_psa_parameters(n_draws = n_draws)
    psa_params_list <- psa_sampled$psa_params
  } else if (is.list(psa_params_list) && "psa_params" %in% names(psa_params_list)) {
    psa_params_list <- psa_params_list$psa_params
  }
  
  n_eval <- length(psa_params_list)
  message(sprintf("[10_sensitivity] Executing %d-draw Monte Carlo PSA...", n_eval))
  
  psa_records <- vector("list", n_eval)
  
  for (i in 1:n_eval) {
    p_draw <- psa_params_list[[i]]
    
    # Scale stock if active_ratio is sampled
    stock_draw <- baseline_stock_36
    if (!is.null(p_draw$active_ratio)) {
      stock_draw$headcount_2020 <- stock_draw$headcount_2020 * (p_draw$active_ratio / 0.88)
    }
    
    # Simulate Scenarios
    sim_runs <- run_all_policy_scenarios(stock_draw, p_draw)
    econ_eval <- evaluate_economic_impact(sim_runs$scenario_runs, p_draw)$cca_summary
    
    scen5_row <- econ_eval %>% filter(scenario_id == "SCEN_5")
    scen1_row <- econ_eval %>% filter(scenario_id == "SCEN_1")
    scen3_row <- econ_eval %>% filter(scenario_id == "SCEN_3")
    
    psa_records[[i]] <- tibble(
      draw_id = i,
      # SCEN_5
      scen5_net_cost_m = scen5_row$discounted_net_cost_million_tnd,
      scen5_emig_averted = scen5_row$cumulative_emigrants_averted,
      scen5_public_years = scen5_row$discounted_public_phys_years,
      scen5_interior_years = scen5_row$discounted_interior_phys_years,
      scen5_icer_public = scen5_row$icer_public_retained_tnd,
      # SCEN_1
      scen1_public_years = scen1_row$discounted_public_phys_years,
      scen1_icer_public = scen1_row$icer_public_retained_tnd,
      # SCEN_3
      scen3_interior_years = scen3_row$discounted_interior_phys_years,
      scen3_icer_interior = scen3_row$icer_interior_retained_tnd
    )
    
    if (i %% 200 == 0) {
      message(sprintf("[10_sensitivity] Processed %d / %d Monte Carlo draws...", i, n_eval))
    }
  }
  
  psa_df <- bind_rows(psa_records)
  
  # Compute 95% Credible Intervals (2.5%, 50%, 97.5%)
  summary_stats <- tibble(
    metric = c(
      "SCEN_5 Discounted Net Cost (Million TND)",
      "SCEN_5 Emigrants Averted",
      "SCEN_5 Public Physician-Years Retained",
      "SCEN_5 Interior Physician-Years Retained",
      "SCEN_5 ICER per Public Physician-Year (TND)"
    ),
    median = c(
      median(psa_df$scen5_net_cost_m, na.rm = TRUE),
      median(psa_df$scen5_emig_averted, na.rm = TRUE),
      median(psa_df$scen5_public_years, na.rm = TRUE),
      median(psa_df$scen5_interior_years, na.rm = TRUE),
      median(psa_df$scen5_icer_public, na.rm = TRUE)
    ),
    lower_95_cri = c(
      quantile(psa_df$scen5_net_cost_m, 0.025, na.rm = TRUE),
      quantile(psa_df$scen5_emig_averted, 0.025, na.rm = TRUE),
      quantile(psa_df$scen5_public_years, 0.025, na.rm = TRUE),
      quantile(psa_df$scen5_interior_years, 0.025, na.rm = TRUE),
      quantile(psa_df$scen5_icer_public, 0.025, na.rm = TRUE)
    ),
    upper_95_cri = c(
      quantile(psa_df$scen5_net_cost_m, 0.975, na.rm = TRUE),
      quantile(psa_df$scen5_emig_averted, 0.975, na.rm = TRUE),
      quantile(psa_df$scen5_public_years, 0.975, na.rm = TRUE),
      quantile(psa_df$scen5_interior_years, 0.975, na.rm = TRUE),
      quantile(psa_df$scen5_icer_public, 0.975, na.rm = TRUE)
    )
  )
  
  # CEAC Computation across WTP thresholds (0 to 500,000 TND)
  wtp_seq <- seq(0, 500000, by = 5000)
  ceac_list <- lapply(wtp_seq, function(wtp) {
    nmb_scen5 <- (wtp * psa_df$scen5_public_years) - (psa_df$scen5_net_cost_m * 1e6)
    nmb_scen1 <- (wtp * psa_df$scen1_public_years) - (psa_df$scen1_public_years * psa_df$scen1_icer_public)
    
    tibble(
      wtp_threshold_tnd = wtp,
      prob_cost_effective_scen5 = mean(nmb_scen5 > 0, na.rm = TRUE),
      prob_cost_effective_scen1 = mean(nmb_scen1 > 0, na.rm = TRUE)
    )
  })
  
  ceac_df <- bind_rows(ceac_list)
  
  message("[10_sensitivity] Completed 1,000-draw Monte Carlo PSA and CEAC generation.")
  
  list(
    psa_draws = psa_df,
    summary_cri = summary_stats,
    ceac_table = ceac_df
  )
}
