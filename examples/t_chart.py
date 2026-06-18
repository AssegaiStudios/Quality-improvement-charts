import matplotlib.pyplot as plt

from pyqicharts import days_between_serious_incidents, qic


df = days_between_serious_incidents()
chart = qic(
    data=df,
    x="event_number",
    y="days_between_events",
    chart="t",
    title="Days between serious incidents",
)

plt.show()
