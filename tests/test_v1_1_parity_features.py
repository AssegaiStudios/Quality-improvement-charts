import pandas as pd
import matplotlib.pyplot as plt

from pyqicharts import (
    nelson_rule_signals,
    qic,
    qic_table,
    signal_table,
    shewhart_rule_signals,
    kpi_table,
)


def test_nelson_rules_return_metadata_for_each_rule():
    cases = {
        "N1": [0, 0, 0, 3.5],
        "N2": [1] * 9,
        "N3": [1, 2, 3, 4, 5, 6],
        "N4": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        "N5": [2.2, 2.3, 0],
        "N6": [1.2, 1.3, 1.4, 1.5, 0],
        "N7": [0.2] * 15,
        "N8": [1.2, -1.3, 1.4, -1.5, 1.6, -1.7, 1.8, -1.9],
    }
    for expected_rule, values in cases.items():
        out = nelson_rule_signals(values, centre=0, sigma=1, chart_type="i")
        assert expected_rule in set(out["rule_id"])
        assert {"rule_name", "start_point", "end_point", "severity"}.issubset(out.columns)


def test_shewhart_rules_can_be_requested_from_qic_table():
    df = pd.DataFrame({"month": range(1, 14), "value": [10] * 12 + [20]})
    out = qic_table(df, "month", "value", chart="i", rules="all")
    assert out["signal_rule"].str.contains("above UCL").any()
    assert "signal_count" in out.columns


def test_signal_table_uses_stable_schema():
    chart = qic(pd.DataFrame({"month": range(1, 14), "value": [10] * 12 + [20]}), "month", "value", chart="i")
    out = signal_table(chart)
    expected = {
        "chart_type",
        "signal_type",
        "rule_type",
        "rule_name",
        "direction",
        "severity",
        "start_index",
        "end_index",
        "start_x",
        "end_x",
        "message",
    }
    assert expected.issubset(out.columns)
    assert len(out) >= 1
    plt.close(chart.figure)


def test_qicharts_style_phase_aliases_and_exclusions_are_available():
    df = pd.DataFrame({"month": range(1, 9), "value": [10, 10, 10, 50, 11, 11, 12, 13]})
    out = qic_table(
        df,
        "month",
        "value",
        chart="i",
        freeze_points=[3],
        break_points=[5],
        exclude_points=[4],
        phases=[{"start": 1, "label": "Baseline"}, {"start": 5, "label": "New process"}],
    )
    assert out.loc[out["month"] == 4, "excluded"].iloc[0]
    assert out.loc[out["month"] == 5, "phase_label"].iloc[0] == "New process"
    assert out["segment_id"].nunique() == 2


def test_powerbi_kpi_table_schema():
    chart = qic(pd.DataFrame({"month": range(1, 14), "value": [10] * 12 + [20]}), "month", "value", chart="i")
    out = kpi_table(chart)
    assert {"schema_version", "chart_type", "signal_count", "latest_value", "latest_signal"}.issubset(out.columns)
    plt.close(chart.figure)


def test_shewhart_rule_helper_returns_dataframe():
    out = shewhart_rule_signals([0, 0, 3.5], centre=0, sigma=1, chart_type="i")
    assert "S1" in set(out["rule_id"])
