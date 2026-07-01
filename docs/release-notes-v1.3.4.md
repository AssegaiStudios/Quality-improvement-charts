# pyqicharts v1.3.4 Release Notes

v1.3.4 is a validation and documentation hardening release.

## Added

- Signal annotations on plotted charts through `qic(..., annotate_signals=True)`.
- Tests proving signal annotations render and can be disabled.
- Dedicated freeze-point tests independent of breaks/recalculation points.
- Segmented G/T validation fixtures with stored expected outputs.
- A narrative worked-examples guide.

## Changed

- Expanded `docs/statistical_reference.md` from a stub into chart-by-chart methodology notes.
- Expanded `docs/user_guide.md` and `docs/reporting.md`.
- Rebuilt `STATISTICAL_REVIEW.md` with formula verification, implementation notes and known deviations.
- Updated parity and validation reports to describe the remaining external certification gap accurately.

## Compatibility

Existing `qic(...)`, `qic_table(...)`, `pareto_chart(...)` and `pareto_table(...)` calls continue to work. `annotate_signals` is additive and defaults to `True`.
