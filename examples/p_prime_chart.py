import matplotlib.pyplot as plt

from pyqicharts import qic, risk_adjusted_readmissions


df = risk_adjusted_readmissions()
chart = qic(
    data=df,
    x="month",
    y="observed",
    expected="expected",
    chart="p_prime",
    title="Risk-adjusted readmissions",
)

plt.close(chart.figure)
