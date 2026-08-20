# R/03_parameters.R
# ==============================================================================
# Pipeline Step 3: Parameter Registry Parsing & Standard Parametric PSA Sampler
# Project: Physician Exodus from Tunisia
# ==============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

get_baseline_parameters <- function(param_registry_file = "data/metadata/parameter_registry.csv") {
  message("[03_parameters] Ingesting parameter registry and constructing baseline parameter list...")
  
  params_df <- readr::read_csv(param_registry_file, show_col_types = FALSE)
  
  # Create named lookup from base_value as pure numeric scalars
  p <- setNames(as.numeric(params_df$base_value), params_df$parameter)
  
  list(
    # Structural & Demographic Multipliers
    active_ratio = unname(p["PAR_ACTIVE_RATIO"]),                         # 0.88
    clearance_mult = unname(p["PAR_CLEARANCE_MULT"]),                     # 0.75
    realization_kappa_base = unname(p["PAR_REALIZATION_KAPPA_BASE"]),     # 0.35
    kappa_gen = unname(p["PAR_KAPPA_GENERALIST"]),                       # 0.245
    kappa_med = unname(p["PAR_KAPPA_MEDICAL"]),                           # 0.350
    kappa_surg = unname(p["PAR_KAPPA_SURGICAL"]),                         # 0.490
    
    # Utility Strata Modifiers
    stage_mod_resident = unname(p["PAR_STAGE_MOD_RESIDENT"]),             # +0.65
    stage_mod_senior = unname(p["PAR_STAGE_MOD_SENIOR"]),                 # -0.85
    sector_mod_public = unname(p["PAR_SECTOR_MOD_PUBLIC"]),               # +0.40
    geo_mod_interior = unname(p["PAR_GEO_MOD_INTERIOR"]),                 # +0.30
    spec_mod_surgical = unname(p["PAR_SPEC_MOD_SURGICAL"]),               # +0.35
    spec_mod_medical = unname(p["PAR_SPEC_MOD_MEDICAL"]),                 # +0.15
    
    # Demographic Transitions & Competing Risks
    grad_rate = unname(p["PAR_INTAKE_GRAD_RATE"]),                         # 0.92
    retire_senior_rate = unname(p["PAR_RETIRE_SENIOR_RATE"]),             # 0.125 (8-year sojourn)
    geo_internal_trans_rate = unname(p["PAR_GEO_INTERNAL_TRANS_RATE"]),   # 0.045 (Interior -> Coast)
    return_mig_rate = unname(p["PAR_RETURN_MIG_RATE"]),                   # 0.015
    pub_priv_trans_rate = unname(p["PAR_PUB_PRIV_TRANS_RATE"]),           # 0.018
    
    # Calibration Intercepts
    beta_0 = unname(p["PAR_BETA_0_SCALE"]),                               # -1.87
    delta_beta_2021 = unname(p["PAR_DELTA_BETA_2021"]),                   # 0.94
    
    # Behavioral Utility Weights (Mandeville 2014 / North African Evidence)
    beta_wage = unname(p["PAR_BETA_WAGE_DCE"]),                           # 0.48
    beta_infra = unname(p["PAR_BETA_INFRA_DCE"]),                         # 0.36
    beta_rural = unname(p["PAR_BETA_RURAL_DCE"]),                         # 0.31
    peer_feedback = unname(p["PAR_PEER_FEEDBACK_COEF"]),                   # 0.25
    
    # Policy Counterfactual Levers & Decay
    scen1_wage_inc = unname(p["PAR_SCEN1_WAGE_INCREASE"]),                # 0.30
    scen1_rrr_wage = unname(p["PAR_SCEN1_RETENTION_RRR"]),                # 0.12 (structural wage elasticity)
    scen2_rrr_infra = unname(p["PAR_SCEN2_INFRA_RRR"]),                   # 0.10
    scen3_rrr_rural = unname(p["PAR_SCEN3_RURAL_RRR"]),                   # 0.18
    scen4_quota_exp = unname(p["PAR_SCEN4_QUOTA_EXPANSION"]),             # 0.15
    scen4_ros_ret = unname(p["PAR_SCEN4_ROS_COMPLIANCE"]),                # 0.75
    policy_decay_annual = unname(p["PAR_POLICY_DECAY_ANNUAL"]),           # 0.035 (3.5%/year)
    
    # Economic Evaluation & CHEERS Costing
    complementary_cost_factor = unname(p["PAR_COMPLEMENTARY_COST_FACTOR"]),# 0.35
    discount_rate = unname(p["PAR_DISCOUNT_RATE"]),                       # 0.03
    gross_train_cost = unname(p["PAR_GROSS_TRAINING_COST_MD"]),           # 85,000 TND
    resident_labor_offset = unname(p["PAR_RESIDENT_LABOR_OFFSET"]),       # 0.40
    net_train_cost = unname(p["PAR_NET_TRAINING_COST_MD"]),               # 51,000 TND
    public_base_salary = unname(p["PAR_PUBLIC_BASE_SALARY_ANN"]),         # 36,000 TND
    infra_capex_annual = unname(p["PAR_INFRA_CAPEX_ANNUAL"])              # 25,000,000 TND
  )
}

sample_psa_parameters <- function(n_draws = 1000, seed = 2026) {
  message(sprintf("[03_parameters] Generating %d Monte Carlo parameter sets using Beta, Log-Normal, and Gamma distributions...", n_draws))
  set.seed(seed)
  
  psa_list <- vector("list", n_draws)
  
  for (i in 1:n_draws) {
    # 1. Structural Multipliers (Beta distributions)
    active_ratio <- rbeta(1, 176, 24)       # mean 0.88, [0.85, 0.90]
    clearance_mult <- rbeta(1, 75, 25)      # mean 0.75, [0.65, 0.85]
    realization_kappa_base <- rbeta(1, 35, 65) # mean 0.35, [0.25, 0.45]
    
    kappa_gen <- realization_kappa_base * rbeta(1, 70, 30) # ~0.70x
    kappa_med <- realization_kappa_base * 1.00
    kappa_surg <- realization_kappa_base * (1 + rbeta(1, 40, 60)) # ~1.40x
    
    # 2. Demographic Transition & Competing Risk Rates (Beta)
    grad_rate <- rbeta(1, 92, 8)            # mean 0.92
    retire_senior_rate <- rbeta(1, 25, 175) # mean 0.125
    geo_internal_trans_rate <- rbeta(1, 18, 382) # mean 0.045
    return_mig_rate <- rbeta(1, 15, 985)    # mean 0.015
    pub_priv_trans_rate <- rbeta(1, 18, 982)# mean 0.018
    
    # 3. Calibration Intercepts & Strata Modifiers (Normal)
    beta_0 <- rnorm(1, -1.87, 0.15)
    delta_beta_2021 <- rnorm(1, 0.94, 0.12)
    
    stage_mod_resident <- rnorm(1, 0.65, 0.08)
    stage_mod_senior <- rnorm(1, -0.85, 0.10)
    sector_mod_public <- rnorm(1, 0.40, 0.06)
    geo_mod_interior <- rnorm(1, 0.30, 0.05)
    spec_mod_surgical <- rnorm(1, 0.35, 0.06)
    spec_mod_medical <- rnorm(1, 0.15, 0.03)
    
    # 4. Behavioral Utility Weights (Normal / Beta)
    beta_wage <- rnorm(1, 0.48, 0.06)
    beta_infra <- rnorm(1, 0.36, 0.05)
    beta_rural <- rnorm(1, 0.31, 0.05)
    peer_feedback <- rbeta(1, 25, 75)       # mean 0.25
    
    # 5. Policy Scenarios & Decay (Log-Normal for RRR, Beta for compliance)
    scen1_wage_inc <- runif(1, 0.20, 0.50)
    scen1_rrr_wage <- rlnorm(1, meanlog = log(0.12), sdlog = 0.15)
    scen2_rrr_infra <- rlnorm(1, meanlog = log(0.10), sdlog = 0.15)
    scen3_rrr_rural <- rlnorm(1, meanlog = log(0.18), sdlog = 0.15)
    scen4_quota_exp <- runif(1, 0.10, 0.25)
    scen4_ros_ret <- rbeta(1, 75, 25)       # mean 0.75
    policy_decay_annual <- rbeta(1, 14, 386)# mean 0.035
    
    # 6. Economic Costing (Gamma distributions for positive costs)
    discount_rate <- sample(c(0.00, 0.03, 0.05, 0.08), 1, prob = c(0.1, 0.6, 0.2, 0.1))
    gross_train_cost <- rgamma(1, shape = 25, scale = 3400) # mean 85,000
    resident_labor_offset <- rbeta(1, 40, 60)               # mean 0.40
    net_train_cost <- gross_train_cost * (1 - resident_labor_offset)
    public_base_salary <- rgamma(1, shape = 36, scale = 1000) # mean 36,000
    infra_capex_annual <- rgamma(1, shape = 25, scale = 1000000) # mean 25M
    complementary_cost_factor <- rgamma(1, shape = 35, scale = 0.01) # mean 0.35
    
    psa_list[[i]] <- list(
      draw_id = i,
      active_ratio = active_ratio,
      clearance_mult = clearance_mult,
      realization_kappa_base = realization_kappa_base,
      kappa_gen = kappa_gen,
      kappa_med = kappa_med,
      kappa_surg = kappa_surg,
      stage_mod_resident = stage_mod_resident,
      stage_mod_senior = stage_mod_senior,
      sector_mod_public = sector_mod_public,
      geo_mod_interior = geo_mod_interior,
      spec_mod_surgical = spec_mod_surgical,
      spec_mod_medical = spec_mod_medical,
      grad_rate = grad_rate,
      retire_senior_rate = retire_senior_rate,
      geo_internal_trans_rate = geo_internal_trans_rate,
      return_mig_rate = return_mig_rate,
      pub_priv_trans_rate = pub_priv_trans_rate,
      beta_0 = beta_0,
      delta_beta_2021 = delta_beta_2021,
      beta_wage = beta_wage,
      beta_infra = beta_infra,
      beta_rural = beta_rural,
      peer_feedback = peer_feedback,
      scen1_wage_inc = scen1_wage_inc,
      scen1_rrr_wage = scen1_rrr_wage,
      scen2_rrr_infra = scen2_rrr_infra,
      scen3_rrr_rural = scen3_rrr_rural,
      scen4_quota_exp = scen4_quota_exp,
      scen4_ros_ret = scen4_ros_ret,
      policy_decay_annual = policy_decay_annual,
      complementary_cost_factor = complementary_cost_factor,
      discount_rate = discount_rate,
      gross_train_cost = gross_train_cost,
      resident_labor_offset = resident_labor_offset,
      net_train_cost = net_train_cost,
      public_base_salary = public_base_salary,
      infra_capex_annual = infra_capex_annual
    )
  }
  
  message("[03_parameters] Successfully generated 1,000 parametric PSA parameter sets.")
  psa_list
}
