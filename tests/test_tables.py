import pandas as pd

from pyqicharts import pareto_table, qic_table


def sample_df():
    return pd.DataFrame({
        "month": range(1, 7),
        "value": [10, 11, 10, 13, 12, 14],
        "category": ["A", "B", "A", "C", "A", "B"],
    })


def test_run_qic_table_has_expected_columns():
    out = qic_table(sample_df(), x="month", y="value", chart="run")
    for col in ["centre", "lcl", "ucl", "signal", "signal_rule"]:
        assert col in out.columns
    assert out["centre"].iloc[0] == 11.5


def test_i_qic_table_has_control_limits():
    out = qic_table(sample_df(), x="month", y="value", chart="i")
    assert out["ucl"].notna().all()
    assert out["lcl"].notna().all()
    assert "moving_range" in out.columns


def test_mr_qic_table_has_moving_ranges():
    out = qic_table(sample_df(), x="month", y="value", chart="mr")
    assert out["moving_range"].isna().iloc[0]
    assert out["moving_range"].notna().sum() == 5
    assert out["lcl"].iloc[0] == 0


def test_pareto_table_counts_and_percentages():
    out = pareto_table(sample_df(), category="category")
    assert list(out.columns) == ["category", "count", "percent", "cumulative_count", "cumulative_percent"]
    assert out["count"].sum() == 6
    assert round(out["cumulative_percent"].iloc[-1], 6) == 100
