"""Output table and export helpers for the Excel Companion."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from pyqicharts import (
    create_report_bundle as core_create_report_bundle,
    export_excel as core_export_excel,
    export_png,
    export_powerpoint as core_export_powerpoint,
    nhs_interpretation_table,
    powerbi_table,
    signal_table,
    spc_summary_table,
)
from pyqicharts.signals import SIGNAL_SCHEMA_VERSION


SIGNAL_COLUMNS = [
    "schema_version",
    "chart_id",
    "chart_type",
    "signal_type",
    "rule_type",
    "rule_id",
    "rule_name",
    "direction",
    "severity",
    "start_index",
    "end_index",
    "start_x",
    "end_x",
    "message",
]


def chart_id(result: Any) -> str:
    """Return a stable chart identifier for workbook outputs."""

    if hasattr(result, "chart") and hasattr(result, "y"):
        return f"{result.chart}:{result.y}"
    if hasattr(result, "category"):
        return f"pareto:{result.category}"
    return "chart"


def _empty_signals(result: Any, chart_type: str) -> pd.DataFrame:
    """Return an empty signal table with the stable workbook schema."""

    return pd.DataFrame(columns=SIGNAL_COLUMNS).assign(
        schema_version=pd.Series(dtype=object),
        chart_id=pd.Series(dtype=object),
        chart_type=pd.Series(dtype=object),
    )


def signal_output_table(result: Any, chart_type: str) -> pd.DataFrame:
    """Return signal rows with all workbook-required columns present."""

    if chart_type == "pareto":
        out = _empty_signals(result, chart_type)
    else:
        out = signal_table(result)
    for column in SIGNAL_COLUMNS:
        if column not in out.columns:
            out[column] = ""
    out["schema_version"] = out["schema_version"].replace("", SIGNAL_SCHEMA_VERSION)
    out["chart_id"] = out["chart_id"].replace("", chart_id(result))
    out["chart_type"] = out["chart_type"].replace("", chart_type)
    return out[SIGNAL_COLUMNS]


def nhs_output_table(result: Any, chart_type: str) -> pd.DataFrame:
    """Return a user-facing NHS interpretation table."""

    if chart_type == "pareto":
        classification = "neutral"
        interpretation = "Pareto charts rank categories and do not use NHS time-series signal rules."
    else:
        base = nhs_interpretation_table(result)
        classification = str(base.get("interpretation_type", pd.Series(["neutral"])).iloc[0])
        interpretation = str(base.get("interpretation", pd.Series(["No interpretation available."])).iloc[0])
    action = "Review alongside operational context and annotate any known process changes."
    return pd.DataFrame(
        [
            {
                "chart_id": chart_id(result),
                "chart_type": chart_type,
                "signal_classification": classification,
                "interpretation": interpretation,
                "recommended_action": action,
            }
        ]
    )


def summary_output_table(result: Any, chart_type: str) -> pd.DataFrame:
    """Return an SPC summary table or a Pareto summary fallback."""

    if chart_type == "pareto":
        return pd.DataFrame(
            [
                {
                    "chart_id": chart_id(result),
                    "chart_type": "pareto",
                    "categories": len(result.table),
                    "total_count": float(result.table["count"].sum()) if "count" in result.table else 0,
                }
            ]
        )
    return spc_summary_table(result)


def powerbi_output_table(result: Any, chart_type: str) -> pd.DataFrame:
    """Return a flattened table suitable for Power BI import."""

    if chart_type == "pareto":
        out = result.table.copy()
        out.insert(0, "table_name", "pareto")
        out.insert(0, "chart_type", "pareto")
        out.insert(0, "chart_id", chart_id(result))
        out.insert(0, "schema_version", SIGNAL_SCHEMA_VERSION)
        return out
    out = powerbi_table(result)
    out.insert(3, "table_name", "chart_data")
    return out


def build_output_tables(result: Any, chart_type: str, include_powerbi: bool = True) -> dict[str, pd.DataFrame]:
    """Build every workbook output table from one chart result."""

    tables = {
        "ChartData": result.table.copy(),
        "SPCSummary": summary_output_table(result, chart_type),
        "Signals": signal_output_table(result, chart_type),
        "NHSInterpretation": nhs_output_table(result, chart_type),
    }
    if include_powerbi:
        tables["PowerBI"] = powerbi_output_table(result, chart_type)
    return tables


def export_outputs(result: Any, output_dir: str | Path, chart_type: str, config: Any) -> pd.DataFrame:
    """Create optional PNG, Excel, PowerPoint and bundle exports."""

    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    if getattr(config, "export_png", False):
        path = export_png(result, folder / "chart.png")
        rows.append({"export_type": "PNG", "path": str(path), "status": "created"})
    if getattr(config, "export_excel", False) and chart_type != "pareto":
        path = core_export_excel(result, folder / "chart_data.xlsx")
        rows.append({"export_type": "Excel", "path": str(path), "status": "created"})
    if getattr(config, "export_powerpoint", False) and chart_type != "pareto":
        path = core_export_powerpoint(result, folder / "report.pptx")
        rows.append({"export_type": "PowerPoint", "path": str(path), "status": "created"})
    if getattr(config, "export_bundle", False) and chart_type != "pareto":
        metadata = core_create_report_bundle([result], folder / "bundle")
        rows.append({"export_type": "Report bundle", "path": str(folder / "bundle"), "status": json.dumps(metadata)})
    return pd.DataFrame(rows or [{"export_type": "", "path": "", "status": "No exports requested"}])

