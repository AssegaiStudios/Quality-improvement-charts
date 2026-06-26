# Quickstart

```python
from pyqicharts import qic, qic_table, sample_healthcare_qi_data

df = sample_healthcare_qi_data()

chart = qic(data=df, x="month", y="wait_time", chart="i", improvement="low is good")
chart.figure

table = qic_table(data=df, x="month", y="wait_time", chart="i")
```

The `qic(...)` function returns a `QicResult` containing the original data, calculated table, matplotlib figure and axes.
