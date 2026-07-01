# User Guide

pyqicharts is table-first. `qic_table(...)` calculates chart rows, limits, process metadata and signal fields. `qic(...)` plots those same rows and returns a `QicResult` with the calculated table attached.

## Quick Start

```python
from pyqicharts import qic, sample_healthcare_qi_data

df = sample_healthcare_qi_data()
chart = qic(df, x="month", y="wait_time", chart="i", improvement="low is good")

chart.figure
chart.table.head()
```

The returned object contains:

- `chart.table`: calculated rows for Excel, Power BI and validation.
- `chart.signal_table()`: stable signal-schema rows.
- `chart.summary()`: compact summary fields.
- `chart.save_png("chart.png")`: image export.

## Choosing a Chart

| Use case | Chart |
| --- | --- |
| Simple time series without control limits | `run` |
| Individual measurements over time | `i` |
| Moving ranges for an Individuals chart | `mr` |
| Counts with constant opportunity | `c` |
| Proportions with denominators | `p` |
| Rates with denominators | `u` |
| Subgroup means | `xbar` |
| Subgroup standard deviations | `s` |
| Cases between rare events | `g` |
| Time between events | `t` |
| Risk-adjusted proportions | `p_prime` |
| Risk-adjusted rates | `u_prime` |

## Process Context

Baseline and recalculation arguments are additive and keep the simple API intact.

```python
chart = qic(
    data=df,
    x="month",
    y="wait_time",
    chart="i",
    baseline_points=12,
    recalculation_points=[19],
    target=60,
    interventions=[{"point": 19, "label": "New pathway"}],
)
```

qicharts-style aliases are also accepted:

```python
qic_table(df, "month", "wait_time", chart="i", freeze=[12], breaks=[19])
```

`freeze_points` freezes the first segment around the supplied baseline endpoint. `breaks` and `recalculation_points` start new process segments.

## Signal Annotations

v1.3.4 renders signal labels on plotted charts by default. Labels are taken from `special_cause_label`, `special_cause_rule` or `signal_rule`, in that order, so the text on the chart matches the calculated table.

```python
chart = qic(df, "month", "wait_time", chart="i", annotate_signals=True)
```

Use `annotate_signals=False` for dense dashboards where labels would be too busy:

```python
chart = qic(df, "month", "wait_time", chart="i", annotate_signals=False)
```

Signal colours follow the interpreted signal type where available: improvement, concern or neutral.

## Working With Tables

```python
from pyqicharts import qic_table

rows = qic_table(df, "month", "wait_time", chart="i")
signals = rows[rows["signal"]]
```

The table includes centre, limits, `plot_value`, signal fields, segment fields, baseline fields, target/intervention fields and chart-specific diagnostic columns.

## Reporting

Install optional reporting dependencies when you need Excel or PowerPoint output:

```bash
pip install pyqicharts[reporting]
```

```python
from pyqicharts import export_excel, export_powerpoint

chart.save_png("wait_time.png")
export_excel(chart, "wait_time_report.xlsx")
export_powerpoint(chart, "wait_time_report.pptx")
```

See `docs/reporting.md` for workbook and deck layouts.

## Validation Position

The validation pack contains deterministic fixtures, expanded healthcare and industrial examples, and expected outputs generated from the package implementation. These are useful regression assets. They are not a substitute for live certification against published qicharts/qicharts2 or NHS workbook outputs.
