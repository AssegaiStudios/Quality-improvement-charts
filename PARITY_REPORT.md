# pyqicharts v1.2.1 Completion Report

## Status

v1.2.1 completes the final evidence-hardening pass requested for pyqicharts. The release implements the documented methodology in Python, adds deterministic validation tests, expands validation fixtures, and keeps a clear distinction between implemented specification parity and live cross-package output certification.

## Completed With Evidence

| Requirement Area | Evidence |
| --- | --- |
| Plain test execution | Conda-environment `pytest` and `python -m pytest` work from the checkout using `pythonpath = ["src"]` in `pyproject.toml`. |
| Anhøj rules | Approximate normal crossing logic removed. Exact binomial lower-tail crossing threshold, median tie removal, missing handling, exclusions, short-series behaviour and deterministic tests are included. |
| bestbox/cutbox | `method="anhoej"`, `method="bestbox"` and `method="cutbox"` are implemented and tested. The experimental qicharts2 methods are deterministic centre-search implementations; limitations are documented. |
| Shewhart and Nelson rules | Nelson Rules 1-8 and Shewhart-compatible rules return unified signal-schema DataFrames. Nelson calculations accept per-point centre/sigma values for segmented and variable-denominator charts. |
| Unified signal schema | `Signal`, `signals_to_frame(...)`, `signal_table(...)` and Power BI signal outputs include schema version, chart type, rule type, rule ID/name, direction, severity, start/end positions and message. |
| Xbar/S charts | Xbar and S charts now use subgroup-specific constants, variable subgroup sizes, recalculation segments, exclusions, targets and phase metadata. |
| P-prime/U-prime | P-prime uses risk-adjusted proportion logic when denominator is supplied. U-prime uses risk-adjusted rate/opportunity logic. Fallback O/E mode is labelled clearly. |
| G/T rare-event charts | Zero, missing, single-observation, repeated, extreme and invalid-negative cases are tested. |
| Process changes | `baseline_points`, `baseline_end`, `freeze`, `freeze_points`, `breaks`, `break_points`, `exclude`, `exclude_points`, `recalculate_after`, phases, interventions, step changes and targets are accepted additively. Excluded observations are removed from calculations. |
| MR/C/P/U recalculation | MR, C, P and U charts now calculate segment-specific centre lines and limits with exclusions. |
| NHS interpretation | `nhs_interpretation_table(...)` provides export-ready plain-English interpretation rows. Direction-aware XmR classification remains supported. |
| Pareto | `pareto_table(...)`, `pareto_chart(...)` and `paretochart(...)` remain implemented and tested. |
| Power BI | Chart data, SPC summary, signal, special-cause, NHS interpretation, KPI, phase, intervention and target tables include `schema_version`, `chart_id` and `chart_type`. |
| Exports | Excel exports include chart data, SPC summary, special causes, signal schema, KPI summary, NHS interpretation, phase metadata, interventions and targets. PNG tests cover every chart family. |
| Public API | `qic()`, `qic_table()`, `pareto_chart()` and `pareto_table()` are preferred; aliases are preserved. `CHART_ALIASES` and `VALID_CHARTS` are public. |
| Statistical review | `STATISTICAL_REVIEW.md` documents formulae, references, implementation notes and known deviations. |
| API stability | `API_STABILITY.md` lists stable APIs, aliases, deprecated APIs and planned removals. |
| Expanded validation data | `validation_data/expanded/` contains normal, process-change and edge-case fixture files for every chart family. `validation_data/expanded_expected_outputs/` contains deterministic expected outputs that are recalculated in tests. |

## Remaining External Certification Work

This release may be described as a specification-complete qicharts2 parity implementation. It does not claim byte-for-byte live R package equivalence or external published-reference-output certification. That would require bundling reference outputs from qicharts/qicharts2/NHS workbooks or published worked examples and comparing generated outputs against those artifacts.
