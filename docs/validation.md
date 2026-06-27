# Validation

The `validation/` folder contains small deterministic datasets and expected outputs used by the v0.9 test suite. These files are intended as regression fixtures, not a final external statistical validation pack.

The `validation_data/` folder contains interim v1.0 chart-by-chart inputs and expected outputs for run, I, MR, C, P, U, Xbar, S, G, T, P-prime and U-prime charts. The test suite checks that generated outputs match these bundled expected outputs.

These fixtures are internal regression evidence. They are not a substitute for external parity testing against qicharts, qicharts2, NHS examples, published Anhøj examples or independently reviewed SPC reference calculations.

See `PARITY_REPORT.md` for the current evidence status before using outputs for local governance or high-stakes operational decisions.
