import matplotlib
matplotlib.use("Agg")
import pandas as pd
import pytest

from pyqicharts import qic, qic_table, risk_adjusted_infection_rates, risk_adjusted_readmissions


def test_p_prime_table_contains_observed_expected_and_adjusted_values():
    df = risk_adjusted_readmissions()
    out = qic_table(df, "month", "observed", chart="p_prime", expected="expected")
    assert out["chart"].iloc[0] == "p_prime"
    assert {"observed", "expected", "oe_ratio", "risk_adjusted_value", "adjusted_rate"}.issubset(out.columns)
    assert out["centre"].iloc[0] == 1.0
    assert out["plot_value"].iloc[0] == df["observed"].iloc[0] / df["expected"].iloc[0]


def test_u_prime_table_contains_observed_expected_and_adjusted_values():
    df = risk_adjusted_infection_rates()
    out = qic_table(df, "month", "observed", chart="u_prime", expected="expected")
    assert out["chart"].iloc[0] == "u_prime"
    assert {"observed", "expected", "oe_ratio", "risk_adjusted_value", "adjusted_rate"}.issubset(out.columns)
    assert out["centre"].iloc[0] == 1.0
    assert out["ucl"].notna().all()


def test_zero_expected_values_handled_safely():
    df = pd.DataFrame({"month": [1, 2, 3], "observed": [1, 2, 3], "expected": [1.0, 0.0, 2.0]})
    out = qic_table(df, "month", "observed", chart="p_prime", expected="expected")
    assert out["expected_zero"].tolist() == [False, True, False]
    assert pd.isna(out["plot_value"].iloc[1])
    assert not out["signal"].iloc[1]


def test_risk_adjusted_chart_rendering_works():
    df = risk_adjusted_readmissions()
    result = qic(df, "month", "observed", chart="p_prime", expected="expected")
    assert result.figure is not None
    assert result.table["chart"].iloc[0] == "p_prime"


def test_invalid_expected_column_raises_clear_error():
    df = risk_adjusted_readmissions()
    with pytest.raises(KeyError, match="expected column not found"):
        qic_table(df, "month", "observed", chart="p_prime", expected="missing")


def test_p_prime_requires_expected_column():
    df = risk_adjusted_readmissions()
    with pytest.raises(ValueError, match="requires an expected column"):
        qic_table(df, "month", "observed", chart="p_prime")


def test_negative_expected_values_raise_clear_error():
    df = pd.DataFrame({"month": [1, 2], "observed": [1, 2], "expected": [1.0, -1.0]})
    with pytest.raises(ValueError, match="expected values must be non-negative"):
        qic_table(df, "month", "observed", chart="u_prime", expected="expected")
