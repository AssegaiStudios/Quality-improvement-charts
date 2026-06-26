import matplotlib.pyplot as plt

from pyqicharts import qic, sample_subgroup_measurements


df = sample_subgroup_measurements()
chart = qic(df, x="subgroup", y="value", chart="s")
plt.close(chart.figure)
