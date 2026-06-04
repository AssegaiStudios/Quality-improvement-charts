import matplotlib
matplotlib.use("Agg")

import pandas as pd

from pyqicharts import paretochart, qic


def sample_df():
    return pd.DataFrame({
        "month": range(1, 7),
        "value": [10, 11, 10, 13, 12, 14],
        "category": ["A", "B", "A", "C", "A", "B"],
    })


def test_qic_run_returns_result():
    result = qic(sample_df(), x="month", y="value", chart="run")
    assert result.chart == "run"
    assert result.anhoej is not None
    assert result.figure is not None
    assert result.table is not None


def test_qic_i_returns_limits():
    result = qic(sample_df(), x="month", y="value", chart="i")
    assert result.chart == "i"
    assert result.ucl is not None
    assert result.lcl is not None


def test_qic_mr_returns_result():
    result = qic(sample_df(), x="month", y="value", chart="mr")
    assert result.chart == "mr"
    assert result.lcl == 0.0
    assert result.ucl is not None


def test_paretochart_returns_table():
    result = paretochart(sample_df(), category="category")
    assert result.table["count"].sum() == 6
    assert result.figure is not None
