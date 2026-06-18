# pyqicharts v0.7.0 Release Notes

pyqicharts v0.7.0 adds specialist healthcare rare-event charts.

## Highlights

- G chart support for cases between events.
- T chart support for time between events.
- Rare-event centre lines and control limits.
- Detection of unusually short and unusually long intervals.
- Clear validation errors for negative intervals.
- Synthetic healthcare example datasets.
- G and T chart examples.

## New Public API

```python
from pyqicharts import (
    days_between_falls_with_harm,
    days_between_serious_incidents,
    infections_between_events,
    qic,
)
```

## Examples

```python
df = infections_between_events()
chart = qic(
    data=df,
    x="case_number",
    y="cases_between_events",
    chart="g",
)
```

```python
df = days_between_serious_incidents()
chart = qic(
    data=df,
    x="event_number",
    y="days_between_events",
    chart="t",
)
```

## Compatibility

Existing calls to `qic(...)`, `qic_table(...)`, reporting helpers and Power BI helpers continue to work. v0.7 adds chart types without changing existing return types.

## Not Included Yet

Risk-adjusted P-prime and U-prime charts are intentionally left for v0.8. Full documentation, validation datasets and release hardening remain planned for v0.9.
