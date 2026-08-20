# R/06_calibration.R
# ==============================================================================
# Pipeline Step 6: 2-Parameter Historical Calibration with Strict Temporal Split
# Training Period: 2020-2021 | Out-of-Sample Holdout: 2022-2024
# Project: Physician Exodus from Tunisia
# ==============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(stats)
})

calibrate_historical_model <- function(baseline_stock_36,
                                       base_params,
                                       imported_data) {
  message("[06_calibration] Executing historical calibration with strict temporal split...")
  message("[06_calibration] Calibration Training Period: 2020-2021 | Out-of-Sample Holdout: 2022-2024")
  
  # 1. Observed Historical Data
  ins_full <- imported_data$ins_physicians %>%
    filter(year >= 2020 & year <= 2024) %>%
    mutate(obs_active_stock = total_physicians * base_params$active_ratio)
  
  cnom_full <- imported_data$cnom_emigration %>%
    filter(year >= 2020 & year <= 2024) %>%
    mutate(obs_realized_flow = cnom_good_standing_certificates * base_params$clearance_mult)
  
  # Training Split (2020-2021)
  ins_train <- ins_full %>% filter(year %in% 2020:2021)
  cnom_train <- cnom_full %>% filter(year %in% 2020:2021)
  
  # Holdout Split (2022-2024)
  ins_test <- ins_full %>% filter(year %in% 2022:2024)
  cnom_test <- cnom_full %>% filter(year %in% 2022:2024)
  
  # 2. Objective Function: Weighted Sum of Squared Errors on TRAINING Period Only (2020-2021)
  obj_fn <- function(theta) {
    p_temp <- base_params
    p_temp$beta_0 <- theta[1]
    p_temp$delta_beta_2021 <- theta[2]
    
    sim_res <- run_workforce_simulation(
      baseline_stock_36 = baseline_stock_36,
      params = p_temp,
      years = 2020:2021
    )
    
    sim_df <- sim_res$summary
    
    # Stock error on training window
    stock_err <- sum(((sim_df$total_active_stock - ins_train$obs_active_stock) / 1000)^2)
    # Flow error on training window
    flow_err <- sum(((sim_df$annual_emigrants - cnom_train$obs_realized_flow) / 100)^2)
    
    stock_err + flow_err
  }
  
  # Initial guess
  init_theta <- c(base_params$beta_0, base_params$delta_beta_2021)
  
  opt <- optim(
    par = init_theta,
    fn = obj_fn,
    method = "BFGS",
    control = list(maxit = 200, reltol = 1e-6)
  )
  
  calibrated_params <- base_params
  calibrated_params$beta_0 <- round(opt$par[1], 4)
  calibrated_params$delta_beta_2021 <- round(opt$par[2], 4)
  
  # 3. Simulate Full 2020-2024 Window with Calibrated Parameters
  final_sim <- run_workforce_simulation(
    baseline_stock_36 = baseline_stock_36,
    params = calibrated_params,
    years = 2020:2024
  )$summary
  
  sim_train <- final_sim %>% filter(year %in% 2020:2021)
  sim_test <- final_sim %>% filter(year %in% 2022:2024)
  
  # Training Fit Metrics (2020-2021)
  train_rmse_stock <- sqrt(mean((sim_train$total_active_stock - ins_train$obs_active_stock)^2))
  train_mape_stock <- mean(abs(sim_train$total_active_stock - ins_train$obs_active_stock) / ins_train$obs_active_stock) * 100
  train_rmse_flow <- sqrt(mean((sim_train$annual_emigrants - cnom_train$obs_realized_flow)^2))
  train_mape_flow <- mean(abs(sim_train$annual_emigrants - cnom_train$obs_realized_flow) / cnom_train$obs_realized_flow) * 100
  
  # Out-of-Sample Holdout Metrics (2022-2024)
  test_rmse_stock <- sqrt(mean((sim_test$total_active_stock - ins_test$obs_active_stock)^2))
  test_mape_stock <- mean(abs(sim_test$total_active_stock - ins_test$obs_active_stock) / ins_test$obs_active_stock) * 100
  test_rmse_flow <- sqrt(mean((sim_test$annual_emigrants - cnom_test$obs_realized_flow)^2))
  test_mape_flow <- mean(abs(sim_test$annual_emigrants - cnom_test$obs_realized_flow) / cnom_test$obs_realized_flow) * 100
  
  # Full 2020-2024 Metrics
  rmse_stock <- sqrt(mean((final_sim$total_active_stock - ins_full$obs_active_stock)^2))
  mape_stock <- mean(abs(final_sim$total_active_stock - ins_full$obs_active_stock) / ins_full$obs_active_stock) * 100
  rmse_flow <- sqrt(mean((final_sim$annual_emigrants - cnom_full$obs_realized_flow)^2))
  mape_flow <- mean(abs(final_sim$annual_emigrants - cnom_full$obs_realized_flow) / cnom_full$obs_realized_flow) * 100
  
  message(sprintf("[06_calibration] Optimization converged: beta_0 = %0.4f, delta_beta_2021 = %0.4f.",
                  calibrated_params$beta_0, calibrated_params$delta_beta_2021))
  message(sprintf("[06_calibration] Training Fit (2020-2021): Stock MAPE = %0.2f%% | Flow MAPE = %0.2f%%.",
                  train_mape_stock, train_mape_flow))
  message(sprintf("[06_calibration] Holdout Validation (2022-2024): Stock MAPE = %0.2f%% | Flow MAPE = %0.2f%%.",
                  test_mape_stock, test_mape_flow))
  
  list(
    calibrated_params = calibrated_params,
    fit_summary = final_sim,
    ins_obs = ins_full,
    cnom_obs = cnom_full,
    training_metrics = list(
      rmse_stock = train_rmse_stock,
      mape_stock = train_mape_stock,
      rmse_flow = train_rmse_flow,
      mape_flow = train_mape_flow
    ),
    holdout_metrics = list(
      rmse_stock = test_rmse_stock,
      mape_stock = test_mape_stock,
      rmse_flow = test_rmse_flow,
      mape_flow = test_mape_flow
    ),
    metrics = list(
      rmse_stock = rmse_stock,
      mape_stock = mape_stock,
      rmse_flow = rmse_flow,
      mape_flow = mape_flow
    )
  )
}
