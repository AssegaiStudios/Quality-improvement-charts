# pyqicharts v0.8.0

This release adds risk-adjusted SPC charts.

## Added

- `chart="p_prime"` for observed-versus-expected proportions
- `chart="u_prime"` for observed-versus-expected rates
- `expected=` argument for risk-adjusted charts
- Observed/expected ratio calculations
- Zero expected value handling
- Risk-adjusted example datasets
- P-prime and U-prime chart examples

## Install

```bash
pip install pyqicharts
```

For reporting helpers:

```bash
pip install pyqicharts[reporting]
```

For local development from this source archive:

```bash
pip install -e .[dev]
pytest
```
