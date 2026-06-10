# pyqicharts v0.4.0 Release Notes

pyqicharts v0.4.0 adds a focused NHS-style XmR signal engine while preserving the v0.3 public API.

## Highlights

- Individuals / XmR charts now detect points above the UCL and below the LCL.
- XmR tables now include shift and trend detection.
- Signals can be interpreted with `improvement="high is good"` or `improvement="low is good"`.
- Returned tables include explicit special-cause fields suitable for Excel, Power BI, dashboards, and reporting workflows.
- Matplotlib charts colour interpreted special causes using Making Data Count-style semantics.

## Implemented Rules

- Rule 1: one point outside the control limits.
- Shift: eight non-centre points above or below the centre line.
- Trend: six consecutive increasing or decreasing points.

## New Table Fields

- `outside_ucl`
- `outside_lcl`
- `shift`
- `trend`
- `special_cause`
- `special_cause_rule`
- `special_cause_direction`
- `special_cause_type`
- `special_cause_colour`
- `special_cause_label`

## Compatibility

Existing calls to `qic(...)` and `qic_table(...)` continue to work. The new arguments and table columns are additive.

## Not Included Yet

Baselines, recalculation periods, targets, interventions, reporting exports, rare-event charts, and risk-adjusted charts are intentionally left for later roadmap releases.
