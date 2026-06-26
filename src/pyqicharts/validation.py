"""Validation dataset helpers.

Validation files in this project are plain CSVs so they can be reviewed by
humans, spreadsheets and tests. This helper keeps CSV loading consistent.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_validation_csv(path: str | Path) -> pd.DataFrame:
    """Read a validation CSV file."""

    return pd.read_csv(path)
