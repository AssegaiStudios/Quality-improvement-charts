# pyqicharts v0.4.0

This release adds NHS-style Individuals / XmR special cause detection and interpretation.

## Added

- Above-UCL and below-LCL detection.
- Shift detection.
- Trend detection.
- Direction-of-improvement classification.
- Special cause table fields for downstream reporting.
- Signal colouring for improvement, concern, and neutral special causes.

## Install

```bash
pip install pyqicharts
```

For local development from this source archive:

```bash
pip install -e .[dev]
pytest
```
