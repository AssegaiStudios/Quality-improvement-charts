"""Main qic API for run and control charts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pyqicharts.rules import AnhoejResult, anhoej_rules, shewhart_rule

ChartType = Literal["run", "i"]


@dataclass
class QicResult:
    """Container returned by :func:`qic`."""

    data: pd.DataFrame
    chart: str
    x: str
    y: str
    centre: float
    lcl: float | None
    ucl: float | None
    anhoej: AnhoejResult | None
    signals: pd.Series
    figure: plt.Figure
    axes: plt.Axes

    def summary(self) -> dict[str, object]:
        """Return a small dictionary of chart diagnostics."""

        output: dict[str, object] = {
            "chart": self.chart,
            "n": int(self.data[self.y].notna().sum()),
            "centre": self.centre,
            "lcl": self.lcl,
            "ucl": self.ucl,
            "n_signals": int(self.signals.sum()),
        }
        if self.anhoej is not None:
            output.update(
                {
                    "runs": self.anhoej.runs,
                    "crossings": self.anhoej.crossings,
                    "longest_run": self.anhoej.longest_run,
                    "signal_long_run": self.anhoej.signal_long_run,
                    "signal_few_crossings": self.anhoej.signal_few_crossings,
                }
            )
        return output


def _ordered_frame(data: pd.DataFrame, x: str, y: str) -> pd.DataFrame:
    if x not in data.columns:
        raise ValueError(f"x column not found: {x}")
    if y not in data.columns:
        raise ValueError(f"y column not found: {y}")
    out = data[[x, y]].copy()
    out = out.dropna(subset=[y]).sort_values(x).reset_index(drop=True)
    if out.empty:
        raise ValueError("data must contain at least one non-missing y value")
    return out


def _individuals_limits(values: pd.Series) -> tuple[float, float, float]:
    arr = values.to_numpy(dtype=float)
    centre = float(np.mean(arr))
    if arr.size < 2:
        return centre, centre, centre
    moving_ranges = np.abs(np.diff(arr))
    mr_bar = float(np.mean(moving_ranges))
    sigma = mr_bar / 1.128 if mr_bar > 0 else 0.0
    lcl = centre - 3 * sigma
    ucl = centre + 3 * sigma
    return centre, lcl, ucl


def qic(
    data: pd.DataFrame,
    x: str,
    y: str,
    chart: ChartType = "run",
    title: str | None = None,
    centre: float | None = None,
    ax: plt.Axes | None = None,
) -> QicResult:
    """Create a Quality Improvement chart.

    Parameters
    ----------
    data:
        Input data as a pandas DataFrame.
    x:
        Time/order column.
    y:
        Measurement column.
    chart:
        ``"run"`` for a run chart or ``"i"`` for an individuals chart.
    title:
        Optional chart title.
    centre:
        Optional centre line. Defaults to median for run charts and mean for
        individuals charts.
    ax:
        Optional matplotlib axes.

    Returns
    -------
    QicResult
        Chart, diagnostics, limits, and underlying data.
    """

    df = _ordered_frame(data, x, y)
    values = df[y].astype(float)
    chart = chart.lower()  # type: ignore[assignment]

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    else:
        fig = ax.figure

    if chart == "run":
        centre_line = float(np.median(values) if centre is None else centre)
        anhoej = anhoej_rules(values, centre_line)
        lcl = ucl = None
        signals = pd.Series(False, index=df.index)
    elif chart == "i":
        calculated_centre, lcl, ucl = _individuals_limits(values)
        centre_line = float(calculated_centre if centre is None else centre)
        if centre is not None:
            sigma = (ucl - calculated_centre) / 3 if ucl is not None else 0
            lcl = centre_line - 3 * sigma
            ucl = centre_line + 3 * sigma
        anhoej = None
        sigma_for_rule = (ucl - centre_line) / 3 if ucl is not None else 0
        signals = shewhart_rule(values, centre_line, sigma_for_rule)
        signals.index = df.index
    else:
        raise ValueError("chart must currently be one of: 'run', 'i'")

    ax.plot(df[x], df[y], marker="o")
    ax.axhline(centre_line, linestyle="--", linewidth=1.5, label="Centre")

    if lcl is not None and ucl is not None:
        ax.axhline(lcl, linestyle=":", linewidth=1.2, label="LCL")
        ax.axhline(ucl, linestyle=":", linewidth=1.2, label="UCL")
        signal_points = df.loc[signals]
        if not signal_points.empty:
            ax.scatter(signal_points[x], signal_points[y], marker="x", s=90, label="Signal")

    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title or f"{chart.upper()} chart of {y}")
    ax.legend(loc="best")
    fig.tight_layout()

    return QicResult(
        data=df,
        chart=chart,
        x=x,
        y=y,
        centre=centre_line,
        lcl=lcl,
        ucl=ucl,
        anhoej=anhoej,
        signals=signals,
        figure=fig,
        axes=ax,
    )
