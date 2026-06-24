"""Power BI Python visual example. Power BI provides a DataFrame named dataset."""
import pandas as pd

from pyqicharts import qic

if "dataset" not in globals():
    dataset = pd.DataFrame({"month": range(1, 7), "value": [10, 11, 10, 13, 12, 14]})

chart = qic(dataset, x="month", y="value", chart="i", theme="nhs")
chart.figure
