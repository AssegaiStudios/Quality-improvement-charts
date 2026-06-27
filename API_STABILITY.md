# pyqicharts API Stability

Status: v1.2.1.

## Stable Public APIs

These APIs are stable and central:

- `qic()`
- `qic_table()`
- `pareto_chart()`
- `pareto_table()`

Stable reporting and integration APIs:

- `export_png()`
- `export_excel()`
- `export_powerpoint()`
- `create_report_bundle()`
- `powerbi_table()`
- `spc_summary_table()`
- `signal_table()`
- `special_cause_summary_table()`
- `kpi_table()`
- `nhs_interpretation_table()`
- `phase_metadata_table()`
- `intervention_metadata_table()`
- `target_metadata_table()`

Stable rule helpers:

- `anhoej_rules()`
- `nelson_rule_signals()`
- `shewhart_rule_signals()`

Stable registries:

- `CHART_ALIASES`
- `VALID_CHARTS`

## Aliases

Chart aliases are documented in `CHART_ALIASES`. The backwards-compatible `paretochart()` alias remains available.

## Deprecated APIs

No public API is deprecated in v1.2.1.

## Planned Removals

No removals are planned.
