"""Shared signal schema for chart rules, reports and Power BI outputs."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

import pandas as pd


SIGNAL_SCHEMA_VERSION = "1.3.1"


@dataclass(frozen=True)
class Signal:
    """A rule signal described independently of a specific output surface."""

    chart_type: str
    signal_type: str
    rule_type: str
    rule_id: str
    rule_name: str
    direction: str
    severity: str
    start_index: int
    end_index: int
    start_x: object
    end_x: object
    message: str


SIGNAL_COLUMNS = [
    "schema_version",
    "chart_type",
    "signal_type",
    "rule_type",
    "rule_id",
    "rule_name",
    "direction",
    "severity",
    "start_point",
    "end_point",
    "start_index",
    "end_index",
    "start_x",
    "end_x",
    "message",
]


def signals_to_frame(signals: Iterable[Signal]) -> pd.DataFrame:
    """Return signals as a stable-schema DataFrame."""

    rows = []
    for signal in signals:
        row = asdict(signal)
        row["schema_version"] = SIGNAL_SCHEMA_VERSION
        row["start_point"] = signal.start_index
        row["end_point"] = signal.end_index
        rows.append(row)
    return pd.DataFrame(rows, columns=SIGNAL_COLUMNS)


def table_signals(table: pd.DataFrame, chart_type: str, x: str | None = None) -> pd.DataFrame:
    """Convert row-level signal columns into the shared signal schema."""

    if table.empty:
        return pd.DataFrame(columns=SIGNAL_COLUMNS)
    x_column = x if x in table.columns else None
    signal_col = "special_cause" if "special_cause" in table.columns else "signal"
    if signal_col not in table.columns:
        return pd.DataFrame(columns=SIGNAL_COLUMNS)

    signals: list[Signal] = []
    for idx, row in table[table[signal_col].fillna(False).astype(bool)].iterrows():
        rule_name = str(row.get("special_cause_rule", row.get("signal_rule", "")))
        if not rule_name:
            rule_name = "Signal"
        direction = str(row.get("special_cause_direction", ""))
        signal_type = str(row.get("special_cause_type", "neutral") or "neutral")
        x_value = row[x_column] if x_column else int(idx) + 1
        signals.append(
            Signal(
                chart_type=chart_type,
                signal_type=signal_type,
                rule_type=str(row.get("rule_type", "row")),
                rule_id=str(row.get("rule_id", "")),
                rule_name=rule_name,
                direction=direction,
                severity=str(row.get("severity", "signal")),
                start_index=int(idx) + 1,
                end_index=int(idx) + 1,
                start_x=x_value,
                end_x=x_value,
                message=str(row.get("special_cause_label", rule_name)),
            )
        )
    return signals_to_frame(signals)
