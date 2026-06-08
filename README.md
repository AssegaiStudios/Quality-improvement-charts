# pyqicharts

Quality Improvement (QI) and Statistical Process Control (SPC) charts for Python.

Inspired by the excellent R package **qicharts2**, pyqicharts aims to provide a modern Python-first toolkit for run charts, control charts, quality improvement analytics, and reporting workflows across Python, Jupyter, Excel, and Power BI.

---

## Current Status

**Version:** 0.3.0

pyqicharts is currently in active development.

The project already provides:

- Run Charts
- Individuals (I) Charts
- Moving Range (MR) Charts
- C Charts
- P Charts
- U Charts
- Pareto Charts
- Anhøj-style run chart diagnostics
- Shewhart 3-sigma signal detection
- Excel-friendly table outputs
- Power BI integration examples
- Built-in chart themes

Future releases will focus on NHS-style SPC signal interpretation, annotation, reporting, and advanced control chart functionality.

---

## Why pyqicharts?

Many Quality Improvement and SPC practitioners use tools such as:

- qicharts2 (R)
- NHS SPC Excel tools
- Commercial SPC software

Python has historically lacked an equivalent open-source package focused on practical quality improvement and healthcare analytics.

pyqicharts aims to bridge that gap by providing:

- Robust statistical calculations
- Clear visualisations
- Excel-friendly outputs
- Power BI integration
- Healthcare-focused SPC functionality
- Open-source development

---

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e .[dev]
```

Run tests:

```bash
pytest
```

---

## Quick Start

```python
import pandas as pd
from pyqicharts import qic

df = pd.DataFrame({
    "month": range(1, 13),
    "value": [12, 13, 14, 12, 11, 15, 16, 17, 15, 14, 18, 19]
})

chart = qic(
    data=df,
    x="month",
    y="value",
    chart="run"
)

chart.figure
```

---

## Supported Charts

| Chart Type | Status |
|------------|---------|
| Run Chart | ✅ |
| Individuals (I) Chart | ✅ |
| Moving Range (MR) Chart | ✅ |
| C Chart | ✅ |
| P Chart | ✅ |
| U Chart | ✅ |
| Pareto Chart | ✅ |
| Xbar Chart | Planned |
| S Chart | Planned |
| G Chart | Planned |
| T Chart | Planned |
| Risk-adjusted P′ Chart | Planned |
| Risk-adjusted U′ Chart | Planned |

---

## Themes

Built-in themes currently include:

```python
theme="default"
theme="nhs"
theme="publication"
theme="dark"
```

---

## Excel and Power BI

pyqicharts is designed around a table-first architecture.

Statistical calculations can be accessed independently of visualisations:

```python
from pyqicharts import qic_table

output = qic_table(
    data=df,
    x="month",
    y="value",
    chart="i"
)
```

This enables integration with Excel Desktop, Excel Python, Power BI, CSV export workflows, dashboards, and reporting pipelines.

---

## NHS SPC Workbook Compatibility

During development, an NHS SPC Excel workbook was analysed as a reference implementation.

Future releases will incorporate validated functionality inspired by this workbook, including:

- Special cause detection
- Signal annotation
- Shift detection
- Trend detection
- Baseline periods
- Step changes
- Target lines
- Reporting and presentation features

The goal is not to replicate the Excel workbook directly, but to provide equivalent functionality through a modern Python architecture.

---

## Roadmap

### v0.4.0 – NHS XmR Signal Engine

- Above-UCL detection
- Below-LCL detection
- Shift detection
- Trend detection
- Signal annotations
- Signal colouring
- Improved SPC interpretation

### v0.5.0 – NHS XmR Feature Parity

- Baseline periods
- Step changes
- Target lines
- High-is-good / low-is-good logic
- Special cause summary tables

### v0.6.0 – Reporting & Office Integration

- PowerPoint export
- Excel export helpers
- Power BI templates
- PNG export utilities

### v1.0.0 – Stable Release

- Stable public API
- Comprehensive documentation
- Full test coverage
- Reference validation
- Production-ready release

---

## Contributing

Contributions, bug reports, feature requests, and suggestions are welcome.

---

## License

MIT License

Copyright © 2026 Assegai Studios Ltd.
