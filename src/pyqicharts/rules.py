"""Rule calculations used by pyqicharts."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import NormalDist
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class AnhoejResult:
    """Summary of Anhøj-style run chart diagnostics.

    Notes
    -----
    Values exactly equal to the median are excluded from the runs/crossings
    calculations, following common run chart practice.
    """

    median: float
    n_used: int
    runs: int
    crossings: int
    longest_run: int
    expected_longest_run: int
    lower_crossings_limit: int
    signal_long_run: bool
    signal_few_crossings: bool

    @property
    def any_signal(self) -> bool:
        """Return True when any Anhøj diagnostic is triggered."""

        return self.signal_long_run or self.signal_few_crossings


def _longest_run(signs: list[int]) -> int:
    if not signs:
        return 0
    longest = 1
    current = 1
    previous = signs[0]
    for sign in signs[1:]:
        if sign == previous:
            current += 1
        else:
            current = 1
            previous = sign
        longest = max(longest, current)
    return longest


def _runs(signs: list[int]) -> int:
    if not signs:
        return 0
    return 1 + sum(1 for a, b in zip(signs, signs[1:]) if a != b)


def _crossings(signs: list[int]) -> int:
    if not signs:
        return 0
    return sum(1 for a, b in zip(signs, signs[1:]) if a != b)


def _expected_longest_run(n: int) -> int:
    """Approximate 95th percentile for longest run in random binary sequence.

    This approximation is intentionally conservative for early releases. It
    behaves similarly to published run chart reference tables for small and
    medium sequences without needing bundled lookup tables.
    """

    if n <= 0:
        return 0
    if n < 10:
        return n
    # Approximate upper 95% longest run threshold.
    return int(np.ceil(np.log2(n) + 3))


def _lower_crossings_limit(n: int) -> int:
    """Approximate lower 5% limit for crossings in a random binary sequence."""

    if n <= 1:
        return 0
    # Crossings is Binomial(n - 1, 0.5) under random above/below median signs.
    mean = (n - 1) * 0.5
    sd = np.sqrt((n - 1) * 0.25)
    z05 = NormalDist().inv_cdf(0.05)
    return max(0, int(np.floor(mean + z05 * sd)))


def anhoej_rules(values: Iterable[float]) -> AnhoejResult:
    """Calculate Anhøj-style run chart diagnostics.

    Parameters
    ----------
    values:
        Ordered numeric observations.

    Returns
    -------
    AnhoejResult
        Median, runs, crossings, longest run and signal flags.
    """

    series = pd.Series(values).dropna()
    median = float(series.median()) if len(series) else float("nan")

    if len(series) == 0:
        return AnhoejResult(
            median=median,
            n_used=0,
            runs=0,
            crossings=0,
            longest_run=0,
            expected_longest_run=0,
            lower_crossings_limit=0,
            signal_long_run=False,
            signal_few_crossings=False,
        )

    signs = [1 if value > median else -1 for value in series if value != median]
    n_used = len(signs)
    runs = _runs(signs)
    crossings = _crossings(signs)
    longest = _longest_run(signs)
    expected_longest = _expected_longest_run(n_used)
    lower_cross = _lower_crossings_limit(n_used)

    return AnhoejResult(
        median=median,
        n_used=n_used,
        runs=runs,
        crossings=crossings,
        longest_run=longest,
        expected_longest_run=expected_longest,
        lower_crossings_limit=lower_cross,
        signal_long_run=longest > expected_longest if expected_longest else False,
        signal_few_crossings=crossings < lower_cross if n_used > 1 else False,
    )


def shewhart_3sigma_signals(values: Iterable[float], centre: float, sigma: float) -> pd.Series:
    """Return True for observations outside centre ± 3 sigma."""

    s = pd.Series(values)
    if sigma is None or np.isnan(sigma) or sigma <= 0:
        return pd.Series([False] * len(s), index=s.index)
    lcl = centre - 3 * sigma
    ucl = centre + 3 * sigma
    return (s < lcl) | (s > ucl)
