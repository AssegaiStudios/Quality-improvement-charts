import pandas as pd
import pytest

from pyqicharts import qic_table


def _base_values():
    return [10, 11, 10, 50, 51, 50, 100, 101, 100]


@pytest.mark.parametrize(
    "chart,frame,kwargs,centre_col",
    [
        ("run", pd.DataFrame({"x": range(1, 10), "y": _base_values()}), {}, "centre"),
        ("i", pd.DataFrame({"x": range(1, 10), "y": _base_values()}), {"rules": "nelson"}, "centre"),
        ("mr", pd.DataFrame({"x": range(1, 10), "y": [10, 11, 13, 50, 55, 65, 100, 120, 150]}), {"rules": "shewhart"}, "centre"),
        ("c", pd.DataFrame({"x": range(1, 10), "y": [2, 3, 2, 20, 21, 20, 40, 41, 40]}), {"rules": "nelson"}, "centre"),
        ("p", pd.DataFrame({"x": range(1, 10), "y": [2, 3, 2, 20, 21, 20, 40, 41, 40], "n": [100] * 9}), {"denominator": "n", "rules": "shewhart"}, "centre"),
        ("u", pd.DataFrame({"x": range(1, 10), "y": [2, 3, 2, 20, 21, 20, 40, 41, 40], "n": [50] * 9}), {"denominator": "n", "rules": "shewhart"}, "centre"),
        ("xbar", pd.DataFrame({"x": [1,1,2,2,3,3,4,4,5,5,6,6], "y": [10,11,10,12,50,51,50,52,100,101,100,102]}), {"rules": "nelson", "breaks": [3, 5]}, "centre"),
        ("s", pd.DataFrame({"x": [1,1,2,2,3,3,4,4,5,5,6,6], "y": [10,11,10,12,50,55,50,60,100,120,100,130]}), {"rules": "nelson", "breaks": [3, 5]}, "centre"),
        ("g", pd.DataFrame({"x": range(1, 10), "y": [5, 6, 5, 20, 21, 20, 60, 61, 60]}), {}, "centre"),
        ("t", pd.DataFrame({"x": range(1, 10), "y": [5, 6, 5, 20, 21, 20, 60, 61, 60]}), {}, "centre"),
        ("p_prime", pd.DataFrame({"x": range(1, 10), "y": [2,3,2,20,21,20,40,41,40], "expected": [2,2,2,18,18,18,38,38,38], "n": [100] * 9}), {"expected": "expected", "denominator": "n"}, "centre"),
        ("u_prime", pd.DataFrame({"x": range(1, 10), "y": [2,3,2,20,21,20,40,41,40], "expected": [2,2,2,18,18,18,38,38,38], "n": [100] * 9}), {"expected": "expected", "denominator": "n"}, "centre"),
    ],
)
def test_three_segments_use_segment_specific_limits(chart, frame, kwargs, centre_col):
    if "breaks" not in kwargs:
        kwargs = {**kwargs, "breaks": [4, 7]}
    out = qic_table(frame, "x", "y", chart=chart, **kwargs)
    assert list(out.groupby("segment_id")[centre_col].first().index) == [1, 2, 3]
    assert out.groupby("segment_id")[centre_col].first().nunique(dropna=False) >= 2
    if chart != "run":
        assert {"lcl", "ucl", "signal_count"}.issubset(out.columns)


def test_excluded_points_are_removed_from_segment_calculations():
    df = pd.DataFrame({"x": range(1, 7), "y": [10, 10, 999, 20, 20, 20]})
    out = qic_table(df, "x", "y", chart="i", breaks=[4], exclude=[3])
    assert out.loc[out["x"] == 3, "excluded"].iloc[0]
    assert out.groupby("segment_id")["centre"].first().iloc[0] == 10


def test_excluded_points_suppress_rare_event_signals():
    for chart_type in ["g", "t"]:
        out = qic_table(
            pd.DataFrame({"x": range(1, 9), "y": [10, 11, 12, 300, 11, 10, 12, 11]}),
            "x",
            "y",
            chart=chart_type,
            exclude_points=[4],
        )
        row = out.loc[out["x"] == 4].iloc[0]
        assert bool(row["excluded"])
        assert not bool(row["signal"])
        assert not bool(row["special_cause"])
        assert row["special_cause_rule"] == ""


def test_excluded_points_suppress_risk_adjusted_signals():
    data = pd.DataFrame(
        {
            "x": range(1, 9),
            "observed": [10, 11, 10, 100, 11, 10, 12, 11],
            "expected": [10] * 8,
            "denominator": [100] * 8,
        }
    )
    for chart_type in ["p_prime", "u_prime"]:
        out = qic_table(
            data,
            "x",
            "observed",
            chart=chart_type,
            expected="expected",
            denominator="denominator",
            exclude_points=[4],
        )
        row = out.loc[out["x"] == 4].iloc[0]
        assert bool(row["excluded"])
        assert not bool(row["signal"])
        assert not bool(row["special_cause"])
        assert row["special_cause_rule"] == ""


@pytest.mark.parametrize(
    "chart_type,frame,kwargs,excluded_x",
    [
        ("mr", pd.DataFrame({"x": range(1, 8), "y": [10, 10, 10, 100, 10, 10, 10]}), {}, 4),
        ("c", pd.DataFrame({"x": range(1, 8), "y": [2, 2, 2, 50, 2, 2, 2]}), {}, 4),
        ("p", pd.DataFrame({"x": range(1, 8), "y": [2, 2, 2, 80, 2, 2, 2], "n": [100] * 7}), {"denominator": "n"}, 4),
        ("u", pd.DataFrame({"x": range(1, 8), "y": [2, 2, 2, 80, 2, 2, 2], "n": [100] * 7}), {"denominator": "n"}, 4),
        ("xbar", pd.DataFrame({"x": [1,1,2,2,3,3,4,4], "y": [10,11,10,11,100,101,10,11]}), {}, 3),
        ("s", pd.DataFrame({"x": [1,1,2,2,3,3,4,4], "y": [10,11,10,11,50,150,10,11]}), {}, 3),
    ],
)
def test_excluded_rows_clear_signal_rule_text_for_limit_charts(chart_type, frame, kwargs, excluded_x):
    # The excluded point/subgroup is intentionally extreme. Without the final
    # cleanup step it would keep a non-empty signal_rule even though signal is
    # masked to False, which is misleading in exported tables.
    out = qic_table(frame, "x", "y", chart=chart_type, exclude_points=[excluded_x], **kwargs)
    row = out.loc[out["x"] == excluded_x].iloc[0]
    assert bool(row["excluded"])
    assert not bool(row["signal"])
    assert row["signal_rule"] == ""
    if "special_cause" in out.columns:
        assert not bool(row["special_cause"])
    if "special_cause_rule" in out.columns:
        assert row["special_cause_rule"] == ""
