"""Power BI-friendly table helpers.

These helpers do not depend on Power BI APIs. They simply reshape chart result
objects into pandas DataFrames that can be returned from Power BI Python
visuals or exported to CSV.
"""
from __future__ import annotations

import pandas as pd

from .signals import SIGNAL_SCHEMA_VERSION, table_signals


def powerbi_table(chart) -> pd.DataFrame:
    """Return all calculated chart rows plus chart metadata columns."""

    out = chart.table.copy()
    out["chart_type"] = chart.chart
    out["measure"] = chart.y
    return out


def spc_summary_table(chart) -> pd.DataFrame:
    """Return one-row SPC summary fields as a DataFrame."""

    return pd.DataFrame(
        [
            {
                "chart": chart.chart,
                "x": chart.x,
                "y": chart.y,
                "centre_label": chart.centre_label,
                "centre": chart.centre,
                "lcl": chart.lcl,
                "ucl": chart.ucl,
                "rows": len(chart.table),
                "signals": int(chart.signals.sum()),
                "segments": int(chart.table["segment_id"].nunique()) if "segment_id" in chart.table else 1,
            }
        ]
    )


def special_cause_summary_table(chart) -> pd.DataFrame:
    """Return rows with detected special causes as a DataFrame."""

    table = chart.table.copy()
    if "special_cause" in table:
        out = table[table["special_cause"]].copy()
    else:
        out = table[table["signal"]].copy()
    if out.empty:
        return pd.DataFrame(
            columns=[
                chart.x,
                chart.y,
                "plot_value",
                "signal_rule",
                "special_cause_type",
                "special_cause_direction",
            ]
        )
    # Keep only columns that exist for the chart type. This allows one helper
    # to serve XmR, rare-event, risk-adjusted and attribute charts.
    columns = [
        col
        for col in [
            chart.x,
            chart.y,
            "plot_value",
            "signal_rule",
            "special_cause_rule",
            "special_cause_type",
            "special_cause_direction",
            "segment_id",
            "baseline_period",
        ]
        if col in out.columns
    ]
    return out[columns].reset_index(drop=True)


def signal_table(chart) -> pd.DataFrame:
    """Return detected chart signals using the stable v1.1 schema."""

    return table_signals(chart.table, chart.chart, chart.x)


def kpi_table(chart) -> pd.DataFrame:
    """Return one-row KPI fields for Power BI and dashboard datasets."""

    table = chart.table.copy()
    latest = table.iloc[-1] if len(table) else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            {
                "schema_version": SIGNAL_SCHEMA_VERSION,
                "chart_type": chart.chart,
                "measure": chart.y,
                "rows": len(table),
                "centre": chart.centre,
                "lcl": chart.lcl,
                "ucl": chart.ucl,
                "signal_count": int(chart.signals.sum()),
                "latest_x": latest.get(chart.x, None),
                "latest_value": latest.get("plot_value", None),
                "latest_signal": bool(latest.get("signal", False)) if len(table) else False,
            }
        ]
    )
