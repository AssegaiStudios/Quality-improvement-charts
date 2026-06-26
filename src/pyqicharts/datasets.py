"""Small example and sample datasets for pyqicharts.

The bundled datasets are synthetic. They are designed for examples, tests and
new-user exploration, not for clinical benchmarking.
"""
from __future__ import annotations

import pandas as pd


def infections_between_events() -> pd.DataFrame:
    """Return synthetic cases-between-infection event data for a G chart."""

    return pd.DataFrame(
        {
            "case_number": range(1, 13),
            "cases_between_events": [22, 18, 25, 21, 19, 24, 85, 20, 23, 17, 2, 21],
        }
    )


def sample_healthcare_qi_data() -> pd.DataFrame:
    """Return a broad sample dataset end users can use for first experiments."""

    return pd.DataFrame(
        {
            "month": list(range(1, 13)),
            "wait_time": [34, 33, 35, 36, 34, 32, 31, 28, 27, 26, 25, 24],
            "falls": [6, 5, 7, 6, 5, 4, 5, 3, 4, 3, 2, 3],
            "sample_size": [420, 415, 430, 425, 440, 435, 450, 460, 455, 470, 465, 475],
            "readmissions_observed": [21, 22, 20, 23, 21, 20, 19, 17, 18, 16, 15, 16],
            "readmissions_expected": [20.0, 20.5, 20.2, 21.0, 20.8, 20.1, 19.8, 19.5, 19.2, 18.9, 18.5, 18.3],
            "cases_between_infections": [18, 20, 21, 19, 22, 24, 30, 28, 35, 40, 38, 42],
            "days_between_incidents": [12, 15, 14, 18, 20, 22, 25, 30, 28, 35, 38, 40],
        }
    )


def sample_subgroup_measurements() -> pd.DataFrame:
    """Return observation-level subgroup data for Xbar and S chart examples."""

    rows = []
    measurements = [
        [10.1, 10.4, 10.2, 10.3],
        [10.3, 10.5, 10.4, 10.6],
        [10.2, 10.1, 10.3, 10.4],
        [10.6, 10.8, 10.7, 10.9],
        [10.5, 10.6, 10.4, 10.7],
        [10.7, 10.9, 10.8, 11.0],
    ]
    for subgroup, values in enumerate(measurements, start=1):
        for observation, value in enumerate(values, start=1):
            rows.append({"subgroup": subgroup, "observation": observation, "value": value})
    return pd.DataFrame(rows)


def days_between_serious_incidents() -> pd.DataFrame:
    """Return synthetic days-between-serious-incidents data for a T chart."""

    return pd.DataFrame(
        {
            "event_number": range(1, 13),
            "days_between_events": [31, 27, 35, 29, 33, 30, 120, 28, 32, 26, 1, 34],
        }
    )


def days_between_falls_with_harm() -> pd.DataFrame:
    """Return synthetic days-between-falls-with-harm data for a T chart."""

    return pd.DataFrame(
        {
            "event_number": range(1, 13),
            "days_between_events": [14, 17, 12, 16, 15, 13, 19, 18, 55, 11, 15, 2],
        }
    )


def risk_adjusted_readmissions() -> pd.DataFrame:
    """Return synthetic observed/expected readmissions data for a P-prime chart."""

    return pd.DataFrame(
        {
            "month": range(1, 13),
            "observed": [18, 21, 19, 22, 20, 24, 23, 42, 21, 20, 18, 19],
            "expected": [20.0, 20.5, 19.8, 21.0, 20.2, 21.5, 22.0, 22.1, 21.0, 20.6, 19.7, 20.1],
        }
    )


def risk_adjusted_infection_rates() -> pd.DataFrame:
    """Return synthetic observed/expected infection data for a U-prime chart."""

    return pd.DataFrame(
        {
            "month": range(1, 13),
            "observed": [4, 5, 3, 4, 6, 5, 4, 12, 5, 4, 3, 5],
            "expected": [4.5, 4.8, 4.2, 4.4, 4.9, 5.1, 4.7, 5.0, 4.6, 4.5, 4.3, 4.8],
        }
    )
