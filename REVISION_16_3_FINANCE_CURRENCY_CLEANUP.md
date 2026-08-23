# Revision 16.3 — Finance Currency Cleanup

## Change
Removed the hard-coded `SAR` suffix from Finance dashboard portfolio KPI values.

Affected KPI values:
- Portfolio Revenue
- Program Costs
- Sponsorship
- Net Position

The underlying numeric values and calculations are unchanged. No replacement currency label was introduced.

## Validation
- No standalone `SAR` token remains in the live `static/index.html` Finance UI.
- Python server syntax check passed.
- Extracted application JavaScript syntax check passed.
