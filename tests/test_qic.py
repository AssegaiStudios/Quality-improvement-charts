import matplotlib
matplotlib.use("Agg")
import pandas as pd
from pyqicharts import pareto_chart, paretochart, qic

def sample_df():
    return pd.DataFrame({"month": range(1,7), "value": [10,11,10,13,12,14], "count": [3,4,2,5,6,4], "denominator": [100,110,95,105,115,108], "category": ["A","B","A","C","A","B"]})

def test_qic_run_returns_result():
    result = qic(sample_df(), "month", "value", chart="run", theme="nhs"); assert result.chart == "run"; assert result.centre_label == "Median"; assert result.anhoej is not None

def test_qic_i_returns_limits():
    result = qic(sample_df(), "month", "value", chart="i"); assert result.chart == "i"; assert result.centre_label == "Mean"; assert result.ucl is not None

def test_qic_mr_returns_result():
    result = qic(sample_df(), "month", "value", chart="mr"); assert result.chart == "mr"; assert result.centre_label == "Mean moving range"; assert result.lcl == 0.0

def test_qic_c_returns_result():
    result = qic(sample_df(), "month", "count", chart="c"); assert result.chart == "c"; assert result.centre_label == "Mean count"

def test_qic_p_returns_result():
    result = qic(sample_df(), "month", "count", denominator="denominator", chart="p"); assert result.chart == "p"; assert result.centre_label == "Mean proportion"

def test_qic_u_returns_result():
    result = qic(sample_df(), "month", "count", denominator="denominator", chart="u"); assert result.chart == "u"; assert result.centre_label == "Mean rate"

def test_paretochart_returns_table():
    result = paretochart(sample_df(), "category", theme="nhs"); assert result.table["count"].sum() == 6; assert result.figure is not None

def test_pareto_chart_alias_returns_table():
    result = pareto_chart(sample_df(), "category", theme="nhs"); assert result.table["count"].sum() == 6; assert result.figure is not None
