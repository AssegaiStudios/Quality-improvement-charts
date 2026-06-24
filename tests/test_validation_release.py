import runpy
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from pandas.testing import assert_frame_equal

import pyqicharts
from pyqicharts import qic_table


ROOT = Path(__file__).resolve().parents[1]


def _rounded_core(out):
    cols = ["centre", "lcl", "ucl", "plot_value", "signal"]
    rounded = out[cols].copy()
    for col in ["centre", "lcl", "ucl", "plot_value"]:
        rounded[col] = rounded[col].round(6)
    return rounded


def test_validation_datasets_reproduce_expected_outputs():
    cases = [
        ("xmr", "xmr.csv", "xmr_expected.csv", dict(x="month", y="value", chart="i")),
        ("g", "g_chart.csv", "g_chart_expected.csv", dict(x="case_number", y="cases_between_events", chart="g")),
        ("t", "t_chart.csv", "t_chart_expected.csv", dict(x="event_number", y="days_between_events", chart="t")),
        ("p_prime", "p_prime.csv", "p_prime_expected.csv", dict(x="month", y="observed", expected="expected", chart="p_prime")),
    ]
    for _, dataset, expected, kwargs in cases:
        data = pd.read_csv(ROOT / "validation" / "datasets" / dataset)
        actual = _rounded_core(qic_table(data, **kwargs))
        expected_df = pd.read_csv(ROOT / "validation" / "expected_outputs" / expected)
        assert_frame_equal(actual.reset_index(drop=True), expected_df, check_dtype=False)


def test_examples_run_without_error(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for example in sorted((ROOT / "examples").glob("*.py")):
        runpy.run_path(str(example), run_name="__main__")
        plt.close("all")


def test_package_metadata_version_matches():
    assert pyqicharts.__version__ == "0.9.0"


def test_required_release_files_exist():
    required = [
        "CHANGELOG.md",
        "LICENSE",
        "README.md",
        "pyproject.toml",
        ".github/workflows/tests.yml",
        "validation/README.md",
        "validation/acceptance_checklist.md",
    ]
    for path in required:
        assert (ROOT / path).exists(), path
