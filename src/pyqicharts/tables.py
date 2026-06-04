"""Excel, Power BI, and dashboard-friendly tabular outputs."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .rules import anhoej_rules


def _ordered_numeric(data: pd.DataFrame, x: str, y: str) -> pd.DataFrame:
    if x not in data.columns:
        raise KeyError(f"x column not found: {x!r}")
    if y not in data.columns:
        raise KeyError(f"y column not found: {y!r}")
    df = data[[x, y]].copy()
    df[y] = pd.to_numeric(df[y], errors="coerce")
    df = df.dropna(subset=[y])
    return df.reset_index(drop=True)


def qic_table(data: pd.DataFrame, x: str, y: str, chart: str = "run") -> pd.DataFrame:
    """Return chart calculations as a pandas DataFrame.

    This function is intentionally designed for tools that prefer table
    outputs, including Excel Python, Excel Desktop integrations, Power BI,
    dashboards and reporting pipelines.

    Supported chart values in v0.2.0:
    - "run"
    - "i" / "individuals"
    - "mr" / "moving_range"
    """

    chart_key = chart.lower().replace("-", "_").replace(" ", "_")
    df = _ordered_numeric(data, x, y)

    if chart_key == "individuals":
        chart_key = "i"
    if chart_key in {"movingrange", "moving_range"}:
        chart_key = "mr"

    if chart_key not in {"run", "i", "mr"}:
        raise ValueError("v0.2.0 supports chart='run', chart='i', and chart='mr'.")

    out = df.copy()
    out["chart"] = chart_key

    if chart_key == "run":
        rules = anhoej_rules(out[y])
        out["centre"] = rules.median
        out["lcl"] = np.nan
        out["ucl"] = np.nan
        out["moving_range"] = np.nan
        out["signal"] = False
        out["signal_rule"] = ""
        out["anhoej_signal_long_run"] = rules.signal_long_run
        out["anhoej_signal_few_crossings"] = rules.signal_few_crossings
        return out

    if chart_key == "i":
        values = out[y].astype(float)
        mr = values.diff().abs()
        mrbar = float(mr.dropna().mean()) if len(mr.dropna()) else np.nan
        sigma = mrbar / 1.128 if mrbar == mrbar else np.nan
        centre = float(values.mean()) if len(values) else np.nan
        lcl = centre - 3 * sigma if sigma == sigma else np.nan
        ucl = centre + 3 * sigma if sigma == sigma else np.nan
        signal = (values < lcl) | (values > ucl) if sigma == sigma else pd.Series(False, index=out.index)

        out["centre"] = centre
        out["lcl"] = lcl
        out["ucl"] = ucl
        out["moving_range"] = mr
        out["signal"] = signal.astype(bool)
        out["signal_rule"] = np.where(out["signal"], "Shewhart 3-sigma", "")
        out["mrbar"] = mrbar
        out["sigma"] = sigma
        return out

    # MR chart
    values = out[y].astype(float)
    mr = values.diff().abs()
    mrbar = float(mr.dropna().mean()) if len(mr.dropna()) else np.nan
    centre = mrbar
    lcl = 0.0
    ucl = 3.267 * mrbar if mrbar == mrbar else np.nan
    signal = (mr > ucl) if mrbar == mrbar else pd.Series(False, index=out.index)

    out["moving_range"] = mr
    out["centre"] = centre
    out["lcl"] = lcl
    out["ucl"] = ucl
    out["signal"] = signal.fillna(False).astype(bool)
    out["signal_rule"] = np.where(out["signal"], "MR above UCL", "")
    out["mrbar"] = mrbar
    return out


def pareto_table(data: pd.DataFrame, category: str, count: str | None = None) -> pd.DataFrame:
    """Return Pareto calculations as a pandas DataFrame."""

    if category not in data.columns:
        raise KeyError(f"category column not found: {category!r}")

    if count is None:
        out = (
            data[category]
            .dropna()
            .value_counts()
            .rename_axis(category)
            .reset_index(name="count")
        )
    else:
        if count not in data.columns:
            raise KeyError(f"count column not found: {count!r}")
        out = (
            data[[category, count]]
            .dropna(subset=[category])
            .groupby(category, as_index=False)[count]
            .sum()
            .rename(columns={count: "count"})
            .sort_values("count", ascending=False)
            .reset_index(drop=True)
        )

    total = out["count"].sum()
    out["percent"] = out["count"] / total * 100 if total else 0
    out["cumulative_count"] = out["count"].cumsum()
    out["cumulative_percent"] = out["percent"].cumsum()
    return out
