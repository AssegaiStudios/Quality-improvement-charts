"""Regression checks for the interim chart validation fixtures.

These tests prove the current implementation is stable against the bundled
expected outputs. They are not qicharts/qicharts2 parity tests; those require
external reference outputs and remain tracked in PARITY_REPORT.md.
"""

from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from pyqicharts import qic_table


ROOT = Path(__file__).resolve().parents[2]


CASES = {
    "run": dict(x="month", y="value", chart="run"),
    "i": dict(x="month", y="value", chart="i"),
    "mr": dict(x="month", y="value", chart="mr"),
    "c": dict(x="month", y="count", chart="c"),
    "p": dict(x="month", y="events", denominator="denominator", chart="p"),
    "u": dict(x="month", y="events", denominator="denominator", chart="u"),
    "xbar": dict(x="subgroup", y="value", chart="xbar"),
    "s": dict(x="subgroup", y="value", chart="s"),
    "g": dict(x="case_number", y="cases_between_events", chart="g"),
    "t": dict(x="event_number", y="days_between_events", chart="t"),
    "p_prime": dict(x="month", y="observed", expected="expected", chart="p_prime"),
    "u_prime": dict(x="month", y="observed", expected="expected", chart="u_prime"),
}


def _normalise_output(table: pd.DataFrame) -> pd.DataFrame:
    columns = ["centre", "ucl", "lcl", "signal", "signal_rule", "special_cause_label"]
    out = table.copy()
    for column in columns:
        if column not in out.columns:
            out[column] = ""
    out = out[columns].copy()
    for column in ["centre", "ucl", "lcl"]:
        out[column] = pd.to_numeric(out[column], errors="coerce").round(6)
    for column in ["signal_rule", "special_cause_label"]:
        out[column] = out[column].fillna("").astype(str)
    return out


def test_chart_validation_data_matches_expected_outputs():
    for name, kwargs in CASES.items():
        data = pd.read_csv(ROOT / "validation_data" / "inputs" / f"{name}.csv")
        actual = _normalise_output(qic_table(data, **kwargs))
        expected = pd.read_csv(ROOT / "validation_data" / "expected_outputs" / f"{name}_expected.csv")
        expected = _normalise_output(expected)
        assert_frame_equal(actual.reset_index(drop=True), expected, check_dtype=False)
