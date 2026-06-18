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
