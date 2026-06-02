import pandas as pd

from pyqicharts import paretochart, qic


def test_qic_run_returns_summary():
    df = pd.DataFrame({"week": range(1, 7), "value": [1, 2, 3, 4, 5, 6]})
    result = qic(df, x="week", y="value", chart="run")
    summary = result.summary()
    assert summary["chart"] == "run"
    assert summary["n"] == 6
    assert "runs" in summary


def test_qic_i_returns_limits():
    df = pd.DataFrame({"week": range(1, 7), "value": [10, 11, 9, 10, 10, 12]})
    result = qic(df, x="week", y="value", chart="i")
    assert result.lcl is not None
    assert result.ucl is not None


def test_paretochart_counts_categories():
    df = pd.DataFrame({"type": ["A", "B", "A", "C", "A"]})
    result = paretochart(df, category="type")
    assert result.table.loc[0, "count"] == 3
