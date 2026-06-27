# Methodology Limitations

pyqicharts v1.2.0 implements published-methodology parity without requiring a live R/qicharts2 runtime.

Limitations:

- bestbox and cutbox are experimental in qicharts2 documentation; pyqicharts implements deterministic centre-search equivalents and records the chosen method in output tables.
- P-prime and U-prime are strongest when expected values and denominators/opportunities are supplied. Without denominators, pyqicharts labels the result as an observed/expected fallback.
- Live cross-package certification requires frozen reference-output files from qicharts, qicharts2 and NHS workbooks. Those files are not bundled in v1.2.0.
