# Migration From qicharts2

The central Python entry points are:

- `qic(...)`
- `qic_table(...)`
- `pareto_chart(...)`
- `pareto_table(...)`

qicharts-style phase vocabulary is available through additive arguments such as `freeze_points`, `break_points`, `exclude_points` and `phases`.

This guide is a starting point. Full qicharts2 parity migration documentation will need reference-output comparisons for every supported chart type.
