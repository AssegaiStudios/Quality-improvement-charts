# pyqicharts v0.6.0

This release adds reporting and Office integration helpers while keeping the core package lightweight.

## Added

- `chart.save_png(...)`
- `export_png(...)`
- `export_excel(...)`
- `export_powerpoint(...)`
- `create_report_bundle(...)`
- `powerbi_table(...)`
- `spc_summary_table(...)`
- `special_cause_summary_table(...)`
- Optional `reporting` extra for Excel and PowerPoint dependencies

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
