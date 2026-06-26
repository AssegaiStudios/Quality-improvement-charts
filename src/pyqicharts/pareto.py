"""Pareto chart functionality.

Pareto charts sit beside the time-series SPC charts. They reuse
`pareto_table()` so the plotted categories and exported table stay aligned.
"""
from __future__ import annotations
from dataclasses import dataclass
import matplotlib.pyplot as plt
import pandas as pd
from .tables import pareto_table
from .themes import get_theme

@dataclass
class ParetoResult:
    """Result returned by `paretochart()`."""
    data: pd.DataFrame
    category: str
    table: pd.DataFrame
    figure: object
    axes: object

def paretochart(data: pd.DataFrame, category: str, count: str | None = None, title: str | None = None, figsize: tuple[int,int] = (10,5), theme: str = "default") -> ParetoResult:
    """Create a Pareto chart."""
    style = get_theme(theme); table = pareto_table(data=data, category=category, count=count)
    fig, ax1 = plt.subplots(figsize=figsize)
    # The bar axis shows category contribution; the secondary line axis shows
    # cumulative percentage so users can inspect the 80/20 pattern directly.
    ax1.bar(table[category].astype(str), table["count"], color=style.line); ax1.set_ylabel("Count"); ax1.set_xlabel(category); ax1.set_title(title or f"Pareto chart of {category}"); ax1.tick_params(axis="x", rotation=45); ax1.grid(True, axis="y", alpha=style.grid_alpha)
    ax2 = ax1.twinx(); ax2.plot(table[category].astype(str), table["cumulative_percent"], marker="o", color=style.centre); ax2.set_ylabel("Cumulative percent"); ax2.set_ylim(0,105); ax2.axhline(80, linestyle="--", linewidth=1, color=style.limits)
    fig.tight_layout(); return ParetoResult(data.copy(), category, table, fig, ax1)
