"""Generate a demo chart image suitable for README or LinkedIn."""
import pandas as pd
from pyqicharts import qic

df = pd.DataFrame({
    "month": range(1, 25),
    "value": [12, 13, 11, 14, 12, 13, 12, 11, 13, 12, 14, 13, 17, 18, 19, 17, 20, 21, 19, 20, 22, 21, 23, 24],
})

chart = qic(data=df, x="month", y="value", chart="i", theme="nhs", title="Example Individuals Chart")
chart.figure.savefig("linkedin_i_chart.png", dpi=300, bbox_inches="tight")
print("Saved linkedin_i_chart.png")
