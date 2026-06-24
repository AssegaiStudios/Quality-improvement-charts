import matplotlib.pyplot as plt
import pandas as pd

from pyqicharts import export_excel, qic


df = pd.DataFrame({"month": range(1, 7), "value": [10, 11, 10, 13, 12, 14]})
chart = qic(df, "month", "value", chart="i")
export_excel(chart, "example_report.xlsx")
plt.close(chart.figure)
