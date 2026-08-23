# Revision 16.4 Validation

## Code checks

- `python3 -m py_compile server.py` — passed.
- Extracted application JavaScript with `node --check` — passed.
- All SVG files parsed as valid XML — passed.

## Icon-system audit

- Shared icon files: **46 SVG files** including `sprite.svg`.
- Static/dynamic application SVG icon markup references the internal sprite system.
- Current final source check: **93 shared-sprite references**.
- Inline emoji/status-symbol audit (`U+2600` and above): **0**.
- SVG-only static buttons missing an accessible label/title: **0**.
- Sprite and individual icons use `currentColor` for theme inheritance.
- No external icon CDN is used.

## Finance regression check

- `SAR` occurrences in the application UI source: **0**.

## Instructor API checks

Local server validation:

- `/` — HTTP 200.
- `/api/store` — HTTP 200.
- `/icons/sprite.svg` — HTTP 200.
- `/api/instructor-template` — HTTP 200 and opens as a valid XLSX workbook.
- Template sheets: `Instructors`, `Instructions`.
- Template headers: Name, Email, Phone, Specialty, Level, Source, Work Schedule, Availability, Region, Notes.

Import parser test covered:

- valid instructor row — accepted;
- invalid email — reported and skipped;
- missing Name — reported and skipped;
- duplicate name inside file — reported and skipped.

## Actual-render harness checks

The actual application HTML/CSS/JavaScript was loaded in Chromium's layout engine with only local API transport mocked because managed browser navigation blocks localhost.

Verified:

- Academy Manager sees Add Instructor / Import Excel / Load Test Instructors / Template controls.
- Test instructors create real directory profile cards.
- Manual Add Instructor creates a profile.
- Excel preview modal shows valid rows, existing-name conflicts, and warnings before commit.
- Dashboard Insight cards render shared SVG icons.
- Instructors mobile view at 390 px has **0 px document-level horizontal overflow**.
- JavaScript page errors during the harness flow: **0**.

## Clean-package check

The package was restored to the clean baseline after testing:

- user: null
- tasks: 0
- Programs: 0
- assignments: 0
- notifications: 0
- documents: 0
- SQLite tasks/programs/assignments/audit rows: 0

Test instructors and the test Manager account exist only in the validation harness/screenshots and are not shipped in the package.
