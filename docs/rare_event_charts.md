# Rare-Event Charts

G charts monitor cases between rare events. T charts monitor time between events.

```python
from pyqicharts import infections_between_events, days_between_serious_incidents, qic

g = qic(infections_between_events(), "case_number", "cases_between_events", chart="g")
t = qic(days_between_serious_incidents(), "event_number", "days_between_events", chart="t")
```

Intervals must be non-negative. Tables include rare-event centre, limits and signal fields.
