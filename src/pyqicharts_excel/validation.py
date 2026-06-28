"""Workbook and data validation for the Excel Companion."""
from __future__ import annotations

import pandas as pd

from .config import ExcelConfig, VALID_CHART_TYPES, VALID_METHODS, VALID_RULES


class WorkbookValidationError(ValueError):
    """Friendly validation error intended for Excel users."""


def validate_config(config: ExcelConfig) -> list[str]:
    """Return user-friendly config validation errors."""

    errors: list[str] = []
    if not config.data_sheet:
        errors.append("Config field 'data_sheet' is required.")
    if not config.x_column:
        errors.append("Config field 'x_column' is required.")
    if not config.y_column:
        errors.append("Config field 'y_column' is required.")
    if config.chart_type not in VALID_CHART_TYPES:
        errors.append(f"Chart type '{config.chart_type}' is not supported.")
    if config.method not in VALID_METHODS:
        errors.append(f"Run chart method '{config.method}' is not supported.")
    if config.rules not in VALID_RULES:
        errors.append(f"Rules option '{config.rules}' is not supported.")
    if config.chart_type in {"p", "u"} and not config.denominator_column:
        errors.append(f"{config.chart_type.upper()} charts require denominator_column.")
    if config.chart_type in {"p_prime", "u_prime"} and not config.expected_column:
        errors.append(f"{config.chart_type} charts require expected_column.")
    if config.chart_type in {"xbar", "s"} and not config.x_column:
        errors.append("Xbar and S charts require a subgroup x_column.")
    return errors


def validate_data(frame: pd.DataFrame, config: ExcelConfig) -> list[str]:
    """Return validation errors for the configured data table."""

    errors: list[str] = []
    if frame.empty:
        return ["The configured data table is empty."]
    if frame.columns.duplicated().any():
        duplicated = sorted(set(frame.columns[frame.columns.duplicated()].astype(str)))
        errors.append(f"Duplicate column header(s): {', '.join(duplicated)}.")

    required = [config.x_column, config.y_column]
    if config.chart_type in {"p", "u"}:
        required.append(config.denominator_column)
    if config.chart_type in {"p_prime", "u_prime"}:
        required.append(config.expected_column)
    if config.denominator_column and config.chart_type in {"p_prime", "u_prime"}:
        required.append(config.denominator_column)
    missing = [column for column in required if column and column not in frame.columns]
    if missing:
        errors.append(f"Missing required column(s): {', '.join(missing)}.")
        return errors

    y_values = pd.to_numeric(frame[config.y_column], errors="coerce")
    if y_values.dropna().empty:
        errors.append(f"Column '{config.y_column}' has no numeric values.")
    if config.chart_type in {"c", "p", "u", "g", "t", "p_prime", "u_prime"} and (y_values.dropna() < 0).any():
        errors.append(f"Column '{config.y_column}' contains negative values, which are invalid for {config.chart_type} charts.")
    if config.chart_type in {"p", "u"} and config.denominator_column in frame:
        denom = pd.to_numeric(frame[config.denominator_column], errors="coerce")
        if (denom.dropna() <= 0).any() or denom.dropna().empty:
            errors.append("Denominator values must be positive.")
    if config.chart_type in {"p_prime", "u_prime"} and config.expected_column in frame:
        expected = pd.to_numeric(frame[config.expected_column], errors="coerce")
        if (expected.dropna() < 0).any() or expected.dropna().empty:
            errors.append("Expected values must be non-negative and contain at least one numeric value.")
    return errors


def raise_if_errors(errors: list[str]) -> None:
    """Raise one friendly error containing all validation issues."""

    if errors:
        raise WorkbookValidationError(" ".join(errors))

