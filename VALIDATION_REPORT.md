# pyqicharts v1.3.2 Validation Report

## Test Evidence

- Repository test inventory: 109 `test_...` functions.
- Plain conda-environment `pytest`: 125 tests passing.
- `python -m pytest`: 125 tests passing.
- `pytest --cov=pyqicharts --cov=pyqicharts_excel --cov-report=term-missing`: 90.70% total coverage, passing the 90% gate.
- Validation fixtures cover run, I, MR, C, P, U, Xbar, S, G, T, P-prime and U-prime outputs.
- v1.3.2 tests include deterministic checks for Anhoej edge cases, bestbox/cutbox methods, segmented Nelson calculations, distinct P-prime/U-prime logic, Xbar/S process metadata, Power BI schemas, Excel workbook contents, rare-event edge cases and excluded-row signal-rule clearance across MR, C, P, U, Xbar/S, G, T, P-prime and U-prime charts.

## Methodology Notes

- Anhoej crossings use exact Binomial(n-1, 0.5) lower-tail thresholds.
- Longest-run limits use the published Schilling-style logarithmic rule commonly used in Anhoej run chart guidance.
- bestbox/cutbox are documented by qicharts2 as experimental. This implementation uses deterministic candidate-centre search; cutbox trims one low and one high value before centre search when at least five observations exist.
- P-prime and U-prime use denominator-aware risk-adjusted proportion/rate logic when denominators are supplied. When denominators are absent, outputs are explicitly labelled as observed/expected fallback charts.
- Rare-event G and T charts use geometric/exponential tail approximations with non-negative interval validation.

## Known Limitations

Expanded validation fixtures include deterministic expected-output files in `validation_data/expanded_expected_outputs/`, and tests recalculate each fixture before comparing outputs. These files improve regression evidence for every normal, process-change and edge-case fixture.

Live cross-package certification against qicharts/qicharts2/NHS workbook outputs is not included because the request explicitly excluded a live R execution environment. Published-reference validation artifacts remain a separate evidence task: the current deterministic expected outputs are not presented as externally published reference outputs.
