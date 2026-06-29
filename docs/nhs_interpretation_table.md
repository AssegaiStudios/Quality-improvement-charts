# NHS Interpretation Table

`nhs_interpretation_table(chart)` returns a small pandas DataFrame intended for Excel exports, Power BI models and automated reports.

It is a reporting helper. It does not run separate SPC calculations; it reads the signal fields already calculated by `qic(...)`.

## Worked Example

```python
import pandas as pd
from pyqicharts import nhs_interpretation_table, qic

df = pd.DataFrame(
    {
        "month": range(1, 14),
        "wait_time": [30, 31, 29, 30, 32, 31, 30, 29, 22, 21, 20, 19, 18],
    }
)

chart = qic(
    data=df,
    x="month",
    y="wait_time",
    chart="i",
    improvement="low is good",
)

interpretation = nhs_interpretation_table(chart)
print(interpretation)
```

## Output Format

The table includes stable reporting metadata:

```text
schema_version
chart_id
chart_type
interpretation_type
interpretation
```

`schema_version` identifies the output schema. `chart_id` combines chart type and measure. `chart_type` is the internal chart key such as `i`, `run`, `p` or `u`. `interpretation_type` is a compact classification such as `improvement`, `concern` or `neutral`. `interpretation` is plain-English text for reports.

## Typical Use

```python
from pyqicharts import export_excel, nhs_interpretation_table

interpretation = nhs_interpretation_table(chart)
export_excel(chart, "spc_report.xlsx")
```

The same interpretation table is written automatically by `export_excel(...)` and by the Excel Companion on the `NHSInterpretation` sheet.

## Notes

For charts without detected special-cause signals, the helper returns a neutral interpretation. For Pareto charts, use the Excel Companion's Pareto-specific interpretation text because Pareto charts are not NHS time-series signal charts.

