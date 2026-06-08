"""Power BI Python visual example. Power BI provides a DataFrame named dataset."""
from pyqicharts import qic
chart = qic(dataset, x="month", y="value", chart="i", theme="nhs")
chart.figure
