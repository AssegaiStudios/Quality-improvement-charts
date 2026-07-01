import matplotlib
matplotlib.use("Agg")
import pandas as pd
import pytest
from pathlib import Path
from pandas.testing import assert_frame_equal

from pyqicharts import (
    days_between_falls_with_harm,
    days_between_serious_incidents,
    infections_between_events,
    qic,
    qic_table,
)

ROOT = Path(__file__).resolve().parents[1]


def test_g_chart_table_calculations():
    df = infections_between_events()
    out = qic_table(df, "case_number", "cases_between_events", chart="g")
    assert out["chart"].iloc[0] == "g"
    assert out["centre_label"].iloc[0] == "Mean cases between events"
    assert out["rare_event_probability"].notna().all()
    assert out["lcl"].iloc[0] >= 0
    assert out["ucl"].iloc[0] > out["centre"].iloc[0]


def test_t_chart_table_calculations():
    df = days_between_serious_incidents()
    out = qic_table(df, "event_number", "days_between_events", chart="t")
    assert out["chart"].iloc[0] == "t"
    assert out["centre_label"].iloc[0] == "Mean time between events"
    assert out["rare_event_mean"].iloc[0] == df["days_between_events"].mean()
    assert out["lcl"].iloc[0] >= 0
    assert out["ucl"].iloc[0] > out["centre"].iloc[0]


def test_g_chart_rendering_smoke():
    df = infections_between_events()
    result = qic(df, "case_number", "cases_between_events", chart="g")
    assert result.figure is not None
    assert result.table["chart"].iloc[0] == "g"


def test_t_chart_rendering_smoke():
    df = days_between_falls_with_harm()
    result = qic(df, "event_number", "days_between_events", chart="t")
    assert result.figure is not None
    assert result.table["chart"].iloc[0] == "t"


def test_invalid_negative_g_intervals_raise_useful_error():
    df = pd.DataFrame({"case_number": [1, 2, 3], "cases_between_events": [10, -1, 12]})
    with pytest.raises(ValueError, match="G chart intervals must be non-negative"):
        qic_table(df, "case_number", "cases_between_events", chart="g")


def test_invalid_negative_t_intervals_raise_useful_error():
    df = pd.DataFrame({"event_number": [1, 2, 3], "days_between_events": [10, -1, 12]})
    with pytest.raises(ValueError, match="T chart intervals must be non-negative"):
        qic_table(df, "event_number", "days_between_events", chart="t")


def test_g_chart_rare_event_signal_detection_works():
    df = pd.DataFrame({"case_number": range(1, 52), "cases_between_events": [20] * 50 + [300]})
    out = qic_table(df, "case_number", "cases_between_events", chart="g")
    assert out["signal"].iloc[-1]
    assert out["outside_ucl"].iloc[-1]
    assert out["signal_rule"].iloc[-1] == "Unusually long interval"


def test_t_chart_rare_event_short_interval_signal_detection_works():
    df = pd.DataFrame({"event_number": range(1, 12), "days_between_events": [30] * 10 + [0]})
    out = qic_table(df, "event_number", "days_between_events", chart="t")
    assert out["signal"].iloc[-1]
    assert out["outside_lcl"].iloc[-1]
    assert out["signal_rule"].iloc[-1] == "Unusually short interval"


def test_segmented_rare_event_validation_fixtures_match_expected_outputs():
    fixture_dir = ROOT / "validation_data" / "segmented_rare_event"
    manifest = pd.read_csv(fixture_dir / "segmented_rare_event_manifest.csv")
    columns = ["chart", "point_index", "segment_id", "centre", "lcl", "ucl", "plot_value", "signal", "special_cause", "signal_rule", "special_cause_rule"]

    for _, row in manifest.iterrows():
        data = pd.read_csv(fixture_dir / row["input_file"])
        actual = qic_table(data, "x", "y", chart=row["chart"], breaks=[5, 9])
        actual = actual[[col for col in columns if col in actual]].copy()
        for col in actual.select_dtypes(include="number").columns:
            actual[col] = actual[col].round(6)
        expected = pd.read_csv(fixture_dir / row["expected_file"])
        assert_frame_equal(actual.fillna("").reset_index(drop=True), expected.fillna("").reset_index(drop=True), check_dtype=False)
