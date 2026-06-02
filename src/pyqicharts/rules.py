"""Rules for detecting non-random variation in QI charts."""

from __future__ import annotations

from dataclasses import dataclass
from math import comb
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class AnhoejResult:
    """Result from Anhøj-style run-chart diagnostics.

    The implementation intentionally starts conservatively: it calculates runs,
    crossings, longest run, and simple probability estimates for unusually long
    runs and few crossings. These diagnostics are suitable for early package use
    and can be statistically refined as the package matures.
    """

    median: float
    n_used: int
    runs: int
    crossings: int
    longest_run: int
    signal_long_run: bool
    signal_few_crossings: bool


def _drop_points_on_centre_line(values: Iterable[float], centre: float) -> np.ndarray:
    arr = np.asarray(list(values), dtype=float)
    arr = arr[~np.isnan(arr)]
    return arr[arr != centre]


def _signs(values: np.ndarray, centre: float) -> np.ndarray:
    return np.where(values > centre, 1, -1)


def _runs(signs: np.ndarray) -> int:
    if signs.size == 0:
        return 0
    return int(1 + np.sum(signs[1:] != signs[:-1]))


def _crossings(signs: np.ndarray) -> int:
    if signs.size < 2:
        return 0
    return int(np.sum(signs[1:] != signs[:-1]))


def _longest_run(signs: np.ndarray) -> int:
    if signs.size == 0:
        return 0
    longest = current = 1
    for idx in range(1, signs.size):
        if signs[idx] == signs[idx - 1]:
            current += 1
        else:
            longest = max(longest, current)
            current = 1
    return max(longest, current)


def _long_run_limit(n: int) -> int:
    """Approximate 5% upper limit for longest run in random binary sequences.

    The limit is intentionally conservative and mirrors common run-chart practice
    for small-to-medium healthcare improvement datasets.
    """

    if n < 10:
        return n + 1
    if n < 20:
        return 8
    if n < 30:
        return 9
    if n < 50:
        return 10
    if n < 100:
        return 11
    return 12


def _expected_crossings(n: int) -> float:
    # For a random sequence split around a median, expected crossings are close
    # to (n - 1) / 2 when the two groups are approximately balanced.
    return (n - 1) / 2


def _few_crossings_limit(n: int) -> int:
    """Approximate lower 5% crossing limit using a normal approximation."""

    if n < 10:
        return -1
    mean = _expected_crossings(n)
    sd = np.sqrt((n - 1) / 4)
    return int(np.floor(mean - 1.96 * sd))


def anhoej_rules(values: Iterable[float], centre: float | None = None) -> AnhoejResult:
    """Calculate run-chart diagnostics inspired by the Anhøj rules.

    Parameters
    ----------
    values:
        Sequence of measurements ordered by time.
    centre:
        Optional centre line. Defaults to the median of ``values``.

    Returns
    -------
    AnhoejResult
        Runs, crossings, longest run, and signal flags.
    """

    raw = np.asarray(list(values), dtype=float)
    raw = raw[~np.isnan(raw)]
    if raw.size == 0:
        raise ValueError("values must contain at least one non-missing number")

    median = float(np.median(raw) if centre is None else centre)
    used = _drop_points_on_centre_line(raw, median)
    signs = _signs(used, median) if used.size else np.array([], dtype=int)

    n = int(used.size)
    runs = _runs(signs)
    crossings = _crossings(signs)
    longest = _longest_run(signs)

    return AnhoejResult(
        median=median,
        n_used=n,
        runs=runs,
        crossings=crossings,
        longest_run=longest,
        signal_long_run=longest >= _long_run_limit(n),
        signal_few_crossings=crossings <= _few_crossings_limit(n),
    )


def shewhart_rule(values: Iterable[float], centre: float, sigma: float) -> pd.Series:
    """Return True for points outside 3-sigma control limits."""

    arr = np.asarray(list(values), dtype=float)
    if sigma < 0:
        raise ValueError("sigma must be non-negative")
    upper = centre + 3 * sigma
    lower = centre - 3 * sigma
    return pd.Series((arr > upper) | (arr < lower))
