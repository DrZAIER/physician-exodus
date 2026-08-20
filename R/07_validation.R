# R/07_validation.R
# ==============================================================================
# Pipeline Step 7: Out-of-Sample Holdout and Destination Registry Validation
# Project: Physician Exodus from Tunisia
# ==============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
})

validate_out_of_sample <- function(calibration_results, params, imported_data) {
  message("[07_validation] Performing out-of-sample holdout and external destination registry validation...")
  
  sim_summary <- calibration_results$fit_summary
  
  # 1. Ingested Destination Registries (Official DREES & BAK datasets from 01_import)
  dest_raw <- imported_data$destination_registries %>%
    filter(year >= 2020 & year <= 2024) %>%
    group_by(year) %>%
    summarise(
      france_padhue_inflow = sum(inflow_headcount[country_code == "FRA"], na.rm = TRUE),
      germany_bak_inflow = sum(inflow_headcount[country_code == "DEU"], na.rm = TRUE),
      total_euro_intake = sum(inflow_headcount, na.rm = TRUE),
      .groups = "drop"
    )
  
  # 2. Merge with Simulated Departure Flows
  val_df <- sim_summary %>%
    select(year, annual_emigrants) %>%
    left_join(dest_raw, by = "year") %>%
    mutate(
      simulated_euro_dest = annual_emigrants * 0.82, # ~82% of departures target France+Germany per CNOM
      intake_ratio = total_euro_intake / simulated_euro_dest,
      error = simulated_euro_dest - total_euro_intake
    )
  
  mean_intake_coverage <- mean(val_df$intake_ratio) * 100
  corr_alignment <- cor(val_df$simulated_euro_dest, val_df$total_euro_intake)
  
  # 3. Holdout Evaluation Metrics (2022-2024)
  holdout_metrics <- calibration_results$holdout_metrics
  
  message(sprintf("[07_validation] Out-of-Sample Holdout (2022-2024): Stock MAPE = %0.2f%% | Flow MAPE = %0.2f%%.",
                  holdout_metrics$mape_stock, holdout_metrics$mape_flow))
  message(sprintf("[07_validation] Destination Registry Alignment: Concordance r = %0.3f, Destination Coverage = %0.1f%%.",
                  corr_alignment, mean_intake_coverage))
  
  list(
    val_table = val_df,
    concordance_r = corr_alignment,
    mean_coverage = mean_intake_coverage,
    holdout_metrics = holdout_metrics
  )
}
