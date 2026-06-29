"""Table-first SPC calculations used by charting, exports and dashboards.

The public plotting API delegates here first. Keeping calculations in this
module means every downstream surface (matplotlib, Excel, Power BI and tests)
uses the same values and column names.
"""
from __future__ import annotations
import math
import numpy as np
import pandas as pd
from .nelson import nelson_rule_signals, shewhart_rule_signals
from .nhs_rules import NhsRuleConfig, nhs_xmr_signals
from .rules import anhoej_rules

CHART_ALIASES = {
    "individuals": "i",
    "individual": "i",
    "movingrange": "mr",
    "moving_range": "mr",
    "count": "c",
    "proportion": "p",
    "rate": "u",
    "rare_event": "g",
    "time_between": "t",
    "p'": "p_prime",
    "pprime": "p_prime",
    "u'": "u_prime",
    "uprime": "u_prime",
    "x_bar": "xbar",
    "x-bar": "xbar",
}
VALID_CHARTS = {"run", "i", "mr", "c", "p", "u", "xbar", "s", "g", "t", "p_prime", "u_prime"}


def _point_to_position(point, x_values: pd.Series, n: int) -> int | None:
    """Resolve a marker point from either x-axis value or 1-based row number."""
    matches = x_values[x_values == point]
    if len(matches):
        return int(matches.index[0])
    if isinstance(point, (int, np.integer)) and 1 <= int(point) <= n:
        return int(point) - 1
    return None


def _segment_ids(out: pd.DataFrame, x: str, recalculation_points: list | None) -> pd.Series:
    """Create stable segment IDs for process recalculation periods."""
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
    """Return marker labels aligned to the calculated table rows."""
    labels = pd.Series("", index=out.index, dtype=object)
    n = len(out)
    for marker in markers or []:
        point = marker.get("point") if isinstance(marker, dict) else None
        pos = _point_to_position(point, out[x], n)
        if pos is None:
            continue
        labels.iloc[pos] = str(marker.get("label", "")) if isinstance(marker, dict) else ""
    return labels


def _point_flags(out: pd.DataFrame, x: str, points: list | None) -> pd.Series:
    """Return booleans for rows addressed by x value or 1-based row number."""

    flags = pd.Series(False, index=out.index)
    n = len(out)
    for point in points or []:
        pos = _point_to_position(point, out[x], n)
        if pos is not None:
            flags.iloc[pos] = True
    return flags


def _phase_labels(out: pd.DataFrame, x: str, phases: list[dict] | None) -> pd.Series:
    """Create qicharts-style phase labels from ordered phase start markers."""

    labels = pd.Series("", index=out.index, dtype=object)
    if not phases:
        return labels
    starts: list[tuple[int, str]] = []
    for phase in phases:
        if not isinstance(phase, dict):
            continue
        point = phase.get("start", phase.get("point"))
        pos = _point_to_position(point, out[x], len(out))
        if pos is not None:
            starts.append((pos, str(phase.get("label", f"Phase {len(starts) + 1}"))))
    starts = sorted(starts)
    for index, (start, label) in enumerate(starts):
        end = starts[index + 1][0] if index + 1 < len(starts) else len(out)
        labels.iloc[start:end] = label
    return labels


def _add_process_metadata(
    out: pd.DataFrame,
    x: str,
    baseline_points: int | None,
    recalculation_points: list | None,
    target: float | int | None,
    interventions: list[dict] | None,
    step_changes: list[dict] | None,
    exclude_points: list | None = None,
    phases: list[dict] | None = None,
) -> pd.DataFrame:
    """Add process-context columns used across all chart tables."""
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
    out["excluded"] = _point_flags(out, x, exclude_points)
    out["phase_label"] = _phase_labels(out, x, phases)
    return out


def _segment_source(values: pd.Series, segment_index: pd.Index, baseline_points: int | None, excluded: pd.Series | None = None) -> pd.Series:
    """Choose the rows used to calculate a segment's centre and limits."""
    segment_values = values.loc[segment_index]
    if baseline_points and int(segment_index[0]) == 0:
        segment_values = segment_values.iloc[: int(baseline_points)]
    if excluded is not None:
        segment_values = segment_values[~excluded.loc[segment_values.index].astype(bool)]
    return segment_values


def _normalise_rules(rules: str | None) -> str | None:
    """Normalise configurable rule-set names."""

    if rules is None:
        return None
    key = str(rules).strip().lower()
    if key in {"none", "off", ""}:
        return None
    if key not in {"nelson", "shewhart", "all"}:
        raise ValueError("rules must be one of None, 'nelson', 'shewhart', or 'all'.")
    return key


def _add_rule_metadata(out: pd.DataFrame, x: str, chart_key: str, rules: str | None) -> pd.DataFrame:
    """Attach summary counts for configured Nelson/Shewhart rule sets."""

    out["signal_count"] = out["signal"].fillna(False).astype(bool).astype(int) if "signal" in out else 0
    out["rule_set"] = rules or ""
    if not rules or "plot_value" not in out or "centre" not in out or "sigma" not in out:
        return out
    frames = []
    for _, group in out.groupby("segment_id" if "segment_id" in out else pd.Series(1, index=out.index), sort=True):
        values = pd.to_numeric(group["plot_value"], errors="coerce")
        centres = pd.to_numeric(group["centre"], errors="coerce")
        sigmas = pd.to_numeric(group["sigma"], errors="coerce")
        if sigmas.dropna().empty or centres.dropna().empty:
            continue
        if rules in {"nelson", "all"}:
            frames.append(nelson_rule_signals(values, centre=centres, sigma=sigmas, chart_type=chart_key, x_values=group[x]))
        if rules in {"shewhart", "all"}:
            frames.append(shewhart_rule_signals(values, centre=centres, sigma=sigmas, chart_type=chart_key, x_values=group[x]))
    if frames:
        detected = pd.concat(frames, ignore_index=True)
        out["signal_count"] = out["signal_count"] + 0
        for _, signal in detected.iterrows():
            start = int(signal["start_index"]) - 1
            end = int(signal["end_index"]) - 1
            out.loc[start:end, "signal_count"] = out.loc[start:end, "signal_count"] + 1
    return out

def _ordered_numeric(data: pd.DataFrame, x: str, y: str) -> pd.DataFrame:
    """Return x/y rows with y coerced to numeric and missing y removed."""
    if x not in data.columns: raise KeyError(f"x column not found: {x!r}")
    if y not in data.columns: raise KeyError(f"y column not found: {y!r}")
    df = data[[x, y]].copy(); df[y] = pd.to_numeric(df[y], errors="coerce")
    return df.dropna(subset=[y]).reset_index(drop=True)

def _ordered_numeric_with_denominator(data: pd.DataFrame, x: str, y: str, denominator: str) -> pd.DataFrame:
    """Return x/y/denominator rows for P and U charts."""
    if denominator not in data.columns: raise KeyError(f"denominator column not found: {denominator!r}")
    if x not in data.columns: raise KeyError(f"x column not found: {x!r}")
    if y not in data.columns: raise KeyError(f"y column not found: {y!r}")
    df = data[[x, y, denominator]].copy()
    df[y] = pd.to_numeric(df[y], errors="coerce"); df[denominator] = pd.to_numeric(df[denominator], errors="coerce")
    df = df.dropna(subset=[y, denominator]); df = df[df[denominator] > 0]
    return df.reset_index(drop=True)


def _ordered_numeric_with_expected(data: pd.DataFrame, x: str, y: str, expected: str) -> pd.DataFrame:
    """Return x/y/expected rows for risk-adjusted charts."""
    if expected not in data.columns: raise KeyError(f"expected column not found: {expected!r}")
    if x not in data.columns: raise KeyError(f"x column not found: {x!r}")
    if y not in data.columns: raise KeyError(f"y column not found: {y!r}")
    df = data[[x, y, expected]].copy()
    df[y] = pd.to_numeric(df[y], errors="coerce"); df[expected] = pd.to_numeric(df[expected], errors="coerce")
    return df.dropna(subset=[y, expected]).reset_index(drop=True)


def _ordered_numeric_with_expected_and_optional_denominator(data: pd.DataFrame, x: str, y: str, expected: str, denominator: str | None) -> pd.DataFrame:
    """Return observed/expected rows and include denominator when supplied."""

    columns = [x, y, expected] + ([denominator] if denominator else [])
    if expected not in data.columns:
        raise KeyError(f"expected column not found: {expected!r}")
    for column in columns:
        if column not in data.columns:
            raise KeyError(f"column not found: {column!r}")
    df = data[columns].copy()
    for column in [y, expected] + ([denominator] if denominator else []):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    required = [y, expected] + ([denominator] if denominator else [])
    df = df.dropna(subset=required)
    if denominator:
        df = df[df[denominator] > 0]
    return df.reset_index(drop=True)

def _chart_key(chart: str) -> str:
    """Normalise public chart aliases to internal chart keys."""
    key = chart.lower().replace("-", "_").replace(" ", "_")
    return CHART_ALIASES.get(key, key)


def _validate_non_negative(values: pd.Series, chart_key: str) -> None:
    """Reject impossible negative intervals for rare-event charts."""
    if (values < 0).any():
        label = "G" if chart_key == "g" else "T"
        raise ValueError(f"{label} chart intervals must be non-negative.")


def _rare_event_fields(out: pd.DataFrame, y: str, chart_key: str) -> pd.DataFrame:
    """Calculate G and T chart fields using lightweight distribution limits."""
    values = out[y].astype(float)
    _validate_non_negative(values, chart_key)
    out["plot_value"] = values
    out["centre"] = np.nan
    out["moving_range"] = np.nan
    out["rare_event_mean"] = np.nan
    out["lcl"] = np.nan
    out["ucl"] = np.nan
    out["rare_event_probability"] = np.nan
    out["centre_label"] = "Mean cases between events" if chart_key == "g" else "Mean time between events"

    for _, group in out.groupby("segment_id", sort=True):
        active = group.index[~out.loc[group.index, "excluded"].astype(bool)] if "excluded" in out else group.index
        segment_values = values.loc[active]
        centre = float(segment_values.mean()) if len(segment_values) else np.nan
        if chart_key == "g":
            p = 1 / (centre + 1) if centre == centre and centre >= 0 else np.nan
            if p == p and 0 < p < 1:
                lcl = max(0.0, np.log(0.99865) / np.log(1 - p) - 1)
                ucl = max(0.0, np.log(0.00135) / np.log(1 - p) - 1)
            else:
                lcl = np.nan
                ucl = np.nan
            out.loc[group.index, "rare_event_probability"] = p
        else:
            if centre == centre and centre > 0:
                lcl = -centre * np.log(0.99865)
                ucl = -centre * np.log(0.00135)
            else:
                lcl = np.nan
                ucl = np.nan
        out.loc[group.index, "centre"] = centre
        out.loc[group.index, "rare_event_mean"] = centre
        out.loc[group.index, "lcl"] = lcl
        out.loc[group.index, "ucl"] = ucl
    out["outside_lcl"] = (values < out["lcl"]).fillna(False)
    out["outside_ucl"] = (values > out["ucl"]).fillna(False)
    out["signal"] = (out["outside_lcl"] | out["outside_ucl"]).astype(bool)
    out["signal_rule"] = np.where(out["outside_lcl"], "Unusually short interval", np.where(out["outside_ucl"], "Unusually long interval", ""))
    out["special_cause"] = out["signal"]
    out["special_cause_rule"] = out["signal_rule"]
    out["special_cause_direction"] = np.where(out["outside_lcl"], "low", np.where(out["outside_ucl"], "high", ""))
    out["special_cause_type"] = np.where(out["signal"], "neutral", "")
    out["special_cause_colour"] = np.where(out["signal"], "#768692", "")
    out["special_cause_label"] = np.where(out["signal"], out["special_cause_rule"], "")
    out["sigma"] = np.nan
    if "excluded" in out:
        out.loc[out["excluded"], ["signal", "special_cause"]] = False
        out.loc[out["excluded"], ["signal_rule", "special_cause_rule", "special_cause_direction", "special_cause_type", "special_cause_colour", "special_cause_label"]] = ""
    return out


def _risk_adjusted_fields(out: pd.DataFrame, y: str, expected: str, chart_key: str, denominator: str | None = None) -> pd.DataFrame:
    """Calculate distinct risk-adjusted P-prime and U-prime chart fields."""
    observed = out[y].astype(float)
    expected_values = out[expected].astype(float)
    if (expected_values < 0).any():
        raise ValueError("expected values must be non-negative.")
    safe_expected = expected_values.replace(0, np.nan)
    oe_ratio = observed / safe_expected
    out["plot_value"] = np.nan
    out["centre"] = np.nan
    out["lcl"] = np.nan
    out["ucl"] = np.nan
    out["sigma"] = np.nan
    if denominator and denominator in out.columns:
        opportunities = out[denominator].astype(float)
        method_label = "Risk-adjusted proportion" if chart_key == "p_prime" else "Risk-adjusted rate"
        for _, group in out.groupby("segment_id", sort=True):
            active = group.index[~out.loc[group.index, "excluded"].astype(bool)] if "excluded" in out else group.index
            centre = float(observed.loc[active].sum() / opportunities.loc[active].sum()) if len(active) and opportunities.loc[active].sum() > 0 else np.nan
            plot_value = oe_ratio.loc[group.index] * centre
            if chart_key == "p_prime":
                expected_probability = (expected_values.loc[group.index] / opportunities.loc[group.index]).clip(lower=1e-12, upper=1 - 1e-12)
                se = centre * np.sqrt((1 - expected_probability) / (expected_probability * opportunities.loc[group.index]))
            else:
                se = centre / np.sqrt(safe_expected.loc[group.index])
            out.loc[group.index, "plot_value"] = plot_value
            out.loc[group.index, "centre"] = centre
            out.loc[group.index, "lcl"] = np.maximum(0, centre - 3 * se)
            out.loc[group.index, "ucl"] = centre + 3 * se
            out.loc[group.index, "sigma"] = se
    else:
        method_label = "Observed/expected ratio fallback"
        for _, group in out.groupby("segment_id", sort=True):
            centre = 1.0
            se = 1 / np.sqrt(safe_expected.loc[group.index])
            out.loc[group.index, "plot_value"] = oe_ratio.loc[group.index]
            out.loc[group.index, "centre"] = centre
            out.loc[group.index, "lcl"] = np.maximum(0, centre - 3 * se)
            out.loc[group.index, "ucl"] = centre + 3 * se
            out.loc[group.index, "sigma"] = se

    out["observed"] = observed
    out["expected"] = expected_values
    out["oe_ratio"] = oe_ratio
    out["risk_adjusted_value"] = oe_ratio
    out["centre_label"] = method_label
    out["moving_range"] = np.nan
    out["expected_zero"] = expected_values == 0
    out["adjusted_rate"] = out["plot_value"]
    out["risk_adjusted_chart"] = chart_key
    out["outside_lcl"] = (out["plot_value"] < out["lcl"]).fillna(False)
    out["outside_ucl"] = (out["plot_value"] > out["ucl"]).fillna(False)
    out["signal"] = (out["outside_lcl"] | out["outside_ucl"]).astype(bool)
    out["signal_rule"] = np.where(out["outside_lcl"], "Observed below expected limits", np.where(out["outside_ucl"], "Observed above expected limits", ""))
    out["special_cause"] = out["signal"]
    out["special_cause_rule"] = out["signal_rule"]
    out["special_cause_direction"] = np.where(out["outside_lcl"], "low", np.where(out["outside_ucl"], "high", ""))
    out["special_cause_type"] = np.where(out["signal"], "neutral", "")
    out["special_cause_colour"] = np.where(out["signal"], "#768692", "")
    out["special_cause_label"] = np.where(out["signal"], out["special_cause_rule"], "")
    if "excluded" in out:
        out.loc[out["excluded"], ["signal", "special_cause"]] = False
        out.loc[out["excluded"], ["signal_rule", "special_cause_rule", "special_cause_direction", "special_cause_type", "special_cause_colour", "special_cause_label"]] = ""
    return out


def _c4(n: float) -> float:
    """Return the normal-theory correction factor for subgroup standard deviation."""
    if n <= 1:
        return np.nan
    return float(np.sqrt(2 / (n - 1)) * np.exp(math.lgamma(n / 2) - math.lgamma((n - 1) / 2)))


def _xbar_s_fields(
    raw: pd.DataFrame,
    x: str,
    y: str,
    chart_key: str,
    baseline_points: int | None = None,
    recalculation_points: list | None = None,
    target: float | int | None = None,
    interventions: list[dict] | None = None,
    step_changes: list[dict] | None = None,
    exclude_points: list | None = None,
    phases: list[dict] | None = None,
) -> pd.DataFrame:
    """Aggregate observation-level rows into segment-aware Xbar or S rows."""
    grouped = raw.groupby(x, sort=False)[y]
    out = grouped.agg(subgroup_mean="mean", subgroup_std="std", subgroup_n="count").reset_index()
    out["subgroup_std"] = out["subgroup_std"].fillna(0.0)
    out["chart"] = chart_key
    out = _add_process_metadata(out, x, baseline_points, recalculation_points, target, interventions, step_changes, exclude_points, phases)
    out["moving_range"] = np.nan
    out["sigma"] = np.nan
    out["centre"] = np.nan
    out["lcl"] = np.nan
    out["ucl"] = np.nan
    out["plot_value"] = out["subgroup_mean"] if chart_key == "xbar" else out["subgroup_std"]
    out["centre_label"] = "Grand mean" if chart_key == "xbar" else "Mean subgroup standard deviation"

    for _, group in out.groupby("segment_id", sort=True):
        active = group.index[~out.loc[group.index, "excluded"].astype(bool)]
        if baseline_points and int(group.index[0]) == 0:
            active = active[: int(baseline_points)]
        if len(active) == 0:
            continue
        sbar = float(out.loc[active, "subgroup_std"].mean())
        nbar = float(out.loc[active, "subgroup_n"].mean())
        c4_bar = _c4(nbar)
        sigma = sbar / c4_bar if c4_bar == c4_bar and c4_bar > 0 else np.nan
        if chart_key == "xbar":
            centre = float((out.loc[active, "subgroup_mean"] * out.loc[active, "subgroup_n"]).sum() / out.loc[active, "subgroup_n"].sum())
            se = sigma / np.sqrt(out.loc[group.index, "subgroup_n"]) if sigma == sigma else np.nan
            lcl = centre - 3 * se
            ucl = centre + 3 * se
        else:
            centre = sbar
            c4_each = out.loc[group.index, "subgroup_n"].astype(float).map(_c4)
            factor = 3 * np.sqrt(np.maximum(0.0, 1 - c4_each**2)) / c4_each
            lcl = np.maximum(0.0, centre * (1 - factor))
            ucl = centre * (1 + factor)
        out.loc[group.index, "centre"] = centre
        out.loc[group.index, "lcl"] = lcl
        out.loc[group.index, "ucl"] = ucl
        out.loc[group.index, "sigma"] = sigma
    out["signal"] = ((out["plot_value"] < out["lcl"]) | (out["plot_value"] > out["ucl"])).fillna(False).astype(bool)
    out["signal_rule"] = np.where(out["signal"], f"Outside {chart_key.upper()} chart limits", "")
    out["special_cause"] = out["signal"]
    out["special_cause_rule"] = out["signal_rule"]
    out["special_cause_direction"] = np.where(out["plot_value"] < out["lcl"], "low", np.where(out["plot_value"] > out["ucl"], "high", ""))
    out["special_cause_type"] = np.where(out["signal"], "neutral", "")
    out["special_cause_colour"] = np.where(out["signal"], "#768692", "")
    out["special_cause_label"] = np.where(out["signal"], out["special_cause_rule"], "")
    out["signal_count"] = out["signal"].astype(int)
    out["rule_set"] = ""
    out.loc[out["excluded"], ["signal", "special_cause"]] = False
    return out

def qic_table(
    data: pd.DataFrame,
    x: str,
    y: str,
    chart: str = "run",
    denominator: str | None = None,
    expected: str | None = None,
    improvement: str | None = None,
    shift_points: int = 8,
    trend_points: int = 6,
    baseline_points: int | None = None,
    recalculation_points: list | None = None,
    target: float | int | None = None,
    interventions: list[dict] | None = None,
    step_changes: list[dict] | None = None,
    freeze_points: list | None = None,
    break_points: list | None = None,
    exclude_points: list | None = None,
    phases: list[dict] | None = None,
    rules: str | None = None,
    method: str = "anhoej",
    baseline_start=None,
    baseline_end=None,
    freeze: list | None = None,
    breaks: list | None = None,
    exclude: list | None = None,
    recalculate_after: list | None = None,
    targets=None,
) -> pd.DataFrame:
    """Return QI/SPC chart calculations as a pandas DataFrame.

    Version 1.2.0 supports run, I, MR, C, P, U, Xbar, S, G, T, P-prime and U-prime charts. P and U charts
    require a denominator column. Individuals charts include NHS-style
    special cause fields for points outside limits, shifts and trends.
    Baseline periods, recalculation segments, targets, interventions and
    step changes are represented as additive table fields. qicharts-style
    phase aliases are also available as additive metadata.
    """
    chart_key = _chart_key(chart)
    rule_set = _normalise_rules(rules)
    freeze_points = list(freeze_points or []) + list(freeze or [])
    break_point_list = list(break_points or []) + list(breaks or []) + list(recalculate_after or [])
    exclude_points = list(exclude_points or []) + list(exclude or [])
    if target is None and targets is not None:
        target = targets[0] if isinstance(targets, list) and targets else targets
    if baseline_end is not None and baseline_points is None:
        baseline_points = int(baseline_end)
    if baseline_points is None and freeze_points:
        baseline_points = int(freeze_points[0])
    if break_point_list:
        recalculation_points = list(recalculation_points or []) + break_point_list
    if chart_key in {"xbar", "s"}:
        raw = _ordered_numeric(data, x, y)
        table = _xbar_s_fields(raw, x, y, chart_key, baseline_points, recalculation_points, target, interventions, step_changes, exclude_points, phases)
        return _add_rule_metadata(table, x, chart_key, rule_set)
    out = _ordered_numeric_with_expected_and_optional_denominator(data, x, y, expected, denominator) if chart_key in {"p_prime","u_prime"} and expected else _ordered_numeric_with_denominator(data, x, y, denominator) if chart_key in {"p","u"} and denominator else _ordered_numeric(data, x, y)
    if chart_key in {"p","u"} and denominator is None: raise ValueError(f"chart={chart!r} requires a denominator column.")
    if chart_key in {"p_prime","u_prime"} and expected is None: raise ValueError(f"chart={chart!r} requires an expected column.")
    if chart_key not in VALID_CHARTS: raise ValueError(f"Unsupported chart {chart!r}. Valid chart names are: {', '.join(sorted(VALID_CHARTS))}.")
    out["chart"] = chart_key
    out = _add_process_metadata(out, x, baseline_points, recalculation_points, target, interventions, step_changes, exclude_points, phases)
    if chart_key == "run":
        out["plot_value"] = out[y]
        out["centre"] = np.nan
        out["centre_label"] = "Median"
        out["lcl"] = np.nan; out["ucl"] = np.nan; out["moving_range"] = np.nan; out["signal"] = False; out["signal_rule"] = ""
        out["anhoej_signal_long_run"] = False; out["anhoej_signal_few_crossings"] = False; out["run_chart_method"] = method
        for _, group in out.groupby("segment_id", sort=True):
            centre_source = _segment_source(out[y], group.index, baseline_points, out["excluded"])
            rules = anhoej_rules(centre_source, method=method)
            out.loc[group.index, "centre"] = rules.median
            out.loc[group.index, "centre_label"] = "Median" if rules.method == "anhoej" else f"{rules.method} centre"
            out.loc[group.index, "anhoej_signal_long_run"] = rules.signal_long_run
            out.loc[group.index, "anhoej_signal_few_crossings"] = rules.signal_few_crossings
            out.loc[group.index, "run_chart_method"] = rules.method
            if rules.any_signal:
                out.loc[group.index, "signal"] = True
                out.loc[group.index, "signal_rule"] = "; ".join(rule for rule, active in [("unusually long run", rules.signal_long_run), ("unusually few crossings", rules.signal_few_crossings)] if active)
        out["special_cause"] = out["signal"]
        out["special_cause_rule"] = out["signal_rule"]
        out["special_cause_direction"] = np.where(out["signal"], "run", "")
        out["special_cause_type"] = np.where(out["signal"], "neutral", "")
        out["special_cause_colour"] = np.where(out["signal"], "#768692", "")
        out["special_cause_label"] = out["signal_rule"]
        return _add_rule_metadata(out, x, chart_key, rule_set)
    if chart_key == "i":
        values = out[y].astype(float); mr = values.diff().abs()
        out["plot_value"] = values; out["centre"] = np.nan; out["centre_label"] = "Mean"; out["lcl"] = np.nan; out["ucl"] = np.nan
        out["moving_range"] = mr; out["mrbar"] = np.nan; out["sigma"] = np.nan
        for _, group in out.groupby("segment_id", sort=True):
            source = _segment_source(values, group.index, baseline_points, out["excluded"])
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
        out = pd.concat([out, nhs], axis=1)
        out.loc[out["excluded"], ["signal", "special_cause"]] = False
        return _add_rule_metadata(out, x, chart_key, rule_set)
    if chart_key in {"g", "t"}:
        return _add_rule_metadata(_rare_event_fields(out, y, chart_key), x, chart_key, rule_set)
    if chart_key in {"p_prime", "u_prime"}:
        return _add_rule_metadata(_risk_adjusted_fields(out, y, expected, chart_key, denominator), x, chart_key, rule_set)
    if chart_key == "mr":
        values = out[y].astype(float); mr = values.diff().abs()
        out["moving_range"] = mr; out["plot_value"] = mr; out["centre"] = np.nan; out["centre_label"] = "Mean moving range"; out["lcl"] = 0.0; out["ucl"] = np.nan
        out["signal"] = False; out["signal_rule"] = ""; out["mrbar"] = np.nan; out["sigma"] = np.nan
        for _, group in out.groupby("segment_id", sort=True):
            source = _segment_source(values, group.index, baseline_points, out["excluded"])
            segment_mr = source.diff().abs()
            mrbar = float(segment_mr.dropna().mean()) if len(segment_mr.dropna()) else np.nan
            ucl = 3.267 * mrbar if mrbar == mrbar else np.nan
            signal = (mr.loc[group.index] > ucl).fillna(False) if ucl == ucl else pd.Series(False, index=group.index)
            out.loc[group.index, "centre"] = mrbar
            out.loc[group.index, "ucl"] = ucl
            out.loc[group.index, "signal"] = signal.astype(bool)
            out.loc[group.index, "signal_rule"] = np.where(signal, "MR above UCL", "")
            out.loc[group.index, "mrbar"] = mrbar
            out.loc[group.index, "sigma"] = mrbar / 1.128 if mrbar == mrbar else np.nan
        out.loc[out["excluded"], ["signal"]] = False
        return _add_rule_metadata(out, x, chart_key, rule_set)
    if chart_key == "c":
        counts = out[y].astype(float)
        out["plot_value"] = counts; out["centre"] = np.nan; out["centre_label"] = "Mean count"; out["lcl"] = np.nan; out["ucl"] = np.nan
        out["moving_range"] = np.nan; out["signal"] = False; out["signal_rule"] = ""; out["sigma"] = np.nan
        for _, group in out.groupby("segment_id", sort=True):
            source = _segment_source(counts, group.index, baseline_points, out["excluded"])
            centre = float(source.mean()) if len(source) else np.nan; sqrt_c = np.sqrt(centre) if centre == centre else np.nan
            lcl = max(0.0, centre - 3*sqrt_c) if sqrt_c == sqrt_c else np.nan; ucl = centre + 3*sqrt_c if sqrt_c == sqrt_c else np.nan
            signal = ((counts.loc[group.index] < lcl) | (counts.loc[group.index] > ucl)).fillna(False) if sqrt_c == sqrt_c else pd.Series(False, index=group.index)
            out.loc[group.index, "centre"] = centre; out.loc[group.index, "lcl"] = lcl; out.loc[group.index, "ucl"] = ucl
            out.loc[group.index, "signal"] = signal.astype(bool); out.loc[group.index, "signal_rule"] = np.where(signal, "Outside C chart limits", ""); out.loc[group.index, "sigma"] = sqrt_c
        out.loc[out["excluded"], ["signal"]] = False
        return _add_rule_metadata(out, x, chart_key, rule_set)
    if chart_key == "p":
        events = out[y].astype(float); denom = out[denominator].astype(float); proportion = events / denom
        out["plot_value"] = proportion; out["centre"] = np.nan; out["centre_label"] = "Mean proportion"; out["lcl"] = np.nan; out["ucl"] = np.nan
        out["moving_range"] = np.nan; out["signal"] = False; out["signal_rule"] = ""; out["sigma"] = np.nan
        for _, group in out.groupby("segment_id", sort=True):
            active = group.index[~out.loc[group.index, "excluded"].astype(bool)]
            pbar = float(events.loc[active].sum()/denom.loc[active].sum()) if len(active) and denom.loc[active].sum() > 0 else np.nan
            se = np.sqrt(pbar*(1-pbar)/denom.loc[group.index]) if pbar == pbar else np.nan; lcl = np.maximum(0, pbar - 3*se); ucl = np.minimum(1, pbar + 3*se); signal = (proportion.loc[group.index] < lcl) | (proportion.loc[group.index] > ucl)
            out.loc[group.index, "centre"] = pbar; out.loc[group.index, "lcl"] = lcl; out.loc[group.index, "ucl"] = ucl
            out.loc[group.index, "signal"] = signal.astype(bool); out.loc[group.index, "signal_rule"] = np.where(signal, "Outside P chart limits", ""); out.loc[group.index, "sigma"] = se
        out.loc[out["excluded"], ["signal"]] = False
        return _add_rule_metadata(out, x, chart_key, rule_set)
    events = out[y].astype(float); denom = out[denominator].astype(float); rate = events / denom
    out["plot_value"] = rate; out["centre"] = np.nan; out["centre_label"] = "Mean rate"; out["lcl"] = np.nan; out["ucl"] = np.nan
    out["moving_range"] = np.nan; out["signal"] = False; out["signal_rule"] = ""; out["sigma"] = np.nan
    for _, group in out.groupby("segment_id", sort=True):
        active = group.index[~out.loc[group.index, "excluded"].astype(bool)]
        ubar = float(events.loc[active].sum()/denom.loc[active].sum()) if len(active) and denom.loc[active].sum() > 0 else np.nan
        se = np.sqrt(ubar/denom.loc[group.index]) if ubar == ubar else np.nan; lcl = np.maximum(0, ubar - 3*se); ucl = ubar + 3*se; signal = (rate.loc[group.index] < lcl) | (rate.loc[group.index] > ucl)
        out.loc[group.index, "centre"] = ubar; out.loc[group.index, "lcl"] = lcl; out.loc[group.index, "ucl"] = ucl
        out.loc[group.index, "signal"] = signal.astype(bool); out.loc[group.index, "signal_rule"] = np.where(signal, "Outside U chart limits", ""); out.loc[group.index, "sigma"] = se
    out.loc[out["excluded"], ["signal"]] = False
    return _add_rule_metadata(out, x, chart_key, rule_set)

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
