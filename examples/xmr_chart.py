import matplotlib.pyplot as plt
import pandas as pd

from pyqicharts import qic


df = pd.DataFrame({"month": range(1, 13), "value": [12, 13, 14, 12, 11, 15, 16, 17, 15, 14, 18, 19]})
chart = qic(df, "month", "value", chart="i", improvement="high is good")
plt.close(chart.figure)
