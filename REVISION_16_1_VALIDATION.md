# Revision 16.1 — Commercial Hotfix Validation

## Section 4B behavior
Validated in Chromium against the actual Revision 16.1 HTML/JavaScript with an Academy Manager profile.

### Incomplete route behavior
- B2C: completion remains blocked and shows the missing B2C requirement inline.
- B2B: completion remains blocked and shows all missing contract-route requirements inline.
- Mixed: completion remains blocked and shows blockers for both applicable routes inline.
- No JavaScript page errors occurred.

### Valid route completion
- B2C: Commercial changes to `Completed`, 4 Operational Activity work items are activated, and 1 supervisor review is created.
- B2B: Commercial changes to `Completed`, 4 Operational Activity work items are activated, and 1 supervisor review is created.
- Mixed: Commercial changes to `Completed`, 4 Operational Activity work items are activated, and 1 supervisor review is created.

### Code checks
- `python3 -m py_compile server.py` — passed.
- Extracted application JavaScript `node --check` — passed.
- Academy Manager alone can edit/complete Section 4B through the existing manager authority override.
