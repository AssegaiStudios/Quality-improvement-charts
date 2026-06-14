# pyqicharts

Quality Improvement (QI) and Statistical Process Control (SPC) charts for Python.

pyqicharts is a lightweight, Python-first toolkit for practical healthcare QI charting. It is inspired by qicharts2, NHS Making Data Count, Anhoej run chart rules, and Shewhart SPC methodology.

## Current Status

**Version:** 0.6.0

pyqicharts is currently in active development. The project already provides:

- Run charts
- Individuals / XmR charts
- Moving range charts
- C charts
- P charts
- U charts
- Pareto charts
- Anhoej-style run chart diagnostics
- NHS-style XmR special cause detection
- Direction-of-improvement interpretation
- Baseline periods and recalculation segments
- Targets, interventions and step-change metadata
- PNG export
- Excel export with optional reporting dependencies
- PowerPoint export with optional reporting dependencies
- Report bundles
- Power BI-friendly tables
- Built-in chart themes

Future releases will focus on specialist healthcare SPC charts, risk-adjusted charts, validation, and production documentation.

## Installation

```bash
pip install pyqicharts
```

For local development:

```bash
pip install -e .[dev]
pytest
```

Reporting features use optional dependencies:

```bash
pip install pyqicharts[reporting]
```

## Quick Start

```python
import pandas as pd
from pyqicharts import qic

df = pd.DataFrame({
    "month": range(1, 13),
    "value": [12, 13, 14, 12, 11, 15, 16, 17, 15, 14, 18, 19],
})

chart = qic(
    data=df,
    x="month",
    y="value",
    chart="i",
    improvement="high is good",
)

chart.figure
```

## Reporting

Version 0.6.0 adds lightweight reporting helpers.

```python
from pyqicharts import (
    create_report_bundle,
    export_excel,
    export_png,
    export_powerpoint,
)

chart.save_png("chart.png")
export_png(chart, "chart.png")
export_excel(chart, "report.xlsx")
export_powerpoint(chart, "report.pptx")

create_report_bundle(
    charts=[chart],
    output_dir="report",
)
```

`export_excel(...)`, `export_powerpoint(...)`, and `create_report_bundle(...)` require the `reporting` extra. If optional dependencies are missing, pyqicharts raises a clear `ImportError` explaining how to install them.

## Power BI Tables

```python
from pyqicharts import (
    powerbi_table,
    special_cause_summary_table,
    spc_summary_table,
)

rows = powerbi_table(chart)
summary = spc_summary_table(chart)
signals = special_cause_summary_table(chart)
```

These helpers return pandas DataFrames for use in Power BI, Excel, dashboards, and reporting pipelines.

## Process Features

```python
chart = qic(
    data=df,
    x="month",
    y="value",
    chart="i",
    baseline_points=12,
    recalculation_points=[18],
    target=95,
    interventions=[{"point": 10, "label": "New pathway introduced"}],
    step_changes=[{"point": 18, "label": "Limits recalculated"}],
)
```

Marker `point` values can match either a 1-based row position or the x-axis value.

## Supported Charts

| Chart Type | Status |
|------------|--------|
| Run chart | Supported |
| Individuals / XmR chart | Supported |
| Moving range chart | Supported |
| C chart | Supported |
| P chart | Supported |
| U chart | Supported |
| Pareto chart | Supported |
| Xbar chart | Planned |
| S chart | Planned |
| G chart | Planned |
| T chart | Planned |
| Risk-adjusted P-prime chart | Planned |
| Risk-adjusted U-prime chart | Planned |

## Roadmap

### v0.7.0 - Specialist Healthcare SPC Charts

- G charts
- T charts
- Example rare-event datasets

### v0.8.0 - Risk-Adjusted SPC

- P-prime charts
- U-prime charts
- Observed versus expected calculations

### v1.0.0 - Stable Release

- Stable public API
- Comprehensive documentation
- Full test coverage
- Reference validation
- Production-ready release

## License

MIT License

Copyright (c) 2026 Assegai Studios Ltd.
