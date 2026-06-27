# pyqicharts v1.1.0 Parity Report

## Release Status

v1.1.0 is a parity-readiness release. It makes substantial local progress toward qicharts/qicharts2/NHS parity, but it is not a final parity-certified release because external reference outputs from qicharts, qicharts2 and NHS workbooks are not bundled and compared end to end.

## Evidence Summary

| Area | Status | Evidence | Remaining Work |
| --- | --- | --- | --- |
| Clean test execution | Complete locally | Local pytest suite passes from the v1.1 source tree and from extracted release archives. CI covers Linux, Windows and macOS on Python 3.10, 3.11 and 3.12. | Confirm hosted CI run after publishing to GitHub. |
| Coverage targets | Complete locally | Local coverage is 96.06% overall with calculation modules at 95%+ in the v1.1 test run. | Keep the threshold enforced in CI and raise focused coverage when new modules are added. |
| Chart validation framework | Complete for internal fixtures | `tests/validation/` and `validation_data/` cover run, I, MR, C, P, U, Xbar, S, G, T, P-prime and U-prime internal regression outputs. | Add externally reviewed expected outputs. |
| Anhøj parity | Partial | Run-chart diagnostics handle medians and ties, with regression tests. | Validate against published Anhøj and qicharts2 examples before marking complete. |
| Nelson rules | Complete locally | `nelson_rule_signals(...)` implements Rules 1-8 with rule ID, name, start/end point, direction and severity metadata. Tests cover every rule. | Compare against qicharts2/reference examples if those outputs become available. |
| Shewhart rules | Partial | `shewhart_rule_signals(...)` exposes a compact Shewhart-compatible rule set and `rules=` configuration exists. | Add full zone-rule reference validation and documented equivalence mapping. |
| Unified signal engine | Complete locally | `Signal`, `signals_to_frame(...)`, `signal_table(...)` and `chart.signal_table()` provide a stable schema for reports and Power BI. | Continue migrating all future rule paths through this schema. |
| Chart family coverage | Partial | Run, I, MR, C, P, U, Xbar, S, G, T, P-prime, U-prime and Pareto APIs exist and are tested. | External parity validation remains required; risk-adjusted methods remain approximate. |
| Phase changes | Partial | Baseline, recalculation, target, intervention, step-change, `freeze_points`, `break_points`, `exclude_points` and `phases` metadata are available. | Validate exact qicharts phase/freeze/break semantics across every chart type. |
| NHS interpretation | Partial | Improvement/concern/neutral signal classification is available for supported XmR signals. | Add full narrative interpretation and validate against NHS examples. |
| Exports | Complete locally | PNG, Excel, PowerPoint and bundle tests pass. Excel exports now include signal schema and KPI sheets. | Add visual/content reference checks for every chart type. |
| Power BI | Complete locally | `powerbi_table(...)`, `spc_summary_table(...)`, `special_cause_summary_table(...)`, `signal_table(...)` and `kpi_table(...)` return DataFrames with versioned schemas. | Publish richer Power BI templates and schema examples. |
| API standardisation | Partial | `qic(...)`, `qic_table(...)`, `pareto_chart(...)` and `pareto_table(...)` are central; `paretochart(...)` remains as an alias. | Add deprecation warnings only if old names are ever scheduled for removal. |
| Documentation | Partial | User, statistical, validation, Power BI, Excel, NHS and migration guide stubs are included. | Expand every public API with full worked examples and reference-method notes. |
| Cross-package parity testing | Not complete | No R/qicharts/qicharts2/NHS comparison outputs are bundled. | Add reference outputs, generated outputs, difference reports and acceptance records. |
| Beyond-parity enhancements | Not started | Reporting and Office helpers exist. | Do not claim beyond-parity completion until parity phases are externally validated. |

## Definition Of Done Gap

The project should only be described as full qicharts/qicharts2/NHS parity when cross-package parity tests compare generated outputs with reference outputs for every supported chart type and no unexplained differences remain.

v1.1.0 does not meet that final definition. It is a stronger base for completing that work honestly.
