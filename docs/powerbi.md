# Power BI

Power BI-friendly helpers return pandas DataFrames.

```python
from pyqicharts import powerbi_table, spc_summary_table, special_cause_summary_table, signal_table, kpi_table

rows = powerbi_table(chart)
summary = spc_summary_table(chart)
special_causes = special_cause_summary_table(chart)
signals = signal_table(chart)
kpis = kpi_table(chart)
```

The v1.1 signal schema uses `schema_version = "1.1"` and includes chart type, rule type, rule name, direction, severity, start/end positions, x-axis values and a message.
