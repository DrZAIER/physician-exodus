# run_analysis.R
# ==============================================================================
# Master Pipeline Orchestrator: Physician Exodus from Tunisia (2020-2050)
# ==============================================================================

cat("\n==============================================================================\n")
cat("  PHYSICIAN EXODUS FROM TUNISIA: WORKFORCE SIMULATION & ECONOMIC EVALUATION   \n")
cat("==============================================================================\n\n")

start_time <- proc.time()

# 1. Source all modular R scripts
cat("[1/11] Sourcing pipeline modules...\n")
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

# 2. Ingest Data
cat("\n[2/11] Ingesting empirical raw datasets and metadata...\n")
raw_data <- import_raw_data("data")

# 3. Clean & Initialize 36-Cell Tensor via IPF
cat("\n[3/11] Cleaning data and initializing 36-cell stock tensor via IPF (t0 = 2020)...\n")
clean_res <- clean_and_initialize_stock(raw_data, alpha_baseline = 0.88)
baseline_stock_36 <- clean_res$baseline_stock_36

# 4. Ingest Parameters & Set Up Samplers
cat("\n[4/11] Ingesting parameters and configuring Monte Carlo sampler...\n")
base_params <- get_baseline_parameters("data/metadata/parameter_registry.csv")
psa_draws <- sample_psa_parameters(n_draws = 1000, seed = 2026)

# 5. Historical 2-Parameter Calibration (2015-2024)
cat("\n[5/11] Calibrating 2 scalar parameters (beta_0, delta_beta_2021+)...\n")
calib_res <- calibrate_historical_model(baseline_stock_36, base_params, raw_data)
calibrated_params <- calib_res$calibrated_params

# 6. Out-of-Sample Validation vs Destination Registries
cat("\n[6/11] Validating outflows against French DREES and German BAK registries...\n")
val_res <- validate_out_of_sample(calib_res, calibrated_params, raw_data)

# 7. Simulate 6 Policy Counterfactual Scenarios (2020-2050)
cat("\n[7/11] Simulating 6 policy counterfactual scenarios (2020-2050)...\n")
scenario_res <- run_all_policy_scenarios(baseline_stock_36, calibrated_params, years = 2020:2050)

# 8. Economic Evaluation (CCA, BIA, ICERs)
cat("\n[8/11] Conducting Cost-Consequence and Budget Impact evaluation...\n")
econ_res <- evaluate_economic_impact(scenario_res$scenario_runs, calibrated_params)

# 9. Sensitivity Analysis: Tornado & 1,000-Draw Monte Carlo PSA
cat("\n[9/11] Executing Deterministic Tornado & 1,000-Draw Monte Carlo PSA...\n")
tornado_res <- run_one_way_sensitivity(baseline_stock_36, calibrated_params)
psa_res <- run_probabilistic_sensitivity(baseline_stock_36, calibrated_params, psa_params_list = psa_draws, n_draws = 1000)

# 10. Generate Figures & Formatted Tables
cat("\n[10/11] Generating publication figures and formatted output tables...\n")
fig_tab_res <- generate_all_figures_and_tables(
  baseline_stock_36 = baseline_stock_36,
  calibration_results = calib_res,
  scenario_results = scenario_res,
  economic_results = econ_res,
  tornado_results = tornado_res,
  psa_results = psa_res,
  output_dir = "outputs"
)

# 11. Pipeline Completion & Execution Summary
total_elapsed <- (proc.time() - start_time)["elapsed"]

cat("\n==============================================================================\n")
cat("                           PIPELINE EXECUTION SUMMARY                         \n")
cat("==============================================================================\n")
cat(sprintf("Total Execution Time       : %0.2f seconds\n", total_elapsed))
cat(sprintf("Historical Calibration Fit : Stock MAPE = %0.2f%% | Flow MAPE = %0.2f%%\n",
            calib_res$metrics$mape_stock, calib_res$metrics$mape_flow))
cat(sprintf("Out-of-Sample Concordance  : r = %0.3f | Overseas Coverage = %0.1f%%\n",
            val_res$concordance_r, val_res$mean_coverage))
cat(sprintf("SCEN_0 Status Quo (2050)   : %0.0f active doctors (%0.1f per 10k)\n",
            tail(scenario_res$scenario_runs$SCEN_0$data$total_active_stock, 1),
            tail(scenario_res$scenario_runs$SCEN_0$data$national_density_per_10k, 1)))
cat(sprintf("SCEN_5 Comprehensive (2050): %0.0f active doctors (%0.1f per 10k)\n",
            tail(scenario_res$scenario_runs$SCEN_5$data$total_active_stock, 1),
            tail(scenario_res$scenario_runs$SCEN_5$data$national_density_per_10k, 1)))
cat(sprintf("Emigrants Averted (2050)   : %0.0f physicians (SCEN_5 vs SCEN_0)\n",
            econ_res$cca_summary$cumulative_emigrants_averted[econ_res$cca_summary$scenario_id == "SCEN_5"]))
cat(sprintf("Public ICER (SCEN_5)       : %0.0f TND per discounted public physician-year retained\n",
            econ_res$cca_summary$icer_public_retained_tnd[econ_res$cca_summary$scenario_id == "SCEN_5"]))
cat("==============================================================================\n")
cat("Status: PIPELINE COMPLETED SUCCESSFULLY WITH ZERO ERRORS.\n\n")
