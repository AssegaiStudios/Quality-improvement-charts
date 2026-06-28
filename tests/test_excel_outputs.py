import pandas as pd

from pyqicharts import qic
from pyqicharts_excel.config import ExcelConfig
from pyqicharts_excel.outputs import build_output_tables, export_outputs


def test_output_tables_include_required_workbook_tables():
    chart = qic(pd.DataFrame({"period": range(1, 10), "value": [10, 11, 10, 12, 11, 10, 12, 13, 12]}), "period", "value")
    tables = build_output_tables(chart, "run")
    assert {"ChartData", "SPCSummary", "Signals", "NHSInterpretation", "PowerBI"}.issubset(tables)
    assert {"schema_version", "chart_id", "chart_type", "signal_type"}.issubset(tables["Signals"].columns)
    assert {"chart_id", "chart_type", "signal_classification", "recommended_action"}.issubset(tables["NHSInterpretation"].columns)


def test_export_outputs_reports_no_exports_when_disabled(tmp_path):
    chart = qic(pd.DataFrame({"period": range(1, 6), "value": [1, 2, 3, 2, 1]}), "period", "value")
    out = export_outputs(chart, tmp_path, "run", ExcelConfig())
    assert out["status"].iloc[0] == "No exports requested"


def test_export_outputs_creates_png(tmp_path):
    chart = qic(pd.DataFrame({"period": range(1, 6), "value": [1, 2, 3, 2, 1]}), "period", "value")
    out = export_outputs(chart, tmp_path, "run", ExcelConfig(export_png=True))
    assert out["export_type"].iloc[0] == "PNG"
    assert (tmp_path / "chart.png").exists()

