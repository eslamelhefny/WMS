# Revision 17 — Clear & Informative UI

## Goal

Translate the approved visual mockups into the real Andalusia Academy Work Management System without replacing the existing data model, manager governance, Program lifecycle, task ownership, Instructor management, or Finance rules.

## Implemented screen direction

### Manager Dashboard
- Keeps the approved **Command + Balanced** structure and **Insight** card language.
- The first row communicates Active Programs, Open Tasks, Overdue, Upcoming Sessions, Team Workload, and Financial Position.
- Every card explains the metric, shows health/attention context, and links to the relevant workspace.
- Operational attention and today's schedule appear before deeper analytics.
- Program Health, My Tasks, Instructor Readiness, Upcoming Delivery, Finance Snapshot, and Recent Activity use a shared compact panel language.
- Advanced manager controls remain collapsed by default to protect dashboard clarity.

### Programs
- Replaced the large portfolio-card-first list with a clearer **table-first** management view on desktop.
- Columns: Program, Stage, Status, Owner, Start Date, Target End, Progress, Actions.
- Lifecycle intelligence remains visible above the table.
- At mobile widths the table changes to readable Program cards instead of shrinking columns into illegibility.

### Program Workspace
- Clearer Program identity/header and lifecycle strip.
- Stage purpose, requirements, blockers, readiness/progress, assigned work, evidence, and manager completion controls are visually separated.
- Existing eight-stage workflow and Academy Manager completion authority are preserved.

### Tasks & Team workflow
- Compact searchable/filterable task workspace with summary KPIs and attention state.
- Manager Hybrid behavior remains intact.
- **All Team** continues to open the dedicated Team Members page.
- Selecting a team member continues to open that member profile with their assigned tasks and full filters.

### Schedule
- Weekly hourly schedule remains the primary delivery calendar.
- Date navigation is clearer and tablet controls wrap instead of widening the page.
- The dense timeline uses an intentional internal scroll region, never root-page overflow.

### Finance
- KPI-to-analysis-to-record hierarchy is simplified and made more readable.
- Revenue/cost/net, cash-flow, settlements, revenue mix, profitability, and Program finance records remain data-driven.
- No hard-coded `SAR` label is shown.

### Documents & Reports
- Search/filter bars and record cards use the same spacing, border, type, and action language as the rest of Revision 17.
- Report choices are easier to scan and use consistent action affordances.

## Shared visual system
- Fixed dark-navy sidebar and blended Academy identity.
- Hide/Collapse remains anchored at the sidebar bottom.
- Consistent internal SVG icon system retained from Revision 16.4.
- Reduced decorative shadows and oversized radii.
- Stronger whitespace hierarchy between page header, summary, analysis, and records.
- Consistent badges, progress indicators, tables, filters, controls, and responsive card rules.

## Preserved governance and functionality
- Manager Dashboard, Team management, Administration, and Academy Manager stage completion controls remain manager-only.
- Contributors complete owned work; Academy Manager completes/hands off lifecycle stages.
- Instructor Add / Excel Import / Load Test Instructors tools remain available according to the manager rules.
- Section 4B Commercial hotfix behavior remains intact.
- Store package remains clean; representative review data is used only inside the screenshot/audit harness.
