"""Power BI P chart example. Power BI provides a DataFrame named dataset."""
from pyqicharts import qic
chart = qic(dataset, x="month", y="defects", denominator="sample_size", chart="p", theme="nhs")
chart.figure
