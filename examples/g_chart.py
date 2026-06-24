import matplotlib.pyplot as plt

from pyqicharts import infections_between_events, qic


df = infections_between_events()
chart = qic(
    data=df,
    x="case_number",
    y="cases_between_events",
    chart="g",
    title="Infections between events",
)

plt.close(chart.figure)
