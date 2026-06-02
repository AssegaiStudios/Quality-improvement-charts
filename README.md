# pyqicharts

Python package for Quality Improvement (QI) charts, including run charts, Shewhart control charts, Pareto charts, Anhøj run-chart rules, and healthcare improvement analytics.

This project is inspired by the excellent R package `qicharts2`. The aim is to bring practical Quality Improvement and Statistical Process Control charting to Python users working in healthcare, public services, operations, research, and improvement science.

> Status: early alpha. The first implementation includes run charts, individuals charts, Pareto charts, basic Anhøj-style diagnostics, and Shewhart 3-sigma detection for individuals charts.

## Installation

From a local checkout:

```bash
pip install -e .
```

With development tools:

```bash
pip install -e .[dev]
```

## Quick start

```python
import pandas as pd
from pyqicharts import qic

sample = pd.DataFrame({
    "month": range(1, 13),
    "infections": [12, 13, 14, 12, 11, 15, 16, 17, 15, 14, 18, 19],
})

result = qic(
    data=sample,
    x="month",
    y="infections",
    chart="run",
    title="Hospital infections",
)

print(result.summary())
result.figure.show()
```

## Individuals chart

```python
from pyqicharts import qic

result = qic(
    data=sample,
    x="month",
    y="infections",
    chart="i",
)

print(result.summary())
result.figure.show()
```

## Pareto chart

```python
import pandas as pd
from pyqicharts import paretochart

incidents = pd.DataFrame({
    "incident_type": [
        "Medication",
        "Falls",
        "Medication",
        "Pressure ulcer",
        "Falls",
        "Medication",
    ]
})

result = paretochart(incidents, category="incident_type")
print(result.table)
result.figure.show()
```

## Current features

- `qic()` for run charts
- `qic()` for individuals charts
- `paretochart()` for Pareto charts
- Median, runs, crossings, and longest-run diagnostics
- Early Anhøj-style signal flags for long runs and few crossings
- Shewhart 3-sigma detection for individuals charts
- Matplotlib chart output
- Pandas-friendly API
- Pytest test suite

## Planned chart types

- MR chart
- Xbar chart
- S chart
- T chart
- C chart
- U chart
- U′ chart
- P chart
- P′ chart
- G chart
- Bernoulli CUSUM chart

## Development

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

Build package:

```bash
python -m build
```

## Project goals

The long-term goal is to provide a complete Python toolkit for:

- Quality Improvement
- Statistical Process Control
- Healthcare analytics
- Improvement science
- Process behaviour charts
- Continuous improvement

while remaining easy to use, statistically transparent, well tested, and suitable for real-world analytical workflows.

## Important note on statistical validation

This package is in early development. The current Anhøj-style rule implementation is deliberately conservative and should be reviewed and validated against authoritative references before clinical, regulatory, operational, or publication use.

## References

- Anhøj J, Olesen AV. Run charts revisited: A simulation study of run chart rules for detection of non-random variation in health care processes. PLOS ONE. 2014.
- Mohammed MA, Worthington P, Woodall WH. Plotting basic control charts: tutorial notes for healthcare practitioners. Quality and Safety in Health Care. 2008.
- Provost LP, Murray SK. The Health Care Data Guide: Learning from Data for Improvement.
- Wheeler DJ. Understanding Variation: The Key to Managing Chaos.

## License

MIT License. See `LICENSE` for details.
