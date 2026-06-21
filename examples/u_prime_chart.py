import matplotlib.pyplot as plt

from pyqicharts import qic, risk_adjusted_infection_rates


df = risk_adjusted_infection_rates()
chart = qic(
    data=df,
    x="month",
    y="observed",
    expected="expected",
    chart="u_prime",
    title="Risk-adjusted infection rates",
)

plt.show()
