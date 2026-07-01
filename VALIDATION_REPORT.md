# pyqicharts v1.3.4 Validation Report

## Test Evidence

- Repository test inventory: 136 `test_...` functions.
- `python -m pytest --cov=pyqicharts --cov=pyqicharts_excel --cov-report=term-missing`: 152 tests passing.
- Total coverage: 96.76%, passing the 95% gate.
- The v1.3.4 suite adds dedicated freeze-point isolation coverage.
- The v1.3.4 suite adds segmented G/T fixture validation with stored expected outputs.
- The v1.3.4 suite adds plotted signal-annotation coverage.
- Coverage remains governed by the 95% gate in `pyproject.toml`.

## Validation Assets

- `validation_data/inputs/` contains the original deterministic fixtures.
- `validation_data/expected_outputs/` contains expected outputs for those fixtures.
- `validation_data/expanded/` contains normal, process-change and edge-case examples.
- `validation_data/expanded_expected_outputs/` contains deterministic expected outputs for expanded examples.
- `validation_data/segmented_rare_event/` contains v1.3.4 G/T process-change fixtures and expected outputs.

## Methodology Notes

- Anhøj crossings use an exact `Binomial(n - 1, 0.5)` lower-tail threshold.
- Longest-run checks use the commonly cited logarithmic run-length threshold.
- bestbox/cutbox are deterministic centre-search methods because the published qicharts2 descriptions are experimental rather than a fixed closed-form standard.
- P-prime and U-prime use separate denominator-aware proportion/rate logic.
- Rare-event G and T charts use geometric/exponential tail approximations with non-negative interval validation.
- Segmented chart families use segment-specific centre lines and limits.

## Known Limitations

Current expected-output files are regression fixtures generated from the implementation. They are valuable for preventing accidental changes, but they are not externally published reference outputs.

Live cross-package certification against qicharts/qicharts2/NHS workbook outputs is not included in v1.3.4. That remains the main evidence gap for a future certification release.
