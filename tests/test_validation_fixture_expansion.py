from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from pyqicharts import pareto_table, qic_table


ROOT = Path(__file__).resolve().parents[1]


def test_expanded_validation_fixture_manifest_files_exist():
    folder = ROOT / "validation_data" / "expanded"
    manifest = pd.read_csv(folder / "fixture_manifest.csv")
    for _, row in manifest.iterrows():
        for column in ["normal_example", "process_change_example", "edge_case_example"]:
            path = folder / row[column]
            assert path.exists(), f"missing fixture for {row['chart']}: {path.name}"


def test_expanded_validation_fixture_covers_all_chart_families():
    manifest = pd.read_csv(ROOT / "validation_data" / "expanded" / "fixture_manifest.csv")
    assert set(manifest["chart"]) == {
        "run", "i", "mr", "c", "p", "u", "xbar", "s", "g", "t", "p_prime", "u_prime", "pareto"
    }


def _fixture_kwargs(chart, data):
    if chart == "pareto":
        return {
            "category": "category" if "category" in data else data.columns[0],
            "count": "count" if "count" in data else (data.columns[1] if len(data.columns) > 1 else None),
        }
    kwargs = {"x": "x", "y": "y", "chart": chart}
    if chart in {"p", "u", "p_prime", "u_prime"}:
        kwargs["denominator"] = "n" if "n" in data else "denominator"
    if chart in {"p_prime", "u_prime"}:
        kwargs["expected"] = "expected"
    return kwargs


def _rounded_expected_shape(chart, data):
    if chart == "pareto":
        actual = pareto_table(data, **_fixture_kwargs(chart, data))
    else:
        actual = qic_table(data, **_fixture_kwargs(chart, data))
        columns = [
            col
            for col in [
                "chart",
                "point_index",
                "segment_id",
                "centre",
                "lcl",
                "ucl",
                "plot_value",
                "signal",
                "special_cause",
                "signal_rule",
                "special_cause_rule",
            ]
            if col in actual
        ]
        actual = actual[columns]
    actual = actual.copy()
    for col in actual.select_dtypes(include="number").columns:
        actual[col] = actual[col].round(6)
    return actual


def test_expanded_validation_fixtures_reproduce_expected_outputs():
    folder = ROOT / "validation_data" / "expanded"
    expected_folder = ROOT / "validation_data" / "expanded_expected_outputs"
    manifest = pd.read_csv(expected_folder / "expected_manifest.csv")
    for _, row in manifest.iterrows():
        data = pd.read_csv(folder / row["input_file"])
        actual = _rounded_expected_shape(row["chart"], data)
        expected = pd.read_csv(expected_folder / row["expected_file"]).fillna("")
        actual = actual.fillna("")
        assert_frame_equal(actual.reset_index(drop=True), expected.reset_index(drop=True), check_dtype=False)
