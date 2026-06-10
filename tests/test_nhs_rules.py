import pandas as pd

from pyqicharts import nhs_xmr_signals, qic, qic_table


def test_point_above_ucl_detected():
    out = qic_table(pd.DataFrame({"month": range(13), "value": [10] * 12 + [20]}), "month", "value", "i")
    last = out.iloc[-1]
    assert last["outside_ucl"]
    assert last["signal"]
    assert last["signal_rule"] == "above UCL"


def test_point_below_lcl_detected():
    out = qic_table(pd.DataFrame({"month": range(13), "value": [10] * 12 + [0]}), "month", "value", "i")
    last = out.iloc[-1]
    assert last["outside_lcl"]
    assert last["signal"]
    assert last["signal_rule"] == "below LCL"


def test_high_is_good_improvement_signal():
    signals = nhs_xmr_signals(pd.Series([20.0]), centre=10.0, lcl=5.0, ucl=15.0, improvement="high is good")
    assert signals["special_cause_type"].iloc[0] == "improvement"


def test_high_is_good_concern_signal():
    signals = nhs_xmr_signals(pd.Series([0.0]), centre=10.0, lcl=5.0, ucl=15.0, improvement="high is good")
    assert signals["special_cause_type"].iloc[0] == "concern"


def test_low_is_good_improvement_signal():
    signals = nhs_xmr_signals(pd.Series([0.0]), centre=10.0, lcl=5.0, ucl=15.0, improvement="low is good")
    assert signals["special_cause_type"].iloc[0] == "improvement"


def test_low_is_good_concern_signal():
    signals = nhs_xmr_signals(pd.Series([20.0]), centre=10.0, lcl=5.0, ucl=15.0, improvement="low is good")
    assert signals["special_cause_type"].iloc[0] == "concern"


def test_shift_detection():
    out = qic_table(pd.DataFrame({"month": range(16), "value": [10] * 8 + [12] * 8}), "month", "value", "i")
    assert out["shift"].sum() == 16
    assert out["special_cause_rule"].str.contains("shift").any()


def test_trend_detection():
    out = qic_table(pd.DataFrame({"month": range(6), "value": [1, 2, 3, 4, 5, 6]}), "month", "value", "i")
    assert out["trend"].sum() == 6
    assert out["special_cause_rule"].str.contains("trend").any()


def test_no_false_positive_signal_on_stable_data():
    out = qic_table(pd.DataFrame({"month": range(12), "value": [10, 11] * 6}), "month", "value", "i")
    assert not out["signal"].any()


def test_qic_colours_interpreted_signals():
    result = qic(
        pd.DataFrame({"month": range(13), "value": [10] * 12 + [20]}),
        "month",
        "value",
        chart="i",
        improvement="high is good",
    )
    assert result.table["special_cause_type"].iloc[-1] == "improvement"
    assert result.figure is not None
