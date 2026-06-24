import matplotlib.pyplot as plt
import pandas as pd

from pyqicharts import qic


df = pd.DataFrame({"month": range(1, 7), "events": [3, 4, 2, 5, 6, 4], "denominator": [100, 110, 95, 105, 115, 108]})
chart = qic(df, "month", "events", denominator="denominator", chart="u")
plt.close(chart.figure)
