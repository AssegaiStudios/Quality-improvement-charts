import pandas as pd
import pytest
from pyqicharts import pareto_table, qic_table

def sample_df():
    return pd.DataFrame({"month": range(1,7), "value": [10,11,10,13,12,14], "count": [3,4,2,5,6,4], "denominator": [100,110,95,105,115,108], "category": ["A","B","A","C","A","B"]})

def test_run_qic_table_uses_median_label():
    out = qic_table(sample_df(), "month", "value", "run"); assert out["centre_label"].iloc[0] == "Median"; assert out["centre"].iloc[0] == 11.5

def test_i_qic_table_uses_mean_label():
    out = qic_table(sample_df(), "month", "value", "i"); assert out["centre_label"].iloc[0] == "Mean"; assert out["ucl"].notna().all()

def test_mr_qic_table_has_moving_ranges():
    out = qic_table(sample_df(), "month", "value", "mr"); assert out["centre_label"].iloc[0] == "Mean moving range"; assert out["lcl"].iloc[0] == 0

def test_c_chart_table_has_count_limits():
    out = qic_table(sample_df(), "month", "count", "c"); assert out["centre_label"].iloc[0] == "Mean count"; assert out["lcl"].ge(0).all()

def test_p_chart_requires_denominator():
    with pytest.raises(ValueError): qic_table(sample_df(), "month", "count", "p")

def test_p_chart_table_has_variable_limits():
    out = qic_table(sample_df(), "month", "count", "p", denominator="denominator"); assert out["centre_label"].iloc[0] == "Mean proportion"; assert out["plot_value"].between(0,1).all()

def test_u_chart_table_has_rate_limits():
    out = qic_table(sample_df(), "month", "count", "u", denominator="denominator"); assert out["centre_label"].iloc[0] == "Mean rate"; assert out["plot_value"].ge(0).all()

def test_pareto_table_counts_and_percentages():
    out = pareto_table(sample_df(), "category"); assert out["count"].sum() == 6; assert round(out["cumulative_percent"].iloc[-1], 6) == 100
