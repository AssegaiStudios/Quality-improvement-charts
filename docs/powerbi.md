# Power BI

Power BI-friendly helpers return pandas DataFrames.

```python
from pyqicharts import powerbi_table, spc_summary_table, special_cause_summary_table

rows = powerbi_table(chart)
summary = spc_summary_table(chart)
signals = special_cause_summary_table(chart)
```
