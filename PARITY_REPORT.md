# pyqicharts v1.3.4 Parity Report

## Status

v1.3.4 is a specification-complete, validation-enhanced parity candidate. It implements the documented Python-side feature set, adds targeted reviewer evidence, and keeps public APIs stable.

It should not be described as externally certified against live R `qicharts`, live R `qicharts2` or NHS workbook reference outputs until those external artifacts are bundled and compared in tests.

## Completed With Evidence

| Requirement Area | Evidence |
| --- | --- |
| Core chart families | Run, I, MR, C, P, U, Xbar, S, G, T, P-prime and U-prime chart tables and plots are implemented. |
| Run-chart methods | Anhøj, bestbox and cutbox methods are deterministic and tested. |
| NHS XmR interpretation | Direction-aware improvement/concern/neutral fields are available for Individuals/XmR signals. |
| Signal annotations | v1.3.4 plots signal annotations by default through `qic(..., annotate_signals=True)` and tests that annotation text renders. |
| Shewhart and Nelson rules | Nelson Rules 1-8 and Shewhart-compatible helpers return stable signal-schema rows. |
| Segment behaviour | Baselines, freeze points, breaks, recalculation points, phases and exclusions are table metadata and calculation inputs. v1.3.4 adds freeze-only tests. |
| Rare-event segmentation | v1.3.4 adds segmented G/T CSV fixtures and expected-output validation. |
| Risk-adjusted charts | P-prime and U-prime keep proportion and rate logic separate, handle denominators, and safely treat zero expected values. |
| Excluded-row cleanup | Excluded rows are retained for auditability but Boolean and text signal fields are cleared across supported chart families. |
| Reporting | PNG, Excel, PowerPoint, report bundle and Power BI helpers are implemented. |
| Public API | `qic()`, `qic_table()`, `pareto_chart()` and `pareto_table()` remain stable. Aliases are preserved. |
| Documentation | v1.3.4 expands the statistical reference, user guide, reporting guide, worked examples and statistical review. |
| Validation fixtures | Normal, process-change and edge-case fixture files exist for supported chart families; deterministic expected outputs are tested. |

## Remaining External Certification Work

The validation pack is internally deterministic, not externally published reference output. To close this evidence gap, a future release should add one or more of:

- committed qicharts/qicharts2 reference outputs generated from fixed R package versions;
- NHS workbook examples with permission to redistribute expected outputs;
- published textbook/example datasets with independently calculated expected values;
- a reproducible cross-package CI job that compares pyqicharts outputs with pinned external tools.

Until that work is complete, the honest release label remains: specification-complete, validation-enhanced parity candidate.
