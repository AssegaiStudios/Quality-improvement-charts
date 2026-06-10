"""Chart construction functions for pyqicharts."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .rules import AnhoejResult, anhoej_rules
from .tables import qic_table
from .themes import get_theme

@dataclass
class QicResult:
    """Result returned by qic()."""
    data: pd.DataFrame
    chart: str
    x: str
    y: str
    centre: float
    centre_label: str
    lcl: Optional[float]
    ucl: Optional[float]
    anhoej: Optional[AnhoejResult]
    signals: pd.Series
    table: pd.DataFrame
    figure: object
    axes: object
    def summary(self) -> dict:
        out = {"chart": self.chart, "centre_label": self.centre_label, "centre": self.centre, "lcl": self.lcl, "ucl": self.ucl, "signals": int(self.signals.sum())}
        if self.anhoej is not None: out["anhoej"] = self.anhoej
        return out
    def show(self):
        plt.show()

def _normalise_chart_name(chart: str) -> str:
    key = chart.lower().replace("-", "_").replace(" ", "_")
    return {"individuals":"i", "movingrange":"mr", "moving_range":"mr", "count":"c", "proportion":"p", "rate":"u"}.get(key, key)

def _scalar_or_none(series: pd.Series) -> float | None:
    non_null = series.dropna()
    return None if len(non_null) == 0 else float(non_null.iloc[0])

def qic(
    data: pd.DataFrame,
    x: str,
    y: str,
    chart: str = "run",
    denominator: str | None = None,
    title: str | None = None,
    figsize: tuple[int,int] = (10,5),
    theme: str = "default",
    improvement: str | None = None,
    shift_points: int = 8,
    trend_points: int = 6,
) -> QicResult:
    """Create a QI/SPC chart.

    Version 0.4.0 supports run, I, MR, C, P and U charts. P and U charts
    require a denominator column. Individuals charts include NHS-style
    special cause colouring and interpretation.
    """
    chart_key = _normalise_chart_name(chart); style = get_theme(theme)
    table = qic_table(
        data=data,
        x=x,
        y=y,
        chart=chart_key,
        denominator=denominator,
        improvement=improvement,
        shift_points=shift_points,
        trend_points=trend_points,
    )
    fig, ax = plt.subplots(figsize=figsize)
    ylabel = y
    if chart_key == "mr": ylabel = f"Moving range of {y}"
    elif chart_key == "p": ylabel = f"Proportion of {y}"
    elif chart_key == "u": ylabel = f"Rate of {y}"
    ax.plot(table[x], table["plot_value"], marker="o", linewidth=1.8, color=style.line, markerfacecolor=style.marker, markeredgecolor=style.marker)
    signal_rows = table[table["signal"]]
    if not signal_rows.empty:
        if "special_cause_type" in signal_rows:
            plotted_labels = set()
            for signal_type, rows in signal_rows.groupby("special_cause_type", dropna=False):
                label = str(signal_type).title() if signal_type else "Signal"
                color = str(rows["special_cause_colour"].iloc[0]) or style.signal
                ax.scatter(rows[x], rows["plot_value"], s=90, color=color, marker="o", zorder=5, label=None if label in plotted_labels else label)
                plotted_labels.add(label)
        else:
            ax.scatter(signal_rows[x], signal_rows["plot_value"], s=90, color=style.signal, marker="o", zorder=5, label="Signal")
    centre = _scalar_or_none(table["centre"]); lcl = _scalar_or_none(table["lcl"]); ucl = _scalar_or_none(table["ucl"]); centre_label = str(table["centre_label"].iloc[0]) if len(table) else "Centre"
    if centre is not None and not np.isnan(centre): ax.axhline(centre, linestyle="--", linewidth=1.4, color=style.centre, label=centre_label)
    if lcl is not None and not np.isnan(lcl): ax.axhline(lcl, linestyle=":", linewidth=1.2, color=style.limits, label="LCL")
    if ucl is not None and not np.isnan(ucl): ax.axhline(ucl, linestyle=":", linewidth=1.2, color=style.limits, label="UCL")
    ax.set_xlabel(x); ax.set_ylabel(ylabel); ax.set_title(title or f"{chart_key.upper()} chart of {y}"); ax.grid(True, alpha=style.grid_alpha); ax.legend(loc="best"); fig.tight_layout()
    anhoej = anhoej_rules(table[y]) if chart_key == "run" else None
    return QicResult(data.copy(), chart_key, x, y, centre if centre is not None else float("nan"), centre_label, lcl, ucl, anhoej, table["signal"], table, fig, ax)
