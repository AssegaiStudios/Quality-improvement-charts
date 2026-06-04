"""Power BI Python visual example.

Power BI provides a pandas DataFrame named `dataset`.

Expected fields:
- month
- value
"""

from pyqicharts import qic

chart = qic(dataset, x="month", y="value", chart="i")
chart.figure
