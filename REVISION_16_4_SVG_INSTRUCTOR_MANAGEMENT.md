# Revision 16.4 — Unified SVG Icons & Instructor Management

## Scope

This revision standardizes the application icon language and adds Academy Manager instructor-directory management without changing the Revision 16.2 role-governance model or the Revision 16.3 Finance currency cleanup.

## Unified internal SVG icon system

- Added a local `/static/icons/` library with a reusable `sprite.svg` plus individual SVG files.
- Icons use a consistent 24×24 viewBox, stroke-based visual language, and `currentColor` so they inherit active theme colors.
- No icon CDN or runtime third-party dependency is required.
- Standard display sizes are 16, 20, and 24 px.
- Sidebar navigation now uses the shared SVG family.
- Dashboard Insight cards now use semantic SVGs instead of letter/symbol placeholders.
- Program lifecycle stages and stage states use the shared icon system.
- Task status, priority, filters, and common actions use the shared icon system.
- Finance, Schedule, Documents, Reports, History, Training, Administration, Profile, and common actions use the same family where icons are present.
- Success, warning, blocked, overdue, pending, and completion states use semantic SVGs while retaining semantic state colors.
- Icon-only controls include an accessible label/title; decorative SVGs are hidden from assistive technology.

## Instructor management — Academy Manager only

The Instructors workspace now exposes four manager controls:

1. **Add Instructor** — opens a structured instructor form.
2. **Import Excel** — validates an XLSX/CSV file and previews the result before saving.
3. **Load Test Instructors** — adds a small set of clearly marked test profiles for demonstration/testing.
4. **Download Excel Template** — downloads the supported instructor-import workbook.

These controls are hidden from non-manager roles and guarded by the existing Academy Manager authorization logic.

## Instructor profile fields

The instructor master directory can now store:

- Name
- Email
- Phone
- Specialty
- Level
- Source
- Work Schedule
- Availability
- Region
- Notes
- Test-record marker

Existing Program instructor-selection behavior is preserved. Program-linked instructor records are enriched with the master-directory profile fields when available.

## Excel / CSV import

Supported columns:

| Column | Required | Notes |
|---|---|---|
| Name | Yes | Used as the directory match key |
| Email | No | Basic email validation |
| Phone | No | Free text to preserve international formats |
| Specialty | No | Instructor expertise/specialty |
| Level | No | Seniority/level |
| Source | No | Defaults to External |
| Work Schedule | No | Defaults to Project Based |
| Availability | No | Defaults to Available |
| Region | No | Country/region |
| Notes | No | Free-text notes |

The import workflow:

1. Reads XLSX or CSV.
2. Requires a Name column.
3. Skips blank rows.
4. Reports invalid rows instead of silently importing them.
5. Detects duplicate names inside the uploaded file.
6. Detects names that already exist in the Academy directory.
7. Shows valid rows, existing matches, and warnings in a preview modal.
8. Allows the Manager to either **Keep Existing & Add New** or **Replace Existing Matches**.

No data is written until the Manager confirms the preview.

## Test instructors

`Load Test Instructors` inserts six clearly marked test profiles with varied specialties, levels, schedules, availability states, and regions. It avoids duplicate insertion by name and can be used to inspect populated Instructor UI states.

## Compatibility

- Revision 16 manager-only Dashboard and stage-completion governance is unchanged.
- Team execution / Academy Manager stage handoff rules are unchanged.
- Finance remains currency-label neutral; `SAR` is not reintroduced.
- Existing master-data strings are still normalized and remain compatible.
