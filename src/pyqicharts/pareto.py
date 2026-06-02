"""Pareto chart support."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import pandas as pd


@dataclass
class ParetoResult:
    """Container returned by :func:`paretochart`."""

    table: pd.DataFrame
    figure: plt.Figure
    axes: plt.Axes


def paretochart(
    data: pd.DataFrame,
    category: str,
    value: str | None = None,
    title: str | None = None,
    ax: plt.Axes | None = None,
) -> ParetoResult:
    """Create a Pareto chart.

    Parameters
    ----------
    data:
        Input data.
    category:
        Categorical column containing causes/groups.
    value:
        Optional numeric value column. When omitted, rows are counted.
    title:
        Optional chart title.
    ax:
        Optional matplotlib axes.
    """

    if category not in data.columns:
        raise ValueError(f"category column not found: {category}")

    if value is None:
        counts = data[category].value_counts(dropna=False)
    else:
        if value not in data.columns:
            raise ValueError(f"value column not found: {value}")
        counts = data.groupby(category, dropna=False)[value].sum().sort_values(ascending=False)

    table = counts.rename("count").reset_index().rename(columns={"index": category})
    table["cum_count"] = table["count"].cumsum()
    total = table["count"].sum()
    table["cum_percent"] = 100 * table["cum_count"] / total if total else 0

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    else:
        fig = ax.figure

    ax.bar(table[category].astype(str), table["count"])
    ax.set_xlabel(category)
    ax.set_ylabel("Count" if value is None else value)
    ax.set_title(title or f"Pareto chart of {category}")
    ax.tick_params(axis="x", rotation=45)

    ax2 = ax.twinx()
    ax2.plot(table[category].astype(str), table["cum_percent"], marker="o")
    ax2.set_ylabel("Cumulative percent")
    ax2.set_ylim(0, 105)

    fig.tight_layout()
    return ParetoResult(table=table, figure=fig, axes=ax)
