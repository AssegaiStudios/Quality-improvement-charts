# pyqicharts Excel Companion

The Excel Companion lets non-Python users run pyqicharts from an Excel workbook through xlwings. The workbook remains a thin interface:

```text
Excel input -> Python config -> pyqicharts -> Excel output
```

It does not reimplement SPC calculations. Charting, signal detection, Power BI tables and reporting exports all call the public pyqicharts APIs.

## Workbook Sheets

The template contains `Data`, `Config`, `Chart`, `ChartData`, `SPCSummary`, `Signals`, `NHSInterpretation`, `PowerBI`, `Exports`, `Log` and `Help`.

`Data` is where users paste tabular data with headers. `Config` controls chart type, columns, rules, targets and export options. Generated outputs are written to the remaining output sheets.

## Callable xlwings Functions

Assign Excel buttons to:

```python
pyqicharts_excel.runner.generate_chart()
pyqicharts_excel.runner.generate_all_outputs()
pyqicharts_excel.runner.export_report_bundle()
pyqicharts_excel.runner.clear_outputs()
pyqicharts_excel.runner.validate_workbook()
```

`main()` calls `generate_chart()` by default.

## Supported Chart Types

The companion supports `run`, `i`, `mr`, `xmr`, `c`, `p`, `u`, `xbar`, `s`, `g`, `t`, `p_prime`, `u_prime` and `pareto`.

## Outputs

A successful run writes a chart image, calculated chart data, an SPC summary, unified signal rows, NHS interpretation, Power BI rows, export statuses and log messages.

