from pathlib import Path

import pandas as pd


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
