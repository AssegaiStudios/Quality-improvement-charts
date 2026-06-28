import importlib.util

import pytest

from pyqicharts_excel.excel_io import create_template
from pyqicharts_excel.runner import clear_outputs, generate_chart, validate_workbook


pytestmark = pytest.mark.skipif(importlib.util.find_spec("openpyxl") is None, reason="openpyxl is not installed")


def test_generate_chart_writes_outputs(tmp_path):
    from openpyxl import load_workbook

    path = create_template(tmp_path / "template.xlsx")
    message = generate_chart(path)
    assert "completed successfully" in message
    workbook = load_workbook(path, data_only=True)
    assert workbook["ChartData"]["A1"].value is not None
    assert workbook["SPCSummary"]["A1"].value == "schema_version"
    assert workbook["NHSInterpretation"]["A1"].value == "chart_id"


def test_validate_workbook_returns_success(tmp_path):
    path = create_template(tmp_path / "template.xlsx")
    assert validate_workbook(path) == "Workbook validation passed."


def test_clear_outputs_clears_generated_sheets(tmp_path):
    from openpyxl import load_workbook

    path = create_template(tmp_path / "template.xlsx")
    generate_chart(path)
    assert clear_outputs(path) == "Outputs cleared."
    workbook = load_workbook(path, data_only=True)
    assert workbook["ChartData"]["A1"].value is None


def test_runner_logs_friendly_error(tmp_path):
    from openpyxl import load_workbook

    path = create_template(tmp_path / "template.xlsx")
    workbook = load_workbook(path)
    ws = workbook["Config"]
    for row in ws.iter_rows(min_row=2):
        if row[0].value == "chart_type":
            row[1].value = "p"
        if row[0].value == "denominator_column":
            row[1].value = ""
    workbook.save(path)

    message = generate_chart(path)
    assert "failed" in message
    workbook = load_workbook(path, data_only=True)
    log_values = [cell.value for cell in workbook["Log"]["C"] if cell.value]
    assert any("denominator" in value for value in log_values)

