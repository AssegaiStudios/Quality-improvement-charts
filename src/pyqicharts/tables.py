"""Excel, Power BI and dashboard-friendly tabular outputs."""
from __future__ import annotations
import numpy as np
import pandas as pd
from .nhs_rules import NhsRuleConfig, nhs_xmr_signals
from .rules import anhoej_rules


def _point_to_position(point, x_values: pd.Series, n: int) -> int | None:
    matches = x_values[x_values == point]
    if len(matches):
        return int(matches.index[0])
    if isinstance(point, (int, np.integer)) and 1 <= int(point) <= n:
        return int(point) - 1
    return None


def _segment_ids(out: pd.DataFrame, x: str, recalculation_points: list | None) -> pd.Series:
    n = len(out)
    starts = [0]
    for point in recalculation_points or []:
        pos = _point_to_position(point, out[x], n)
        if pos is not None and 0 < pos < n:
            starts.append(pos)
    starts = sorted(set(starts))
    segment = pd.Series(1, index=out.index, dtype=int)
    for segment_id, start in enumerate(starts, start=1):
        end = starts[segment_id] if segment_id < len(starts) else n
        segment.iloc[start:end] = segment_id
    return segment


def _marker_labels(out: pd.DataFrame, x: str, markers: list[dict] | None) -> pd.Series:
    labels = pd.Series("", index=out.index, dtype=object)
    n = len(out)
    for marker in markers or []:
        point = marker.get("point") if isinstance(marker, dict) else None
        pos = _point_to_position(point, out[x], n)
        if pos is None:
            continue
        labels.iloc[pos] = str(marker.get("label", "")) if isinstance(marker, dict) else ""
    return labels


def _add_process_metadata(
    out: pd.DataFrame,
    x: str,
    baseline_points: int | None,
    recalculation_points: list | None,
    target: float | int | None,
    interventions: list[dict] | None,
    step_changes: list[dict] | None,
) -> pd.DataFrame:
    out["point_index"] = np.arange(1, len(out) + 1)
    out["baseline_period"] = out["point_index"] <= int(baseline_points) if baseline_points else False
    out["baseline_label"] = np.where(out["baseline_period"], "Baseline", "")
    out["segment_id"] = _segment_ids(out, x, recalculation_points)
    out["segment_label"] = "Segment " + out["segment_id"].astype(str)
    out["target"] = target if target is not None else np.nan
    out["intervention_label"] = _marker_labels(out, x, interventions)
    out["intervention"] = out["intervention_label"] != ""
    out["step_change_label"] = _marker_labels(out, x, step_changes)
    out["step_change"] = out["step_change_label"] != ""
    return out


def _segment_source(values: pd.Series, segment_index: pd.Index, baseline_points: int | None) -> pd.Series:
    segment_values = values.loc[segment_index]
    if baseline_points and int(segment_index[0]) == 0:
        return segment_values.iloc[: int(baseline_points)]
    return segment_values

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
    baseline_points: int | None = None,
    recalculation_points: list | None = None,
    target: float | int | None = None,
    interventions: list[dict] | None = None,
    step_changes: list[dict] | None = None,
) -> pd.DataFrame:
    """Return QI/SPC chart calculations as a pandas DataFrame.

    Version 0.6.0 supports run, I, MR, C, P and U charts. P and U charts
    require a denominator column. Individuals charts include NHS-style
    special cause fields for points outside limits, shifts and trends.
    Baseline periods, recalculation segments, targets, interventions and
    step changes are represented as additive table fields.
    """
    chart_key = _chart_key(chart)
    out = _ordered_numeric_with_denominator(data, x, y, denominator) if chart_key in {"p","u"} and denominator else _ordered_numeric(data, x, y)
    if chart_key in {"p","u"} and denominator is None: raise ValueError(f"chart={chart!r} requires a denominator column.")
    if chart_key not in {"run","i","mr","c","p","u"}: raise ValueError("v0.6.0 supports chart='run', 'i', 'mr', 'c', 'p', and 'u'.")
    out["chart"] = chart_key
    out = _add_process_metadata(out, x, baseline_points, recalculation_points, target, interventions, step_changes)
    if chart_key == "run":
        centre_source = out[y].iloc[: int(baseline_points)] if baseline_points else out[y]
        rules = anhoej_rules(centre_source); out["plot_value"] = out[y]; out["centre"] = rules.median; out["centre_label"] = "Median"
        out["lcl"] = np.nan; out["ucl"] = np.nan; out["moving_range"] = np.nan; out["signal"] = False; out["signal_rule"] = ""
        out["anhoej_signal_long_run"] = rules.signal_long_run; out["anhoej_signal_few_crossings"] = rules.signal_few_crossings
        return out
    if chart_key == "i":
        values = out[y].astype(float); mr = values.diff().abs()
        out["plot_value"] = values; out["centre"] = np.nan; out["centre_label"] = "Mean"; out["lcl"] = np.nan; out["ucl"] = np.nan
        out["moving_range"] = mr; out["mrbar"] = np.nan; out["sigma"] = np.nan
        for _, group in out.groupby("segment_id", sort=True):
            source = _segment_source(values, group.index, baseline_points)
            segment_mr = source.diff().abs()
            mrbar = float(segment_mr.dropna().mean()) if len(segment_mr.dropna()) else np.nan
            sigma = mrbar / 1.128 if mrbar == mrbar else np.nan
            centre = float(source.mean()) if len(source) else np.nan
            lcl = centre - 3 * sigma if sigma == sigma else np.nan
            ucl = centre + 3 * sigma if sigma == sigma else np.nan
            out.loc[group.index, "centre"] = centre
            out.loc[group.index, "lcl"] = lcl
            out.loc[group.index, "ucl"] = ucl
            out.loc[group.index, "mrbar"] = mrbar
            out.loc[group.index, "sigma"] = sigma
        nhs = nhs_xmr_signals(values, out["centre"], out["lcl"], out["ucl"], improvement, NhsRuleConfig(shift_points, trend_points))
        out["signal"] = nhs["special_cause"].astype(bool); out["signal_rule"] = nhs["special_cause_rule"]
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
