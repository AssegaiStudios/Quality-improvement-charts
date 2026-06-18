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
    def save_png(self, path: str, dpi: int = 150):
        from .export import export_png
        return export_png(self, path, dpi=dpi)
    def summary(self) -> dict:
        out = {"chart": self.chart, "centre_label": self.centre_label, "centre": self.centre, "lcl": self.lcl, "ucl": self.ucl, "signals": int(self.signals.sum())}
        if self.anhoej is not None: out["anhoej"] = self.anhoej
        return out
    def show(self):
        plt.show()

def _normalise_chart_name(chart: str) -> str:
    key = chart.lower().replace("-", "_").replace(" ", "_")
    return {"individuals":"i", "movingrange":"mr", "moving_range":"mr", "count":"c", "proportion":"p", "rate":"u", "rare_event":"g", "time_between":"t"}.get(key, key)

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
    baseline_points: int | None = None,
    recalculation_points: list | None = None,
    target: float | int | None = None,
    interventions: list[dict] | None = None,
    step_changes: list[dict] | None = None,
) -> QicResult:
    """Create a QI/SPC chart.

    Version 0.7.0 supports run, I, MR, C, P, U, G and T charts. P and U charts
    require a denominator column. Individuals charts include NHS-style
    special cause colouring and interpretation, plus baseline, recalculation,
    target, intervention and step-change metadata.
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
        baseline_points=baseline_points,
        recalculation_points=recalculation_points,
        target=target,
        interventions=interventions,
        step_changes=step_changes,
    )
    fig, ax = plt.subplots(figsize=figsize)
    ylabel = y
    if chart_key == "mr": ylabel = f"Moving range of {y}"
    elif chart_key == "p": ylabel = f"Proportion of {y}"
    elif chart_key == "u": ylabel = f"Rate of {y}"
    elif chart_key == "g": ylabel = f"Cases between events: {y}"
    elif chart_key == "t": ylabel = f"Time between events: {y}"
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
    for segment_id, rows in table.groupby("segment_id" if "segment_id" in table else table.index, sort=True):
        first_x = rows[x].iloc[0]; last_x = rows[x].iloc[-1]
        seg_centre = _scalar_or_none(rows["centre"]); seg_lcl = _scalar_or_none(rows["lcl"]); seg_ucl = _scalar_or_none(rows["ucl"])
        label_suffix = "" if segment_id == 1 else f" S{segment_id}"
        if seg_centre is not None and not np.isnan(seg_centre): ax.hlines(seg_centre, first_x, last_x, linestyle="--", linewidth=1.4, color=style.centre, label=centre_label + label_suffix)
        if seg_lcl is not None and not np.isnan(seg_lcl): ax.hlines(seg_lcl, first_x, last_x, linestyle=":", linewidth=1.2, color=style.limits, label="LCL" + label_suffix)
        if seg_ucl is not None and not np.isnan(seg_ucl): ax.hlines(seg_ucl, first_x, last_x, linestyle=":", linewidth=1.2, color=style.limits, label="UCL" + label_suffix)
    if target is not None:
        ax.axhline(target, linestyle="-.", linewidth=1.2, color="#330072", label="Target")
    if "intervention" in table:
        for _, row in table[table["intervention"]].iterrows():
            ax.axvline(row[x], linestyle="-", linewidth=1.0, color="#425563", alpha=0.65)
            if row["intervention_label"]:
                ax.text(row[x], row["plot_value"], str(row["intervention_label"]), rotation=90, va="bottom", ha="right", fontsize=8)
    if "step_change" in table:
        for _, row in table[table["step_change"]].iterrows():
            ax.axvline(row[x], linestyle="--", linewidth=1.0, color="#007F3B", alpha=0.75)
            if row["step_change_label"]:
                ax.text(row[x], row["plot_value"], str(row["step_change_label"]), rotation=90, va="bottom", ha="left", fontsize=8)
    ax.set_xlabel(x); ax.set_ylabel(ylabel); ax.set_title(title or f"{chart_key.upper()} chart of {y}"); ax.grid(True, alpha=style.grid_alpha); ax.legend(loc="best"); fig.tight_layout()
    anhoej = anhoej_rules(table[y]) if chart_key == "run" else None
    return QicResult(data.copy(), chart_key, x, y, centre if centre is not None else float("nan"), centre_label, lcl, ucl, anhoej, table["signal"], table, fig, ax)
