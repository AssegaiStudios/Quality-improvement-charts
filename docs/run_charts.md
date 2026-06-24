# Run Charts

Run charts use the median as the centre line and include Anhoej-style run chart diagnostics.

```python
chart = qic(data=df, x="month", y="value", chart="run")
```

The calculated table includes run chart centre fields and Anhoej signal summary fields.
