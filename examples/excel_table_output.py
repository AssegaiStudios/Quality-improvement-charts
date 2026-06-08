"""Excel-friendly table output example."""
import pandas as pd
from pyqicharts import qic_table, pareto_table

df = pd.DataFrame({"month": range(1, 7), "incidents": [3,4,2,5,6,4], "sample_size": [100,110,95,105,115,108], "incident_type": ["A","B","A","C","A","B"]})
print(qic_table(df, x="month", y="incidents", denominator="sample_size", chart="p"))
print(pareto_table(df, category="incident_type"))
