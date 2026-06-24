"""Power BI P chart example. Power BI provides a DataFrame named dataset."""
import pandas as pd

from pyqicharts import qic

if "dataset" not in globals():
    dataset = pd.DataFrame({"month": range(1, 7), "defects": [3, 4, 2, 5, 6, 4], "sample_size": [100, 110, 95, 105, 115, 108]})

chart = qic(dataset, x="month", y="defects", denominator="sample_size", chart="p", theme="nhs")
chart.figure
