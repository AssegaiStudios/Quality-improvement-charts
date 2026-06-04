"""Example for Excel-friendly table output."""

import pandas as pd
from pyqicharts import qic_table, pareto_table

df = pd.DataFrame({
    "month": range(1, 13),
    "value": [12, 13, 14, 12, 11, 15, 16, 17, 15, 14, 18, 19],
    "incident_type": [
        "Medication", "Falls", "Falls", "Pressure ulcer",
        "Medication", "Medication", "Infection", "Falls",
        "Medication", "Infection", "Falls", "Medication",
    ],
})

qic_output = qic_table(df, x="month", y="value", chart="i")
pareto_output = pareto_table(df, category="incident_type")

print(qic_output)
print(pareto_output)
