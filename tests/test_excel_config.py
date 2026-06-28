import pandas as pd
import pytest

from pyqicharts_excel.config import ExcelConfig, config_defaults_frame, parse_config_frame, parse_config_mapping
from pyqicharts_excel.validation import validate_config, validate_data


def test_config_defaults_include_required_fields():
    frame = config_defaults_frame()
    assert {"field", "value"}.issubset(frame.columns)
    assert {"data_sheet", "chart_type", "debug_mode", "export_bundle"}.issubset(set(frame["field"]))


def test_config_parsing_normalises_values():
    cfg = parse_config_mapping(
        {
            "data_sheet": "Data",
            "x_column": "month",
            "y_column": "events",
            "chart_type": "P Prime",
            "expected_column": "expected",
            "export_png": "yes",
            "break_points": "4, 8",
            "debug_mode": "TRUE",
        }
    )
    assert cfg.chart_type == "p_prime"
    assert cfg.export_png is True
    assert cfg.debug_mode is True
    assert cfg.break_points == [4, 8]


def test_config_frame_parsing():
    frame = pd.DataFrame({"field": ["x_column", "y_column", "chart_type"], "value": ["period", "value", "i"]})
    cfg = parse_config_frame(frame)
    assert cfg.x_column == "period"
    assert cfg.chart_type == "i"


def test_unknown_config_field_is_rejected():
    with pytest.raises(ValueError, match="Unsupported config"):
        parse_config_mapping({"x_column": "period", "unknown": "value"})


def test_invalid_chart_type_validation():
    cfg = ExcelConfig(chart_type="not_a_chart")
    assert validate_config(cfg)


def test_data_validation_requires_denominator_for_p_chart():
    cfg = ExcelConfig(chart_type="p", denominator_column="denominator")
    data = pd.DataFrame({"period": [1, 2], "value": [1, 2]})
    assert "Missing required column" in validate_data(data, cfg)[0]


def test_data_validation_catches_empty_numeric_y():
    cfg = ExcelConfig(x_column="period", y_column="value")
    data = pd.DataFrame({"period": [1, 2], "value": ["", None]})
    assert "no numeric values" in validate_data(data, cfg)[0]

