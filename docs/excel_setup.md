# Excel Companion Setup

## Standard User Install

```bash
pip install pyqicharts pyqicharts-excel xlwings
xlwings addin install
```

Open `excel/pyqicharts_excel_template.xlsx`, enable the xlwings add-in, then assign sheet buttons to the functions listed on the `Chart` sheet.

## Local Development Install

```bash
pip install -e ".[excel,dev]"
xlwings addin install
```

Create a fresh template:

```bash
pyqicharts-excel-init
```

## Windows Notes

Use the same Python environment that has `pyqicharts`, `xlwings`, `pandas`, `matplotlib`, `openpyxl` and optional `python-pptx` installed.

## macOS Notes

Install the xlwings add-in from the same Python environment. macOS may require workbook and Python locations to be trusted by Excel.

## Ribbon/Add-in Option

Phase 2 provides a documented ribbon path rather than a full Office.js add-in. Use `pyqicharts_excel.ribbon.RIBBON_CALLBACKS` and `RIBBON_XML_SNIPPET` as the deployment starting point for an organisation-managed Excel ribbon.

