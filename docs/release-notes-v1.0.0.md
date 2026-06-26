# pyqicharts v1.0.0 Release Notes

pyqicharts v1.0.0 is the first stable public release.

## Highlights

- Stable public release metadata.
- Xbar and S chart support.
- End-user sample datasets in `sample_data/`.
- Python helpers for sample datasets.
- Full roadmap chart family coverage through v1.0.
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

From v1.0 onward, public APIs should avoid breaking changes. Deprecations should be documented before removal.

## Scope Note

The package provides practical SPC and QI charting tools. Users should validate outputs for local governance and high-stakes operational decisions.
