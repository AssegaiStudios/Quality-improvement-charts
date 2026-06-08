"""Quick-start example for pyqicharts v0.3.0."""
import pandas as pd
from pyqicharts import qic, paretochart

df = pd.DataFrame({
    "month": range(1, 13),
    "value": [12, 13, 14, 12, 11, 15, 16, 17, 15, 14, 18, 19],
    "incidents": [3, 4, 2, 3, 5, 4, 6, 5, 7, 6, 8, 7],
    "sample_size": [100, 102, 98, 105, 101, 99, 103, 107, 110, 108, 111, 115],
    "bed_days": [900, 910, 880, 930, 920, 915, 940, 950, 960, 970, 980, 995],
    "incident_type": ["Medication", "Falls", "Falls", "Pressure ulcer", "Medication", "Medication", "Infection", "Falls", "Medication", "Infection", "Falls", "Medication"],
})

print(qic(df, "month", "value", chart="run", theme="nhs").summary())
print(qic(df, "month", "value", chart="i", theme="nhs").summary())
print(qic(df, "month", "value", chart="mr", theme="nhs").summary())
print(qic(df, "month", "incidents", chart="c", theme="nhs").summary())
print(qic(df, "month", "incidents", denominator="sample_size", chart="p", theme="nhs").summary())
print(qic(df, "month", "incidents", denominator="bed_days", chart="u", theme="nhs").summary())
print(paretochart(df, "incident_type", theme="nhs").table)
