# Risk-Adjusted SPC

pyqicharts supports P-prime and U-prime charts for externally supplied observed and expected values.

## P-prime

Use P-prime when the measure is a risk-adjusted proportion.

```python
from pyqicharts import qic_table

table = qic_table(
    data=df,
    x="month",
    y="observed",
    expected="expected",
    denominator="eligible_patients",
    chart="p_prime",
)
```

Worked example:

Observed events are divided by expected events to create O/E. When a denominator is supplied, pyqicharts scales O/E by the segment observed proportion. Limits use binomial-style standard error from expected probability and denominator.

## U-prime

Use U-prime when the measure is a risk-adjusted rate per opportunity.

```python
table = qic_table(
    data=df,
    x="month",
    y="observed",
    expected="expected",
    denominator="bed_days",
    chart="u_prime",
)
```

Worked example:

Observed events are divided by expected events to create O/E. When opportunities are supplied, pyqicharts scales O/E by the segment observed rate. Limits use a Poisson-style standard error based on expected counts.

## Zero Expected Values

Zero expected values produce missing O/E values rather than division errors. They are flagged in the `expected_zero` column.

## Limitation

pyqicharts does not fit risk models. Expected values must be supplied from an external validated model.
