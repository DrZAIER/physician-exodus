# R/02_clean.R
# ==============================================================================
# Pipeline Step 2: Data Cleaning, Harmonization, and 36-Cell IPF Tensor Construction
# Project: Physician Exodus from Tunisia
# ==============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(readr)
})

clean_and_initialize_stock <- function(imported_data, alpha_baseline = 0.88) {
  message("[02_clean] Harmonizing data and initializing 36-cell stock tensor via IPF (2020)...")
  
  ins_phys <- imported_data$ins_physicians
  carte_san <- imported_data$carte_sanitaire
  ins_pop <- imported_data$ins_population
  
  # 1. Macro-Regional Harmonization
  # Aggregate Carte Sanitaire public physicians by macro-geography
  cs_macro <- carte_san %>%
    group_by(geography_macro) %>%
    summarise(
      public_specialists = sum(public_specialists),
      public_generalists = sum(public_generalists),
      total_public = sum(total_public_physicians),
      hospital_beds = sum(hospital_beds),
      .groups = "drop"
    )
  
  # 2. Baseline 2020 Stock Targets (INS Stat 123)
  ins_2020 <- ins_phys %>% filter(year == 2020)
  raw_total_2020 <- ins_2020$total_physicians # 14,792
  raw_public_2020 <- ins_2020$public_physicians # 6,118
  raw_private_2020 <- ins_2020$private_physicians # 8,674
  
  # Apply baseline active practice filter (alpha = 0.88)
  active_total_2020 <- round(raw_total_2020 * alpha_baseline) # 13,017
  active_public_2020 <- round(raw_public_2020 * alpha_baseline) # 5,384
  active_private_2020 <- active_total_2020 - active_public_2020 # 7,633
  
  # 3. 36-Cell State Space Definition
  career_stages <- c("early_resident", "mid_career", "senior")
  sectors <- c("public", "private")
  geographies <- c("coastal_metro", "interior_underserved")
  specialties <- c("general_medicine", "medical_specialties", "surgical_critical_care")
  
  grid_36 <- expand.grid(
    career_stage = career_stages,
    sector = sectors,
    geography_macro = geographies,
    specialty_cluster = specialties,
    stringsAsFactors = FALSE
  )
  
  # 4. Marginal Target Distributions (Official Empirical Margins)
  # Margins 1: Sector
  target_sector <- c(public = active_public_2020, private = active_private_2020)
  
  # Margins 2: Geography (Public distribution ~81% Coastal / ~19% Interior; Private ~76% Coastal / ~24% Interior)
  prop_coastal_pub <- cs_macro$total_public[cs_macro$geography_macro == "coastal_metro"] / sum(cs_macro$total_public)
  target_geo_pub <- c(
    coastal_metro = active_public_2020 * prop_coastal_pub,
    interior_underserved = active_public_2020 * (1 - prop_coastal_pub)
  )
  target_geo_priv <- c(
    coastal_metro = active_private_2020 * 0.77,
    interior_underserved = active_private_2020 * 0.23
  )
  
  # Margins 3: Career Stage (Early: 35%, Mid: 45%, Senior: 20%)
  stage_weights <- c(early_resident = 0.35, mid_career = 0.45, senior = 0.20)
  
  # Margins 4: Specialty Cluster (General: 42%, Medical: 33%, Surgical/Critical Care: 25%)
  spec_weights <- c(general_medicine = 0.42, medical_specialties = 0.33, surgical_critical_care = 0.25)
  
  # 5. Iterative Proportional Fitting (IPF / Raking)
  # Initialize seed tensor with product of independent priors
  grid_36$initial_weight <- apply(grid_36, 1, function(row) {
    s_w <- if (row["sector"] == "public") target_sector["public"] else target_sector["private"]
    st_w <- stage_weights[row["career_stage"]]
    sp_w <- spec_weights[row["specialty_cluster"]]
    g_w <- if (row["sector"] == "public") {
      target_geo_pub[row["geography_macro"]] / target_sector["public"]
    } else {
      target_geo_priv[row["geography_macro"]] / target_sector["private"]
    }
    s_w * st_w * sp_w * g_w
  })
  
  # Rake to exact sector and macro targets
  tolerance <- 1e-8
  max_iter <- 100
  grid_36$headcount <- grid_36$initial_weight
  
  for (iter in 1:max_iter) {
    # Step A: Fit to Sector totals
    current_sector <- aggregate(headcount ~ sector, data = grid_36, sum)
    for (s in names(target_sector)) {
      factor_s <- target_sector[s] / current_sector$headcount[current_sector$sector == s]
      grid_36$headcount[grid_36$sector == s] <- grid_36$headcount[grid_36$sector == s] * factor_s
    }
    
    # Step B: Fit to Geography by Sector totals
    for (s in c("public", "private")) {
      tgt_geo <- if (s == "public") target_geo_pub else target_geo_priv
      for (g in names(tgt_geo)) {
        sub_idx <- grid_36$sector == s & grid_36$geography_macro == g
        curr_g <- sum(grid_36$headcount[sub_idx])
        if (curr_g > 0) {
          grid_36$headcount[sub_idx] <- grid_36$headcount[sub_idx] * (tgt_geo[g] / curr_g)
        }
      }
    }
    
    # Step C: Fit to Specialty marginals
    current_spec <- aggregate(headcount ~ specialty_cluster, data = grid_36, sum)
    for (sp in names(spec_weights)) {
      tgt_sp <- active_total_2020 * spec_weights[sp]
      factor_sp <- tgt_sp / current_spec$headcount[current_spec$specialty_cluster == sp]
      grid_36$headcount[grid_36$specialty_cluster == sp] <- grid_36$headcount[grid_36$specialty_cluster == sp] * factor_sp
    }
    
    # Check convergence
    diff_tot <- abs(sum(grid_36$headcount) - active_total_2020)
    if (diff_tot < tolerance) break
  }
  
  grid_36$headcount_2020 <- round(grid_36$headcount, 2)
  grid_36$initial_weight <- NULL
  grid_36$headcount <- NULL
  
  # Verify Conservation
  stopifnot(abs(sum(grid_36$headcount_2020) - active_total_2020) < 1.0)
  stopifnot(all(grid_36$headcount_2020 >= 0))
  stopifnot(nrow(grid_36) == 36)
  
  message(sprintf("[02_clean] Baseline 36-cell stock initialized: Total = %0.1f active physicians (Public = %0.1f, Private = %0.1f).",
                  sum(grid_36$headcount_2020),
                  sum(grid_36$headcount_2020[grid_36$sector == "public"]),
                  sum(grid_36$headcount_2020[grid_36$sector == "private"])))
  
  list(
    baseline_stock_36 = grid_36,
    cs_macro = cs_macro,
    active_total_2020 = active_total_2020,
    active_public_2020 = active_public_2020,
    active_private_2020 = active_private_2020
  )
}
