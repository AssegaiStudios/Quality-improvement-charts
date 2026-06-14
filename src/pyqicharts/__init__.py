"""pyqicharts: Quality Improvement and SPC charts for Python."""
from .core import QicResult, qic
from .export import create_report_bundle, export_excel, export_png, export_powerpoint
from .nhs_rules import NhsRuleConfig, nhs_xmr_signals
from .pareto import ParetoResult, paretochart
from .powerbi import powerbi_table, special_cause_summary_table, spc_summary_table
from .rules import AnhoejResult, anhoej_rules
from .tables import qic_table, pareto_table
from .themes import Theme, get_theme, list_themes

__all__ = [
    "AnhoejResult", "NhsRuleConfig", "ParetoResult", "QicResult", "Theme",
    "anhoej_rules", "create_report_bundle", "export_excel", "export_png",
    "export_powerpoint", "get_theme", "list_themes", "pareto_table",
    "paretochart", "powerbi_table", "qic", "qic_table", "nhs_xmr_signals",
    "special_cause_summary_table", "spc_summary_table",
]
__version__ = "0.6.0"
