# Reporting

PNG export is available in the core package. Excel and PowerPoint require `pyqicharts[reporting]`.

```python
from pyqicharts import export_png, export_excel, export_powerpoint, create_report_bundle

export_png(chart, "chart.png")
export_excel(chart, "report.xlsx")
export_powerpoint(chart, "report.pptx")
create_report_bundle([chart], "report")
```

If optional reporting dependencies are missing, pyqicharts raises a clear `ImportError`.
