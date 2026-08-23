# Problem: Full UI/UX Design Audit and Correction

## Project

**Andalusia Academy Work Management System**

The application must undergo a complete UI/UX quality audit. The goal is not merely to verify that pages technically render correctly. The goal is to identify and fix **every visible design, usability, consistency, responsive, accessibility, interaction, and information-hierarchy problem across the entire application**.

The approved UI designs and screenshots must be treated as the visual reference. Existing business logic, permissions, lifecycle rules, data, themes, and Academy branding must remain functional.

---

# Primary Objective

Inspect every screen, every important state, every viewport size, and every theme.

Find and correct all problems related to:

- UI layout
- spacing
- alignment
- typography
- sizing
- card design
- tables
- filters
- forms
- navigation
- sidebar
- headers
- icons
- colors
- themes
- charts
- responsive behavior
- accessibility
- interaction states
- empty states
- loading states
- error states
- information density
- visual hierarchy
- duplicated information
- unclear actions
- workflow usability

Do not stop after the first successful validation.

Perform **multiple independent review passes**.

---

# 1. Visual Match Audit

Compare the actual rendered application with the approved UI design.

For every screen, check:

- overall page composition
- content width
- sidebar width
- header height
- card dimensions
- card placement
- grid proportions
- column proportions
- whitespace
- visual balance
- alignment
- section ordering
- typography hierarchy
- button placement
- filter placement
- table density
- chart dimensions
- lifecycle presentation
- information hierarchy

Do not treat the approved design as loose inspiration.

Reproduce its visual structure as closely as possible while keeping the real system functionality.

Where the approved concept conflicts with real business requirements, preserve the business requirement but redesign it using the same visual language.

---

# 2. Pixel-Level Spacing Audit

Review every major component for consistent spacing.

Check:

- page margins
- section gaps
- card padding
- table-cell padding
- input padding
- button padding
- header spacing
- icon-to-text spacing
- title-to-subtitle spacing
- card-to-card spacing
- vertical rhythm
- mobile spacing

Avoid:

- random 11px / 13px / 17px spacing values
- excessive empty gaps
- components touching each other
- uneven card heights without reason
- different padding for visually identical components

Establish and use a consistent spacing scale.

---

# 3. Typography Audit

Review all visible text.

Check:

- page titles
- section titles
- card labels
- KPI values
- descriptions
- table headers
- table values
- badges
- helper text
- buttons
- filters
- tooltips
- mobile labels

Requirements:

- no unreadably small text
- no accidental bold text
- no inconsistent font weights
- no oversized secondary information
- clear hierarchy between title, subtitle, label and value
- reasonable line-height
- no text clipping
- no unnecessary uppercase text
- no inconsistent capitalization

Desktop body text should generally remain readable at normal viewing distance.

Mobile text must never become tiny just to make content fit.

---

# 4. Dashboard Audit

The Academy Manager Dashboard must be reviewed especially carefully.

Verify:

- Executive Insights are visually clear
- each KPI communicates meaning, not only a number
- trends are understandable
- target and actual values are distinguishable
- variance is clear
- positive/negative indicators are accurate
- charts are not decorative
- Attention Required is immediately visible
- Program Health is understandable
- task information is not duplicated unnecessarily
- financial information is concise
- Today's Schedule is useful
- recent activity has appropriate density
- cards do not all look unnecessarily identical
- no large unused gaps exist

The Manager Dashboard must remain **Academy Manager-only**.

---

# 5. Sidebar Audit

The sidebar must:

- stay fixed
- never move with page content
- visually blend with the Academy logo/branding
- preserve the original Academy logo
- have consistent icon sizes
- have clear active states
- support all themes
- avoid excessive width
- maintain readable labels
- remain usable when collapsed

Footer order must be logical.

The **Collapse / Hide Sidebar** action must remain at the very bottom.

Check desktop, laptop, tablet and mobile navigation separately.

---

# 6. Programs UI Audit

Review:

- Programs table
- search
- filters
- status
- health
- owner
- dates
- progress
- actions
- pagination
- empty states

Ensure important information can be scanned quickly.

Avoid showing too much data at once.

Program health/status/progress must not communicate the same information three different ways unless each has a clear purpose.

---

# 7. Program Workspace Audit

This is one of the highest-priority screens.

Review:

- Program header
- overall progress
- lifecycle
- current stage
- stage requirements
- blockers
- stage ownership
- Program metrics
- finance
- team
- tasks
- documents
- activity
- Manager Control
- next-stage progression

The Academy Manager must always understand:

1. What stage is the Program currently in?
2. What is complete?
3. What is missing?
4. What is blocking completion?
5. Who owns the remaining work?
6. What must happen next?
7. Can the stage be completed?
8. What happens after completion?

The **Academy Manager Control** must be visible only to the Academy Manager.

Contributors may complete their assigned work, but only the Academy Manager can perform the final lifecycle stage completion/handoff.

Verify all eight actual Academy lifecycle stages.

---

# 8. Stage Completion UX Audit

For every lifecycle stage:

Check that there is:

- clear stage name
- status
- requirements checklist
- progress
- missing items
- blockers
- owner information
- completion readiness
- completion action
- next-stage description

If completion is unavailable, never make the user guess why.

Do not simply disable a button.

Display exact blockers such as:

- Instructor not selected
- Contract not signed
- Commercial requirements incomplete
- Finance approval missing
- Sessions not scheduled
- Required evidence missing

When the manager completes the stage:

- provide visible confirmation
- update status immediately
- update lifecycle
- update audit trail
- activate the next stage
- prevent duplicate actions

Test every stage individually and test the complete Stage 1 → Stage 8 journey.

---

# 9. Tasks Manager Audit

Academy Manager Tasks must clearly separate:

- whole-team task summary
- overdue tasks
- blocked tasks
- due today
- workload
- individual assignments

Review:

- KPI cards
- charts
- filters
- table
- status badges
- priorities
- due dates
- assignees
- progress
- actions

Clicking **All Team** must open the dedicated Team Members page.

Do not implement it merely as a filter of the current screen.

---

# 10. Team Members Audit

Review the Team Members page for:

- search
- Position
- Department
- workload
- total tasks
- open tasks
- overdue
- completed
- completion rate
- availability/status
- actions

Clicking a team member must open that member's dedicated profile.

Check whether the table becomes too dense.

Make workload information visually scannable.

---

# 11. Team Member Profile Audit

Review:

- identity
- Position
- contact information
- workload
- Program assignments
- task summary
- assigned tasks
- completion performance
- activity

Assigned Tasks must support complete filtering by:

- Search
- Program
- Stage
- Status
- Priority
- Due Date
- Task Type

Verify that task assignment from this page genuinely assigns the task to that member.

---

# 12. Instructors Audit

Review:

- Instructor directory
- profile presentation
- filters
- status
- specialty
- availability
- Programs
- sessions
- ratings/readiness
- actions

Manager-only controls:

- Add Instructor
- Import Excel
- Load Test Instructors
- Download Excel Template

Excel import must have:

1. Upload
2. Validation
3. Preview
4. Conflict reporting
5. Confirmation
6. Import result

Never silently import invalid rows.

---

# 13. Schedule Audit

Review:

- day/week/month navigation
- date controls
- hourly calendar
- sessions
- colors
- instructor
- venue
- conflicts
- today's agenda
- responsive scrolling

Avoid large blank vertical areas.

Calendar events must be readable without overcrowding.

Tablet layouts require special review.

---

# 14. Finance Audit

Review:

- revenue/income
- costs/expenses
- budget
- net position/surplus
- collections
- receivables
- charts
- filters
- transactions
- Program finance

Do not display **SAR** anywhere.

Check number formatting and chart consistency.

Financial visualizations must communicate useful information rather than adding decorative charts.

---

# 15. Documents Audit

Review:

- search
- filtering
- categories
- file type
- owner
- Program
- date
- size
- download/view/edit actions
- upload
- empty state

Ensure file actions use consistent SVG icons and tooltips.

---

# 16. Reports Audit

Review:

- report categories
- cards
- filters
- report generation actions
- charts
- export
- mobile behavior

Avoid visually oversized empty report cards.

Make the primary action obvious.

---

# 17. Administration & Profile Audit

Administration should not look like another analytics dashboard.

Use clear settings navigation.

Review:

- Profile
- Account
- Roles/permissions
- Security
- Preferences
- Notifications
- Theme
- Integrations
- audit settings

Avoid extremely long single-page forms.

Group related settings logically.

---

# 18. SVG Icon Audit

The application must use the unified SVG icon system.

Check:

- sidebar icons
- buttons
- cards
- filters
- lifecycle
- status
- Finance
- Schedule
- Documents
- Reports
- Tasks
- Instructors

Requirements:

- consistent 16 / 20 / 24px sizes
- consistent stroke weight
- `currentColor`
- theme support
- accessible labels
- tooltips where needed
- no mixed emoji
- no Unicode symbols pretending to be icons
- no random icon families

Remove decorative icons that add no information.

---

# 19. Theme Audit

Test every screen using all existing themes:

- Terracotta
- Ocean
- Forest
- Plum
- Midnight
- Sandstone
- Rose

Themes must affect the full product consistently.

Verify:

- sidebar
- navigation
- buttons
- links
- focus
- cards
- tables
- lifecycle
- charts
- accents
- selected states

Semantic states must remain consistent:

- success = green
- warning = amber/orange
- error/blocked/overdue = red
- informational = appropriate neutral/info treatment

The Academy logo must remain exactly unchanged between themes.

---

# 20. Responsive Audit

Test every workspace at minimum:

- 390 × 844
- 430 × 932
- 768 × 1024
- 1024 × 768
- 1366 × 768
- 1440 × 900
- 1920 × 1080

For every viewport inspect:

- page width
- sidebar/navigation
- card grid
- table width
- filters
- forms
- modals
- charts
- lifecycle
- headers
- buttons
- text
- spacing
- touch targets

No page-level horizontal overflow is allowed.

Internal horizontal scrolling is allowed only where genuinely appropriate, such as dense calendars or large tables.

---

# 21. Mobile UX Audit

Do not simply shrink the desktop layout.

Review mobile separately.

Check:

- bottom navigation
- More navigation
- fixed actions
- filter sheets
- card stacking
- table-to-card transformations
- stage scrolling
- chart sizing
- form layout
- modal layout
- Profile length
- touch targets

Interactive controls should generally be at least **44 × 44 px** on touch devices.

---

# 22. Accessibility Audit

Check:

- keyboard navigation
- focus states
- form labels
- ARIA labels
- buttons
- dialogs
- color contrast
- status communication
- icon-only controls
- headings
- reduced-motion preference

Do not rely on color alone to communicate status.

---

# 23. Interaction-State Audit

For every major interactive component inspect:

- default
- hover
- focus
- active
- selected
- disabled
- loading
- success
- warning
- error

Check:

- buttons
- cards
- links
- tabs
- filters
- dropdowns
- tables
- pagination
- modals
- form controls
- file uploads

No interaction should appear to do nothing.

---

# 24. Empty-State Audit

Test screens with zero data.

Every empty state should explain:

- what is empty
- why the section exists
- what the user can do next

Avoid giant blank cards.

Where appropriate provide a primary action.

---

# 25. Data-Density Audit

For every screen ask:

- Is this information necessary?
- Is anything duplicated?
- Could two cards become one?
- Is a chart more useful than a number?
- Is a number more useful than a chart?
- Is the table showing too many columns?
- Is important information buried?
- Is secondary information too prominent?

Remove visual noise.

Do not maximize the amount of data merely because space is available.

---

# 26. Multi-Pass Review Requirement

The audit must be performed at least **four times**.

### Pass 1 — Structural

Review:

- page architecture
- sections
- grids
- hierarchy
- navigation
- information placement

Fix all structural problems.

### Pass 2 — Visual

Review:

- typography
- spacing
- colors
- cards
- borders
- icons
- tables
- charts
- alignment

Fix visual inconsistencies.

### Pass 3 — UX & Responsive

Review:

- interactions
- forms
- filters
- stage completion
- mobile
- tablet
- accessibility
- touch targets
- empty/error states

Fix usability problems.

### Pass 4 — Final Regression

Review everything again after the previous changes.

Verify that fixing one screen did not break another.

Do not rely only on automated measurements.

Inspect the actual screenshots visually.

---

# 27. Visual Screenshot Review

Capture actual rendered screenshots for every major workspace.

Create:

- desktop comparison sheet
- mobile comparison sheet
- theme comparison sheet
- approved-design vs actual-output comparison

Look for visual problems that automated tests cannot detect, including:

- awkward whitespace
- poor balance
- oversized cards
- tiny cards
- poor hierarchy
- excessive density
- weak contrast
- uneven rows
- inconsistent component proportions
- visually confusing controls

---

# 28. Required Validation

Before release, verify:

- no JavaScript page errors
- no broken buttons
- no dead links
- no broken SVG icons
- no clipped titles
- no unexpected root-level horizontal scrolling
- no tiny unreadable text
- no undersized touch controls
- no inaccessible form controls
- no duplicate stage-completion actions
- no accidental manager controls for contributors
- all seven themes work
- logo files remain unchanged
- all eight Program stages are completable by the Academy Manager
- contributor permissions remain correct
- Commercial completion works for B2C, B2B and Mixed Programs
- Team Members navigation works
- Team Member Profile filters work
- instructor Excel import works
- Finance UI contains no SAR labels

---

# 29. Acceptance Standard

Do not consider the task finished merely because:

- the page loads
- there are no syntax errors
- there is no horizontal overflow
- the CSS looks approximately correct

The task is complete only when the application feels like **one professionally designed product**.

The final UI should be:

- clear
- informative
- consistent
- polished
- efficient
- accessible
- responsive
- role-aware
- action-oriented
- visually balanced

The final implementation must undergo **multiple actual-render screenshot reviews before packaging**.

Any defect discovered during the final review must be fixed and the complete regression audit repeated.