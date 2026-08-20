# tests/test_runner.R
# ==============================================================================
# Standalone Test Runner Script
# ==============================================================================

suppressPackageStartupMessages({
  library(testthat)
})

cat("\n==============================================================================\n")
cat("                       RUNNING AUTOMATED TEST SUITE                           \n")
cat("==============================================================================\n\n")

test_dir_path <- "tests/testthat"
if (!dir.exists(test_dir_path)) {
  test_dir_path <- "testthat"
}

res <- testthat::test_dir(test_dir_path, stop_on_failure = TRUE)

cat("\n==============================================================================\n")
cat("                    ALL AUTOMATED TESTS PASSED SUCCESSFULLY                   \n")
cat("==============================================================================\n\n")
