# pyqicharts

Quality Improvement (QI) and Statistical Process Control (SPC) charts for Python.

pyqicharts is a lightweight, Python-first toolkit for practical healthcare QI charting. It is inspired by qicharts2, NHS Making Data Count, Anhoej run chart rules, and Shewhart SPC methodology.

## Version

**1.3.0 Excel Companion release**

This build implements the outstanding specification-based functionality without requiring a live R runtime. It includes deterministic Anhøj rules, bestbox/cutbox run-chart methods, segment-aware rule calculation, stronger process-change semantics, denominator-aware P-prime/U-prime charts, complete Power BI schemas and expanded validation/reporting tests.

Do not treat qicharts/qicharts2/NHS parity as complete until the evidence in `PARITY_REPORT.md` says so.

## Install

```bash
pip install pyqicharts
pip install pyqicharts[reporting]
pip install pyqicharts[excel]
```

Development:

```bash
pip install -e .[dev]
pytest
pytest --cov=pyqicharts --cov-report=term-missing
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

## Supported Chart Implementations

The current implementation supports run, I, MR, C, P, U, Xbar, S, G, T, P-prime, U-prime and Pareto charts. Some methods are internally regression-tested but are **not yet externally parity-certified** against qicharts/qicharts2/NHS references.

See `PARITY_REPORT.md` for current evidence and open gaps.

## Validation

Two validation areas are included:

- `validation/`: legacy deterministic regression fixtures.
- `validation_data/`: chart-by-chart validation inputs and expected outputs.

These are internal regression fixtures, not complete external statistical parity evidence.

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

## Excel Companion

The Excel Companion lets workbook users run pyqicharts through xlwings without writing Python code. Templates are included in `excel/`, and setup guidance is in `docs/excel_setup.md`.

```bash
pip install pyqicharts[excel]
xlwings addin install
pyqicharts-excel-init
```

## Signal Rules

```python
from pyqicharts import nelson_rule_signals, shewhart_rule_signals, signal_table

nelson = nelson_rule_signals(values, centre=10, sigma=2)
shewhart = shewhart_rule_signals(values, centre=10, sigma=2)
signals = signal_table(chart)
```

`qic(...)` and `qic_table(...)` also accept `rules="nelson"`, `rules="shewhart"` and `rules="all"` for additive rule metadata. Run charts accept `method="anhoej"`, `method="bestbox"` and `method="cutbox"`.

## Compatibility

The simple `qic(...)` interface remains central. Public APIs should avoid breaking changes; deprecations should be documented before removal.

## License

MIT License

Copyright (c) 2026 Assegai Studios Ltd.
