# Excel Guide

Install reporting dependencies with:

```bash
pip install pyqicharts[reporting]
```

Export a chart:

```python
from pyqicharts import export_excel

export_excel(chart, "report.xlsx")
```

v1.1 workbooks include chart data, SPC summary, special causes, signal schema, KPI summary and optional chart images.
