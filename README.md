# pyqicharts

Python package for Quality Improvement (QI) and Statistical Process Control (SPC) charts.

`pyqicharts` is inspired by the R package `qicharts2` and aims to provide a Python-first toolkit for run charts, Shewhart control charts, Pareto charts, improvement analytics, and QI reporting.

> Status: early alpha. Version 0.2.0 is suitable for testing, examples, learning, and early feedback. Validate outputs before operational use.

---

## New in v0.2.0

- Moving Range (MR) charts
- Improved Individuals (I) chart calculations
- `qic_table()` for Excel, Power BI, dashboards and reporting pipelines
- `pareto_table()` for Excel and Power BI integration
- `QicResult.table` output for every chart
- Power BI example script
- Excel/Python example script
- Expanded tests
- Updated documentation and roadmap

---

## Supported charts

| Chart | Status |
|---|---|
| Run chart | Available |
| Individuals / I chart | Available |
| Moving Range / MR chart | Available |
| Pareto chart | Available |
| C chart | Planned |
| P chart | Planned |
| U chart | Planned |
| Xbar chart | Planned |
| S chart | Planned |
| T chart | Planned |
| G chart | Planned |
| P′ / U′ risk-adjusted charts | Planned |

---

## Installation

From a cloned repository:

```bash
pip install -e .[dev]
```

Run tests:

```bash
pytest
```

---

## Quick start

```python
import pandas as pd
from pyqicharts import qic

df = pd.DataFrame({
    "month": range(1, 13),
    "value": [12, 13, 14, 12, 11, 15, 16, 17, 15, 14, 18, 19],
})

chart = qic(df, x="month", y="value", chart="run")
chart.figure
```

Access the calculations:

```python
chart.table
chart.anhoej
chart.summary()
```

---

## Individuals chart

```python
from pyqicharts import qic

chart = qic(df, x="month", y="value", chart="i")
chart.figure
chart.table
```

The I chart uses the average moving range to estimate sigma:

```text
sigma = MRbar / 1.128
UCL = mean + 3 * sigma
LCL = mean - 3 * sigma
```

---

## Moving Range chart

```python
chart = qic(df, x="month", y="value", chart="mr")
chart.figure
chart.table
```

The MR chart uses:

```text
CL = MRbar
LCL = 0
UCL = 3.267 * MRbar
```

---

## Pareto chart

```python
from pyqicharts import paretochart

chart = paretochart(df, category="incident_type")
chart.figure
chart.table
```

For table-only workflows:

```python
from pyqicharts import pareto_table

pareto = pareto_table(df, category="incident_type")
```

---

## Excel and Power BI support

Version 0.2.0 introduces table-first APIs designed for applications that prefer tabular outputs.

### Excel-friendly output

```python
from pyqicharts import qic_table

output = qic_table(df, x="month", y="value", chart="run")
```

This returns a pandas DataFrame containing columns such as:

```text
month, value, chart, centre, lcl, ucl, moving_range, signal, signal_rule
```

That makes the output suitable for:

- Excel Python
- Excel Desktop workflows
- xlwings-based integrations
- CSV export
- dashboard pipelines

### Power BI-friendly output

Power BI Python visuals provide a DataFrame called `dataset`.

```python
from pyqicharts import qic

chart = qic(dataset, x="month", y="value", chart="i")
chart.figure
```

For Power BI transformations or calculated tables:

```python
from pyqicharts import qic_table

result = qic_table(dataset, x="month", y="value", chart="i")
```

---

## Design principles

`pyqicharts` separates:

1. **Statistical calculations**
2. **Table outputs**
3. **Matplotlib visualisation**

This is intentional. It allows the same statistical engine to support:

- Jupyter notebooks
- Python scripts
- Excel Online
- Excel Desktop
- Power BI Desktop
- Power BI Service, where supported
- Future web or API integrations

---

## Example output table

```text
month | value | chart | centre | lcl | ucl | moving_range | signal | signal_rule
```

This makes it easy to create charts natively in Excel or Power BI while using pyqicharts for the statistical calculations.

---

## Roadmap

### v0.3.0

- C charts
- P charts
- U charts
- Better signal annotations
- More robust Anhøj threshold validation

### v0.4.0

- Xbar and S charts
- Additional Shewhart/Nelson-style rules
- Improved chart styling

### v0.5.0

- G and T charts
- Example healthcare datasets
- Documentation site

### v1.0.0

- Stable API
- Validated examples against published references
- Full documentation
- Production-ready release

---

## Disclaimer

This software is provided for quality improvement, process monitoring, education, and research purposes. Users are responsible for validating outputs and ensuring suitability for their intended use. The software is provided without warranty under the MIT License.

---

## License

MIT License.

Copyright © 2026 Assegai Studios Ltd.
