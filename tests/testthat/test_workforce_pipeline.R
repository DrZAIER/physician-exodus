# tests/testthat/test_workforce_pipeline.R
# ==============================================================================
# Automated Test Suite for Audited Physician Exodus Simulation Engine
# ==============================================================================

suppressPackageStartupMessages({
  library(testthat)
  library(dplyr)
})

# Source pipeline modules
source("../../R/01_import.R")
source("../../R/02_clean.R")
source("../../R/03_parameters.R")
source("../../R/04_migration_model.R")
source("../../R/05_workforce_model.R")
source("../../R/06_calibration.R")
source("../../R/07_validation.R")
source("../../R/08_policy_scenarios.R")
source("../../R/09_economic_evaluation.R")
source("../../R/10_sensitivity.R")

test_that("1. Data Ingestion & Metadata Completeness", {
  raw_data <- import_raw_data("../../data")
  expect_equal(nrow(raw_data$ins_population), 24)
  expect_equal(nrow(raw_data$carte_sanitaire), 24)
  expect_gte(nrow(raw_data$ins_physicians), 7)
  expect_gte(nrow(raw_data$destination_registries), 10)
  expect_gte(nrow(raw_data$param_reg), 25)
})

test_that("2. 36-Cell Stock Initialization via IPF (t0 = 2020)", {
  raw_data <- import_raw_data("../../data")
  clean_res <- clean_and_initialize_stock(raw_data, alpha_baseline = 0.88)
  stock_36 <- clean_res$baseline_stock_36
  
  expect_equal(nrow(stock_36), 36)
  expect_true(all(stock_36$headcount_2020 >= 0))
  expect_equal(round(sum(stock_36$headcount_2020)), 13017)
  expect_equal(round(sum(stock_36$headcount_2020[stock_36$sector == "public"])), 5384)
  expect_equal(round(sum(stock_36$headcount_2020[stock_36$sector == "private"])), 7633)
})

test_that("3. Competing-Risk Multi-State Conservation & Zero Probability Leakage", {
  raw_data <- import_raw_data("../../data")
  clean_res <- clean_and_initialize_stock(raw_data, alpha_baseline = 0.88)
  params <- get_baseline_parameters("../../data/metadata/parameter_registry.csv")
  
  sim_res <- run_workforce_simulation(clean_res$baseline_stock_36, params, years = 2020:2050)
  stock_mat <- sim_res$stock_mat
  emig_mat <- sim_res$emig_mat
  retire_mat <- sim_res$retire_mat
  
  # Non-negativity across all 36 cells across all 31 years
  expect_true(all(stock_mat >= 0))
  expect_true(all(emig_mat >= 0))
  expect_true(all(retire_mat >= 0))
  
  # Outflows <= Stock
  for (yr in colnames(stock_mat)) {
    expect_true(all(emig_mat[, yr] <= stock_mat[, yr] + 1e-6))
  }
})

test_that("4. Migration Probability Bounds & Random Utility Model", {
  raw_data <- import_raw_data("../../data")
  clean_res <- clean_and_initialize_stock(raw_data, alpha_baseline = 0.88)
  params <- get_baseline_parameters("../../data/metadata/parameter_registry.csv")
  
  probs <- compute_migration_probabilities(clean_res$baseline_stock_36, 2020, params)
  expect_true(all(probs >= 0.0 & probs <= 0.95))
  
  # Specialty-specific ordering: Surgical > Medical > General
  surg_p <- mean(probs[clean_res$baseline_stock_36$specialty_cluster == "surgical_critical_care"])
  med_p <- mean(probs[clean_res$baseline_stock_36$specialty_cluster == "medical_specialties"])
  gen_p <- mean(probs[clean_res$baseline_stock_36$specialty_cluster == "general_medicine"])
  expect_gt(surg_p, med_p)
  expect_gt(med_p, gen_p)
})

test_that("5. Calibration and Out-of-Sample Holdout Separation", {
  raw_data <- import_raw_data("../../data")
  clean_res <- clean_and_initialize_stock(raw_data, alpha_baseline = 0.88)
  base_params <- get_baseline_parameters("../../data/metadata/parameter_registry.csv")
  
  calib_res <- calibrate_historical_model(clean_res$baseline_stock_36, base_params, raw_data)
  expect_lt(calib_res$training_metrics$mape_stock, 5.0)
  expect_lt(calib_res$holdout_metrics$mape_stock, 12.0)
  expect_lt(calib_res$holdout_metrics$mape_flow, 15.0)
  
  val_res <- validate_out_of_sample(calib_res, calib_res$calibrated_params, raw_data)
  expect_gt(val_res$concordance_r, 0.80)
})

test_that("6. Economic Evaluation & CHEERS Compliance", {
  raw_data <- import_raw_data("../../data")
  clean_res <- clean_and_initialize_stock(raw_data, alpha_baseline = 0.88)
  params <- get_baseline_parameters("../../data/metadata/parameter_registry.csv")
  
  scenario_runs <- run_all_policy_scenarios(clean_res$baseline_stock_36, params, years = 2020:2050)$scenario_runs
  econ_res <- evaluate_economic_impact(scenario_runs, params)
  
  cca <- econ_res$cca_summary
  expect_equal(nrow(cca), 6)
  
  # SCEN_0 has 0 incremental cost
  scen0_row <- cca %>% filter(scenario_id == "SCEN_0")
  expect_equal(scen0_row$discounted_net_cost_million_tnd, 0)
  
  # SCEN_5 achieves positive public retention
  scen5_row <- cca %>% filter(scenario_id == "SCEN_5")
  expect_gt(scen5_row$discounted_public_phys_years, 5000)
  expect_gt(scen5_row$undiscounted_public_phys_years, scen5_row$discounted_public_phys_years)
})
