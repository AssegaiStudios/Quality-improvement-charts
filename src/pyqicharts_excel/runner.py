"""xlwings-callable runner functions for the pyqicharts Excel Companion."""
from __future__ import annotations

import traceback
from pathlib import Path
from typing import Any

import pandas as pd

from pyqicharts import export_png, pareto_chart, qic

from .config import ExcelConfig, config_defaults_frame, parse_config_frame
from .excel_io import (
    clear_output_sheets,
    create_template,
    insert_chart_image,
    read_config_from_workbook,
    read_sheet_frame,
    write_frame_to_sheet,
    write_log,
)
from .outputs import build_output_tables, export_outputs
from .validation import raise_if_errors, validate_config, validate_data


def _calling_workbook_path(workbook_path: str | Path | None = None) -> Path:
    """Resolve the active workbook path for xlwings or tests."""

    if workbook_path:
        return Path(workbook_path)
    try:
        import xlwings as xw

        return Path(xw.Book.caller().fullname)
    except Exception as exc:
        raise RuntimeError("No workbook path supplied and xlwings could not locate the calling workbook.") from exc


def _prepare_data(path: Path, config: ExcelConfig) -> pd.DataFrame:
    """Read and validate the workbook data table."""

    data = read_sheet_frame(path, config.data_sheet, config.data_range)
    errors = validate_config(config) + validate_data(data, config)
    raise_if_errors(errors)
    return data


def _interventions_from_columns(data: pd.DataFrame, config: ExcelConfig) -> list[dict]:
    """Convert optional Excel intervention labels to qic marker dictionaries."""

    if not config.intervention_column or config.intervention_column not in data:
        return []
    markers = []
    for index, label in data[config.intervention_column].fillna("").items():
        if str(label).strip():
            markers.append({"point": index + 1, "label": str(label)})
    return markers


def _exclude_points(data: pd.DataFrame, config: ExcelConfig) -> list[int]:
    """Return 1-based row numbers flagged for exclusion."""

    if not config.exclude_column or config.exclude_column not in data:
        return []
    flags = data[config.exclude_column].fillna("").astype(str).str.lower().isin({"true", "yes", "y", "1", "exclude"})
    return [int(index) + 1 for index in data.index[flags]]


def _call_pyqicharts(data: pd.DataFrame, config: ExcelConfig):
    """Build a pyqicharts result from validated Excel configuration."""

    if config.chart_type == "pareto":
        count_column = config.denominator_column or None
        return pareto_chart(data, category=config.x_column, count=count_column, title=config.chart_title or None, theme=config.theme)

    denominator = config.denominator_column or None
    expected = config.expected_column or None
    recalculation_points = list(config.recalculate_after or []) + list(config.break_points or [])
    freeze_points = [config.freeze_after] if config.freeze_after not in (None, "") else None
    return qic(
        data=data,
        x=config.x_column,
        y=config.y_column,
        chart=config.normalised_chart_type,
        denominator=denominator,
        expected=expected,
        title=config.chart_title or None,
        theme=config.theme,
        improvement=config.direction or None,
        target=config.target_value,
        interventions=_interventions_from_columns(data, config),
        exclude_points=_exclude_points(data, config),
        freeze_points=freeze_points,
        recalculation_points=recalculation_points,
        rules=config.qic_rules,
        method=config.method,
        baseline_start=config.baseline_start or None,
        baseline_end=config.baseline_end or None,
    )


def _write_success_outputs(path: Path, result: Any, config: ExcelConfig) -> pd.DataFrame:
    """Write chart image, tables and export rows back to a workbook."""

    export_dir = (path.parent / config.output_path).resolve()
    export_dir.mkdir(parents=True, exist_ok=True)
    image_path = export_png(result, export_dir / "chart.png")
    insert_chart_image(path, image_path, config.output_chart_sheet, config.chart_title or "pyqicharts chart")
    for sheet, frame in build_output_tables(result, config.chart_type, config.powerbi_enabled).items():
        write_frame_to_sheet(path, sheet, frame)
    exports = export_outputs(result, export_dir, config.chart_type, config)
    write_frame_to_sheet(path, "Exports", exports)
    write_log(path, "Chart generation completed successfully.")
    return exports


def _run_with_friendly_errors(action: str, workbook_path: str | Path | None, callback):
    """Run an Excel action and write friendly failures to the Log sheet."""

    path = _calling_workbook_path(workbook_path)
    try:
        config = read_config_from_workbook(path)
        result = callback(path, config)
        return f"{action} completed successfully."
    except Exception as exc:
        message = f"{action} failed: {exc}"
        try:
            config = read_config_from_workbook(path)
            detail = traceback.format_exc() if config.debug_mode else message
            write_log(path, detail, level="ERROR")
        except Exception:
            pass
        return message


def generate_chart(workbook_path: str | Path | None = None) -> str:
    """Generate one chart and all standard workbook output tables."""

    def callback(path: Path, config: ExcelConfig):
        data = _prepare_data(path, config)
        result = _call_pyqicharts(data, config)
        _write_success_outputs(path, result, config)
        return result

    return _run_with_friendly_errors("Generate chart", workbook_path, callback)


def generate_all_outputs(workbook_path: str | Path | None = None) -> str:
    """Generate chart, tables, Power BI output and any configured exports."""

    return generate_chart(workbook_path)


def export_report_bundle(workbook_path: str | Path | None = None) -> str:
    """Force report-bundle export for the configured chart."""

    def callback(path: Path, config: ExcelConfig):
        config.export_bundle = True
        data = _prepare_data(path, config)
        result = _call_pyqicharts(data, config)
        _write_success_outputs(path, result, config)
        return result

    return _run_with_friendly_errors("Export report bundle", workbook_path, callback)


def clear_outputs(workbook_path: str | Path | None = None) -> str:
    """Clear generated output sheets."""

    path = _calling_workbook_path(workbook_path)
    clear_output_sheets(path)
    write_log(path, "Output sheets cleared.")
    return "Outputs cleared."


def validate_workbook(workbook_path: str | Path | None = None) -> str:
    """Validate workbook config and data, then write the result to Log."""

    path = _calling_workbook_path(workbook_path)
    config = read_config_from_workbook(path)
    data = read_sheet_frame(path, config.data_sheet, config.data_range)
    errors = validate_config(config) + validate_data(data, config)
    if errors:
        write_log(path, "Validation failed: " + " ".join(errors), level="ERROR")
        return "Validation failed: " + " ".join(errors)
    write_log(path, "Workbook validation passed.")
    return "Workbook validation passed."


def refresh_config_defaults(workbook_path: str | Path | None = None) -> str:
    """Rewrite Config with default fields and values."""

    path = _calling_workbook_path(workbook_path)
    write_frame_to_sheet(path, "Config", config_defaults_frame())
    write_log(path, "Config defaults refreshed.")
    return "Config defaults refreshed."


def main(workbook_path: str | Path | None = None) -> str:
    """Default xlwings entry point; generates a chart."""

    return generate_chart(workbook_path)


def init_template(output_path: str | Path = "pyqicharts_excel_template.xlsx") -> Path:
    """Console-command helper to create a fresh workbook template."""

    return create_template(output_path)


def init_template_cli() -> None:
    """Console script entry point."""

    print(init_template())


if __name__ == "__main__":
    init_template_cli()
