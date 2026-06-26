# Individuals / XmR Charts

Individuals charts use the mean and moving-range-derived sigma estimate.

```python
chart = qic(data=df, x="month", y="value", chart="i", improvement="low is good")
```

Supported NHS-style special cause checks include points beyond limits, shifts and trends. v0.5 added baseline periods, recalculation segments, targets, interventions and step changes.

## Xbar and S Charts

v1.0 adds subgroup charts. Use `x` as the subgroup/time period and `y` as the observation column:

```python
from pyqicharts import qic, sample_subgroup_measurements

df = sample_subgroup_measurements()
xbar = qic(df, x="subgroup", y="value", chart="xbar")
s_chart = qic(df, x="subgroup", y="value", chart="s")
```
