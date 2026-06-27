# PowerPoint Export Guide

Install reporting dependencies:

```bash
pip install pyqicharts[reporting]
```

Export a chart deck:

```python
from pyqicharts import export_powerpoint

export_powerpoint(chart, "report.pptx")
```

PowerPoint exports include a title slide and one slide per chart image with a signal summary.
