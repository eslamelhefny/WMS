# Revision 19 — Executive UI Implementation

Revision 19 implements the approved Executive UI direction on top of the Revision 18 functional baseline. It is a real application redesign, not a static mockup layer.

## Visual direction

- Tighter executive information hierarchy with less decorative card weight.
- Manager Dashboard uses **Executive Insights**: target, actual, variance/gap, compact chart/progress signal, and strategic state.
- Shared surfaces use compact radii, softer borders, reduced shadow, consistent white-space rhythm, and theme-driven accents.
- Internal SVG icons remain the single icon system.
- The original Andalusia Academy logo assets are unchanged.

## Manager Dashboard

The manager-only Dashboard now presents:

- Program Completion vs target
- Task Performance vs target
- Team Utilization vs target
- Delivery This Month vs plan
- Budget Utilization vs guardrail
- Financial Health / margin target
- Executive summary strip for active Programs, risk, overdue/blocked work, team size, and approvals
- Needs Attention, Today's Schedule, Program Health, My Tasks, Instructor Readiness, Upcoming Delivery, Finance Snapshot, Recent Activity, and expandable Manager Controls

The metrics are derived from the current application data. Revision 19 does not invent historical trends where no historical series exists.

## Programs

- Executive portfolio header and summary KPIs.
- Lifecycle Intelligence remains available to inspect all eight stages.
- Table-first portfolio view with Program, stage, status, owner, dates, progress, and direct open action.
- Responsive mobile cards replace the wide table at phone widths.

## Program Workspace

- Compact Program identity and overall-readiness header.
- Eight-stage lifecycle rail remains visible and actionable.
- Stage ownership, prerequisite, completion rule, handover, and Academy Manager authority are surfaced before stage-specific detail.
- **Academy Manager Control** stays visible by default.
- Large stage forms/evidence are moved into an expandable **Detailed stage form & evidence** section so the operational decision is not buried.
- Stage Work and Recent Program Activity remain visible alongside the manager control on desktop.

## Tasks, Team Members, Team Member Profile

- Tasks keeps the approved manager Hybrid workflow with executive KPIs, workload, attention state, and dense task records.
- **All Team** continues to open the dedicated Team Members workspace.
- Team Members is table-first on desktop with utilization, tasks, overdue, completion, and workload.
- Team Member Profile retains full assigned-task filtering and task assignment.

## Instructors

- Executive table-first directory on desktop with mobile card fallback.
- Add Instructor, Import Excel, Download Template, and Load Test Instructors remain available to the Academy Manager.
- Instructor Profile and Program links are preserved.

## Other workspaces

Schedule, Finance, Documents, Reports, History, Training, Administration/Profile, Weekly Planner, Monthly Planner, and Quarterly Planner share the same Revision 19 spacing, cards, tables, typography, control sizing, and responsive rules.

Finance continues to display numeric values without a hard-coded SAR label.

## Governance preserved

- Manager Dashboard is Academy Manager-only.
- Team Members management is Academy Manager-only.
- Administration remains manager-restricted in the prototype.
- Contributors complete Position-owned deliverables.
- Only the Academy Manager receives the final lifecycle-stage completion/handoff control.
- Academy Manager controls remain available across all eight lifecycle stages.

## Themes preserved

All seven live themes remain functional:

1. Terracotta
2. Ocean
3. Forest
4. Plum
5. Midnight
6. Sandstone
7. Rose

Revision 19 styling uses the existing live theme tokens rather than introducing a separate hard-coded palette.
