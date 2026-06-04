"""Chart construction functions for pyqicharts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .rules import AnhoejResult, anhoej_rules
from .tables import qic_table


@dataclass
class QicResult:
    """Result returned by :func:`qic`."""

    data: pd.DataFrame
    chart: str
    x: str
    y: str
    centre: float
    lcl: Optional[float]
    ucl: Optional[float]
    anhoej: Optional[AnhoejResult]
    signals: pd.Series
    table: pd.DataFrame
    figure: object
    axes: object

    def summary(self) -> dict:
        """Return a simple dictionary summary suitable for logs/reports."""

        out = {
            "chart": self.chart,
            "centre": self.centre,
            "lcl": self.lcl,
            "ucl": self.ucl,
            "signals": int(self.signals.sum()),
        }
        if self.anhoej is not None:
            out["anhoej"] = self.anhoej
        return out

    def show(self):
        """Display the matplotlib figure."""

        plt.show()


def _normalise_chart_name(chart: str) -> str:
    key = chart.lower().replace("-", "_").replace(" ", "_")
    if key == "individuals":
        key = "i"
    if key in {"movingrange", "moving_range"}:
        key = "mr"
    return key


def qic(
    data: pd.DataFrame,
    x: str,
    y: str,
    chart: str = "run",
    title: str | None = None,
    figsize: tuple[int, int] = (10, 5),
) -> QicResult:
    """Create a QI chart.

    Supported chart values in v0.2.0:
    - ``"run"``
    - ``"i"`` or ``"individuals"``
    - ``"mr"`` or ``"moving_range"``
    """

    chart_key = _normalise_chart_name(chart)
    table = qic_table(data=data, x=x, y=y, chart=chart_key)

    fig, ax = plt.subplots(figsize=figsize)

    if chart_key == "mr":
        plot_y = "moving_range"
        ylabel = f"Moving range of {y}"
    else:
        plot_y = y
        ylabel = y

    ax.plot(table[x], table[plot_y], marker="o", linewidth=1.8)

    signal_rows = table[table["signal"]]
    if not signal_rows.empty:
        ax.scatter(signal_rows[x], signal_rows[plot_y], s=80, marker="o", zorder=5)

    centre = float(table["centre"].dropna().iloc[0]) if table["centre"].notna().any() else np.nan
    lcl = float(table["lcl"].dropna().iloc[0]) if table["lcl"].notna().any() else None
    ucl = float(table["ucl"].dropna().iloc[0]) if table["ucl"].notna().any() else None

    if centre == centre:
        ax.axhline(centre, linestyle="--", linewidth=1.3, label="Centre")
    if lcl is not None:
        ax.axhline(lcl, linestyle=":", linewidth=1.2, label="LCL")
    if ucl is not None:
        ax.axhline(ucl, linestyle=":", linewidth=1.2, label="UCL")

    ax.set_xlabel(x)
    ax.set_ylabel(ylabel)
    ax.set_title(title or f"{chart_key.upper()} chart of {y}")
    ax.grid(True, alpha=0.25)
    if chart_key in {"i", "mr"}:
        ax.legend(loc="best")
    fig.tight_layout()

    anhoej = anhoej_rules(table[y]) if chart_key == "run" else None

    return QicResult(
        data=data.copy(),
        chart=chart_key,
        x=x,
        y=y,
        centre=centre,
        lcl=lcl,
        ucl=ucl,
        anhoej=anhoej,
        signals=table["signal"],
        table=table,
        figure=fig,
        axes=ax,
    )
