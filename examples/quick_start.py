import pandas as pd
from pyqicharts import paretochart, qic


df = pd.DataFrame(
    {
        "month": range(1, 13),
        "infections": [12, 13, 14, 12, 11, 15, 16, 17, 15, 14, 18, 19],
    }
)

run_result = qic(df, x="month", y="infections", chart="run")
print(run_result.summary())

ichart_result = qic(df, x="month", y="infections", chart="i")
print(ichart_result.summary())

causes = pd.DataFrame(
    {
        "incident_type": [
            "Medication",
            "Falls",
            "Medication",
            "Pressure ulcer",
            "Falls",
            "Medication",
        ]
    }
)
pareto_result = paretochart(causes, category="incident_type")
print(pareto_result.table)
