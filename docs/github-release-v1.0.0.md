# pyqicharts v1.0.0

Interim parity-readiness rebuild of pyqicharts. This release preserves the v1.0 API surface while making the validation and parity status explicit.

## Added

- Xbar charts
- S charts
- End-user sample datasets
- Interim beta release metadata
- Chart-by-chart validation fixtures
- Parity report with known gaps
- Expanded source comments and developer notes
- v1.0 release tests

## Important Scope Note

This archive does not claim final qicharts2, qicharts or NHS workbook parity. See `PARITY_REPORT.md` before using the package as validated statistical evidence.

## Install

```bash
pip install pyqicharts
pip install pyqicharts[reporting]
```

For local development from this source archive:

```bash
pip install -e .[dev]
pytest
```
