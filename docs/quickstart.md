# Quickstart

```python
import pandas as pd
from pyqicharts import qic, qic_table

df = pd.DataFrame({
    "month": range(1, 13),
    "value": [12, 13, 14, 12, 11, 15, 16, 17, 15, 14, 18, 19],
})

chart = qic(data=df, x="month", y="value", chart="i")
chart.figure

table = qic_table(data=df, x="month", y="value", chart="i")
```

The `qic(...)` function returns a `QicResult` containing the original data, calculated table, matplotlib figure and axes.
