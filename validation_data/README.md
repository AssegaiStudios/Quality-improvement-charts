# Interim v1.0 Validation Data

This folder contains internal regression fixtures for the v1.0.0 interim rebuild.

## Contents

- `inputs/`: one input CSV for each supported chart family.
- `expected_outputs/`: expected centre line, control limit, signal and annotation fields generated from the current implementation.

## Scope

These files help maintainers detect accidental changes in chart calculations. They do not prove full parity with qicharts, qicharts2, NHS Making Data Count workbooks or published Anhøj examples.

The parity status for each roadmap phase is documented in `PARITY_REPORT.md`.
