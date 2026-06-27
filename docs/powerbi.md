# Power BI

Power BI-friendly helpers return pandas DataFrames.

```python
from pyqicharts import (
    intervention_metadata_table,
    kpi_table,
    nhs_interpretation_table,
    phase_metadata_table,
    powerbi_table,
    signal_table,
    special_cause_summary_table,
    spc_summary_table,
    target_metadata_table,
)

rows = powerbi_table(chart)
summary = spc_summary_table(chart)
special_causes = special_cause_summary_table(chart)
signals = signal_table(chart)
kpis = kpi_table(chart)
interpretation = nhs_interpretation_table(chart)
phases = phase_metadata_table(chart)
interventions = intervention_metadata_table(chart)
targets = target_metadata_table(chart)
```

The v1.2 schemas include `schema_version`, `chart_id` and `chart_type` in every Power BI table. The signal schema includes rule type, rule name, direction, severity, start/end positions, x-axis values and a message.
