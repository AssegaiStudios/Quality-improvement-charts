# Individuals / XmR Charts

Individuals charts use the mean and moving-range-derived sigma estimate.

```python
chart = qic(data=df, x="month", y="value", chart="i", improvement="low is good")
```

Supported NHS-style special cause checks include points beyond limits, shifts and trends. v0.5 added baseline periods, recalculation segments, targets, interventions and step changes.
