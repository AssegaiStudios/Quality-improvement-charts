# pyqicharts

Quality Improvement (QI) and Statistical Process Control (SPC) charts for Python.

pyqicharts is a lightweight, Python-first toolkit for practical healthcare QI charting. It is inspired by qicharts2, NHS Making Data Count, Anhøj run chart rules, and Shewhart SPC methodology.

## Current Status

**Version:** 0.4.0

pyqicharts is currently in active development. The project already provides:

- Run charts
- Individuals / XmR charts
- Moving range charts
- C charts
- P charts
- U charts
- Pareto charts
- Anhøj-style run chart diagnostics
- NHS-style XmR special cause detection
- Direction-of-improvement interpretation
- Excel-friendly table outputs
- Power BI integration examples
- Built-in chart themes

Future releases will focus on baselines, process-change handling, targets, interventions, reporting, and advanced healthcare SPC charts.

## Installation

```bash
pip install -e .
```

For development:

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

chart = qic(
    data=df,
    x="month",
    y="value",
    chart="run",
)

chart.figure
```

## NHS XmR Signals

Version 0.4.0 adds NHS-style special cause fields for Individuals / XmR charts:

- `outside_ucl`
- `outside_lcl`
- `shift`
- `trend`
- `special_cause`
- `special_cause_rule`
- `special_cause_direction`
- `special_cause_type`
- `special_cause_colour`
- `special_cause_label`

Use `improvement` to classify signals as improvement, concern, or neutral:

```python
chart = qic(
    data=df,
    x="month",
    y="value",
    chart="i",
    improvement="low is good",
)

chart.table[[
    "month",
    "value",
    "signal",
    "special_cause_rule",
    "special_cause_type",
]]
```

Supported values are:

```python
improvement="high is good"
improvement="low is good"
```

The implemented v0.4.0 rules are:

- Rule 1: one point outside the control limits.
- Shift: eight non-centre points above or below the centre line.
- Trend: six consecutive increasing or decreasing points.

## Table-First Outputs

Statistical calculations can be accessed independently of visualisations:

```python
from pyqicharts import qic_table

output = qic_table(
    data=df,
    x="month",
    y="value",
    chart="i",
    improvement="high is good",
)
```

This supports Excel Desktop, Excel Python, Power BI, CSV workflows, dashboards, and reporting pipelines.

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

## Themes

Built-in themes currently include:

```python
theme="default"
theme="nhs"
theme="publication"
theme="dark"
```

## Roadmap

### v0.5.0 - Baselines, Targets, Interventions and Recalculation

- Baseline periods
- Recalculation periods
- Target lines
- Intervention markers
- Step-change metadata

### v0.6.0 - Reporting and Office Integration

- PNG export
- Excel export helpers
- PowerPoint export helpers
- Report bundles
- Power BI-friendly tables

### v1.0.0 - Stable Release

- Stable public API
- Comprehensive documentation
- Full test coverage
- Reference validation
- Production-ready release

## License

MIT License

Copyright (c) 2026 Assegai Studios Ltd.
