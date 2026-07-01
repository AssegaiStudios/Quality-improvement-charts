# Changelog

## 1.3.4 - 2026-06-11

### Added

- Plotted signal annotations with `qic(..., annotate_signals=True)`.
- Regression tests for rendered signal annotations and `annotate_signals=False`.
- Freeze-point isolation coverage without break/recalculation points.
- Segmented G/T validation fixtures with expected-output comparison tests.
- Narrative worked examples documentation.

### Changed

- Expanded statistical reference, user guide, reporting guide and formal statistical review.
- Updated parity and validation reports to distinguish internal deterministic fixtures from external published reference certification.

## 1.3.3 - 2026-06-10

### Added

- Practical coverage-hardening tests for Excel Companion validation, outputs, runner branches, helper modules and workbook logging.
- v1.3.3 release notes.

### Changed

- Raised the coverage gate from 90% to 95%.
- Updated validation evidence to 133 test functions, 149 passing tests and 96.80% coverage.

### Fixed

- `write_log(...)` now places headers in row 1 on an empty Log sheet before appending the first message.

## 1.3.2 - 2026-06-10

### Fixed

- Clear `signal_rule` and special-cause text metadata for excluded MR, C, P, U, Xbar and S rows.
- Updated stale validation and API stability documentation.

### Added

- Regression tests for excluded signal-rule clearance across MR, C, P, U, Xbar and S charts.
- `dist/` release artifacts declaration in `MANIFEST.in`.
- v1.3.2 release notes.

## 1.3.1 - 2026-06-10

### Fixed

- Mask excluded G, T, P-prime and U-prime rows out of `signal` and `special_cause` outputs.

### Added

- Regression tests for excluded rare-event and risk-adjusted signals.
- Deterministic expected-output files and comparison tests for expanded validation fixtures.
- Worked `nhs_interpretation_table(chart)` documentation.
- Built distribution artifacts included in the downloadable release bundle.

## 1.3.0 - 2026-06-10

### Added

- Added pyqicharts Excel Companion Phase 1 and Phase 2 using xlwings.
- Added workbook templates, Excel setup docs, user guide, troubleshooting guide and completion report.
- Added `[excel]` optional dependency group and `pyqicharts-excel-init` command.
- Added tests for Excel config parsing, workbook I/O, runner workflow, output tables and friendly error logging.

## 1.2.1 - 2026-06-09

### Added

- `STATISTICAL_REVIEW.md`.
- `API_STABILITY.md`.
- `docs/risk_adjusted_spc.md`.
- `docs/rare_event_spc.md`.
- Expanded validation fixture pack with normal, process-change and edge-case examples for every chart family.
- Dedicated three-segment audit tests for supported chart families.

### Changed

- Bumped version to 1.2.1.
- Made rare-event and risk-adjusted chart calculations segment-specific.

### Notes

- Release wording is now specification-complete qicharts2 parity implementation, without claiming live R byte-for-byte certification.

## 1.2.0 - 2026-06-09

### Added

- Plain `pytest` source-path configuration.
- Deterministic Anhøj run-chart implementation with exact crossing thresholds.
- `method="anhoej"`, `method="bestbox"` and `method="cutbox"` support.
- Segment-aware Nelson/Shewhart rule metadata using per-point centre and sigma values.
- Segment-specific recalculation for MR, C, P and U charts.
- Segment-aware Xbar and S chart calculations with subgroup-specific constants.
- Denominator-aware P-prime and U-prime methodologies.
- Power BI NHS interpretation, phase, intervention and target metadata tables.
- `CHART_ALIASES` and `VALID_CHARTS` public registry constants.
- `VALIDATION_REPORT.md` and consolidated release notes.

### Changed

- Bumped version to 1.2.0.
- Excel export now writes signal, KPI, NHS interpretation, phase, intervention and target sheets.
- Excluded observations are removed from supported chart calculations.

### Notes

- This release implements specification-based parity in Python. Live cross-package certification remains a separate artifact-driven validation task.

## 1.1.0 - 2026-06-09

### Added

- Nelson Rules 1-8 via `nelson_rule_signals(...)`.
- Shewhart-compatible rule helper via `shewhart_rule_signals(...)`.
- Shared signal schema via `Signal`, `signals_to_frame(...)` and `signal_table(...)`.
- Additive `rules="nelson"`, `rules="shewhart"` and `rules="all"` support in `qic(...)` and `qic_table(...)`.
- qicharts-style phase aliases: `freeze_points`, `break_points`, `exclude_points` and `phases`.
- Power BI `signal_table(...)` and `kpi_table(...)` helpers.
- Excel export sheets for signal schema and KPI summary.
- v1.1 tests for Nelson metadata, signal schema, rule configuration, phase aliases and Power BI KPI output.

### Changed

- Bumped package version to 1.1.0.
- Updated docs and parity report to reflect completed local validation and remaining external qicharts/qicharts2/NHS parity evidence.

### Notes

- v1.1.0 is a parity-readiness release. Full qicharts/qicharts2/NHS parity is not claimed until external reference-output comparisons are available and pass without unexplained differences.

## 1.0.0 interim rebuild - 2026-06-09

### Added

- Interim v1.0 release metadata; this is not a final parity-complete release.
- Xbar chart support.
- S chart support.
- End-user sample datasets in `sample_data/`.
- Chart-by-chart interim regression fixtures in `validation_data/`.
- `PARITY_REPORT.md` documenting completed evidence and remaining parity gaps.
- Python sample dataset helpers:
  - `sample_healthcare_qi_data()`
  - `sample_subgroup_measurements()`
- Working Xbar and S chart examples.
- Expanded developer comments and docstrings across source modules.
- v1.0 release tests for sample data, Xbar/S charts, validation fixtures and version alignment.

### Changed

- Bumped package version to 1.0.0.
- Marked package classifier as beta/interim rather than production/stable.
- Updated README and documentation to avoid claiming qicharts/qicharts2/NHS parity before external parity evidence exists.
- Expanded CI configuration to cover Linux, Windows and macOS across Python 3.10, 3.11 and 3.12.

### Notes

- Treat this as an interim v1.0 rebuild. It preserves the public API and strengthens validation scaffolding, but Anhøj parity, complete Nelson/Shewhart rule parity, cross-package qicharts/qicharts2 parity and NHS workbook parity are not marked complete.

## 0.9.0 - 2026-06-09

### Added

- Documentation scaffold for installation, quickstart, chart families, reporting, Power BI, API reference and validation.
- Validation datasets and expected outputs for representative chart calculations.
- Validation helper `read_validation_csv(...)`.
- Example scripts for the roadmap example set.
- GitHub Actions test workflow.
- Release hardening tests for examples, validation outputs and required files.

### Changed

- Bumped package version to 0.9.0.
- Updated README to describe v0.9 validation and release-hardening scope.

### Notes

- This is still a pre-1.0 release. v1.0 should expand validation datasets and finalize public API documentation and compatibility policy.

## 0.8.0 - 2026-06-09

### Added

- P-prime chart support with `chart="p_prime"`.
- U-prime chart support with `chart="u_prime"`.
- Observed/expected ratio calculations.
- Approximate risk-adjusted limits using expected volume.
- Safe handling for zero expected values.
- Clear validation for missing or negative expected values.
- Synthetic observed/expected example datasets.
- P-prime and U-prime examples.
- Focused tests for risk-adjusted calculations, zero expected values, rendering and validation.

### Changed

- Bumped package version to 0.8.0.
- Updated README to document risk-adjusted chart support and v0.9 roadmap focus.

### Notes

- This is an incremental pre-1.0 release. Full validation datasets, documentation and packaging hardening remain planned for v0.9.

## 0.7.0 - 2026-06-09

### Added

- G chart support for rare-event cases-between-events monitoring.
- T chart support for time-between-event monitoring.
- Rare-event centre line, control limits and signal detection.
- Non-negative interval validation with clear errors.
- Synthetic healthcare example datasets for infections between events, days between serious incidents and days between falls with harm.
- G and T chart examples.
- Focused tests for G/T calculations, rendering, invalid intervals and rare-event signals.

### Changed

- Bumped package version to 0.7.0.
- Updated README to document rare-event chart support and v0.8 roadmap focus.

### Notes

- This is an incremental pre-1.0 release. Risk-adjusted P-prime and U-prime charts remain planned for v0.8.

## 0.6.0 - 2026-06-09

### Added

- PNG export via `chart.save_png(...)` and `export_png(...)`.
- Excel export via `export_excel(...)`.
- PowerPoint export via `export_powerpoint(...)`.
- Report bundles via `create_report_bundle(...)`.
- Power BI-friendly tables via `powerbi_table(...)`, `spc_summary_table(...)` and `special_cause_summary_table(...)`.
- Optional `reporting` dependencies for `openpyxl` and `python-pptx`.
- Graceful optional dependency errors when reporting extras are missing.
- Focused tests for PNG, Excel, PowerPoint, bundles, Power BI tables and optional dependency handling.

### Changed

- Bumped package version to 0.6.0.
- Updated README to document reporting and Power BI helpers.

### Notes

- This is an incremental pre-1.0 release. Specialist rare-event charts, risk-adjusted charts and full validation datasets remain planned for later releases.

## 0.5.0 - 2026-06-09

### Added

- Baseline period support with `baseline_points`.
- Recalculation segment support with `recalculation_points`.
- Target table fields and target plotting.
- Intervention metadata and vertical intervention markers.
- Step-change metadata and vertical step-change markers.
- Segment IDs and segment labels in returned tables.
- Plotting support for segmented Individuals / XmR centre lines and limits.
- Focused tests for v0.5 process features.

### Changed

- Bumped package version to 0.5.0.
- Updated README to document baselines, recalculation, targets, interventions and step changes.

### Notes

- This is an incremental pre-1.0 release. Reporting exports, rare-event charts, risk-adjusted charts and full validation datasets remain planned for later releases.

## 0.4.0 - 2026-06-09

### Added

- NHS-style Individuals / XmR special cause detection.
- Above-UCL and below-LCL signal fields.
- Shift detection for eight non-centre points above or below the centre line.
- Trend detection for six increasing or decreasing points.
- Direction-of-improvement interpretation with `improvement="high is good"` and `improvement="low is good"`.
- Special cause table fields for rule, direction, type, colour, and label.
- NHS-style plot colouring for interpreted special causes.
- Focused tests for v0.4 special cause behaviour.

### Changed

- Bumped package version to 0.4.0.
- Updated README to document v0.4 NHS XmR behaviour and the next roadmap stage.

### Notes

- This is an incremental pre-1.0 release. Reporting exports, baselines, targets, interventions, and recalculation periods remain planned for later releases.

## 0.3.0

- Baseline release with run, I, MR, C, P, U, and Pareto charts.
