"""pyqicharts: Quality Improvement and SPC charts for Python.

The package root re-exports the supported public API. Internal helper functions
remain inside their modules so future releases can evolve implementation
details without forcing users to change imports.
"""
from .core import QicResult, qic
from .datasets import days_between_falls_with_harm, days_between_serious_incidents, infections_between_events, risk_adjusted_infection_rates, risk_adjusted_readmissions, sample_healthcare_qi_data, sample_subgroup_measurements
from .export import create_report_bundle, export_excel, export_png, export_powerpoint
from .nelson import nelson_rule_signals, shewhart_rule_signals
from .nhs_rules import NhsRuleConfig, nhs_xmr_signals
from .pareto import ParetoResult, pareto_chart, paretochart
from .powerbi import (
    intervention_metadata_table,
    kpi_table,
    nhs_interpretation_table,
    phase_metadata_table,
    powerbi_table,
    signal_table,
    special_cause_summary_table,
    spc_summary_table,
    target_metadata_table,
)
from .rules import AnhoejResult, anhoej_rules
from .signals import SIGNAL_SCHEMA_VERSION, Signal, signals_to_frame
from .tables import CHART_ALIASES, VALID_CHARTS, qic_table, pareto_table
from .themes import Theme, get_theme, list_themes
from .validation import read_validation_csv

__all__ = [
    "AnhoejResult", "CHART_ALIASES", "NhsRuleConfig", "ParetoResult", "QicResult", "Theme", "VALID_CHARTS",
    "anhoej_rules", "create_report_bundle", "days_between_falls_with_harm",
    "days_between_serious_incidents", "export_excel", "export_png",
    "export_powerpoint", "get_theme", "intervention_metadata_table", "kpi_table", "list_themes", "nelson_rule_signals", "nhs_interpretation_table", "pareto_table",
    "pareto_chart", "paretochart", "powerbi_table", "qic", "qic_table", "infections_between_events", "nhs_xmr_signals",
    "risk_adjusted_infection_rates", "risk_adjusted_readmissions",
    "sample_healthcare_qi_data", "sample_subgroup_measurements", "shewhart_rule_signals",
    "phase_metadata_table", "read_validation_csv", "signal_table", "signals_to_frame", "special_cause_summary_table", "spc_summary_table",
    "target_metadata_table", "SIGNAL_SCHEMA_VERSION", "Signal",
]
__version__ = "1.3.2"
