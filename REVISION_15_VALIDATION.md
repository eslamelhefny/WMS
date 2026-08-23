# Revision 15 Validation

## Actual-render responsive audit

The actual Revision 15 HTML/CSS/JavaScript was loaded in Chromium with representative app data and a mocked local API transport. Seven viewport sizes were checked across 18 workspaces:

- 390 × 844 — compact phone
- 430 × 932 — large phone
- 768 × 1024 — tablet portrait
- 1024 × 768 — tablet landscape
- 1366 × 768 — laptop
- 1440 × 900 — desktop
- 1920 × 1080 — large desktop

Workspaces: Dashboard, Tasks, Weekly Planner, Monthly Planner, Quarterly Planner, Programs, Program Workspace, Instructors, Instructor Profile, Operations, Finance, Schedule, Documents, Reports, History, Training, Administration, and Profile.

**Responsive cases: 126**

Final results:
- Document-level horizontal overflow: **0 / 126**
- Truncated top-bar page titles: **0 / 126**
- Visible audited text below 10 px: **0 / 126**
- JavaScript page errors: **0**
- Audited undersized interactive-target cases using the review thresholds: **0**

Behavior checks:
- Mobile Tasks secondary filters: **collapsed by default**
- Mobile Tasks Search: **visible by default**
- Mobile Filters control updates `aria-expanded`: **passed**
- Dashboard Manager Controls: **collapsed by default**

## Theme audit

All seven existing themes were switched live across Dashboard, Programs, Instructors, Finance, and Schedule.

**Theme/screen checks: 35**
- Theme-related page errors: **0**
- Document overflow in theme checks: **0**
- Expected live primary tokens were observed for Terracotta, Ocean, Forest, Plum, Midnight, Sandstone, and Rose.

## Code and data checks

- `python3 -m py_compile server.py` — passed
- Extracted inline application JavaScript with `node --check` — passed
- Packaged `store.json` — no registered user, tasks, Programs, or assignments
- Packaged SQLite database — `tasks=0`, `programs=0`, `assignments=0`

## Notes

The visual-review harness uses representative data so populated layouts, workload cards, stage intelligence, calendar placement, finance charts, and profile content can be inspected. The representative data exists only inside the test harness and screenshots; it is not saved into the application package.
