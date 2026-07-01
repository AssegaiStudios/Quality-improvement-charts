import matplotlib
matplotlib.use("Agg")
import pandas as pd

from pyqicharts import qic, qic_table


def test_baseline_limits_use_baseline_data_only():
    df = pd.DataFrame({"month": range(1, 6), "value": [10, 10, 10, 10, 50]})
    out = qic_table(df, "month", "value", chart="i", baseline_points=4)
    assert out["baseline_period"].tolist() == [True, True, True, True, False]
    assert out["centre"].iloc[-1] == 10
    assert out["ucl"].iloc[-1] == 10
    assert out["outside_ucl"].iloc[-1]


def test_recalculation_creates_new_segments():
    df = pd.DataFrame({"month": range(1, 9), "value": [10, 11, 10, 11, 30, 31, 30, 31]})
    out = qic_table(df, "month", "value", chart="i", recalculation_points=[5])
    assert out["segment_id"].tolist() == [1, 1, 1, 1, 2, 2, 2, 2]
    assert out.loc[out["segment_id"] == 1, "centre"].iloc[0] == 10.5
    assert out.loc[out["segment_id"] == 2, "centre"].iloc[0] == 30.5


def test_freeze_points_work_without_break_points_or_recalculation():
    df = pd.DataFrame({"month": range(1, 7), "value": [10, 10, 10, 50, 55, 60]})
    out = qic_table(df, "month", "value", chart="i", freeze_points=[3])
    alias_out = qic_table(df, "month", "value", chart="i", freeze=[3])

    assert out["baseline_period"].tolist() == [True, True, True, False, False, False]
    assert out["segment_id"].nunique() == 1
    assert out["centre"].tolist() == [10, 10, 10, 10, 10, 10]
    assert alias_out["centre"].tolist() == out["centre"].tolist()


def test_target_values_appear_in_table():
    df = pd.DataFrame({"month": range(1, 4), "value": [90, 92, 94]})
    out = qic_table(df, "month", "value", chart="i", target=95)
    assert out["target"].tolist() == [95, 95, 95]


def test_intervention_metadata_appears_in_output():
    df = pd.DataFrame({"month": range(1, 5), "value": [10, 11, 12, 13]})
    out = qic_table(df, "month", "value", chart="i", interventions=[{"point": 3, "label": "New pathway introduced"}])
    assert out["intervention"].tolist() == [False, False, True, False]
    assert out["intervention_label"].iloc[2] == "New pathway introduced"


def test_step_change_metadata_appears_in_output():
    df = pd.DataFrame({"month": range(1, 5), "value": [10, 11, 20, 21]})
    out = qic_table(df, "month", "value", chart="i", step_changes=[{"point": 3, "label": "Process changed"}])
    assert out["step_change"].tolist() == [False, False, True, False]
    assert out["step_change_label"].iloc[2] == "Process changed"


def test_plotting_does_not_fail_when_markers_are_present():
    df = pd.DataFrame({"month": range(1, 7), "value": [10, 11, 12, 20, 21, 22]})
    result = qic(
        df,
        "month",
        "value",
        chart="i",
        target=18,
        interventions=[{"point": 3, "label": "Intervention"}],
        step_changes=[{"point": 4, "label": "Step change"}],
        recalculation_points=[4],
    )
    assert result.figure is not None
    assert result.table["intervention"].any()
    assert result.table["step_change"].any()
