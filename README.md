# pyqicharts

Quality Improvement (QI) and Statistical Process Control (SPC) charts for Python.

pyqicharts is a lightweight, Python-first toolkit for practical healthcare QI charting. It is inspired by qicharts2, NHS Making Data Count, Anhoej run chart rules, and Shewhart SPC methodology.

## Current Status

**Version:** 0.8.0

pyqicharts is currently in active development. The project already provides:

- Run charts
- Individuals / XmR charts
- Moving range charts
- C charts
- P charts
- U charts
- G charts
- T charts
- P-prime risk-adjusted charts
- U-prime risk-adjusted charts
- Pareto charts
- Anhoej-style run chart diagnostics
- NHS-style XmR special cause detection
- Baselines, recalculation segments, targets, interventions and step changes
- PNG, Excel and PowerPoint export
- Report bundles
- Power BI-friendly tables

Future releases will focus on validation, documentation, packaging hardening and public release readiness.

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

## Risk-Adjusted Charts

Version 0.8.0 adds observed-versus-expected SPC charts.

```python
from pyqicharts import qic, risk_adjusted_readmissions

df = risk_adjusted_readmissions()
chart = qic(
    data=df,
    x="month",
    y="observed",
    expected="expected",
    chart="p_prime",
)
```

```python
from pyqicharts import qic, risk_adjusted_infection_rates

df = risk_adjusted_infection_rates()
chart = qic(
    data=df,
    x="month",
    y="observed",
    expected="expected",
    chart="u_prime",
)
```

Risk-adjusted tables include:

- `observed`
- `expected`
- `oe_ratio`
- `risk_adjusted_value`
- `adjusted_rate`
- `expected_zero`
- `outside_lcl`
- `outside_ucl`
- `signal`

Rows with zero expected values are retained and marked with `expected_zero=True`; adjusted values and limits are set to missing for those rows.

## Rare-Event Charts

```python
from pyqicharts import infections_between_events, qic

df = infections_between_events()
chart = qic(data=df, x="case_number", y="cases_between_events", chart="g")
```

```python
from pyqicharts import days_between_serious_incidents, qic

df = days_between_serious_incidents()
chart = qic(data=df, x="event_number", y="days_between_events", chart="t")
```

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
| P-prime chart | Supported |
| U-prime chart | Supported |
| Pareto chart | Supported |
| Xbar chart | Planned |
| S chart | Planned |

## Roadmap

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
