"""Example data and configuration helpers for Excel Companion users."""
from __future__ import annotations

import pandas as pd

from .config import config_defaults_frame
from .excel_io import sample_excel_data


def example_data() -> pd.DataFrame:
    """Return sample data suitable for run, I, P, U, Xbar, P-prime and Pareto charts."""

    return sample_excel_data()


def example_config() -> pd.DataFrame:
    """Return the default two-column Config table."""

    return config_defaults_frame()

