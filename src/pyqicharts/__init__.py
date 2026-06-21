"""pyqicharts: Quality Improvement and SPC charts for Python."""
from .core import QicResult, qic
from .datasets import days_between_falls_with_harm, days_between_serious_incidents, infections_between_events, risk_adjusted_infection_rates, risk_adjusted_readmissions
from .export import create_report_bundle, export_excel, export_png, export_powerpoint
from .nhs_rules import NhsRuleConfig, nhs_xmr_signals
from .pareto import ParetoResult, paretochart
from .powerbi import powerbi_table, special_cause_summary_table, spc_summary_table
from .rules import AnhoejResult, anhoej_rules
from .tables import qic_table, pareto_table
from .themes import Theme, get_theme, list_themes

__all__ = [
    "AnhoejResult", "NhsRuleConfig", "ParetoResult", "QicResult", "Theme",
    "anhoej_rules", "create_report_bundle", "days_between_falls_with_harm",
    "days_between_serious_incidents", "export_excel", "export_png",
    "export_powerpoint", "get_theme", "list_themes", "pareto_table",
    "paretochart", "powerbi_table", "qic", "qic_table", "infections_between_events", "nhs_xmr_signals",
    "risk_adjusted_infection_rates", "risk_adjusted_readmissions",
    "special_cause_summary_table", "spc_summary_table",
]
__version__ = "0.8.0"
