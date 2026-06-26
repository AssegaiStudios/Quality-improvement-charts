# Changelog

## 1.0.0 - 2026-06-09

### Added

- Stable public release metadata.
- Xbar chart support.
- S chart support.
- End-user sample datasets in `sample_data/`.
- Python sample dataset helpers:
  - `sample_healthcare_qi_data()`
  - `sample_subgroup_measurements()`
- Working Xbar and S chart examples.
- Expanded developer comments and docstrings across source modules.
- v1.0 release tests for sample data, Xbar/S charts and version alignment.

### Changed

- Bumped package version to 1.0.0.
- Marked package classifier as production/stable.
- Updated README and documentation for stable release expectations.

### Notes

- Public APIs should avoid breaking changes from this release onward. Deprecations should be documented before removal.

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
