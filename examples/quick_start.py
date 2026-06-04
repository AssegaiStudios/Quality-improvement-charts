import pandas as pd
from pyqicharts import qic, paretochart

df = pd.DataFrame({
    "month": range(1, 13),
    "value": [12, 13, 14, 12, 11, 15, 16, 17, 15, 14, 18, 19],
    "incident_type": [
        "Medication", "Falls", "Falls", "Pressure ulcer",
        "Medication", "Medication", "Infection", "Falls",
        "Medication", "Infection", "Falls", "Medication",
    ],
})

run_chart = qic(df, x="month", y="value", chart="run")
i_chart = qic(df, x="month", y="value", chart="i")
mr_chart = qic(df, x="month", y="value", chart="mr")
pareto = paretochart(df, category="incident_type")

print(run_chart.summary())
print(i_chart.table.head())
print(mr_chart.table.head())
print(pareto.table)
