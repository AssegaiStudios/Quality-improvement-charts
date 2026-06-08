"""Rule calculations used by pyqicharts."""
from __future__ import annotations
from dataclasses import dataclass
from statistics import NormalDist
from typing import Iterable
import numpy as np
import pandas as pd

@dataclass(frozen=True)
class AnhoejResult:
    """Summary of Anhøj-style run chart diagnostics."""
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
        return self.signal_long_run or self.signal_few_crossings

def _longest_run(signs: list[int]) -> int:
    if not signs: return 0
    longest = current = 1; previous = signs[0]
    for sign in signs[1:]:
        if sign == previous: current += 1
        else: current = 1; previous = sign
        longest = max(longest, current)
    return longest

def _runs(signs: list[int]) -> int:
    if not signs: return 0
    return 1 + sum(1 for a,b in zip(signs, signs[1:]) if a != b)

def _crossings(signs: list[int]) -> int:
    if not signs: return 0
    return sum(1 for a,b in zip(signs, signs[1:]) if a != b)

def _expected_longest_run(n: int) -> int:
    if n <= 0: return 0
    if n < 10: return n
    return int(np.ceil(np.log2(n) + 3))

def _lower_crossings_limit(n: int) -> int:
    if n <= 1: return 0
    mean = (n - 1) * 0.5
    sd = np.sqrt((n - 1) * 0.25)
    return max(0, int(np.floor(mean + NormalDist().inv_cdf(0.05) * sd)))

def anhoej_rules(values: Iterable[float]) -> AnhoejResult:
    """Calculate Anhøj-style run chart diagnostics.

    Values exactly equal to the median are excluded from runs/crossings.
    The current thresholds are approximate and flagged for validation in a
    later release.
    """
    series = pd.Series(values).dropna()
    median = float(series.median()) if len(series) else float("nan")
    if len(series) == 0:
        return AnhoejResult(median,0,0,0,0,0,0,False,False)
    signs = [1 if value > median else -1 for value in series if value != median]
    n_used = len(signs); runs = _runs(signs); crossings = _crossings(signs)
    longest = _longest_run(signs); expected = _expected_longest_run(n_used); lower = _lower_crossings_limit(n_used)
    return AnhoejResult(median,n_used,runs,crossings,longest,expected,lower,longest > expected if expected else False,crossings < lower if n_used > 1 else False)
