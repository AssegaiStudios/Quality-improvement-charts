# pyqicharts v0.6.0 Release Notes

pyqicharts v0.6.0 adds reporting and Office integration helpers while keeping the core package lightweight.

## Highlights

- PNG export with `chart.save_png(...)` and `export_png(...)`.
- Excel export with chart data, SPC summary, special cause summary and optional embedded chart image.
- PowerPoint export with a title slide and one chart per slide.
- Report bundle helper that creates PNG images, Excel workbook, PowerPoint deck and metadata JSON.
- Power BI-friendly table helpers returning pandas DataFrames.
- Optional reporting dependencies via `pyqicharts[reporting]`.

## New Public API

```python
from pyqicharts import (
    create_report_bundle,
    export_excel,
    export_png,
    export_powerpoint,
    powerbi_table,
    special_cause_summary_table,
    spc_summary_table,
)
```

## Optional Dependencies

The core package remains focused on charting. Excel and PowerPoint support require optional dependencies:

```bash
pip install pyqicharts[reporting]
```

If `openpyxl` or `python-pptx` are missing, export helpers raise a clear `ImportError`.

## Compatibility

Existing calls to `qic(...)` and `qic_table(...)` continue to work. v0.6 adds reporting helpers without changing existing return types.

## Not Included Yet

Specialist rare-event charts, risk-adjusted charts, full documentation, validation datasets and release hardening remain planned for later roadmap releases.
