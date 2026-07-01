# Reporting Guide

The core package can save PNG files with matplotlib. Excel and PowerPoint exports are optional so the base package remains lightweight.

## Install Reporting Support

```bash
pip install pyqicharts[reporting]
```

This installs `openpyxl` and `python-pptx`. If those packages are missing, pyqicharts raises a clear `ImportError` explaining which optional extra is needed.

## PNG Export

```python
chart = qic(df, "month", "value", chart="i")
chart.save_png("chart.png", dpi=150)
```

PNG exports include the plotted line, centre line, control limits, target/intervention markers and v1.3.4 signal annotations unless the chart was created with `annotate_signals=False`.

## Excel Workbook Layout

```python
from pyqicharts import export_excel

export_excel(chart, "report.xlsx")
```

The workbook contains:

- `Chart data`: the full `chart.table` output.
- `SPC summary`: compact chart-level fields.
- `Special causes`: row-level special-cause summary.
- `Signal table`: stable signal-schema rows.
- `KPI summary`: latest-value and signal-count fields.
- `NHS interpretation`: practical interpretation rows for reporting.
- `Phases`, `Interventions` and `Targets` where metadata is present.

For multiple charts, sheet names receive numeric suffixes to avoid collisions.

## PowerPoint Deck Layout

```python
from pyqicharts import export_powerpoint

export_powerpoint(chart, "report.pptx", title="Monthly SPC Report")
```

The deck contains a title slide and one slide per chart. Each chart slide includes the exported chart image and a short signal summary. This is intentionally simple so organisations can apply their own templates downstream.

## Report Bundles

```python
from pyqicharts import create_report_bundle

create_report_bundle([chart1, chart2], output_dir="report")
```

The bundle folder contains:

- PNG images, one per chart.
- An Excel workbook.
- A PowerPoint deck.
- `metadata.json` listing generated files and chart summaries.

## Power BI Tables

Use DataFrame helpers for Power BI Python visuals or dataflows:

```python
from pyqicharts import powerbi_table, spc_summary_table, signal_table

rows = powerbi_table(chart)
summary = spc_summary_table(chart)
signals = signal_table(chart)
```

The returned tables include schema/version metadata and are designed for joins, filtering and model refreshes.

## Practical Notes

Do not treat generated reports as the validation authority. The authoritative calculation surface is the DataFrame returned by `qic_table(...)` or attached as `chart.table`; exports are presentation surfaces built from that table.
