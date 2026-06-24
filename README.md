# pyqicharts

Quality Improvement (QI) and Statistical Process Control (SPC) charts for Python.

pyqicharts is a lightweight, Python-first toolkit for practical healthcare QI charting. It is inspired by qicharts2, NHS Making Data Count, Anhoej run chart rules, and Shewhart SPC methodology.

## Current Status

**Version:** 0.9.0

pyqicharts is in pre-1.0 active development. It currently provides run charts, Individuals/XmR charts, C/P/U charts, G/T rare-event charts, P-prime/U-prime risk-adjusted charts, Pareto charts, NHS-style special cause detection, process context features, reporting exports and Power BI-friendly tables.

v0.9 focuses on documentation, validation fixtures and release hardening. It is not yet a v1.0 stability declaration.

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

## Documentation

Documentation files live in `docs/`:

- `installation.md`
- `quickstart.md`
- `run_charts.md`
- `individuals_charts.md`
- `attribute_charts.md`
- `rare_event_charts.md`
- `risk_adjusted_charts.md`
- `reporting.md`
- `powerbi.md`
- `api_reference.md`
- `validation.md`

## Validation

The `validation/` folder contains small deterministic datasets and expected outputs used by the test suite. These are regression fixtures for release hardening, not a final independent statistical validation pack.

## Examples

The `examples/` folder includes runnable examples for supported chart families, reporting and Power BI helpers. Xbar and S chart files are included as explicit placeholders because those chart types remain planned.

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

### v1.0.0 - Stable Release

- Complete public API documentation
- Expanded independently reviewed validation datasets
- Production-ready packaging metadata
- Backwards compatibility policy
- Clear scope and limitations

## License

MIT License

Copyright (c) 2026 Assegai Studios Ltd.
