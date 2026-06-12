# pyqicharts v0.5.0 Release Notes

pyqicharts v0.5.0 adds NHS Making Data Count-style process context on top of the v0.4 XmR signal engine.

## Highlights

- `baseline_points` marks baseline rows and uses baseline data for the first Individuals / XmR centre line and limits.
- `recalculation_points` creates process segments and recalculates Individuals / XmR centre lines and limits by segment.
- `target` adds a target field to tables and a target line to charts.
- `interventions` add vertical chart markers and intervention metadata.
- `step_changes` add vertical chart markers and process-change metadata.

## New Table Fields

- `point_index`
- `baseline_period`
- `baseline_label`
- `segment_id`
- `segment_label`
- `target`
- `intervention`
- `intervention_label`
- `step_change`
- `step_change_label`

## Example

```python
chart = qic(
    data=df,
    x="month",
    y="value",
    chart="i",
    baseline_points=12,
    recalculation_points=[18],
    target=95,
    interventions=[
        {"point": 10, "label": "New pathway introduced"},
    ],
    step_changes=[
        {"point": 18, "label": "Limits recalculated"},
    ],
)
```

Marker `point` values can match either a 1-based row position or the x-axis value.

## Compatibility

Existing calls to `qic(...)` and `qic_table(...)` continue to work. The v0.5 arguments and table columns are additive.

## Not Included Yet

PNG, Excel, PowerPoint, report bundle and Power BI summary helpers are intentionally left for v0.6. Specialist rare-event and risk-adjusted charts remain planned for later releases.
