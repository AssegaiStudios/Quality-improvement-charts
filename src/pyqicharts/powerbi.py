"""Power BI-friendly table helpers."""
from __future__ import annotations

import pandas as pd


def powerbi_table(chart) -> pd.DataFrame:
    """Return chart rows as a Power BI-friendly DataFrame."""

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
