# pyqicharts v1.1.0 Release Notes

pyqicharts v1.1.0 is a parity-readiness release.

## Added

- Nelson Rules 1-8 with metadata.
- Shewhart-compatible rule helper.
- Shared signal schema for reporting and Power BI.
- `rules=` configuration for chart tables.
- qicharts-style phase aliases and exclusion metadata.
- Power BI signal and KPI tables.
- Excel signal/KPI export sheets.
- Documentation stubs for user, statistical, NHS, Excel and qicharts2 migration guidance.

## Validation

The local test suite and coverage run pass. Cross-package qicharts/qicharts2/NHS parity is still not claimed because external reference outputs are not bundled.
