"""Configuration parsing for the pyqicharts Excel Companion."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


VALID_CHART_TYPES = {
    "run",
    "i",
    "mr",
    "xmr",
    "c",
    "p",
    "u",
    "xbar",
    "s",
    "g",
    "t",
    "p_prime",
    "u_prime",
    "pareto",
}
VALID_METHODS = {"anhoej", "bestbox", "cutbox"}
VALID_RULES = {"anhoej", "shewhart", "nelson", "nhs", "all", ""}

CONFIG_FIELDS = [
    "data_sheet",
    "data_range",
    "x_column",
    "y_column",
    "chart_type",
    "denominator_column",
    "expected_column",
    "subgroup_column",
    "phase_column",
    "exclude_column",
    "target_value",
    "target_column",
    "baseline_start",
    "baseline_end",
    "freeze_after",
    "break_points",
    "recalculate_after",
    "intervention_column",
    "annotation_column",
    "theme",
    "rules",
    "method",
    "direction",
    "output_chart_sheet",
    "output_table_sheet",
    "export_png",
    "export_excel",
    "export_powerpoint",
    "export_bundle",
    "debug_mode",
    "powerbi_enabled",
    "export_dir",
    "chart_title",
]


@dataclass
class ExcelConfig:
    """Parsed workbook configuration with typed values where possible."""

    data_sheet: str = "Data"
    data_range: str = ""
    x_column: str = "period"
    y_column: str = "value"
    chart_type: str = "run"
    denominator_column: str = ""
    expected_column: str = ""
    subgroup_column: str = ""
    phase_column: str = ""
    exclude_column: str = ""
    target_value: float | None = None
    target_column: str = ""
    baseline_start: Any = None
    baseline_end: Any = None
    freeze_after: Any = None
    break_points: list[Any] | None = None
    recalculate_after: list[Any] | None = None
    intervention_column: str = ""
    annotation_column: str = ""
    theme: str = "default"
    rules: str = "nhs"
    method: str = "anhoej"
    direction: str = ""
    output_chart_sheet: str = "Chart"
    output_table_sheet: str = "ChartData"
    export_png: bool = False
    export_excel: bool = False
    export_powerpoint: bool = False
    export_bundle: bool = False
    debug_mode: bool = False
    powerbi_enabled: bool = True
    export_dir: str = "pyqicharts_excel_exports"
    chart_title: str = ""

    @property
    def normalised_chart_type(self) -> str:
        """Map Excel-friendly aliases to pyqicharts chart keys."""

        if self.chart_type == "xmr":
            return "i"
        return self.chart_type

    @property
    def qic_rules(self) -> str | None:
        """Return only rule names supported by the core qic rules argument."""

        return self.rules if self.rules in {"shewhart", "nelson", "all"} else None

    @property
    def output_path(self) -> Path:
        """Return the configured export folder as a path."""

        return Path(self.export_dir)


def _clean(value: Any) -> Any:
    """Normalise blank spreadsheet cells without altering meaningful values."""

    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    if isinstance(value, str):
        return value.strip()
    return value


def _as_bool(value: Any) -> bool:
    """Parse common Excel truthy/falsy values."""

    value = _clean(value)
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return bool(value)
    return str(value).strip().lower() in {"true", "yes", "y", "1", "on"}


def _as_optional_float(value: Any) -> float | None:
    """Parse an optional numeric cell value."""

    value = _clean(value)
    if value == "":
        return None
    return float(value)


def _as_list(value: Any) -> list[Any]:
    """Parse comma/semicolon-separated Excel config values."""

    value = _clean(value)
    if value == "":
        return []
    if isinstance(value, list):
        return value
    text = str(value).replace(";", ",")
    out: list[Any] = []
    for item in text.split(","):
        item = item.strip()
        if item == "":
            continue
        try:
            out.append(int(item))
        except ValueError:
            out.append(item)
    return out


def default_config() -> ExcelConfig:
    """Return a fresh default configuration object."""

    return ExcelConfig()


def parse_config_mapping(mapping: dict[str, Any]) -> ExcelConfig:
    """Parse a two-column Excel config mapping into an ExcelConfig."""

    normalised = {str(key).strip().lower(): _clean(value) for key, value in mapping.items()}
    unknown = sorted(set(normalised) - set(CONFIG_FIELDS))
    if unknown:
        raise ValueError(f"Unsupported config field(s): {', '.join(unknown)}")

    cfg = default_config()
    for field in CONFIG_FIELDS:
        if field in normalised:
            setattr(cfg, field, normalised[field])

    cfg.chart_type = str(cfg.chart_type).lower().replace("-", "_").replace(" ", "_")
    cfg.method = str(cfg.method).lower()
    cfg.rules = str(cfg.rules).lower()
    cfg.target_value = _as_optional_float(cfg.target_value)
    cfg.break_points = _as_list(cfg.break_points)
    cfg.recalculate_after = _as_list(cfg.recalculate_after)
    cfg.export_png = _as_bool(cfg.export_png)
    cfg.export_excel = _as_bool(cfg.export_excel)
    cfg.export_powerpoint = _as_bool(cfg.export_powerpoint)
    cfg.export_bundle = _as_bool(cfg.export_bundle)
    cfg.debug_mode = _as_bool(cfg.debug_mode)
    cfg.powerbi_enabled = _as_bool(cfg.powerbi_enabled)
    return cfg


def parse_config_frame(frame: pd.DataFrame) -> ExcelConfig:
    """Parse a DataFrame containing config fields and values."""

    if frame.empty or len(frame.columns) < 2:
        raise ValueError("Config sheet must contain at least two columns: field and value.")
    fields = frame.iloc[:, 0].dropna().astype(str)
    values = frame.iloc[:, 1]
    return parse_config_mapping(dict(zip(fields, values)))


def config_defaults_frame() -> pd.DataFrame:
    """Return defaults in a shape that writes cleanly to Excel."""

    cfg = default_config()
    rows = []
    for field in CONFIG_FIELDS:
        value = getattr(cfg, field)
        if value is None:
            value = ""
        elif isinstance(value, list):
            value = ", ".join(str(item) for item in value)
        rows.append({"field": field, "value": value})
    return pd.DataFrame(rows)
