# Rare-Event SPC

Rare-event charts monitor time or opportunities between uncommon events.

## G Chart

Use a G chart for cases or opportunities between events.

```python
from pyqicharts import qic_table

table = qic_table(data=df, x="case_number", y="cases_between_events", chart="g")
```

Assumption:

Intervals follow a geometric rare-event model. pyqicharts estimates `p = 1 / (mean_interval + 1)`.

Limits:

Control limits use 0.00135 and 0.99865 tail probabilities, giving 3-sigma-equivalent rare-event limits.

## T Chart

Use a T chart for time between events.

```python
table = qic_table(data=df, x="event_number", y="days_between_events", chart="t")
```

Assumption:

Intervals follow an exponential waiting-time model.

Limits:

`LCL = -mean * log(0.99865)` and `UCL = -mean * log(0.00135)`.

## Valid Values

Zero intervals are allowed. Negative intervals are invalid and raise a clear error.

## Interpretation

Very short intervals can indicate deterioration or clustering. Very long intervals can indicate improvement, but interpretation depends on local context and whether “more time/cases between events” is desirable.
