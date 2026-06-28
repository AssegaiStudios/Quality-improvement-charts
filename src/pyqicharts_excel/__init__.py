"""Excel companion layer for pyqicharts.

The companion package deliberately keeps Excel-specific responsibilities here:
read workbook configuration, call the public pyqicharts APIs, and write the
resulting images/tables back to the workbook. No SPC calculations are
duplicated in this package.
"""
from .config import ExcelConfig, default_config, parse_config_frame, parse_config_mapping
from .excel_io import create_template, create_templates
from .runner import (
    clear_outputs,
    export_report_bundle,
    generate_all_outputs,
    generate_chart,
    main,
    refresh_config_defaults,
    validate_workbook,
)

__all__ = [
    "ExcelConfig",
    "clear_outputs",
    "create_template",
    "create_templates",
    "default_config",
    "export_report_bundle",
    "generate_all_outputs",
    "generate_chart",
    "main",
    "parse_config_frame",
    "parse_config_mapping",
    "refresh_config_defaults",
    "validate_workbook",
]

