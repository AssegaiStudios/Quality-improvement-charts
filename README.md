# pyqicharts

Quality Improvement (QI) and Statistical Process Control (SPC) charts for Python.

pyqicharts is a lightweight, Python-first toolkit for practical healthcare QI charting. It is inspired by qicharts2, NHS Making Data Count, Anhoej run chart rules, and Shewhart SPC methodology.

## Current Status

**Version:** 0.5.0

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
- Baseline periods
- Recalculation segments
- Target lines
- Intervention markers
- Step-change metadata
- Excel-friendly table outputs
- Power BI integration examples
- Built-in chart themes

Future releases will focus on reporting, Office integration, advanced healthcare SPC charts, and validation.

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
    chart="i",
    improvement="high is good",
)

chart.figure
```

## v0.5 Process Features

Version 0.5.0 adds NHS Making Data Count-style process context to `qic(...)` and `qic_table(...)`.

```python
chart = qic(
    data=df,
    x="month",
    y="value",
    chart="i",
    baseline_points=12,
    recalculation_points=[18],
    target=95,
    interventions=[
        {"point": 10, "label": "New pathway introduced"},
    ],
    step_changes=[
        {"point": 18, "label": "Limits recalculated"},
    ],
)
```

New process fields include:

- `point_index`
- `baseline_period`
- `baseline_label`
- `segment_id`
- `segment_label`
- `target`
- `intervention`
- `intervention_label`
- `step_change`
- `step_change_label`

For Individuals / XmR charts, centre lines and limits are recalculated by segment. When `baseline_points` is supplied, the first segment uses the baseline points for the initial centre line and control limits.

Marker `point` values can match either a 1-based row position or the x-axis value.

## NHS XmR Signals

Version 0.4.0 introduced NHS-style special cause fields for Individuals / XmR charts:

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

Supported interpretation values are:

```python
improvement="high is good"
improvement="low is good"
```

The implemented rules are:

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
    baseline_points=12,
    target=95,
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

## Roadmap

### v0.6.0 - Reporting and Office Integration

- PNG export
- Excel export helpers
- PowerPoint export helpers
- Report bundles
- Power BI-friendly tables

### v0.7.0 - Specialist Healthcare SPC Charts

- G charts
- T charts
- Example rare-event datasets

### v1.0.0 - Stable Release

- Stable public API
- Comprehensive documentation
- Full test coverage
- Reference validation
- Production-ready release

## License

MIT License

Copyright (c) 2026 Assegai Studios Ltd.
