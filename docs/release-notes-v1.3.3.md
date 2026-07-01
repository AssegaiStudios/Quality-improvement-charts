# pyqicharts v1.3.3 Release Notes

v1.3.3 is a practical coverage-hardening release.

## Coverage

- Increased automated coverage from 90.70% to 96.80%.
- Raised the configured coverage gate from 90% to 95%.
- Expanded the suite to 133 test functions and 149 passing collected tests.

## Added

- Excel Companion validation tests for invalid config, duplicate headers, bad denominators, invalid expected values and friendly validation exceptions.
- Excel Companion output/export tests for Pareto, Power BI, Excel, PowerPoint and report bundle branches.
- Runner tests for generation aliases, report bundle export, debug logging, config refresh, template initialization and xlwings caller resolution.
- Helper tests for examples, ribbon metadata, workbook template creation, blank/missing sheets, workbook logging and validation CSV loading.

## Fixed

- `write_log(...)` now writes headers directly to row 1 on empty template Log sheets before appending the first message.

