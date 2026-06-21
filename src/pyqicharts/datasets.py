"""Small example datasets for pyqicharts."""
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
