"""Power BI Python table transform example.

Power BI provides a pandas DataFrame named `dataset`.
"""

from pyqicharts import qic_table

result = qic_table(dataset, x="month", y="value", chart="i")
