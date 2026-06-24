import pandas as pd

from pyqicharts import powerbi_table, qic, special_cause_summary_table, spc_summary_table


df = pd.DataFrame({"month": range(1, 7), "value": [10, 11, 10, 13, 12, 14]})
chart = qic(df, "month", "value", chart="i")
rows = powerbi_table(chart)
summary = spc_summary_table(chart)
signals = special_cause_summary_table(chart)
print(len(rows), len(summary), len(signals))
