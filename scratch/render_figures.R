# scratch/render_figures.R
suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(readr)
  library(ggplot2)
  library(scales)
  library(patchwork)
  library(ggrepel)
})

source("R/01_import.R")
source("R/02_clean.R")
source("R/03_parameters.R")
source("R/04_migration_model.R")
source("R/05_workforce_model.R")
source("R/06_calibration.R")
source("R/07_validation.R")
source("R/08_policy_scenarios.R")
source("R/09_economic_evaluation.R")
source("R/10_sensitivity.R")
source("R/11_figures_tables.R")

raw_data <- import_raw_data("data")
clean_res <- clean_and_initialize_stock(raw_data, alpha_baseline = 0.88)
base_params <- get_baseline_parameters("data/metadata/parameter_registry.csv")

calib_res <- calibrate_historical_model(clean_res$baseline_stock_36, base_params, raw_data)
scen_res <- run_all_policy_scenarios(clean_res$baseline_stock_36, calib_res$calibrated_params)
econ_res <- evaluate_economic_impact(scen_res$scenario_runs, calib_res$calibrated_params)
tornado_res <- run_one_way_sensitivity(clean_res$baseline_stock_36, calib_res$calibrated_params)

psa_list <- sample_psa_parameters(n_draws = 200, seed = 2026)
psa_res <- run_probabilistic_sensitivity(clean_res$baseline_stock_36, calib_res$calibrated_params, psa_params_list = psa_list)

generate_all_figures_and_tables(
  baseline_stock_36 = clean_res$baseline_stock_36,
  calibration_results = calib_res,
  scenario_results = scen_res,
  economic_results = econ_res,
  tornado_results = tornado_res,
  psa_results = psa_res,
  output_dir = "outputs"
)

message("Re-rendering complete!")
