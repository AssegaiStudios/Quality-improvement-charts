# Attribute Charts

Supported attribute charts are C, P and U charts. P and U charts require a denominator column.

```python
qic(data=df, x="month", y="events", denominator="denominator", chart="p")
qic(data=df, x="month", y="events", denominator="denominator", chart="u")
qic(data=df, x="month", y="count", chart="c")
```
