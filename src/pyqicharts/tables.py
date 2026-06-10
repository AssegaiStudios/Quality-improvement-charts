"""Excel, Power BI and dashboard-friendly tabular outputs."""
from __future__ import annotations
import numpy as np
import pandas as pd
from .nhs_rules import NhsRuleConfig, nhs_xmr_signals
from .rules import anhoej_rules

def _ordered_numeric(data: pd.DataFrame, x: str, y: str) -> pd.DataFrame:
    if x not in data.columns: raise KeyError(f"x column not found: {x!r}")
    if y not in data.columns: raise KeyError(f"y column not found: {y!r}")
    df = data[[x, y]].copy(); df[y] = pd.to_numeric(df[y], errors="coerce")
    return df.dropna(subset=[y]).reset_index(drop=True)

def _ordered_numeric_with_denominator(data: pd.DataFrame, x: str, y: str, denominator: str) -> pd.DataFrame:
    if denominator not in data.columns: raise KeyError(f"denominator column not found: {denominator!r}")
    if x not in data.columns: raise KeyError(f"x column not found: {x!r}")
    if y not in data.columns: raise KeyError(f"y column not found: {y!r}")
    df = data[[x, y, denominator]].copy()
    df[y] = pd.to_numeric(df[y], errors="coerce"); df[denominator] = pd.to_numeric(df[denominator], errors="coerce")
    df = df.dropna(subset=[y, denominator]); df = df[df[denominator] > 0]
    return df.reset_index(drop=True)

def _chart_key(chart: str) -> str:
    key = chart.lower().replace("-", "_").replace(" ", "_")
    return {"individuals":"i", "movingrange":"mr", "moving_range":"mr", "count":"c", "proportion":"p", "rate":"u"}.get(key, key)

def qic_table(
    data: pd.DataFrame,
    x: str,
    y: str,
    chart: str = "run",
    denominator: str | None = None,
    improvement: str | None = None,
    shift_points: int = 8,
    trend_points: int = 6,
) -> pd.DataFrame:
    """Return QI/SPC chart calculations as a pandas DataFrame.

    Version 0.4.0 supports run, I, MR, C, P and U charts. P and U charts
    require a denominator column. Individuals charts include NHS-style
    special cause fields for points outside limits, shifts and trends.
    """
    chart_key = _chart_key(chart)
    out = _ordered_numeric_with_denominator(data, x, y, denominator) if chart_key in {"p","u"} and denominator else _ordered_numeric(data, x, y)
    if chart_key in {"p","u"} and denominator is None: raise ValueError(f"chart={chart!r} requires a denominator column.")
    if chart_key not in {"run","i","mr","c","p","u"}: raise ValueError("v0.4.0 supports chart='run', 'i', 'mr', 'c', 'p', and 'u'.")
    out["chart"] = chart_key
    if chart_key == "run":
        rules = anhoej_rules(out[y]); out["plot_value"] = out[y]; out["centre"] = rules.median; out["centre_label"] = "Median"
        out["lcl"] = np.nan; out["ucl"] = np.nan; out["moving_range"] = np.nan; out["signal"] = False; out["signal_rule"] = ""
        out["anhoej_signal_long_run"] = rules.signal_long_run; out["anhoej_signal_few_crossings"] = rules.signal_few_crossings
        return out
    if chart_key == "i":
        values = out[y].astype(float); mr = values.diff().abs(); mrbar = float(mr.dropna().mean()) if len(mr.dropna()) else np.nan
        sigma = mrbar / 1.128 if mrbar == mrbar else np.nan; centre = float(values.mean()) if len(values) else np.nan
        lcl = centre - 3*sigma if sigma == sigma else np.nan; ucl = centre + 3*sigma if sigma == sigma else np.nan
        out["plot_value"] = values; out["centre"] = centre; out["centre_label"] = "Mean"; out["lcl"] = lcl; out["ucl"] = ucl
        nhs = nhs_xmr_signals(values, centre, lcl, ucl, improvement, NhsRuleConfig(shift_points, trend_points))
        out["moving_range"] = mr; out["signal"] = nhs["special_cause"].astype(bool); out["signal_rule"] = nhs["special_cause_rule"]
        out["mrbar"] = mrbar; out["sigma"] = sigma
        return pd.concat([out, nhs], axis=1)
    if chart_key == "mr":
        values = out[y].astype(float); mr = values.diff().abs(); mrbar = float(mr.dropna().mean()) if len(mr.dropna()) else np.nan
        ucl = 3.267 * mrbar if mrbar == mrbar else np.nan; signal = (mr > ucl) if mrbar == mrbar else pd.Series(False, index=out.index)
        out["moving_range"] = mr; out["plot_value"] = mr; out["centre"] = mrbar; out["centre_label"] = "Mean moving range"; out["lcl"] = 0.0; out["ucl"] = ucl
        out["signal"] = signal.fillna(False).astype(bool); out["signal_rule"] = np.where(out["signal"], "MR above UCL", ""); out["mrbar"] = mrbar; return out
    if chart_key == "c":
        counts = out[y].astype(float); centre = float(counts.mean()) if len(counts) else np.nan; sqrt_c = np.sqrt(centre) if centre == centre else np.nan
        lcl = max(0.0, centre - 3*sqrt_c) if sqrt_c == sqrt_c else np.nan; ucl = centre + 3*sqrt_c if sqrt_c == sqrt_c else np.nan
        signal = ((counts < lcl) | (counts > ucl)) if sqrt_c == sqrt_c else pd.Series(False, index=out.index)
        out["plot_value"] = counts; out["centre"] = centre; out["centre_label"] = "Mean count"; out["lcl"] = lcl; out["ucl"] = ucl
        out["moving_range"] = np.nan; out["signal"] = signal.astype(bool); out["signal_rule"] = np.where(out["signal"], "Outside C chart limits", ""); return out
    if chart_key == "p":
        events = out[y].astype(float); denom = out[denominator].astype(float); proportion = events / denom; pbar = float(events.sum()/denom.sum()) if denom.sum() > 0 else np.nan
        se = np.sqrt(pbar*(1-pbar)/denom) if pbar == pbar else np.nan; lcl = np.maximum(0, pbar - 3*se); ucl = np.minimum(1, pbar + 3*se); signal = (proportion < lcl) | (proportion > ucl)
        out["plot_value"] = proportion; out["centre"] = pbar; out["centre_label"] = "Mean proportion"; out["lcl"] = lcl; out["ucl"] = ucl
        out["moving_range"] = np.nan; out["signal"] = signal.astype(bool); out["signal_rule"] = np.where(out["signal"], "Outside P chart limits", ""); return out
    events = out[y].astype(float); denom = out[denominator].astype(float); rate = events / denom; ubar = float(events.sum()/denom.sum()) if denom.sum() > 0 else np.nan
    se = np.sqrt(ubar/denom) if ubar == ubar else np.nan; lcl = np.maximum(0, ubar - 3*se); ucl = ubar + 3*se; signal = (rate < lcl) | (rate > ucl)
    out["plot_value"] = rate; out["centre"] = ubar; out["centre_label"] = "Mean rate"; out["lcl"] = lcl; out["ucl"] = ucl
    out["moving_range"] = np.nan; out["signal"] = signal.astype(bool); out["signal_rule"] = np.where(out["signal"], "Outside U chart limits", ""); return out

def pareto_table(data: pd.DataFrame, category: str, count: str | None = None) -> pd.DataFrame:
    """Return Pareto calculations as a pandas DataFrame."""
    if category not in data.columns: raise KeyError(f"category column not found: {category!r}")
    if count is None:
        out = data[category].dropna().value_counts().rename_axis(category).reset_index(name="count")
    else:
        if count not in data.columns: raise KeyError(f"count column not found: {count!r}")
        out = data[[category, count]].dropna(subset=[category]).groupby(category, as_index=False)[count].sum().rename(columns={count:"count"}).sort_values("count", ascending=False).reset_index(drop=True)
    total = out["count"].sum(); out["percent"] = out["count"] / total * 100 if total else 0
    out["cumulative_count"] = out["count"].cumsum(); out["cumulative_percent"] = out["percent"].cumsum(); return out
