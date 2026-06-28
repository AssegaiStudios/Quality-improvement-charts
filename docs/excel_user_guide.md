# Excel Companion User Guide

## Example Workflow

1. Open `pyqicharts_excel_template.xlsx`.
2. Paste data into `Data`, keeping headers in row 1.
3. In `Config`, set `x_column`, `y_column` and `chart_type`.
4. For P and U charts, set `denominator_column`.
5. For P-prime and U-prime charts, set `expected_column`.
6. Choose optional outputs by setting `export_png`, `export_excel`, `export_powerpoint` or `export_bundle` to `TRUE`.
7. Run `Generate Chart`.
8. Review `Chart`, `ChartData`, `SPCSummary`, `Signals`, `NHSInterpretation`, `PowerBI`, `Exports` and `Log`.

## Config Examples

Run chart: `x_column = period`, `y_column = value`, `chart_type = run`, `method = anhoej`.

P chart: `x_column = period`, `y_column = value`, `chart_type = p`, `denominator_column = denominator`.

P-prime chart: `x_column = period`, `y_column = value`, `chart_type = p_prime`, `expected_column = expected`.

Pareto chart: `x_column = category`, `chart_type = pareto`, `denominator_column = count`.

## Screenshot Placeholders

Screenshots should be added before public documentation publication:

- `docs/images/excel_config.png`
- `docs/images/excel_chart.png`
- `docs/images/excel_outputs.png`

