# R/05_workforce_model.R
# ==============================================================================
# Pipeline Step 5: Competing-Risk Markov Cohort Stock-Flow Engine
# Project: Physician Exodus from Tunisia
# ==============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
})

run_workforce_simulation <- function(baseline_stock_36,
                                     params,
                                     years = 2020:2050,
                                     policy_modifiers = list(),
                                     inflow_expansion = 0.0) {
  n_years <- length(years)
  n_cells <- nrow(baseline_stock_36)
  
  # State tensor storage: rows = 36 cells, cols = years
  stock_mat <- matrix(0, nrow = n_cells, ncol = n_years,
                      dimnames = list(as.character(1:n_cells), as.character(years)))
  emig_mat <- matrix(0, nrow = n_cells, ncol = n_years,
                     dimnames = list(as.character(1:n_cells), as.character(years)))
  retire_mat <- matrix(0, nrow = n_cells, ncol = n_years,
                      dimnames = list(as.character(1:n_cells), as.character(years)))
  
  # Initialize baseline stock at t0 = 2020
  stock_mat[, "2020"] <- baseline_stock_36$headcount_2020
  
  # Baseline graduate inflow capacity (2020 = ~835 graduates, growing with quotas)
  base_inflow_series <- c(
    "2020" = 835, "2021" = 860, "2022" = 900, "2023" = 935, "2024" = 990
  )
  
  # Cumulative diaspora tracking
  cumulative_emigrants <- 3300 * params$clearance_mult # baseline prior ~2,475 abroad at 2020
  cum_emig_series <- numeric(n_years)
  names(cum_emig_series) <- years
  cum_emig_series["2020"] <- cumulative_emigrants
  
  # Tracking summary arrays
  annual_returns <- numeric(n_years)
  names(annual_returns) <- years
  annual_inflows <- numeric(n_years)
  names(annual_inflows) <- years
  
  # Inflow distribution weights across the 36 cells (New graduates enter Early/Resident)
  inflow_weights <- numeric(n_cells)
  for (i in 1:n_cells) {
    row <- baseline_stock_36[i, ]
    if (row$career_stage == "early_resident") {
      # 70% public hospital/residency, 30% private/solo
      s_w <- if (row$sector == "public") 0.70 else 0.30
      # 75% coastal, 25% interior
      g_w <- if (row$geography_macro == "coastal_metro") 0.75 else 0.25
      # Specialty shares: General 42%, Medical 33%, Surgical 25%
      sp_w <- switch(row$specialty_cluster,
                     general_medicine = 0.42,
                     medical_specialties = 0.33,
                     surgical_critical_care = 0.25)
      inflow_weights[i] <- s_w * g_w * sp_w
    }
  }
  inflow_weights <- inflow_weights / sum(inflow_weights)
  
  # Base transition rates
  p_early_to_mid <- 0.10   # average duration in early-career is 10 yrs
  p_mid_to_senior <- 0.05  # average duration in mid-career is 20 yrs
  
  lagged_rate <- 0.04
  
  # Main Simulation Loop (2020 to 2050)
  for (t_idx in 1:(n_years - 1)) {
    y_curr <- years[t_idx]
    y_next <- years[t_idx + 1]
    
    current_stock <- stock_mat[, as.character(y_curr)]
    
    # 1. Compute Migration Outflow Probabilities from RUM Engine
    mig_probs <- compute_migration_probabilities(
      stock_df = baseline_stock_36,
      year = y_curr,
      params = params,
      policy_modifiers = policy_modifiers,
      lagged_departure_rate = lagged_rate
    )
    
    # 2. Competing Risk Multi-State Hazard Formulation
    # Convert marginal discrete probabilities to instantaneous intensities
    lambda_emig <- -log(pmax(1 - mig_probs, 1e-6))
    
    lambda_retire <- numeric(n_cells)
    lambda_trans <- numeric(n_cells)
    lambda_geo <- numeric(n_cells)
    lambda_age <- numeric(n_cells)
    
    for (i in 1:n_cells) {
      row <- baseline_stock_36[i, ]
      
      # Retirement hazard (senior cohort)
      if (row$career_stage == "senior") {
        lambda_retire[i] <- -log(max(1 - params$retire_senior_rate, 1e-6))
      }
      
      # Public to private sector transition hazard
      if (row$sector == "public") {
        lambda_trans[i] <- -log(max(1 - params$pub_priv_trans_rate, 1e-6))
      }
      
      # Domestic inter-regional transition hazard (Interior -> Coastal public sector)
      if (row$sector == "public" && row$geography_macro == "interior_underserved") {
        lambda_geo[i] <- -log(max(1 - params$geo_internal_trans_rate, 1e-6))
      }
      
      # Aging progression hazard
      if (row$career_stage == "early_resident") {
        lambda_age[i] <- -log(max(1 - p_early_to_mid, 1e-6))
      } else if (row$career_stage == "mid_career") {
        lambda_age[i] <- -log(max(1 - p_mid_to_senior, 1e-6))
      }
    }
    
    # Total combined exit hazard per cell
    lambda_total <- lambda_emig + lambda_retire + lambda_trans + lambda_geo + lambda_age
    
    # Competing risk multinomial probabilities (sum strictly <= 1; 1 - p_stay)
    p_exit_total <- 1 - exp(-lambda_total)
    p_stay <- exp(-lambda_total)
    
    scale_factor <- ifelse(lambda_total > 0, p_exit_total / lambda_total, 0)
    
    prob_emig <- lambda_emig * scale_factor
    prob_retire <- lambda_retire * scale_factor
    prob_trans <- lambda_trans * scale_factor
    prob_geo <- lambda_geo * scale_factor
    prob_age <- lambda_age * scale_factor
    
    # Calculate physical outflows
    cell_emigrants <- current_stock * prob_emig
    cell_retirements <- current_stock * prob_retire
    cell_trans_out <- current_stock * prob_trans
    cell_geo_out <- current_stock * prob_geo
    cell_aging_out <- current_stock * prob_age
    cell_stay <- current_stock * p_stay
    
    emig_mat[, as.character(y_curr)] <- cell_emigrants
    retire_mat[, as.character(y_curr)] <- cell_retirements
    total_emig_t <- sum(cell_emigrants)
    lagged_rate <- total_emig_t / max(sum(current_stock), 1)
    
    # 3. Diaspora Return Flow
    returns_t <- params$return_mig_rate * cumulative_emigrants
    annual_returns[as.character(y_curr)] <- returns_t
    
    cumulative_emigrants <- max(cumulative_emigrants + total_emig_t - returns_t, 0)
    cum_emig_series[as.character(y_next)] <- cumulative_emigrants
    
    # 4. Graduate Inflow for y_next
    base_inflow <- if (as.character(y_curr) %in% names(base_inflow_series)) {
      base_inflow_series[as.character(y_curr)]
    } else {
      990 * (1 + inflow_expansion)
    }
    realized_graduates <- base_inflow * params$grad_rate
    annual_inflows[as.character(y_curr)] <- realized_graduates
    cell_inflows <- realized_graduates * inflow_weights
    
    # 5. Returnees Allocation: 30% Public CHU, 70% Private Practice across Mid-Career/Senior
    return_weights <- numeric(n_cells)
    for (i in 1:n_cells) {
      row <- baseline_stock_36[i, ]
      if (row$career_stage %in% c("mid_career", "senior")) {
        sec_w <- if (row$sector == "public") 0.30 else 0.70
        geo_w <- if (row$geography_macro == "coastal_metro") 0.80 else 0.20
        return_weights[i] <- sec_w * geo_w
      }
    }
    return_weights <- return_weights / sum(return_weights)
    cell_returns <- returns_t * return_weights
    
    # 6. Redistribute Internal Transfers and Career Aging
    aging_in <- numeric(n_cells)
    trans_in <- numeric(n_cells)
    geo_in <- numeric(n_cells)
    
    for (i in 1:n_cells) {
      row <- baseline_stock_36[i, ]
      
      # Aging transfer into next career stage
      if (row$career_stage == "early_resident") {
        tgt_idx <- which(baseline_stock_36$career_stage == "mid_career" &
                           baseline_stock_36$sector == row$sector &
                           baseline_stock_36$geography_macro == row$geography_macro &
                           baseline_stock_36$specialty_cluster == row$specialty_cluster)
        aging_in[tgt_idx] <- aging_in[tgt_idx] + cell_aging_out[i]
      } else if (row$career_stage == "mid_career") {
        tgt_idx <- which(baseline_stock_36$career_stage == "senior" &
                           baseline_stock_36$sector == row$sector &
                           baseline_stock_36$geography_macro == row$geography_macro &
                           baseline_stock_36$specialty_cluster == row$specialty_cluster)
        aging_in[tgt_idx] <- aging_in[tgt_idx] + cell_aging_out[i]
      }
      
      # Sector transfer (Public -> Private matching cell)
      if (row$sector == "public") {
        tgt_idx <- which(baseline_stock_36$sector == "private" &
                           baseline_stock_36$career_stage == row$career_stage &
                           baseline_stock_36$geography_macro == row$geography_macro &
                           baseline_stock_36$specialty_cluster == row$specialty_cluster)
        trans_in[tgt_idx] <- trans_in[tgt_idx] + cell_trans_out[i]
      }
      
      # Geographic transfer (Interior public -> Coastal public matching cell)
      if (row$sector == "public" && row$geography_macro == "interior_underserved") {
        tgt_idx <- which(baseline_stock_36$sector == "public" &
                           baseline_stock_36$geography_macro == "coastal_metro" &
                           baseline_stock_36$career_stage == row$career_stage &
                           baseline_stock_36$specialty_cluster == row$specialty_cluster)
        geo_in[tgt_idx] <- geo_in[tgt_idx] + cell_geo_out[i]
      }
    }
    
    # 7. Exact Stock Conservation Update
    next_stock <- cell_stay +
      cell_inflows +
      cell_returns +
      aging_in +
      trans_in +
      geo_in
    
    stock_mat[, as.character(y_next)] <- pmax(next_stock, 0.0)
  }
  
  # Fill last year outflows
  last_y <- as.character(years[n_years])
  prev_y <- as.character(years[n_years - 1])
  emig_mat[, last_y] <- emig_mat[, prev_y]
  retire_mat[, last_y] <- retire_mat[, prev_y]
  annual_inflows[last_y] <- annual_inflows[prev_y]
  annual_returns[last_y] <- annual_returns[prev_y]
  
  # Build Tidy Annual Summary Tibble
  summary_list <- lapply(years, function(yr) {
    st_col <- stock_mat[, as.character(yr)]
    em_col <- emig_mat[, as.character(yr)]
    ret_col <- retire_mat[, as.character(yr)]
    
    tot_stock <- sum(st_col)
    pub_stock <- sum(st_col[baseline_stock_36$sector == "public"])
    priv_stock <- sum(st_col[baseline_stock_36$sector == "private"])
    coastal_stock <- sum(st_col[baseline_stock_36$geography_macro == "coastal_metro"])
    interior_stock <- sum(st_col[baseline_stock_36$geography_macro == "interior_underserved"])
    
    pop_t <- 11850000 * ((1 + 0.007)^(yr - 2023))
    pop_coastal_t <- pop_t * 0.70
    pop_interior_t <- pop_t * 0.30
    
    tibble(
      year = yr,
      total_active_stock = tot_stock,
      public_stock = pub_stock,
      private_stock = priv_stock,
      coastal_stock = coastal_stock,
      interior_stock = interior_stock,
      annual_emigrants = sum(em_col),
      annual_graduates = annual_inflows[as.character(yr)],
      annual_returns = annual_returns[as.character(yr)],
      annual_retirements = sum(ret_col),
      cumulative_diaspora = cum_emig_series[as.character(yr)],
      national_density_per_10k = (tot_stock / pop_t) * 10000,
      coastal_density_per_10k = (coastal_stock / pop_coastal_t) * 10000,
      interior_density_per_10k = (interior_stock / pop_interior_t) * 10000,
      public_interior_stock = sum(st_col[baseline_stock_36$sector == "public" & 
                                           baseline_stock_36$geography_macro == "interior_underserved"])
    )
  })
  
  summary_df <- bind_rows(summary_list)
  
  list(
    summary = summary_df,
    stock_mat = stock_mat,
    emig_mat = emig_mat,
    retire_mat = retire_mat
  )
}
