"""Run-chart rule calculations.

The default `anhoej` method follows the published run-chart convention used by
Anhøj and Wentzel-Larsen: observations equal to the median are removed from the
run/crossing sequence, longest runs are judged with the Schilling-style
logarithmic critical length, and unusually few crossings use the exact lower
tail of a binomial distribution with p=0.5.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import comb, log2
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class AnhoejResult:
    """Summary of run-chart diagnostics for a chosen centre line."""

    median: float
    n_used: int
    runs: int
    crossings: int
    longest_run: int
    expected_longest_run: int
    lower_crossings_limit: int
    signal_long_run: bool
    signal_few_crossings: bool
    method: str = "anhoej"

    @property
    def any_signal(self) -> bool:
        return self.signal_long_run or self.signal_few_crossings


def _clean_series(values: Iterable[float], exclude: Iterable[bool] | None = None) -> pd.Series:
    """Return numeric non-missing observations after optional exclusions."""

    series = pd.Series(values, dtype="float64")
    if exclude is not None:
        flags = pd.Series(list(exclude), index=series.index).reindex(series.index, fill_value=False)
        series = series[~flags.astype(bool)]
    return series.dropna()


def _signs(values: pd.Series, centre: float) -> list[int]:
    """Return signs relative to centre, omitting centre-line ties."""

    return [1 if value > centre else -1 for value in values if value != centre]


def _longest_run(signs: list[int]) -> int:
    if not signs:
        return 0
    longest = current = 1
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
    return 1 + sum(1 for left, right in zip(signs, signs[1:]) if left != right)


def _crossings(signs: list[int]) -> int:
    if not signs:
        return 0
    return sum(1 for left, right in zip(signs, signs[1:]) if left != right)


def _longest_run_limit(n: int) -> int:
    """Return the critical longest-run length for n useful observations."""

    if n <= 0:
        return 0
    if n < 10:
        return n
    return int(np.ceil(log2(n) + 3))


def _binom_cdf(k: int, trials: int) -> float:
    """Exact lower-tail probability for Binomial(trials, 0.5)."""

    if k < 0:
        return 0.0
    return sum(comb(trials, i) for i in range(0, min(k, trials) + 1)) / (2**trials)


def _lower_crossings_limit(n: int, alpha: float = 0.05) -> int:
    """Return the exact lower crossing threshold.

    Crossings among n useful observations have n-1 opportunities. The returned
    value is the largest crossing count whose lower-tail probability is within
    alpha. A chart signals when observed crossings are below this value.
    """

    trials = n - 1
    if trials <= 0:
        return 0
    limit = 0
    for crossings in range(trials + 1):
        if _binom_cdf(crossings, trials) <= alpha:
            limit = crossings
        else:
            break
    return limit


def _candidate_centres(series: pd.Series) -> list[float]:
    """Return deterministic centre candidates for bestbox/cutbox search."""

    values = sorted(series.dropna().unique())
    if not values:
        return [float("nan")]
    candidates = set(float(v) for v in values)
    candidates.update(float((left + right) / 2) for left, right in zip(values, values[1:]))
    candidates.add(float(series.median()))
    return sorted(candidates)


def _score_result(result: AnhoejResult) -> tuple[int, int, int, float]:
    """Rank centre choices by signal absence and distance from thresholds."""

    return (
        0 if result.any_signal else 1,
        result.lower_crossings_limit - result.crossings,
        result.longest_run - result.expected_longest_run,
        -abs(result.median),
    )


def _evaluate(values: pd.Series, centre: float, method: str) -> AnhoejResult:
    signs = _signs(values, centre)
    n_used = len(signs)
    runs = _runs(signs)
    crossings = _crossings(signs)
    longest = _longest_run(signs)
    longest_limit = _longest_run_limit(n_used)
    crossing_limit = _lower_crossings_limit(n_used)
    return AnhoejResult(
        median=float(centre),
        n_used=n_used,
        runs=runs,
        crossings=crossings,
        longest_run=longest,
        expected_longest_run=longest_limit,
        lower_crossings_limit=crossing_limit,
        signal_long_run=bool(longest > longest_limit) if longest_limit else False,
        signal_few_crossings=bool(crossings < crossing_limit) if n_used > 1 else False,
        method=method,
    )


def anhoej_rules(values: Iterable[float], exclude: Iterable[bool] | None = None, method: str = "anhoej") -> AnhoejResult:
    """Calculate run-chart diagnostics.

    `method="anhoej"` uses the ordinary median. `method="bestbox"` searches
    deterministic observed/midpoint centre candidates and chooses the centre
    with the strongest non-signal margins. `method="cutbox"` uses the same
    candidate search after trimming the most extreme low and high observation
    when at least five observations are available. The latter two qicharts2
    methods are documented as experimental; this implementation is deterministic
    and documented in `VALIDATION_REPORT.md`.
    """

    method_key = method.lower().replace("-", "_")
    if method_key not in {"anhoej", "bestbox", "cutbox"}:
        raise ValueError("method must be 'anhoej', 'bestbox', or 'cutbox'.")
    series = _clean_series(values, exclude)
    if series.empty:
        return AnhoejResult(float("nan"), 0, 0, 0, 0, 0, 0, False, False, method_key)

    if method_key == "anhoej":
        return _evaluate(series, float(series.median()), method_key)

    search = series.copy()
    if method_key == "cutbox" and len(search) >= 5:
        ordered = search.sort_values()
        search = ordered.iloc[1:-1]
    candidates = _candidate_centres(search)
    results = [_evaluate(series, centre, method_key) for centre in candidates]
    return max(results, key=_score_result)
