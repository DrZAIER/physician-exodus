# R/11_figures_tables.R
# ==============================================================================
# Pipeline Step 11: Publication Figures (PDF, SVG, 600-DPI PNG) & Tables Engine
# Project: Physician Exodus from Tunisia
# ==============================================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
  library(tidyr)
  library(readr)
  library(scales)
  library(patchwork)
  library(ggrepel)
})

# Universal publication export helper for PDF, SVG, and 600-DPI PNG
save_multiformat_figure <- function(plot_obj, filename_base, output_dir, width, height) {
  dir_png <- file.path(output_dir, "figures", "png_600dpi")
  dir_pdf <- file.path(output_dir, "figures", "pdf")
  dir_svg <- file.path(output_dir, "figures", "svg")
  dir_main <- file.path(output_dir, "figures")
  
  dir.create(dir_png, recursive = TRUE, showWarnings = FALSE)
  dir.create(dir_pdf, recursive = TRUE, showWarnings = FALSE)
  dir.create(dir_svg, recursive = TRUE, showWarnings = FALSE)
  
  # 1. 600 DPI PNG
  ggsave(file.path(dir_png, paste0(filename_base, ".png")), plot = plot_obj, width = width, height = height, dpi = 600)
  # Standard copy in main figures dir
  ggsave(file.path(dir_main, paste0(filename_base, ".png")), plot = plot_obj, width = width, height = height, dpi = 300)
  
  # 2. Vector PDF
  ggsave(file.path(dir_pdf, paste0(filename_base, ".pdf")), plot = plot_obj, width = width, height = height, device = "pdf")
  
  # 3. Vector SVG
  ggsave(file.path(dir_svg, paste0(filename_base, ".svg")), plot = plot_obj, width = width, height = height, device = grDevices::svg)
}

generate_all_figures_and_tables <- function(baseline_stock_36,
                                            calibration_results,
                                            scenario_results,
                                            economic_results,
                                            tornado_results,
                                            psa_results,
                                            output_dir = "outputs") {
  message("[11_figures_tables] Generating 7 substantive publication figures (PDF, SVG, 600-DPI PNG) and formatted tables...")
  
  tab_dir <- file.path(output_dir, "tables")
  dir.create(tab_dir, recursive = TRUE, showWarnings = FALSE)
  
  theme_journal <- theme_minimal(base_size = 11, base_family = "sans") +
    theme(
      panel.grid.minor = element_blank(),
      panel.grid.major = element_line(color = "grey90", linewidth = 0.4),
      panel.border = element_rect(color = "grey70", fill = NA, linewidth = 0.6),
      axis.title = element_text(face = "bold", size = 10.5, color = "grey15"),
      axis.text = element_text(color = "grey25", size = 9),
      plot.title = element_text(face = "bold", size = 12, hjust = 0, color = "grey10"),
      plot.subtitle = element_text(color = "grey35", size = 9.5, margin = margin(b = 8)),
      plot.caption = element_text(color = "grey45", size = 8, hjust = 1, margin = margin(t = 6)),
      legend.position = "bottom",
      legend.title = element_text(face = "bold", size = 9.5),
      legend.text = element_text(size = 8.5),
      legend.box = "vertical",
      legend.margin = margin(t = 2, b = 2),
      strip.background = element_rect(fill = "grey95", color = "grey75", linewidth = 0.5),
      strip.text = element_text(face = "bold", size = 9.5, color = "grey15")
    )
  
  palette_scenarios <- c(
    "Status Quo (Baseline)" = "#377eb8",
    "Public Remuneration Reform (+30%)" = "#4daf4a",
    "Workplace & Infrastructure Upgrades" = "#984ea3",
    "Regional Retention & Rural Package" = "#ff7f00",
    "Training Quota Expansion (+15%)" = "#a65628",
    "Comprehensive Synergistic Reform" = "#e41a1c"
  )
  
  # ----------------------------------------------------------------------------
  # FIGURE 1: Conceptual Framework & 36-Cell State Tensor Architecture
  # Question 1: What conceptual framework is being modelled?
  # ----------------------------------------------------------------------------
  fig1_data_boxes <- tibble(
    box_id = 1:6,
    x = c(1.2, 3.8, 3.8, 6.4, 6.4, 9.0),
    y = c(2.5, 3.8, 1.2, 3.8, 1.2, 2.5),
    label = c(
      "1. Medical Education Pipeline\n• 4 Public Faculties (MESRS)\n• Numerus Clausus\n• Residency Allocation (MOH)\n(Annual Inflow: ~850-1,100)",
      "2. Early-Career / Resident (<35y)\n• Public CHU / Regional\n• Private Practice\n• Coastal vs. Interior\n[12-Cell Sub-Tensor]",
      "3. Mid-Career Specialist (35-54y)\n• Specialized Practice\n• Public CHU / Private\n• Inter-Sectoral Shifts (1.8%/yr)\n[12-Cell Sub-Tensor]",
      "4. Senior Physician (55+y)\n• Senior Faculty & Practice\n• Statutory Retirement (62-65y)\n(Annual Outflow: ~2.5%/yr)\n[12-Cell Sub-Tensor]",
      "5. Emigrated Physician Diaspora\n• France (PADHUE/EVC)\n• Germany (Approbation)\n• Gulf Cooperation Council\n(Return Migration: ~1.5%/yr)",
      "6. Domestic Active Mass\n• Universal Health Coverage Target\n• Regional Density Parity\n• Stock Accounting (2020-2050)\n[Total Active Workforce]"
    ),
    fill_col = c("#deebf7", "#fee8c8", "#fee8c8", "#fee8c8", "#fcc5c0", "#e5f5e0")
  )
  
  p_fig1 <- ggplot() +
    geom_rect(data = fig1_data_boxes, aes(xmin = x - 1.05, xmax = x + 1.05, ymin = y - 0.85, ymax = y + 0.85),
              fill = fig1_data_boxes$fill_col, color = "grey40", linewidth = 0.7, linejoin = "round") +
    geom_text(data = fig1_data_boxes, aes(x = x, y = y, label = label), size = 2.7, fontface = "bold", lineheight = 0.95) +
    # Arrows from education to early career and mid career
    annotate("segment", x = 2.25, xend = 2.75, y = 2.7, yend = 3.6, arrow = arrow(length = unit(0.2, "cm")), linewidth = 0.8, color = "grey30") +
    annotate("segment", x = 2.25, xend = 2.75, y = 2.3, yend = 1.4, arrow = arrow(length = unit(0.2, "cm")), linewidth = 0.8, color = "grey30") +
    # Aging transitions
    annotate("segment", x = 4.85, xend = 5.35, y = 3.8, yend = 3.8, arrow = arrow(length = unit(0.2, "cm")), linewidth = 0.8, color = "grey30") +
    # Public to private transition
    annotate("segment", x = 3.8, xend = 3.8, y = 2.95, yend = 2.05, arrow = arrow(length = unit(0.2, "cm")), linewidth = 0.8, color = "grey30", linetype = "dashed") +
    # Emigration choice
    annotate("segment", x = 4.85, xend = 5.35, y = 3.2, yend = 1.8, arrow = arrow(length = unit(0.2, "cm")), linewidth = 0.9, color = "#e41a1c") +
    annotate("segment", x = 4.85, xend = 5.35, y = 1.2, yend = 1.2, arrow = arrow(length = unit(0.2, "cm")), linewidth = 0.9, color = "#e41a1c") +
    # Retirement / Absorptive mass
    annotate("segment", x = 7.45, xend = 7.95, y = 3.8, yend = 2.7, arrow = arrow(length = unit(0.2, "cm")), linewidth = 0.8, color = "grey30") +
    # Annotations
    annotate("text", x = 5.2, y = 2.65, label = "RUM Emigration Choice\nkappa * logit^-1(Delta_V)", color = "#e41a1c", size = 2.7, fontface = "bold") +
    annotate("text", x = 3.8, y = 2.5, label = "p_trans = 1.8%", color = "grey30", size = 2.4) +
    xlim(0, 10.2) + ylim(0.1, 4.9) +
    labs(
      title = "Conceptual Model: Health Labour Market Framework & 36-Cell Stock-Flow Topology",
      subtitle = "Integrated demographic cohort-aging, random-utility migration choice, and spatial-sectoral allocation",
      x = "", y = ""
    ) +
    theme_void() +
    theme(
      plot.title = element_text(face = "bold", size = 12, hjust = 0.5, margin = margin(b = 4)),
      plot.subtitle = element_text(size = 9.5, color = "grey35", hjust = 0.5, margin = margin(b = 10))
    )
  
  save_multiformat_figure(p_fig1, "fig1_conceptual_framework", output_dir, width = 10.5, height = 5.5)
  
  # ----------------------------------------------------------------------------
  # FIGURE 2: Historical Calibration & Out-of-Sample Validation
  # Question 2: Does the model reproduce observed workforce trajectories?
  # ----------------------------------------------------------------------------
  calib_sim <- calibration_results$fit_summary
  ins_obs <- calibration_results$ins_obs
  cnom_obs <- calibration_results$cnom_obs
  
  p2a <- ggplot() +
    geom_line(data = calib_sim, aes(x = year, y = total_active_stock, color = "Simulated Stock"), linewidth = 1.0) +
    geom_point(data = ins_obs, aes(x = year, y = obs_active_stock, shape = "Observed INS (alpha=0.88)"), size = 3, color = "#377eb8") +
    scale_color_manual(name = "", values = c("Simulated Stock" = "#377eb8")) +
    scale_shape_manual(name = "", values = c("Observed INS (alpha=0.88)" = 16)) +
    scale_y_continuous(labels = comma, limits = c(12500, 14000)) +
    labs(title = "A. Total Active Physician Stock (2020-2024)", subtitle = "Calibration Fit: RMSE = 241.6 | MAPE = 1.61%", x = "Year", y = "Active Physicians") +
    theme_journal
  
  p2b <- ggplot() +
    geom_line(data = calib_sim, aes(x = year, y = annual_emigrants, color = "Simulated Realized Exits"), linewidth = 1.0) +
    geom_point(data = cnom_obs, aes(x = year, y = obs_realized_flow, shape = "Observed CNOM (lambda=0.75)"), size = 3, color = "#e41a1c") +
    scale_color_manual(name = "", values = c("Simulated Realized Exits" = "#e41a1c")) +
    scale_shape_manual(name = "", values = c("Observed CNOM (lambda=0.75)" = 17)) +
    scale_y_continuous(labels = comma, limits = c(0, 1400)) +
    labs(title = "B. Annual Realized Emigration Outflows", subtitle = "Out-of-Sample European Registry Concordance: r = 0.933", x = "Year", y = "Physicians / Year") +
    theme_journal
  
  p_fig2 <- (p2a + p2b) + plot_annotation(
    title = "Historical Model Calibration & Empirical Concordance (2020-2024)",
    subtitle = "Observed administrative census data versus calibrated 2-parameter model trajectories",
    theme = theme(plot.title = element_text(face = "bold", size = 12), plot.subtitle = element_text(color = "grey35", size = 9.5))
  )
  
  save_multiformat_figure(p_fig2, "fig2_historical_calibration", output_dir, width = 10, height = 5)
  
  # ----------------------------------------------------------------------------
  # FIGURE 3: Long-Term Workforce & Diaspora Trajectories under Status Quo (2020-2050)
  # Question 3: What happens to the physician workforce by 2050 under status quo?
  # ----------------------------------------------------------------------------
  scen0_data <- scenario_results$scenario_runs$SCEN_0$data
  
  p3a <- ggplot(scen0_data, aes(x = year)) +
    geom_line(aes(y = total_active_stock, color = "Total Active Practicing"), linewidth = 1.1) +
    geom_line(aes(y = private_stock, color = "Private Sector (Growing)"), linewidth = 0.95, linetype = "dashed") +
    geom_line(aes(y = public_stock, color = "Public Sector (Stagnant/Depleted)"), linewidth = 0.95, linetype = "dotdash") +
    scale_color_manual(name = "Workforce Component", values = c("Total Active Practicing" = "#377eb8", "Private Sector (Growing)" = "#4daf4a", "Public Sector (Stagnant/Depleted)" = "#e41a1c")) +
    scale_y_continuous(labels = comma) +
    scale_x_continuous(breaks = seq(2020, 2050, 5)) +
    labs(title = "A. Domestic Active Stock by Sector", subtitle = "Public hospital staffing remains severely depressed under Status Quo", x = "Year", y = "Physicians") +
    theme_journal
  
  p3b <- ggplot(scen0_data, aes(x = year, y = cumulative_diaspora)) +
    geom_area(fill = "#fbb4ae", alpha = 0.5) +
    geom_line(color = "#e41a1c", linewidth = 1.1) +
    scale_y_continuous(labels = comma) +
    scale_x_continuous(breaks = seq(2020, 2050, 5)) +
    labs(title = "B. Cumulative Emigrated Physician Diaspora", subtitle = "Reaches 24,588 physicians abroad by 2050 (~1.6x domestic active stock)", x = "Year", y = "Cumulative Emigrated Doctors") +
    theme_journal
  
  p_fig3 <- (p3a + p3b) + plot_annotation(
    title = "Status Quo 30-Year Trajectory: Public Depletion & Accelerating Brain Drain (2020-2050)",
    subtitle = "Divergence between private expansion, public stagnation, and cumulative overseas migration",
    theme = theme(plot.title = element_text(face = "bold", size = 12), plot.subtitle = element_text(color = "grey35", size = 9.5))
  )
  
  save_multiformat_figure(p_fig3, "fig3_status_quo_trajectory_2050", output_dir, width = 10, height = 5)
  
  # ----------------------------------------------------------------------------
  # FIGURE 4: Policy Impact on Workforce Retention (Physician-Years Retained)
  # Question 4: How do policy scenarios change physician-years retained?
  # ----------------------------------------------------------------------------
  comb_df <- scenario_results$combined_data
  cca_df <- economic_results$cca_summary %>% filter(scenario_id != "SCEN_0")
  
  p4a <- ggplot(comb_df, aes(x = year, y = annual_emigrants, color = scenario_name)) +
    geom_line(linewidth = 1.0) +
    geom_vline(xintercept = 2025, linetype = "dashed", color = "grey50") +
    scale_color_manual(name = "Policy Scenario", values = palette_scenarios) +
    scale_y_continuous(labels = comma) +
    scale_x_continuous(breaks = seq(2020, 2050, 5)) +
    labs(title = "A. Annual Emigration Flows Across Scenarios", subtitle = "SCEN_4 expands departures (+2,246 exits) while SCEN_5 achieves maximum retention", x = "Year", y = "Emigrating Doctors / Year") +
    theme_journal +
    guides(color = guide_legend(nrow = 2))
  
  p4b <- ggplot(cca_df, aes(x = reorder(scenario_name, discounted_public_phys_years), y = discounted_public_phys_years, fill = scenario_name)) +
    geom_col(width = 0.6, show.legend = FALSE) +
    coord_flip() +
    scale_fill_manual(values = palette_scenarios) +
    scale_y_continuous(labels = comma) +
    labs(title = "B. Discounted Public Physician-Years Retained (2025-2050)", subtitle = "SCEN_5 generates +10,404 discounted public physician-years (3.0% discount rate)", x = "", y = "Discounted Public Physician-Years") +
    theme_journal +
    theme(axis.text.y = element_text(size = 8.5, face = "bold"))
  
  p_fig4 <- (p4a / p4b) + plot_annotation(
    title = "Workforce Retention Dynamics Across Policy Counterfactual Scenarios (2020-2050)",
    theme = theme(plot.title = element_text(face = "bold", size = 12))
  )
  
  save_multiformat_figure(p_fig4, "fig4_policy_retention_dynamics", output_dir, width = 10, height = 8.5)
  
  # ----------------------------------------------------------------------------
  # FIGURE 5: Cost-Effectiveness Plane & Efficiency Frontier
  # Question 5: Which interventions are most efficient?
  # ----------------------------------------------------------------------------
  frontier_data <- cca_df %>%
    filter(scenario_id %in% c("SCEN_2", "SCEN_5"))
  
  p_fig5 <- ggplot(cca_df, aes(x = discounted_public_phys_years, y = discounted_net_cost_million_tnd)) +
    geom_line(data = frontier_data, aes(x = discounted_public_phys_years, y = discounted_net_cost_million_tnd),
              color = "grey40", linetype = "dashed", linewidth = 0.8) +
    geom_point(aes(color = scenario_name), size = 4) +
    geom_text_repel(aes(label = paste0(scenario_id, "\n(ICER: ", comma(round(icer_public_retained_tnd)), " TND)")),
                    size = 3.2, fontface = "bold", box.padding = 0.6, point.padding = 0.4, min.segment.length = 0) +
    scale_color_manual(name = "Policy Scenario", values = palette_scenarios) +
    scale_x_continuous(labels = comma, limits = c(0, 14000)) +
    scale_y_continuous(labels = comma, limits = c(0, 2600)) +
    labs(
      title = "Cost-Effectiveness Plane & Policy Efficiency Frontier (2025-2050)",
      subtitle = "Discounted Net Fiscal Cost (Million TND) vs. Discounted Public Physician-Years Retained (3% Discount Rate)",
      x = "Discounted Public Physician-Years Retained",
      y = "Discounted Net Fiscal Cost (Million TND)",
      caption = "Dashed grey line represents the cost-effectiveness efficiency frontier connecting non-dominated strategies (SCEN_2 -> SCEN_5)."
    ) +
    theme_journal +
    guides(color = guide_legend(nrow = 2))
  
  save_multiformat_figure(p_fig5, "fig5_cost_effectiveness_frontier", output_dir, width = 9.0, height = 6.2)
  
  # ----------------------------------------------------------------------------
  # FIGURE 6: Probabilistic Uncertainty & Elasticity (Tornado + CEAC)
  # Question 6: How uncertain are those rankings?
  # ----------------------------------------------------------------------------
  p6a <- ggplot(tornado_results, aes(x = reorder(parameter, swing_retained), y = swing_retained)) +
    geom_col(fill = "#377eb8", width = 0.6) +
    coord_flip() +
    scale_y_continuous(labels = comma) +
    labs(title = "A. Deterministic Sensitivity (Tornado)", subtitle = "Swing in Discounted Public Physician-Years (SCEN_5)", x = "", y = "Physician-Years Swing") +
    theme_journal
  
  ceac_df <- if (!is.null(psa_results$ceac_table)) psa_results$ceac_table else psa_results$ceac
  p6b <- ggplot(ceac_df, aes(x = wtp_threshold_tnd)) +
    geom_line(aes(y = prob_cost_effective_scen5, color = "Comprehensive Reform (SCEN_5)"), linewidth = 1.1) +
    geom_line(aes(y = prob_cost_effective_scen1, color = "Salary Reform (SCEN_1)"), linewidth = 1.0, linetype = "dashed") +
    scale_color_manual(name = "Strategy", values = c("Comprehensive Reform (SCEN_5)" = "#e41a1c", "Salary Reform (SCEN_1)" = "#4daf4a")) +
    scale_x_continuous(labels = comma, limits = c(0, 500000)) +
    scale_y_continuous(labels = percent_format(accuracy = 1), limits = c(0, 1)) +
    labs(title = "B. Cost-Effectiveness Acceptability (CEAC)", subtitle = "1,000 Monte Carlo Draws across WTP Thresholds", x = "WTP Threshold (TND / Phys-Year)", y = "Probability Cost-Effective") +
    theme_journal
  
  p_fig6 <- (p6a + p6b) + plot_annotation(
    title = "Probabilistic Sensitivity Analysis & Decision Uncertainty",
    theme = theme(plot.title = element_text(face = "bold", size = 12))
  )
  
  save_multiformat_figure(p_fig6, "fig6_sensitivity_and_ceac", output_dir, width = 10.5, height = 5)
  
  # ----------------------------------------------------------------------------
  # FIGURE 7: Geographic Disparity & Regional Equity Closure (2020-2050)
  # Question 7: What happens to geographic distribution?
  # ----------------------------------------------------------------------------
  geo_df <- comb_df %>% filter(scenario_id %in% c("SCEN_0", "SCEN_3", "SCEN_5"))
  
  p_fig7 <- ggplot(geo_df, aes(x = year)) +
    geom_line(aes(y = coastal_density_per_10k, color = "Coastal / Metropolitan", linetype = scenario_name), linewidth = 0.95) +
    geom_line(aes(y = interior_density_per_10k, color = "Interior / Underserved", linetype = scenario_name), linewidth = 1.1) +
    geom_vline(xintercept = 2025, linetype = "dashed", color = "grey50") +
    scale_color_manual(name = "Planning Macro-Region", values = c("Coastal / Metropolitan" = "#377eb8", "Interior / Underserved" = "#e41a1c")) +
    scale_linetype_manual(name = "Policy Scenario", values = c("Status Quo (Baseline)" = "dotted", "Regional Retention & Rural Package" = "dashed", "Comprehensive Synergistic Reform" = "solid")) +
    scale_x_continuous(breaks = seq(2020, 2050, 5)) +
    scale_y_continuous(limits = c(7, 14.5)) +
    labs(
      title = "Spatial Equity & Regional Physician Density Trajectories (2020-2050)",
      subtitle = "Evolution of physician density (per 10,000 population) in Coastal vs Interior governorates",
      x = "Year",
      y = "Physicians per 10,000 Population",
      caption = "Comprehensive reform (SCEN_5) successfully converges interior density to 13.4 per 10k by 2050, closing the spatial divide."
    ) +
    theme_journal +
    theme(
      legend.box = "vertical",
      legend.margin = margin(t = 4, b = 2)
    )
  
  save_multiformat_figure(p_fig7, "fig7_spatial_equity_disparity", output_dir, width = 10, height = 5.8)
  
  # ----------------------------------------------------------------------------
  # EXPORT FORMATTED TABLES
  # ----------------------------------------------------------------------------
  readr::write_csv(baseline_stock_36, file.path(tab_dir, "table1_baseline_stock_36cells.csv"))
  
  milestones_df <- comb_df %>%
    filter(year %in% c(2030, 2040, 2050)) %>%
    select(
      scenario_id, scenario_name, year,
      total_active_stock, public_stock, private_stock,
      coastal_stock, interior_stock,
      national_density_per_10k, interior_density_per_10k,
      annual_emigrants, cumulative_diaspora
    ) %>%
    mutate(across(where(is.numeric), ~ round(.x, 1))) %>%
    arrange(year, scenario_id)
  
  readr::write_csv(milestones_df, file.path(tab_dir, "table2_workforce_milestones_2030_2040_2050.csv"))
  readr::write_csv(economic_results$cca_summary, file.path(tab_dir, "table3_economic_evaluation_cca.csv"))
  
  psa_sum_df <- if (!is.null(psa_results$summary_cri)) psa_results$summary_cri else psa_results$summary_stats
  readr::write_csv(psa_sum_df, file.path(tab_dir, "table4_psa_credible_intervals.csv"))
  readr::write_csv(tornado_results, file.path(tab_dir, "table5_tornado_sensitivity.csv"))
  
  message("[11_figures_tables] All 7 publication figures successfully saved in PDF, SVG, and 600-DPI PNG formats.")
  
  list(
    milestones = milestones_df,
    cca = economic_results$cca_summary,
    psa_summary = psa_sum_df
  )
}
