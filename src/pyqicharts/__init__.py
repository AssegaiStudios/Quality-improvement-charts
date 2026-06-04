"""pyqicharts: Quality Improvement and SPC charts for Python."""

from .core import QicResult, qic
from .pareto import ParetoResult, paretochart
from .rules import AnhoejResult, anhoej_rules
from .tables import qic_table, pareto_table

__all__ = [
    "AnhoejResult",
    "ParetoResult",
    "QicResult",
    "anhoej_rules",
    "pareto_table",
    "paretochart",
    "qic",
    "qic_table",
]

__version__ = "0.2.0"
