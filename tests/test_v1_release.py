from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import pyqicharts
from pyqicharts import qic, qic_table, sample_healthcare_qi_data, sample_subgroup_measurements


ROOT = Path(__file__).resolve().parents[1]


def test_version_is_1_3_4():
    assert pyqicharts.__version__ == "1.3.4"


def test_sample_healthcare_dataset_is_available_as_function_and_csv():
    from_function = sample_healthcare_qi_data()
    from_csv = pd.read_csv(ROOT / "sample_data" / "sample_healthcare_qi_data.csv")
    assert list(from_function.columns) == list(from_csv.columns)
    assert len(from_function) == len(from_csv) == 12


def test_sample_subgroup_dataset_supports_xbar_and_s():
    df = sample_subgroup_measurements()
    assert {"subgroup", "observation", "value"}.issubset(df.columns)
    assert len(df) == 24


def test_xbar_chart_table_calculations():
    out = qic_table(sample_subgroup_measurements(), "subgroup", "value", chart="xbar")
    assert out["chart"].iloc[0] == "xbar"
    assert {"subgroup_mean", "subgroup_std", "subgroup_n"}.issubset(out.columns)
    assert out["centre_label"].iloc[0] == "Grand mean"
    assert out["ucl"].iloc[0] > out["centre"].iloc[0] > out["lcl"].iloc[0]


def test_s_chart_table_calculations():
    out = qic_table(sample_subgroup_measurements(), "subgroup", "value", chart="s")
    assert out["chart"].iloc[0] == "s"
    assert {"subgroup_mean", "subgroup_std", "subgroup_n"}.issubset(out.columns)
    assert out["centre_label"].iloc[0] == "Mean subgroup standard deviation"
    assert out["ucl"].iloc[0] > out["centre"].iloc[0] >= out["lcl"].iloc[0]


def test_xbar_and_s_rendering_smoke():
    plt.close("all")
    xbar = qic(sample_subgroup_measurements(), "subgroup", "value", chart="xbar")
    s_chart = qic(sample_subgroup_measurements(), "subgroup", "value", chart="s")
    assert xbar.figure is not None
    assert s_chart.figure is not None
    plt.close(xbar.figure)
    plt.close(s_chart.figure)
