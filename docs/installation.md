# Installation

Install the core package:

```bash
pip install pyqicharts
```

For reporting helpers that create Excel and PowerPoint files:

```bash
pip install pyqicharts[reporting]
```

For local development from a source checkout:

```bash
pip install -e .[dev]
pytest
```

The core dependency set is intentionally small: numpy, pandas and matplotlib. Reporting dependencies are optional.
