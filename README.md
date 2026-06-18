# pyqicharts

Quality Improvement (QI) and Statistical Process Control (SPC) charts for Python.

pyqicharts is a lightweight, Python-first toolkit for practical healthcare QI charting. It is inspired by qicharts2, NHS Making Data Count, Anhoej run chart rules, and Shewhart SPC methodology.

## Current Status

**Version:** 0.7.0

pyqicharts is currently in active development. The project already provides:

- Run charts
- Individuals / XmR charts
- Moving range charts
- C charts
- P charts
- U charts
- G charts for rare-event monitoring
- T charts for time-between-event monitoring
- Pareto charts
- Anhoej-style run chart diagnostics
- NHS-style XmR special cause detection
- Direction-of-improvement interpretation
- Baseline periods and recalculation segments
- Targets, interventions and step-change metadata
- PNG, Excel and PowerPoint export
- Report bundles
- Power BI-friendly tables
- Built-in chart themes

Future releases will focus on risk-adjusted SPC, validation, and production documentation.

## Installation

```bash
pip install pyqicharts
```

Reporting features use optional dependencies:

```bash
pip install pyqicharts[reporting]
```

For local development:

```bash
pip install -e .[dev]
pytest
```

## Quick Start

```python
import pandas as pd
from pyqicharts import qic

df = pd.DataFrame({
    "month": range(1, 13),
    "value": [12, 13, 14, 12, 11, 15, 16, 17, 15, 14, 18, 19],
})

chart = qic(data=df, x="month", y="value", chart="i")
chart.figure
```

## Rare-Event Charts

Version 0.7.0 adds G and T charts for healthcare rare-event workflows.

```python
from pyqicharts import infections_between_events, qic

df = infections_between_events()
chart = qic(
    data=df,
    x="case_number",
    y="cases_between_events",
    chart="g",
)
```

```python
from pyqicharts import days_between_serious_incidents, qic

df = days_between_serious_incidents()
chart = qic(
    data=df,
    x="event_number",
    y="days_between_events",
    chart="t",
)
```

Rare-event intervals must be non-negative. G and T chart tables include:

- `rare_event_mean`
- `rare_event_probability`
- `outside_lcl`
- `outside_ucl`
- `signal`
- `signal_rule`
- `special_cause`
- `special_cause_rule`

## Reporting

```python
from pyqicharts import create_report_bundle, export_excel, export_png, export_powerpoint

chart.save_png("chart.png")
export_png(chart, "chart.png")
export_excel(chart, "report.xlsx")
export_powerpoint(chart, "report.pptx")
create_report_bundle(charts=[chart], output_dir="report")
```

Excel and PowerPoint helpers require `pyqicharts[reporting]`.

## Power BI Tables

```python
from pyqicharts import powerbi_table, special_cause_summary_table, spc_summary_table

rows = powerbi_table(chart)
summary = spc_summary_table(chart)
signals = special_cause_summary_table(chart)
```

## Supported Charts

| Chart Type | Status |
|------------|--------|
| Run chart | Supported |
| Individuals / XmR chart | Supported |
| Moving range chart | Supported |
| C chart | Supported |
| P chart | Supported |
| U chart | Supported |
| G chart | Supported |
| T chart | Supported |
| Pareto chart | Supported |
| Xbar chart | Planned |
| S chart | Planned |
| Risk-adjusted P-prime chart | Planned |
| Risk-adjusted U-prime chart | Planned |

## Roadmap

### v0.8.0 - Risk-Adjusted SPC

- P-prime charts
- U-prime charts
- Observed versus expected calculations

### v0.9.0 - Documentation, Validation and Release Hardening

- Full documentation
- Examples
- Validation datasets
- CI and packaging hardening

### v1.0.0 - Stable Release

- Stable public API
- Comprehensive documentation
- Full test coverage
- Reference validation
- Production-ready release

## License

MIT License

Copyright (c) 2026 Assegai Studios Ltd.
