# pyqicharts v0.8.0 Release Notes

pyqicharts v0.8.0 adds risk-adjusted SPC charts using observed and expected values.

## Highlights

- P-prime chart support for risk-adjusted proportions.
- U-prime chart support for risk-adjusted rates.
- Observed, expected and observed/expected ratio fields.
- Approximate control limits that account for expected volume.
- Safe handling for zero expected values.
- Clear validation errors for missing or invalid expected columns.
- Synthetic observed/expected example datasets.

## New Public API

```python
from pyqicharts import (
    risk_adjusted_infection_rates,
    risk_adjusted_readmissions,
    qic,
)
```

## Examples

```python
df = risk_adjusted_readmissions()
chart = qic(
    data=df,
    x="month",
    y="observed",
    expected="expected",
    chart="p_prime",
)
```

```python
df = risk_adjusted_infection_rates()
chart = qic(
    data=df,
    x="month",
    y="observed",
    expected="expected",
    chart="u_prime",
)
```

## Compatibility

Existing calls to `qic(...)`, `qic_table(...)`, reporting helpers and Power BI helpers continue to work. v0.8 adds chart types and an optional `expected=` argument without changing existing return types.

## Not Included Yet

Full documentation, validation datasets, CI and packaging hardening remain planned for v0.9.
