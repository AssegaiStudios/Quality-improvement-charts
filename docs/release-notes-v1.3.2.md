# pyqicharts v1.3.2 Release Notes

v1.3.2 closes reviewer-raised documentation, exclusion-handling and packaging gaps.

## Fixed

- Excluded rows now clear `signal_rule` and related special-cause text fields consistently for MR, C, P, U, Xbar and S charts.
- Added regression tests proving excluded MR, C, P, U, Xbar and S rows clear signal text, not only Boolean signal flags.

## Documentation

- Updated `VALIDATION_REPORT.md` with current test-function count, passing test count and coverage evidence.
- Updated `API_STABILITY.md` status to v1.3.2.

## Packaging

- Declared `dist/` artifacts in `MANIFEST.in` for release-bundle consistency.
- The downloadable release bundle includes the v1.3.2 wheel and source distribution.

## Code Maintainability

- Added a shared `_clear_excluded_signal_fields(...)` helper with comments explaining why excluded output rows must clear both Boolean and text signal fields.

