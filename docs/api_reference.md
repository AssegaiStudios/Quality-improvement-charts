# API Reference

Core charting:

- `qic(data, x, y, chart="run", ...)`
- `qic_table(data, x, y, chart="run", ...)`
- `pareto_chart(data, category, count=None)`
- `paretochart(data, category, count=None)` remains available for backwards compatibility.
- `pareto_table(data, category, count=None)`

Supported `chart=` values include `run`, `i`, `mr`, `c`, `p`, `u`, `xbar`, `s`, `g`, `t`, `p_prime` and `u_prime`.

Common optional process arguments include `baseline_points`, `recalculation_points`, `target`, `interventions`, `step_changes`, `freeze_points`, `break_points`, `exclude_points`, `phases` and `rules`.

Signal rules:

- `nelson_rule_signals(values, centre, sigma)`
- `shewhart_rule_signals(values, centre, sigma)`
- `signal_table(chart)`

Reporting:

- `export_png(chart, path)`
- `export_excel(chart, path)`
- `export_powerpoint(chart, path)`
- `create_report_bundle(charts, output_dir)`

Power BI:

- `powerbi_table(chart)`
- `spc_summary_table(chart)`
- `special_cause_summary_table(chart)`
- `signal_table(chart)`
- `kpi_table(chart)`

Example and sample datasets are exposed from the package root, including `sample_healthcare_qi_data()` and `sample_subgroup_measurements()`.
