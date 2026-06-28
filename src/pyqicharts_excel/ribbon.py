"""Ribbon/add-in deployment notes for xlwings users."""

RIBBON_CALLBACKS = {
    "Generate Chart": "pyqicharts_excel.runner.generate_chart",
    "Generate All Outputs": "pyqicharts_excel.runner.generate_all_outputs",
    "Export Report Bundle": "pyqicharts_excel.runner.export_report_bundle",
    "Clear Outputs": "pyqicharts_excel.runner.clear_outputs",
    "Validate Workbook": "pyqicharts_excel.runner.validate_workbook",
}

RIBBON_XML_SNIPPET = """<customUI xmlns="http://schemas.microsoft.com/office/2009/07/customui">
  <ribbon>
    <tabs>
      <tab id="pyqichartsTab" label="pyqicharts">
        <group id="pyqichartsGroup" label="SPC">
          <button id="generateChart" label="Generate Chart" onAction="RunPython"/>
          <button id="generateAll" label="Generate All Outputs" onAction="RunPython"/>
          <button id="exportBundle" label="Export Report Bundle" onAction="RunPython"/>
        </group>
      </tab>
    </tabs>
  </ribbon>
</customUI>"""


def ribbon_instructions() -> str:
    """Return concise setup instructions for the documented Phase 2 path."""

    callbacks = "\n".join(f"- {label}: `{callback}`" for label, callback in RIBBON_CALLBACKS.items())
    return (
        "Install the xlwings add-in, then either assign sheet buttons to the "
        "callbacks below or package them into an organisation-managed ribbon.\n\n"
        f"{callbacks}\n\n"
        "The XML snippet is a starting point for Office Custom UI Editor workflows."
    )

