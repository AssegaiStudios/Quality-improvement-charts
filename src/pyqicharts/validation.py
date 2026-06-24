"""Validation dataset helpers."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_validation_csv(path: str | Path) -> pd.DataFrame:
    """Read a validation CSV file."""

    return pd.read_csv(path)
