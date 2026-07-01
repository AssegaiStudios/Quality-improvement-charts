import pandas as pd
import pytest

from pyqicharts_excel.config import ExcelConfig, config_defaults_frame, parse_config_frame, parse_config_mapping
from pyqicharts_excel.validation import WorkbookValidationError, raise_if_errors, validate_config, validate_data


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


def test_config_parsing_handles_bool_number_float_and_lists():
    cfg = parse_config_mapping(
        {
            "target_value": "12.5",
            "export_excel": 1,
            "export_powerpoint": False,
            "powerbi_enabled": "off",
            "recalculate_after": ["April"],
            "break_points": "2; April",
            "chart_type": "xmr",
            "rules": "all",
        }
    )
    assert cfg.target_value == 12.5
    assert cfg.export_excel is True
    assert cfg.export_powerpoint is False
    assert cfg.powerbi_enabled is False
    assert cfg.recalculate_after == ["April"]
    assert cfg.break_points == [2, "April"]
    assert cfg.normalised_chart_type == "i"
    assert cfg.qic_rules == "all"
    assert str(cfg.output_path).endswith("pyqicharts_excel_exports")


def test_parse_config_frame_rejects_bad_shape():
    with pytest.raises(ValueError, match="Config sheet"):
        parse_config_frame(pd.DataFrame({"only_one_column": ["x_column"]}))


def test_validate_config_reports_all_common_errors():
    cfg = ExcelConfig(data_sheet="", x_column="", y_column="", chart_type="p_prime", method="bad", rules="bad")
    errors = validate_config(cfg)
    joined = " ".join(errors)
    assert "data_sheet" in joined
    assert "x_column" in joined
    assert "y_column" in joined
    assert "method" in joined
    assert "Rules" in joined
    assert "expected_column" in joined


def test_validate_config_reports_denominator_and_subgroup_requirements():
    assert any("denominator" in error for error in validate_config(ExcelConfig(chart_type="u", denominator_column="")))
    assert validate_config(ExcelConfig(chart_type="s", x_column=""))


def test_data_validation_catches_empty_dataset_duplicate_headers_and_bad_values():
    assert validate_data(pd.DataFrame(), ExcelConfig())[0].startswith("The configured data table is empty")

    duplicate = pd.DataFrame([[1, 2, 3]], columns=["period", "value", "value"])
    assert "Duplicate" in validate_data(duplicate, ExcelConfig(x_column="period", y_column="value"))[0]

    negative = pd.DataFrame({"period": [1], "value": [-1]})
    assert "negative" in " ".join(validate_data(negative, ExcelConfig(chart_type="c")))

    bad_denominator = pd.DataFrame({"period": [1], "value": [1], "denominator": [0]})
    assert "Denominator" in " ".join(validate_data(bad_denominator, ExcelConfig(chart_type="p", denominator_column="denominator")))

    bad_expected = pd.DataFrame({"period": [1], "value": [1], "expected": [-1]})
    assert "Expected" in " ".join(validate_data(bad_expected, ExcelConfig(chart_type="p_prime", expected_column="expected")))


def test_raise_if_errors_uses_friendly_exception():
    with pytest.raises(WorkbookValidationError, match="first second"):
        raise_if_errors(["first", "second"])
