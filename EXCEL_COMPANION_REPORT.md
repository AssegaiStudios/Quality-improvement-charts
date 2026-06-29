# pyqicharts Excel Companion Phase 1 and Phase 2 Report

Reviewer-fix status: v1.3.2 adds consistent excluded-row signal-text cleanup, expanded regression coverage, deterministic expanded-fixture expected outputs, `nhs_interpretation_table(chart)` documentation and built distribution artifacts in the downloadable bundle.

## Implemented Features

- Added `pyqicharts_excel` package with config parsing, workbook I/O, validation, output table generation, xlwings runner functions, ribbon guidance and examples.
- Added workbook templates under `excel/` with the required sheets and sample data/config.
- Added callable functions: `main`, `generate_chart`, `generate_all_outputs`, `export_report_bundle`, `clear_outputs`, `validate_workbook` and `refresh_config_defaults`.
- Added optional `[excel]` dependency group and `pyqicharts-excel-init` command.
- Added docs for setup, user workflow, troubleshooting and companion architecture.
- Added tests for config parsing, workbook I/O, runner execution, output tables, logging and errors.

## Workbook Structure

The template contains `Data`, `Config`, `Chart`, `ChartData`, `SPCSummary`, `Signals`, `NHSInterpretation`, `PowerBI`, `Exports`, `Log` and `Help`.

## Tested Chart Types

Automated tests exercise the workbook run-chart path. Existing pyqicharts tests continue to cover run, I, MR, C, P, U, Xbar, S, G, T, P-prime, U-prime and Pareto calculations/rendering. Manual Excel smoke tests should verify the button workflow for each high-value chart type before public rollout.

## Manual Smoke Test Checklist

- Open `pyqicharts_excel_template.xlsx`.
- Confirm all required sheets are present.
- Run `Validate Workbook`.
- Run `Generate Chart` with the default run chart config.
- Confirm chart image appears on `Chart`.
- Confirm `ChartData`, `SPCSummary`, `Signals`, `NHSInterpretation`, `PowerBI`, `Exports` and `Log` are written.
- Switch to I chart, P chart, U chart, Xbar chart, P-prime chart and Pareto chart configs and repeat.
- Enable `export_png`, `export_excel`, `export_powerpoint` and `export_bundle` and confirm files are created.
- Break a config value intentionally and confirm a friendly error appears in `Log`.

## Known Limitations

- The companion requires xlwings for interactive Excel button execution.
- The `.xlsm` workbook is an xlwings-ready shell; signed VBA controls and managed ribbon deployment must be added through normal Excel governance.
- Office.js is intentionally out of scope for this phase.

## Future Phase 3 Recommendation

Build a governed Office.js add-in or signed enterprise ribbon package once the xlwings workflow has been piloted with real improvement teams.
