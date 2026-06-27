"""Nelson and Shewhart rule detection helpers."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .signals import Signal, signals_to_frame


NELSON_RULE_NAMES = {
    "N1": "One point more than 3 sigma from the centre line",
    "N2": "Nine points in a row on the same side of the centre line",
    "N3": "Six points in a row increasing or decreasing",
    "N4": "Fourteen points in a row alternating up and down",
    "N5": "Two of three points more than 2 sigma from the centre line",
    "N6": "Four of five points more than 1 sigma from the centre line",
    "N7": "Fifteen points in a row within 1 sigma of the centre line",
    "N8": "Eight points in a row more than 1 sigma from the centre line",
}


SHEWHART_RULE_NAMES = {
    "S1": "One point outside the 3 sigma control limits",
    "S2": "Two of three points beyond 2 sigma on the same side",
    "S3": "Four of five points beyond 1 sigma on the same side",
    "S4": "Run of points on one side of the centre line",
    "S5": "Trend of consecutive increasing or decreasing points",
}


def _x_value(x_values, index: int):
    """Return a display x value for a zero-based index."""

    if x_values is None:
        return index + 1
    return list(x_values)[index]


def _signal(
    chart_type: str,
    rule_type: str,
    rule_id: str,
    rule_name: str,
    direction: str,
    severity: str,
    start: int,
    end: int,
    x_values=None,
) -> Signal:
    """Create a shared schema signal from zero-based positions."""

    message = f"{rule_id}: {rule_name}"
    return Signal(
        chart_type=chart_type,
        signal_type="neutral",
        rule_type=rule_type,
        rule_id=rule_id,
        rule_name=rule_name,
        direction=direction,
        severity=severity,
        start_index=start + 1,
        end_index=end + 1,
        start_x=_x_value(x_values, start),
        end_x=_x_value(x_values, end),
        message=message,
    )


def _window_direction(values: np.ndarray) -> str:
    """Return high/low when a window is all on one side of zero."""

    if np.all(values > 0):
        return "high"
    if np.all(values < 0):
        return "low"
    return "mixed"


def nelson_rule_signals(values, centre: float, sigma: float, chart_type: str = "i", x_values=None) -> pd.DataFrame:
    """Detect Nelson Rules 1-8 and return a stable-schema DataFrame."""

    series = pd.Series(values, dtype="float64").reset_index(drop=True)
    if not len(series) or sigma is None or not np.isfinite(sigma) or sigma <= 0:
        return signals_to_frame([])

    z = ((series - centre) / sigma).to_numpy()
    signals: list[Signal] = []

    for i, value in enumerate(z):
        if abs(value) > 3:
            signals.append(_signal(chart_type, "nelson", "N1", NELSON_RULE_NAMES["N1"], "high" if value > 0 else "low", "critical", i, i, x_values))

    for i in range(0, len(z) - 8):
        window = z[i : i + 9]
        if np.all(window > 0) or np.all(window < 0):
            signals.append(_signal(chart_type, "nelson", "N2", NELSON_RULE_NAMES["N2"], _window_direction(window), "warning", i, i + 8, x_values))

    diffs = np.diff(series.to_numpy())
    for i in range(0, len(diffs) - 4):
        window = diffs[i : i + 5]
        if np.all(window > 0) or np.all(window < 0):
            signals.append(_signal(chart_type, "nelson", "N3", NELSON_RULE_NAMES["N3"], "high" if np.all(window > 0) else "low", "warning", i, i + 5, x_values))

    signs = np.sign(diffs)
    for i in range(0, len(signs) - 12):
        window = signs[i : i + 13]
        if not np.any(window == 0) and np.all(window[:-1] != window[1:]):
            signals.append(_signal(chart_type, "nelson", "N4", NELSON_RULE_NAMES["N4"], "alternating", "warning", i, i + 13, x_values))

    for i in range(0, len(z) - 2):
        window = z[i : i + 3]
        high = np.sum(window > 2)
        low = np.sum(window < -2)
        if high >= 2 or low >= 2:
            signals.append(_signal(chart_type, "nelson", "N5", NELSON_RULE_NAMES["N5"], "high" if high >= 2 else "low", "warning", i, i + 2, x_values))

    for i in range(0, len(z) - 4):
        window = z[i : i + 5]
        high = np.sum(window > 1)
        low = np.sum(window < -1)
        if high >= 4 or low >= 4:
            signals.append(_signal(chart_type, "nelson", "N6", NELSON_RULE_NAMES["N6"], "high" if high >= 4 else "low", "warning", i, i + 4, x_values))

    for i in range(0, len(z) - 14):
        window = z[i : i + 15]
        if np.all(np.abs(window) < 1):
            signals.append(_signal(chart_type, "nelson", "N7", NELSON_RULE_NAMES["N7"], "near-centre", "information", i, i + 14, x_values))

    for i in range(0, len(z) - 7):
        window = z[i : i + 8]
        if np.all(np.abs(window) > 1) and np.any(window > 0) and np.any(window < 0):
            signals.append(_signal(chart_type, "nelson", "N8", NELSON_RULE_NAMES["N8"], "mixed", "warning", i, i + 7, x_values))

    return signals_to_frame(signals).drop_duplicates().reset_index(drop=True)


def shewhart_rule_signals(values, centre: float, sigma: float, chart_type: str = "i", x_values=None) -> pd.DataFrame:
    """Return a compact Shewhart-compatible rule set."""

    nelson = nelson_rule_signals(values, centre=centre, sigma=sigma, chart_type=chart_type, x_values=x_values)
    if nelson.empty:
        return nelson
    mapping = {"N1": "S1", "N5": "S2", "N6": "S3", "N2": "S4", "N3": "S5"}
    out = nelson[nelson["rule_id"].isin(mapping)].copy()
    out["rule_type"] = "shewhart"
    out["rule_id"] = out["rule_id"].map(mapping)
    out["rule_name"] = out["rule_id"].map(SHEWHART_RULE_NAMES)
    out["message"] = out["rule_id"] + ": " + out["rule_name"]
    return out.reset_index(drop=True)
