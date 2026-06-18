# pyqicharts v0.7.0

This release adds specialist healthcare rare-event charts.

## Added

- `chart="g"` for cases-between-events monitoring
- `chart="t"` for time-between-event monitoring
- Rare-event control limits and signal detection
- Negative interval validation
- Example healthcare datasets
- G and T chart examples

## Install

```bash
pip install pyqicharts
```

For reporting helpers:

```bash
pip install pyqicharts[reporting]
```

For local development from this source archive:

```bash
pip install -e .[dev]
pytest
```
