# Risk-Adjusted Charts

P-prime and U-prime charts use observed and expected values. The plotted value is the observed/expected ratio.

```python
chart = qic(data=df, x="month", y="observed", expected="expected", chart="p_prime")
chart = qic(data=df, x="month", y="observed", expected="expected", chart="u_prime")
```

Rows with zero expected values are retained with missing adjusted values and `expected_zero=True`.
