# R/09_economic_evaluation.R
# ==============================================================================
# Pipeline Step 9: CHEERS-Compliant Cost-Consequence & Economic Evaluation Engine
# Project: Physician Exodus from Tunisia
# ==============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(purrr)
})

evaluate_economic_impact <- function(scenario_runs, params) {
  message("[09_economic_evaluation] Conducting CHEERS-compliant Cost-Consequence and Budget Impact evaluation (2025-2050)...")
  
  scen0_df <- scenario_runs$SCEN_0$data %>% filter(year >= 2025)
  disc_rate <- params$discount_rate
  
  eval_list <- list()
  
  for (scen_name in names(scenario_runs)) {
    scen_df <- scenario_runs[[scen_name]]$data %>% filter(year >= 2025)
    n_yrs <- nrow(scen_df)
    
    # Discount factors: (1 + r)^-(t - 2025)
    disc_factors <- (1 + disc_rate)^(-(scen_df$year - 2025))
    
    # 1. Cost Calculations (TND)
    # A. Public Wage Bill Expansion (Inframarginal Payroll Costing)
    wage_cost_t <- if (scen_name %in% c("SCEN_1", "SCEN_5")) {
      rate_inc <- if (scen_name == "SCEN_1") params$scen1_wage_inc else params$scen1_wage_inc * 0.80
      scen_df$public_stock * (params$public_base_salary * rate_inc)
    } else {
      rep(0, n_yrs)
    }
    
    # B. Complementary Clinical Operational Support (Nursing, Diagnostics, Consumables per CHEERS Item 13)
    comp_factor <- if (!is.null(params$complementary_cost_factor)) params$complementary_cost_factor else 0.35
    complementary_cost_t <- wage_cost_t * comp_factor
    
    # C. Infrastructure & Security Capex/Opex
    infra_cost_t <- if (scen_name %in% c("SCEN_2", "SCEN_5")) {
      rep(params$infra_capex_annual, n_yrs)
    } else {
      rep(0, n_yrs)
    }
    
    # D. Rural Hardship Package
    rural_cost_t <- if (scen_name %in% c("SCEN_3", "SCEN_5")) {
      scen_df$public_interior_stock * ((params$public_base_salary * 0.40) + 6000)
    } else {
      rep(0, n_yrs)
    }
    
    # E. Training Expansion Operating Costs & Fiscal Deadweight Loss on Emigrants
    extra_graduates_t <- scen_df$annual_graduates - scen0_df$annual_graduates
    extra_emigrants_t <- scen_df$annual_emigrants - scen0_df$annual_emigrants
    
    train_cost_t <- if (scen_name %in% c("SCEN_4", "SCEN_5")) {
      # Gross operational education outlay for expanded student cohorts
      gross_exp_cost <- extra_graduates_t * params$gross_train_cost
      # Deadweight subsidy loss on incremental emigrants leaving without serving
      deadweight_emig_loss <- pmax(extra_emigrants_t, 0) * params$net_train_cost
      gross_exp_cost + deadweight_emig_loss
    } else {
      rep(0, n_yrs)
    }
    
    # Total Gross Intervention Outlay
    gross_intervention_cost <- wage_cost_t + complementary_cost_t + infra_cost_t + rural_cost_t + train_cost_t
    
    # F. Net Training Loss Avoided (Offset Savings from Retained Physicians)
    emig_averted_t <- scen0_df$annual_emigrants - scen_df$annual_emigrants
    train_savings_t <- pmax(emig_averted_t, 0) * params$net_train_cost
    
    # Net Fiscal Cost
    net_cost_t <- gross_intervention_cost - train_savings_t
    
    # Discounted Streams
    disc_net_cost_t <- net_cost_t * disc_factors
    disc_gross_cost_t <- gross_intervention_cost * disc_factors
    
    # 2. Workforce Outcomes (Physical Headcounts & Retained Years)
    phys_years_retained_total <- scen_df$total_active_stock - scen0_df$total_active_stock
    phys_years_retained_public <- scen_df$public_stock - scen0_df$public_stock
    phys_years_retained_interior <- scen_df$interior_stock - scen0_df$interior_stock
    
    disc_phys_years_total <- phys_years_retained_total * disc_factors
    disc_phys_years_public <- phys_years_retained_public * disc_factors
    disc_phys_years_interior <- phys_years_retained_interior * disc_factors
    
    # Totals (2025 to 2050)
    tot_undisc_net_cost <- sum(net_cost_t)
    tot_disc_net_cost <- sum(disc_net_cost_t)
    tot_disc_gross_cost <- sum(disc_gross_cost_t)
    
    tot_emig_averted <- sum(emig_averted_t)
    tot_undisc_phys_years_public <- sum(phys_years_retained_public)
    tot_disc_phys_years_public <- sum(disc_phys_years_public)
    tot_disc_phys_years_interior <- sum(disc_phys_years_interior)
    tot_disc_phys_years_total <- sum(disc_phys_years_total)
    
    # Incremental Cost-Effectiveness Ratios (ICERs)
    icer_public <- if (tot_disc_phys_years_public > 0) tot_disc_net_cost / tot_disc_phys_years_public else NA_real_
    icer_interior <- if (tot_disc_phys_years_interior > 0) tot_disc_net_cost / tot_disc_phys_years_interior else NA_real_
    
    eval_list[[scen_name]] <- list(
      scenario_id = scen_name,
      scenario_name = scenario_runs[[scen_name]]$scenario_name,
      total_undisc_net_cost_tnd = tot_undisc_net_cost,
      total_disc_net_cost_tnd = tot_disc_net_cost,
      total_disc_gross_cost_tnd = tot_disc_gross_cost,
      total_emig_averted = tot_emig_averted,
      undisc_phys_years_public = tot_undisc_phys_years_public,
      disc_phys_years_total = tot_disc_phys_years_total,
      disc_phys_years_public = tot_disc_phys_years_public,
      disc_phys_years_interior = tot_disc_phys_years_interior,
      icer_per_public_phys_year = icer_public,
      icer_per_interior_phys_year = icer_interior,
      annual_streams = tibble(
        year = scen_df$year,
        gross_cost = gross_intervention_cost,
        wage_cost = wage_cost_t,
        comp_cost = complementary_cost_t,
        infra_cost = infra_cost_t,
        rural_cost = rural_cost_t,
        train_cost = train_cost_t,
        train_savings = train_savings_t,
        net_cost = net_cost_t,
        emig_averted = emig_averted_t,
        phys_years_public = phys_years_retained_public,
        phys_years_interior = phys_years_retained_interior
      )
    )
  }
  
  # Summary Table (CHEERS Cost-Consequence Matrix)
  cca_table <- map_dfr(eval_list, function(x) {
    tibble(
      scenario_id = x$scenario_id,
      scenario_name = x$scenario_name,
      undiscounted_net_cost_million_tnd = round(x$total_undisc_net_cost_tnd / 1e6, 2),
      discounted_net_cost_million_tnd = round(x$total_disc_net_cost_tnd / 1e6, 2),
      cumulative_emigrants_averted = round(x$total_emig_averted),
      undiscounted_public_phys_years = round(x$undisc_phys_years_public),
      discounted_public_phys_years = round(x$disc_phys_years_public),
      discounted_interior_phys_years = round(x$disc_phys_years_interior),
      icer_public_retained_tnd = round(x$icer_per_public_phys_year),
      icer_interior_retained_tnd = round(x$icer_per_interior_phys_year)
    )
  })
  
  message("[09_economic_evaluation] Completed CCA and ICER computations across all scenarios.")
  
  list(
    cca_summary = cca_table,
    scenario_details = eval_list
  )
}
