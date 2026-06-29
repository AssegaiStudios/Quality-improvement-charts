# pyqicharts v1.3.1 Release Notes

v1.3.1 is a reviewer-fix release for the Excel Companion and validation pack.

## Fixed

- Excluded observations now suppress `signal` and `special_cause` fields for G, T, P-prime and U-prime charts.
- Added regression tests proving exclusions suppress rare-event and risk-adjusted signals.

## Added

- Added deterministic expected-output CSVs for every expanded validation fixture.
- Expanded fixture tests now recalculate outputs and compare them to expected files.
- Added worked documentation for `nhs_interpretation_table(chart)`.
- Final downloadable archive includes built wheel and source distribution artifacts in `dist/`.

## Validation Note

The expanded expected-output files are deterministic regression artifacts generated from the implemented methods. They are useful for change detection but are not a substitute for external published-reference validation datasets.

