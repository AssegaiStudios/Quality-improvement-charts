import pandas as pd

from pyqicharts import pareto_chart, qic
from pyqicharts_excel.config import ExcelConfig
from pyqicharts_excel.outputs import build_output_tables, chart_id, export_outputs, nhs_output_table, powerbi_output_table, signal_output_table, summary_output_table


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


def test_pareto_output_tables_cover_non_time_series_branches():
    result = pareto_chart(pd.DataFrame({"category": ["A", "B", "A"], "count": [3, 1, 2]}), "category", "count")
    assert chart_id(result) == "pareto:category"
    assert chart_id(object()) == "chart"

    signals = signal_output_table(result, "pareto")
    assert list(signals.columns)[0] == "schema_version"
    assert signals.empty

    nhs = nhs_output_table(result, "pareto")
    assert nhs["signal_classification"].iloc[0] == "neutral"

    summary = summary_output_table(result, "pareto")
    assert summary["total_count"].iloc[0] == 6

    powerbi = powerbi_output_table(result, "pareto")
    assert {"schema_version", "chart_id", "chart_type", "table_name"}.issubset(powerbi.columns)


def test_build_output_tables_can_omit_powerbi():
    chart = qic(pd.DataFrame({"period": range(1, 6), "value": [1, 2, 3, 2, 1]}), "period", "value")
    assert "PowerBI" not in build_output_tables(chart, "run", include_powerbi=False)


def test_export_outputs_creates_excel_powerpoint_and_bundle(tmp_path):
    chart = qic(pd.DataFrame({"period": range(1, 8), "value": [1, 2, 3, 2, 1, 2, 3]}), "period", "value")
    config = ExcelConfig(export_excel=True, export_powerpoint=True, export_bundle=True)
    out = export_outputs(chart, tmp_path, "run", config)
    assert {"Excel", "PowerPoint", "Report bundle"}.issubset(set(out["export_type"]))
    assert (tmp_path / "chart_data.xlsx").exists()
    assert (tmp_path / "report.pptx").exists()
    assert (tmp_path / "bundle" / "metadata.json").exists()


def test_pareto_export_skips_non_png_report_exports(tmp_path):
    result = pareto_chart(pd.DataFrame({"category": ["A", "B"], "count": [2, 1]}), "category", "count")
    config = ExcelConfig(export_excel=True, export_powerpoint=True, export_bundle=True)
    out = export_outputs(result, tmp_path, "pareto", config)
    assert out["status"].iloc[0] == "No exports requested"
