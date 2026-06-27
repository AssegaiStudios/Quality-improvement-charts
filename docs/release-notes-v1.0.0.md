# pyqicharts v1.0.0 Interim Release Notes

pyqicharts v1.0.0 is an interim parity-readiness rebuild. It is not a final parity-complete release.

## Highlights

- Beta/interim release metadata.
- Xbar and S chart support.
- End-user sample datasets in `sample_data/`.
- Python helpers for sample datasets.
- Full roadmap chart family coverage through v1.0.
- Interim chart validation fixtures in `validation_data/`.
- A formal `PARITY_REPORT.md` describing evidence and known gaps.
- Expanded developer comments and docstrings.
- Tests for sample data, examples, validation fixtures and package build readiness.

## Sample Data

CSV files:

- `sample_data/sample_healthcare_qi_data.csv`
- `sample_data/sample_subgroup_measurements.csv`

Python helpers:

```python
from pyqicharts import sample_healthcare_qi_data, sample_subgroup_measurements
```

## Compatibility

The simple public APIs such as `qic(...)`, `qic_table(...)`, `pareto_chart(...)` and `pareto_table(...)` remain central. Deprecations should be documented before removal.

## Scope Note

The package provides practical SPC and QI charting tools. Full Anhøj, qicharts2, qicharts and NHS Making Data Count parity is not claimed in this interim rebuild. Users should validate outputs for local governance and high-stakes operational decisions.
