# R/04_migration_model.R
# ==============================================================================
# Pipeline Step 4: Random Utility Migration Choice & Realization Engine
# Project: Physician Exodus from Tunisia
# ==============================================================================

suppressPackageStartupMessages({
  library(dplyr)
})

compute_migration_probabilities <- function(stock_df, 
                                            year, 
                                            params, 
                                            policy_modifiers = list(),
                                            lagged_departure_rate = 0.05) {
  # 1. Base Logit Intercept (Historical vs Post-2021 Crisis Regime)
  regime_shift <- if (year >= 2021) params$delta_beta_2021 else 0.0
  base_intercept <- params$beta_0 + regime_shift
  
  # 2. Structural Utility Modifiers (Parsed Directly from Parameter Registry)
  stage_mod <- c(
    early_resident = params$stage_mod_resident,
    mid_career = 0.0,
    senior = params$stage_mod_senior
  )
  
  sector_mod <- c(
    public = params$sector_mod_public,
    private = -0.5 * params$sector_mod_public
  )
  
  geo_mod <- c(
    coastal_metro = 0.0,
    interior_underserved = params$geo_mod_interior
  )
  
  spec_mod <- c(
    general_medicine = 0.0,
    medical_specialties = params$spec_mod_medical,
    surgical_critical_care = params$spec_mod_surgical
  )
  
  # Peer feedback loop (dynamic cohort feedback)
  peer_term <- params$peer_feedback * (lagged_departure_rate - 0.04)
  
  # Policy implementation and annual decay factor (starts in 2025)
  decay_factor <- if (year >= 2025) (1 - params$policy_decay_annual)^(year - 2025) else 0.0
  
  # 3. Compute Delta V for each of the 36 cells
  delta_v_vec <- numeric(nrow(stock_df))
  
  for (i in 1:nrow(stock_df)) {
    row <- stock_df[i, ]
    
    dv <- base_intercept + 
      stage_mod[row$career_stage] + 
      sector_mod[row$sector] + 
      geo_mod[row$geography_macro] + 
      spec_mod[row$specialty_cluster] + 
      peer_term
    
    # Apply Endogenous Policy Utility Shifts in Random Utility Framework
    if (!is.null(policy_modifiers$wage_utility_shift) && row$sector == "public") {
      dv <- dv - (policy_modifiers$wage_utility_shift * decay_factor)
    }
    if (!is.null(policy_modifiers$infra_utility_shift) && row$sector == "public") {
      dv <- dv - (policy_modifiers$infra_utility_shift * decay_factor)
    }
    if (!is.null(policy_modifiers$rural_utility_shift) && row$geography_macro == "interior_underserved") {
      dv <- dv - (policy_modifiers$rural_utility_shift * decay_factor)
    }
    if (!is.null(policy_modifiers$ros_compliance_shift) && row$career_stage == "early_resident") {
      dv <- dv - (policy_modifiers$ros_compliance_shift * decay_factor)
    }
    
    delta_v_vec[i] <- dv
  }
  
  # 4. Logistic Latent Willingness
  latent_prob <- 1 / (1 + exp(-delta_v_vec))
  
  # 5. Specialty-Specific Intention-to-Action Realization Vector
  base_k <- if (!is.null(params$realization_kappa_base)) params$realization_kappa_base else 0.35
  kappa_vec <- ifelse(
    stock_df$specialty_cluster == "general_medicine", base_k * 0.70,
    ifelse(stock_df$specialty_cluster == "surgical_critical_care", base_k * 1.40, base_k * 1.00)
  )
  
  realized_prob <- kappa_vec * latent_prob
  
  # Enforce strict probability bounds [0, 0.95]
  pmax(pmin(realized_prob, 0.95), 0.0)
}
