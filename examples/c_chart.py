import matplotlib.pyplot as plt
import pandas as pd

from pyqicharts import qic


df = pd.DataFrame({"month": range(1, 7), "count": [3, 4, 2, 5, 6, 4]})
chart = qic(df, "month", "count", chart="c")
plt.close(chart.figure)
