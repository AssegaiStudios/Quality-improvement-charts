"""NHS-style special cause rules for SPC charts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd

ImprovementDirection = Literal["high is good", "low is good"]


@dataclass(frozen=True)
class NhsRuleConfig:
    """Configuration for NHS-style XmR special cause detection."""

    shift_points: int = 8
    trend_points: int = 6


def _normalise_improvement(improvement: str | None) -> ImprovementDirection | None:
    if improvement is None:
        return None
    key = improvement.strip().lower().replace("_", " ").replace("-", " ")
    if key in {"high is good", "higher is good", "increase is good", "increasing is good"}:
        return "high is good"
    if key in {"low is good", "lower is good", "decrease is good", "decreasing is good"}:
        return "low is good"
    raise ValueError("improvement must be 'high is good', 'low is good', or None.")


def _classify_direction(direction: str, improvement: ImprovementDirection | None) -> str:
    if improvement is None or direction == "":
        return "neutral"
    high_is_improvement = improvement == "high is good"
    if direction == "high":
        return "improvement" if high_is_improvement else "concern"
    if direction == "low":
        return "concern" if high_is_improvement else "improvement"
    return "neutral"


def _signal_colour(signal_type: str) -> str:
    return {
        "improvement": "#005EB8",
        "concern": "#ED8B00",
        "neutral": "#768692",
    }.get(signal_type, "#768692")


def _mark_shift(values: pd.Series, centre: pd.Series | float, length: int) -> tuple[pd.Series, pd.Series]:
    centre_series = centre if isinstance(centre, pd.Series) else pd.Series(centre, index=values.index)
    signs = pd.Series(np.sign(values - centre_series), index=values.index).fillna(0).astype(int)
    signal = pd.Series(False, index=values.index)
    direction = pd.Series("", index=values.index, dtype=object)
    run_indices: list[int] = []
    run_sign = 0

    for idx, sign in signs.items():
        if sign == 0:
            continue
        if sign != run_sign:
            if len(run_indices) >= length:
                signal.loc[run_indices] = True
                direction.loc[run_indices] = "high" if run_sign > 0 else "low"
            run_indices = [idx]
            run_sign = sign
        else:
            run_indices.append(idx)

    if len(run_indices) >= length:
        signal.loc[run_indices] = True
        direction.loc[run_indices] = "high" if run_sign > 0 else "low"
    return signal, direction


def _mark_trend(values: pd.Series, length: int) -> tuple[pd.Series, pd.Series]:
    signal = pd.Series(False, index=values.index)
    direction = pd.Series("", index=values.index, dtype=object)
    run_indices: list[int] = []
    run_sign = 0
    previous = None
    previous_idx = None

    for idx, value in values.items():
        if previous is None or pd.isna(value) or pd.isna(previous):
            previous = value
            previous_idx = idx
            continue
        diff = value - previous
        sign = 1 if diff > 0 else -1 if diff < 0 else 0
        previous = value
        start_idx = previous_idx
        previous_idx = idx
        if sign == 0:
            continue
        if sign != run_sign:
            if len(run_indices) >= length:
                signal.loc[run_indices] = True
                direction.loc[run_indices] = "high" if run_sign > 0 else "low"
            run_indices = [start_idx, idx]
            run_sign = sign
        else:
            run_indices.append(idx)

    if len(run_indices) >= length:
        signal.loc[run_indices] = True
        direction.loc[run_indices] = "high" if run_sign > 0 else "low"
    return signal, direction


def nhs_xmr_signals(
    values: pd.Series,
    centre: pd.Series | float,
    lcl: pd.Series | float | None,
    ucl: pd.Series | float | None,
    improvement: str | None = None,
    config: NhsRuleConfig | None = None,
) -> pd.DataFrame:
    """Return NHS-style special cause fields for an Individuals/XmR chart.

    Rules implemented in v0.4.0:
    - Rule 1: one point outside the control limits.
    - Shift: eight non-centre points above or below the centre line.
    - Trend: six consecutive increases or decreases.
    """

    cfg = config or NhsRuleConfig()
    improvement_key = _normalise_improvement(improvement)
    values = values.astype(float)
    out = pd.DataFrame(index=values.index)
    out["outside_ucl"] = False
    out["outside_lcl"] = False

    if ucl is not None:
        ucl_series = ucl if isinstance(ucl, pd.Series) else pd.Series(ucl, index=values.index)
        out["outside_ucl"] = (values > ucl_series).fillna(False)
    if lcl is not None:
        lcl_series = lcl if isinstance(lcl, pd.Series) else pd.Series(lcl, index=values.index)
        out["outside_lcl"] = (values < lcl_series).fillna(False)

    shift_signal, shift_direction = _mark_shift(values, centre, cfg.shift_points)
    trend_signal, trend_direction = _mark_trend(values, cfg.trend_points)
    out["shift"] = shift_signal
    out["trend"] = trend_signal

    rules: list[str] = []
    directions: list[str] = []
    labels: list[str] = []
    for idx in values.index:
        row_rules = []
        row_directions = []
        if bool(out.at[idx, "outside_ucl"]):
            row_rules.append("above UCL")
            row_directions.append("high")
        if bool(out.at[idx, "outside_lcl"]):
            row_rules.append("below LCL")
            row_directions.append("low")
        if bool(shift_signal.at[idx]):
            row_rules.append("shift")
            row_directions.append(str(shift_direction.at[idx]))
        if bool(trend_signal.at[idx]):
            row_rules.append("trend")
            row_directions.append(str(trend_direction.at[idx]))
        direction = row_directions[0] if row_directions else ""
        signal_type = _classify_direction(direction, improvement_key)
        rules.append("; ".join(row_rules))
        directions.append(direction)
        labels.append(signal_type if row_rules else "")

    out["special_cause"] = out[["outside_ucl", "outside_lcl", "shift", "trend"]].any(axis=1)
    out["special_cause_rule"] = rules
    out["special_cause_direction"] = directions
    out["special_cause_type"] = labels
    out["special_cause_colour"] = [
        _signal_colour(signal_type) if is_signal else ""
        for signal_type, is_signal in zip(out["special_cause_type"], out["special_cause"])
    ]
    out["special_cause_label"] = np.where(
        out["special_cause"],
        out["special_cause_type"].str.title() + ": " + out["special_cause_rule"],
        "",
    )
    return out
