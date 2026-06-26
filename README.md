# pyqicharts

Quality Improvement (QI) and Statistical Process Control (SPC) charts for Python.

pyqicharts is a lightweight, Python-first toolkit for practical healthcare QI charting. It is inspired by qicharts2, NHS Making Data Count, Anhoej run chart rules, and Shewhart SPC methodology.

## Version

**1.0.0**

This is the first stable public release. The simple `qic(...)` interface remains the centre of the package, with table outputs available through `qic_table(...)`.

## Install

```bash
pip install pyqicharts
```

Optional reporting exports:

```bash
pip install pyqicharts[reporting]
```

Development:

```bash
pip install -e .[dev]
pytest
```

## Quick Start

```python
from pyqicharts import qic, sample_healthcare_qi_data

df = sample_healthcare_qi_data()

chart = qic(
    data=df,
    x="month",
    y="wait_time",
    chart="i",
    improvement="low is good",
    baseline_points=6,
    target=25,
)

chart.figure
chart.table.head()
```

## Sample Data

End-user sample CSVs are included in `sample_data/`:

- `sample_healthcare_qi_data.csv`
- `sample_subgroup_measurements.csv`

The same data is available from Python:

```python
from pyqicharts import sample_healthcare_qi_data, sample_subgroup_measurements
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
| Xbar chart | Supported |
| S chart | Supported |
| G chart | Supported |
| T chart | Supported |
| P-prime chart | Supported |
| U-prime chart | Supported |
| Pareto chart | Supported |

## Reporting

```python
from pyqicharts import export_png, export_excel, export_powerpoint, create_report_bundle

chart.save_png("chart.png")
export_png(chart, "chart.png")
export_excel(chart, "report.xlsx")
export_powerpoint(chart, "report.pptx")
create_report_bundle([chart], "report")
```

Excel and PowerPoint helpers require `pyqicharts[reporting]`.

## Validation

The `validation/` folder contains deterministic datasets and expected outputs used by the test suite. These are regression fixtures and starter validation references. External clinical/statistical validation should still be performed before high-stakes operational use.

## Documentation

See `docs/` for installation, quickstart, chart-family guides, reporting, Power BI, API reference and validation notes.

## Compatibility

From v1.0 onward, public APIs should avoid breaking changes. Deprecations should be documented before removal.

## License

MIT License

Copyright (c) 2026 Assegai Studios Ltd.
