"""Power BI-friendly table helpers with stable schemas."""
from __future__ import annotations

import pandas as pd

from .signals import SIGNAL_SCHEMA_VERSION, table_signals


def _chart_id(chart) -> str:
    return f"{chart.chart}:{chart.y}"


def _with_schema(chart, table: pd.DataFrame) -> pd.DataFrame:
    out = table.copy()
    out.insert(0, "chart_type", chart.chart)
    out.insert(0, "chart_id", _chart_id(chart))
    out.insert(0, "schema_version", SIGNAL_SCHEMA_VERSION)
    return out


def powerbi_table(chart) -> pd.DataFrame:
    """Return all calculated chart rows plus schema metadata."""

    out = chart.table.copy()
    out["measure"] = chart.y
    return _with_schema(chart, out)


def spc_summary_table(chart) -> pd.DataFrame:
    """Return one-row SPC summary fields as a DataFrame."""

    table = pd.DataFrame(
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
    return _with_schema(chart, table)


def special_cause_summary_table(chart) -> pd.DataFrame:
    """Return rows with detected special causes as a DataFrame."""

    table = chart.table.copy()
    signal_col = "special_cause" if "special_cause" in table else "signal"
    out = table[table[signal_col].fillna(False).astype(bool)].copy() if signal_col in table else table.iloc[0:0].copy()
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
    return _with_schema(chart, out[columns].reset_index(drop=True) if columns else pd.DataFrame())


def signal_table(chart) -> pd.DataFrame:
    """Return detected chart signals using the stable signal schema."""

    out = table_signals(chart.table, chart.chart, chart.x)
    if out.empty:
        out = pd.DataFrame(columns=["schema_version", "chart_type"])
    out["chart_id"] = _chart_id(chart)
    columns = ["schema_version", "chart_id", "chart_type"] + [c for c in out.columns if c not in {"schema_version", "chart_id", "chart_type"}]
    return out[columns]


def kpi_table(chart) -> pd.DataFrame:
    """Return one-row KPI fields for Power BI and dashboard datasets."""

    table = chart.table.copy()
    latest = table.iloc[-1] if len(table) else pd.Series(dtype=object)
    out = pd.DataFrame(
        [
            {
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
    return _with_schema(chart, out)


def nhs_interpretation_table(chart) -> pd.DataFrame:
    """Return plain-English interpretation rows for reporting."""

    signals = signal_table(chart)
    if signals.empty or len(signals.columns) <= 3:
        text = "This chart shows no detected special cause signal."
        signal_type = "neutral"
    else:
        signal_type = str(signals["signal_type"].replace("", "neutral").iloc[0])
        text = f"This chart demonstrates a special cause {signal_type}."
    return _with_schema(chart, pd.DataFrame([{"interpretation_type": signal_type, "interpretation": text}]))


def phase_metadata_table(chart) -> pd.DataFrame:
    table = chart.table.copy()
    cols = [c for c in [chart.x, "segment_id", "segment_label", "phase_label", "baseline_period"] if c in table]
    return _with_schema(chart, table[cols].drop_duplicates().reset_index(drop=True) if cols else pd.DataFrame())


def intervention_metadata_table(chart) -> pd.DataFrame:
    table = chart.table.copy()
    cols = [c for c in [chart.x, "intervention", "intervention_label", "step_change", "step_change_label"] if c in table]
    out = table[cols] if cols else pd.DataFrame()
    if "intervention" in out:
        out = out[out[["intervention", "step_change"]].any(axis=1)]
    return _with_schema(chart, out.reset_index(drop=True))


def target_metadata_table(chart) -> pd.DataFrame:
    table = chart.table.copy()
    cols = [c for c in [chart.x, "target"] if c in table]
    out = table[cols].dropna(subset=["target"]).drop_duplicates().reset_index(drop=True) if "target" in cols else pd.DataFrame()
    return _with_schema(chart, out)
