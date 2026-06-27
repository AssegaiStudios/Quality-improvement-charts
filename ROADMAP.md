# pyqicharts Roadmap

## Vision

pyqicharts aims to become the leading open-source Python package for Quality Improvement (QI) and Statistical Process Control (SPC) charts, with strong support for healthcare improvement, Excel, Power BI, Jupyter, and Python workflows.

The project is inspired by:

- qicharts2 (R)
- NHS SPC Excel tools
- Practical healthcare and operational improvement methodologies

The goal is not to replicate existing tools, but to provide equivalent and enhanced functionality through a modern Python-first architecture.

---

# Completed Releases

## v0.1.0 – Initial Public Release ✅

Released: June 2026

### Features

- Run Charts
- Individuals (I) Charts
- Pareto Charts
- Anhøj-style run chart diagnostics
- Shewhart 3-sigma signal detection
- Pandas integration
- Matplotlib visualisation
- Automated testing framework
- GitHub repository and documentation

### Outcome

Established the foundation for a Python implementation inspired by qicharts2.

---

## v0.2.0 – Analytics & Integration Release ✅

Released: June 2026

### Features

- Moving Range (MR) Charts
- Improved Individuals Chart calculations
- qic_table()
- pareto_table()
- Power BI examples
- Excel-friendly outputs
- Expanded test suite
- Improved documentation

### Outcome

Separated statistical calculations from visualisation and established support for Excel and Power BI workflows.

---

## v0.3.0 – Attribute Charts & Themes ✅

Released: June 2026

### Features

- C Charts
- P Charts
- U Charts
- Dynamic centre-line labels
- NHS visual theme
- Publication theme
- Dark theme
- Improved signal highlighting
- Expanded examples
- Expanded test coverage

### Outcome

Added commonly used healthcare and operational SPC chart types while improving usability and presentation.

---

# Planned Releases

## v0.4.0 – NHS XmR Signal Engine

### Planned Features

- Above UCL detection
- Below LCL detection
- Shift detection
- Trend detection
- Signal annotation
- Signal colouring
- Special cause identification
- Improved chart legends
- Improved SPC interpretation support

### Goal

Implement NHS-style SPC signal interpretation and chart annotation functionality.

---

## v0.5.0 – NHS XmR Feature Parity

### Planned Features

- Baseline periods
- Recalculated control limits
- Step changes
- Target lines
- High-is-good / Low-is-good logic
- Special cause summary tables
- SPC reporting enhancements

### Goal

Achieve functional parity with key analytical capabilities of the NHS SPC Excel workbook.

---

## v0.6.0 – Reporting & Office Integration

### Planned Features

- PowerPoint export
- Excel export helpers
- PNG export utilities
- Power BI templates
- Reporting automation helpers
- Dashboard integration examples

### Goal

Provide seamless integration with organisational reporting environments.

---

## v0.7.0 – Advanced Shewhart Charts

### Planned Features

- Xbar Charts
- S Charts
- Enhanced styling options
- Optional target overlays
- Enhanced annotations

### Goal

Expand support for variable-data control charts.

---

## v0.8.0 – Specialist Healthcare Charts

### Planned Features

- G Charts
- T Charts
- Additional SPC signal rules
- Expanded healthcare examples
- Reference datasets

### Goal

Provide specialist charts commonly used in healthcare and service improvement.

---

## v0.9.0 – Risk Adjusted Charts

### Planned Features

- P′ Charts
- U′ Charts
- Risk-adjusted examples
- Validation datasets

### Goal

Support more advanced healthcare quality-improvement use cases.

---

## v1.0.0 - Interim Parity-Readiness Release

### Planned Features

- Supported public API
- Comprehensive documentation
- Full automated test coverage
- Reference validation against published examples
- PyPI publication
- Long-term support roadmap

### Goal

Create a clean, testable interim v1.0 base while full qicharts, qicharts2 and NHS parity evidence is completed. This should not be described as production-ready until `PARITY_REPORT.md` shows that all parity acceptance criteria have been satisfied.

---

# Long-Term Vision

Future exploration areas include:

- Interactive visualisations
- Streamlit integration
- Web dashboards
- Real-time monitoring
- Excel add-ins
- Power BI custom visuals
- Educational toolkits
- Healthcare quality-improvement templates

---

## Reference Implementations

The roadmap is informed by:

- qicharts2
- NHS SPC Excel workbook analysis
- Healthcare quality-improvement methodologies
- Practical Power BI and Excel workflows

---

## Contributing

Contributions, bug reports, feature requests, and suggestions are welcome.

Please raise an issue or submit a pull request via GitHub.
