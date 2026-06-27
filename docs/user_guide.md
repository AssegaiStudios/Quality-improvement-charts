# User Guide

Start with `qic(...)` for charts and `qic_table(...)` when you need the calculated rows without plotting.

```python
from pyqicharts import qic

chart = qic(data=df, x="month", y="value", chart="i")
```

Use `chart.table` for calculated values, `chart.signal_table()` for rule metadata, and export helpers for PNG, Excel and PowerPoint reporting.
