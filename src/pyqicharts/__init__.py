"""pyqicharts: Quality Improvement and SPC charts for Python."""
from .core import QicResult, qic
from .pareto import ParetoResult, paretochart
from .rules import AnhoejResult, anhoej_rules
from .tables import qic_table, pareto_table
from .themes import Theme, get_theme, list_themes

__all__ = [
    "AnhoejResult", "ParetoResult", "QicResult", "Theme",
    "anhoej_rules", "get_theme", "list_themes", "pareto_table",
    "paretochart", "qic", "qic_table",
]
__version__ = "0.3.0"
