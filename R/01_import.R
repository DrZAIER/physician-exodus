# R/01_import.R
# ==============================================================================
# Pipeline Step 1: Raw Data Ingestion and Metadata Validation
# Project: Physician Exodus from Tunisia
# ==============================================================================

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

import_raw_data <- function(data_dir = "data") {
  message("[01_import] Ingesting empirical raw datasets and metadata registries...")
  
  raw_dir <- file.path(data_dir, "raw")
  meta_dir <- file.path(data_dir, "metadata")
  
  # Check paths
  stopifnot(dir.exists(raw_dir))
  stopifnot(dir.exists(meta_dir))
  
  # 1. Ingest Raw Datasets
  ins_physicians <- readr::read_csv(
    file.path(raw_dir, "ins_physician_series_2017_2024.csv"),
    show_col_types = FALSE
  )
  
  ins_population <- readr::read_csv(
    file.path(raw_dir, "ins_population_governorate_2023.csv"),
    show_col_types = FALSE
  )
  
  carte_sanitaire <- readr::read_csv(
    file.path(raw_dir, "carte_sanitaire_regional_physicians_2023.csv"),
    show_col_types = FALSE
  )
  
  cnom_emigration <- readr::read_csv(
    file.path(raw_dir, "cnom_emigration_series_2015_2024.csv"),
    show_col_types = FALSE
  )
  
  training_capacity <- readr::read_csv(
    file.path(raw_dir, "medical_training_capacity_2018_2025.csv"),
    show_col_types = FALSE
  )
  
  dest_registries <- readr::read_csv(
    file.path(raw_dir, "destination_registries_france_germany.csv"),
    show_col_types = FALSE
  )
  
  # 2. Ingest Metadata Registries
  source_reg <- readr::read_csv(
    file.path(meta_dir, "source_registry.csv"),
    show_col_types = FALSE
  )
  
  param_reg <- readr::read_csv(
    file.path(meta_dir, "parameter_registry.csv"),
    show_col_types = FALSE
  )
  
  data_dict <- readr::read_csv(
    file.path(meta_dir, "data_dictionary.csv"),
    show_col_types = FALSE
  )
  
  # Basic Validation Checks
  stopifnot(nrow(ins_physicians) >= 7)
  stopifnot(nrow(ins_population) == 24)
  stopifnot(nrow(carte_sanitaire) == 24)
  stopifnot(nrow(cnom_emigration) >= 10)
  stopifnot(nrow(param_reg) >= 25)
  
  message(sprintf("[01_import] Successfully ingested %d raw tables and %d metadata records.", 5, nrow(param_reg)))
  
  list(
    ins_physicians = ins_physicians,
    ins_population = ins_population,
    carte_sanitaire = carte_sanitaire,
    cnom_emigration = cnom_emigration,
    training_capacity = training_capacity,
    destination_registries = dest_registries,
    source_reg = source_reg,
    param_reg = param_reg,
    data_dict = data_dict
  )
}
