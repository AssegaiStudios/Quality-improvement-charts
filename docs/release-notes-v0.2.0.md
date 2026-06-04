# Release notes: v0.2.0

## Highlights

Version 0.2.0 expands pyqicharts from a first working proof of concept into a more useful early alpha package.

## Added

- Moving Range (MR) charts
- Table-first APIs:
  - `qic_table()`
  - `pareto_table()`
- Power BI example scripts
- Excel-friendly example script
- `QicResult.table`
- Signal rule labels
- Expanded README and documentation
- Additional tests

## Changed

- Improved I chart calculations
- Clearer package architecture separating calculation tables from plotting

## Known limitations

- Anhøj thresholds use an approximate implementation and need validation against published reference tables.
- Chart styling remains basic matplotlib.
- C, P, U, Xbar, S, T, G, P′ and U′ charts are not yet implemented.

## Recommended tag

`v0.2.0`
