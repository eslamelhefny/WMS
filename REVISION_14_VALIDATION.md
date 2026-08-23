# Revision 14 Validation

## Automated responsive UI audit

Chromium's layout engine was used in an isolated test harness because the managed browser environment blocks direct URL navigation to localhost. The harness loaded the actual Revision 14 HTML/CSS/JavaScript and representative app data while mocking only the local API transport.

### Viewports tested

- 390 × 844 — compact phone
- 430 × 932 — large phone
- 768 × 1024 — tablet portrait
- 1024 × 768 — tablet landscape
- 1366 × 768 — laptop
- 1440 × 900 — desktop
- 1920 × 1080 — large desktop

### Workspaces tested at every viewport

Dashboard, Tasks, Weekly Planner, Monthly Planner, Quarterly Planner, Programs, Program Workspace, Instructors, Instructor Profile, Operations, Finance, Schedule, Documents, Reports, History, Training, Administration, and Profile.

**Total responsive cases: 126.**

### Final results

- JavaScript page errors: **0**
- Document-level horizontal overflow cases: **0 / 126**
- Visible clipped control/card cases outside intentional scroll regions: **0 / 126**
- Audited visible text below 10 px: **0 / 126**
- Audited undersized interactive targets: **0 / 126**

## Theme coverage audit

All seven themes were switched live and validated across five high-density representative workspaces: Dashboard, Programs, Instructors, Finance, and Schedule.

**Theme/screen checks: 35.** Each theme produced its own expected primary theme token while the screens continued to use shared themed surfaces and borders.

Validated primary colors:

- Terracotta — `#8F4F3B`
- Ocean — `#1F5F7A`
- Forest — `#315F45`
- Plum — `#5C3D68`
- Midnight — `#243A60`
- Sandstone — `#76542D`
- Rose — `#8B4058`

## Code checks

- `python3 -m py_compile server.py` — passed.
- Extracted application JavaScript with `node --check` — passed.
- Final package data was restored to the clean baseline: no test user, tasks, or Programs are included.

## Notes

The responsive audit intentionally allows horizontal scrolling inside components where dense information requires it, such as Schedule calendars and wide data tables. The pass criterion is that those components scroll internally and never widen the overall page.
