# Worked Examples

These examples show the intended end-user flow: calculate a chart, inspect the table, and export or reuse the result.

## Individuals Chart With NHS Interpretation

```python
from pyqicharts import qic, sample_healthcare_qi_data

df = sample_healthcare_qi_data()
chart = qic(
    df,
    x="month",
    y="wait_time",
    chart="i",
    improvement="low is good",
    baseline_points=12,
    target=60,
)

chart.table[["month", "plot_value", "centre", "lcl", "ucl", "signal", "special_cause_label"]]
```

Use this when a healthcare team wants a Making Data Count-style view of waiting times, infection rates or other monthly indicators.

## Proportion Chart

```python
from pyqicharts import qic_table

rows = qic_table(
    data=df,
    x="month",
    y="missed_appointments",
    denominator="appointments",
    chart="p",
)
```

P charts use the total number of events divided by the total denominator to calculate the centre line, with row-specific limits for each denominator.

## Rare-Event G Chart

```python
from pyqicharts import infections_between_events, qic

df = infections_between_events()
chart = qic(df, "case_number", "cases_between_events", chart="g")
```

G charts are useful when improvement means longer intervals between events, such as cases between infections. Short intervals are usually adverse signals; long intervals may indicate improvement, but interpretation remains local to the measure.

## Time-Between T Chart

```python
from pyqicharts import days_between_serious_incidents, qic_table

df = days_between_serious_incidents()
rows = qic_table(df, "event_number", "days_between_events", chart="t")
```

T charts use already-calculated intervals. pyqicharts does not calculate calendar differences from event dates.

## Risk-Adjusted Chart

```python
from pyqicharts import qic

chart = qic(
    data=df,
    x="month",
    y="observed",
    expected="expected",
    denominator="patients",
    chart="p_prime",
)
```

Use P-prime for adjusted proportions and U-prime for adjusted rates. Zero expected values are handled safely as missing adjusted ratios.

## Pareto Table

```python
from pyqicharts import pareto_table

pareto = pareto_table(df, category="reason", count="count")
```

Pareto outputs are ordinary DataFrames with count, percent, cumulative count and cumulative percent columns.

## Export Bundle

```python
from pyqicharts import create_report_bundle

create_report_bundle([chart], output_dir="monthly_qi_report")
```

This writes chart images, an Excel workbook, a PowerPoint deck and metadata JSON in one folder.
