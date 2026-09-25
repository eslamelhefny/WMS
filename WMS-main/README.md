# Andalusia Academy Work Management System — Prototype V5 Revision 17 Clear Informative UI

## Plan and Visits

- **Plan** is a dashboard of operational activities, networking visits, and open visit follow-ups, grouped into **In progress** and **Upcoming**. Summary cards show completed and overdue items as well. Activity dates use the program start date; visits and follow-ups use their own dates.
- **Visits → Contact directory** stores reusable contact names, organizations, roles, email addresses, phone numbers, and relationship notes. Use **History** to see a contact's visits.
- **Visits → Visit records** lets you add and edit a visit's contact, program (or General networking), activity, date/time, type, location, purpose, outcome, status, and follow-up. A completed visit requires an outcome. Follow-up dates cannot precede the visit. Mark follow-ups complete in the visit editor or cancel an unwanted visit using its status.
- Both workspaces support combined **Program**, **Activity**, and text filters. Contact-directory program/activity filters select contacts through their linked visits. Unvisited contacts appear when those filters are cleared.
- Existing operational interactions appear in the Visits database and open in their original activity. New networking visits are separate relationship records; they do not change operational lifecycle completion or replace its evidence requirements.
- Both tabs are available in the desktop sidebar, mobile **More** menu, and Profile's default-view selection. The existing calendar **Planner** remains available.
- Contact and networking visit records are stored in `masterData.networking`, persisted by the existing SQLite store and included in JSON backup export/import. The existing Excel export remains the personal-task workbook.

### Networking verification

Run `python tests/networking_server.py` to start an isolated test database on port 8876, then `node tests/networking.test.cjs` with Playwright installed (and Microsoft Edge available). The test server writes only to `tests/test-data`, never the app's `data` directory. Checks cover forms, validation, combined filters, operational history, follow-up status, SQLite reload, JSON backup, mobile navigation, and page overflow. Screenshots are written to `tests/`.

Revision 17 implements the clearer, more informative screen direction approved in the visual design review while preserving the Revision 16.4 workflow, role-governance, lifecycle, instructor-import, and SVG-icon behavior.

## Revision 17 — clearer information architecture

- **Manager Dashboard:** concise Insight KPIs, operational attention, schedule, Program health, My Tasks, instructor readiness, upcoming delivery, Finance snapshot, and recent activity with advanced manager controls collapsed by default.
- **Programs:** table-first management view with lifecycle stage, status, owner, dates, progress, and direct actions; mobile automatically switches to readable Program cards.
- **Program Workspace:** clearer Program identity, lifecycle progress, manager completion control, blockers, stage work, and evidence while retaining all eight workflow stages.
- **Tasks:** compact filter controls, summary KPIs, team workload, attention state, and task table while preserving the dedicated Team Members / member-profile flow.
- **Schedule:** weekly hourly delivery calendar with agenda controls and deliberate internal horizontal scrolling where the time grid requires it.
- **Finance:** clean KPI + analytics hierarchy with no hard-coded SAR suffix; Program profitability, settlements, and finance records remain connected to real Program data.
- **Documents / Reports:** cleaner search/filter hierarchy, compact records, and report tiles consistent with the approved mockups.
- **Shared UI:** fixed navy sidebar with bottom Hide Sidebar control, consistent SVG icons, restrained borders/shadows, cleaner typography, and clearer table/card density.
- **Responsive:** all 21 audited workspaces pass at 7 viewport sizes (147 cases) with no root-page horizontal overflow, no visible leaf text below 10 px, no audited mobile controls below the target size, and no JavaScript page errors.

See **REVISION_17_CLEAR_UI_REPORT.md** and **REVISION_17_VALIDATION.md**.

Revision 15 is a visual-quality pass performed against the **actual rendered application**, not concept images. It preserves the approved Revision 13 workflows and Revision 14 theme system, then corrects the small details that a technical overflow test alone cannot catch: hierarchy, density, touch targets, mobile title truncation, filter behavior, stage scanning, calendar usefulness, report length, profile tool visibility, and compact-control readability.

## Revision 15 — actual-output polish

- **Dashboard:** restored strong Command hero contrast on every size, surfaced launch-decision exceptions in Needs Attention, and collapsed advanced manager controls by default to keep the Balanced dashboard focused.
- **Tasks:** mobile Search stays visible while secondary filters collapse behind a Filters control; long member task lists now default to a manageable subset with Show All / Show Less.
- **Programs:** Lifecycle Intelligence selects the most meaningful non-empty/risk stage on first load instead of opening an empty stage.
- **Program Workspace:** the eight-stage navigator now uses concise stage labels for scanning while retaining the full stage names in accessible labels/tooltips.
- **Schedule:** replaced the sparse day-card calendar with a true hourly week timeline (08:00–20:00) while retaining Agenda view.
- **Operations:** added selected-Program KPIs for activity count, completion, open follow-ups, and average progress.
- **Finance:** main financial KPIs use neutral numeric amounts without a hard-coded currency suffix, and Program chart labels can wrap to two lines instead of unreadable truncation.
- **Reports / Weekly Planner:** long content is contained inside deliberate scroll regions on desktop so the entire page no longer grows unnecessarily.
- **Profile:** import/export/test-data utilities are grouped inside a collapsed Data, backup & developer tools section.
- **Mobile usability:** page titles no longer truncate, compact actions/tabs meet a 44 px minimum audited target through tablet widths, and document references use a readable minimum text size.
- **Themes:** all seven existing themes remain intact across the full application.

See **REVISION_15_ACTUAL_OUTPUT_REVIEW.md** and **REVISION_15_VALIDATION.md**. The included ACTUAL_UI_REVIEW images are screenshots of the implemented HTML/CSS/JavaScript rendered with representative review data; that review data is not included in the packaged store.

Revision 14 keeps the approved Revision 13 Command Center workflows and adds a complete application-wide theme and responsive sizing layer. The seven existing themes now drive the shared surfaces, accents, borders, charts, tabs, filters, cards, and high-density dashboards instead of styling only selected areas. Typography, controls, tables, cards, stages, Schedule, Finance, Program Workspace, and Instructor Profile were also normalized across phone, tablet, laptop, desktop, and large-desktop sizes.

## Revision 14 — themes and responsive scale

- **All seven existing themes retained and expanded:** Terracotta, Ocean, Forest, Plum, Midnight, Sandstone, and Rose.
- **Theme coverage is application-wide:** Dashboard, Tasks, Planner, Programs, Program Workspace, Instructors, Instructor Profile, Operations, Finance, Schedule, Documents, Reports, History, Training, Administration, and Profile all use the selected theme tokens.
- **Revision 13 blue-only accents removed from shared UI:** newer command-center cards, stage indicators, charts, filters, tabs, Schedule and Finance now inherit the active theme while semantic success/warning/error colors remain stable.
- **Responsive scale normalized:** spacing, card grids, typography, buttons, forms, tables, stage strips, team-member cards, Schedule, Reports, Finance, and profile surfaces adapt from 390 px phones through 1920 px desktops.
- **Microcopy readability raised:** visible audited UI text is 10 px or larger, with larger body/control text where appropriate.
- **Touch and control sizing improved:** mobile controls use 46 px sizing and coarse-pointer targets use at least 44 px; sliders receive a larger interaction box without visually enlarging the track.
- **Tables and calendars stay contained:** dense records use explicit horizontal scroll regions instead of widening the whole page.

See **REVISION_14_THEME_RESPONSIVE_REPORT.md** and **REVISION_14_VALIDATION.md** for the implementation and test matrix.

## Revision 13 — approved UI direction

- **Main Dashboard — Command + Balanced:** six operational KPIs, Needs Attention, Today’s Schedule, Program Health, My Tasks, Instructor Readiness, Upcoming Delivery, Finance Snapshot, and Recent Activity.
- **Tasks — Hybrid Manager View:** whole-team summary, attention indicators, workload by team Position, and detailed tasks for one selected Position/member. The current data model assigns workflow work to Positions; the current employee name is shown for their own Position where available.
- **Programs — Portfolio + Lifecycle Intelligence:** portfolio KPIs, all eight lifecycle stages visible together, stage purpose/actions/risk counts, Programs in each stage, and richer Program cards.
- **Instructors — Analytics + People-First Directory:** network KPIs, readiness/availability analytics, attention items, profile cards, and a dedicated Instructor Profile for every instructor record.
- **Schedule — Calendar:** weekly seven-day delivery calendar, Today agenda, upcoming sessions, calendar/agenda switch, instructor coverage, and detailed session records.
- **Finance — Analytical:** revenue/cost/net/margin KPIs, Program comparison chart, cash-flow summary, revenue mix, profitability, settlement/closure health, and detailed Program finance records.

See **REVISION_13_UI_DECISIONS.md** and **REVISION_13_VALIDATION.md** for the implementation scope and checks.

## Previous UI/UX hardening retained

## Revision 10 UI/UX fixes

- Eliminates document-level horizontal overflow across the tested 390×844, 1280×720, and 1920×1080 viewports.
- Adds a mobile **More** navigation sheet so every secondary workspace remains reachable on small screens.
- Keeps the current page title visible on mobile and restores useful top-bar labels on wider desktop layouts.
- Adds visible keyboard focus states, larger touch targets, reduced-motion support, and stronger disabled/placeholder states.
- Gives dialogs semantic roles, focus management, Escape handling, focus trapping, and focus restoration.
- Associates form labels and hints programmatically, including dynamically rendered delivery-session fields.
- Makes interactive Program cards and dynamic result cards keyboard-operable.
- Increases microcopy/table/control readability and removes hover elevation from non-clickable cards.
- Improves table usability with horizontal regions, sticky first columns, and swipe guidance on narrow screens.
- Converts dense mobile dashboard analytics into a horizontal snap row instead of an excessively long stack.
- Prevents Profile, Reports, Programs, and filter/control groups from widening the mobile page.
- Adds accessible status announcements for save/toast feedback and readable labels for icon-only controls.

See **UI_UX_FIX_REPORT.md** for the audit, implementation notes, and validation matrix.

## Review changes included

- The sidebar can be hidden from inside the navigation and restored with a fixed **Show sidebar** button.
- Sidebar visibility is remembered on the same device and can be changed without leaving the current screen.
- Hiding the sidebar releases its full width to the workspace, improving the Stage and dashboard layouts at 1280×720.
- The Andalusia Academy emblem is softly blended into the compact top-bar background while the readable wordmark remains available.
- Stages 4–8 display an explicit **Academy Manager · Stage Completion** control when the Academy Manager Position is active.
- Manager completion uses the existing workflow validators; required fields, evidence, approvals, counts, incidents, follow-ups, Finance separation, and lifecycle gates are not bypassed.
- Combined Stage 4 and Stage 5 assignments are normalized into the correct **Stage Work** panel, including legacy subsection assignment names.
- The Andalusia Academy logo is removed from the sidebar and displayed once in the compact top bar.
- The top bar is reduced to a 52 px desktop control bar, with responsive control labels for HD and 720p displays.
- The sidebar includes a new **Instructors** workspace for the Academy instructor directory and Program assignments.
- The Instructor workspace shows R/H, Project Based, Part / Full Time, Level, Assigned Groups, Internal / External, fee, contract, onboarding, status, and direct Program access.
- Instructor KPIs show total unique instructors, selected instructors, external instructors, and ready/onboarded instructors.
- Instructor search and Program / Directory filters are included.
- **Save Draft** stores Stage 1 without changing its Active/Returned status and without creating approval work.
- **Submit for Greenlight** validates every required Stage 1 field, locks the submitted request, creates one Academy Manager approval, and records only the submission audit event.
- Stage 1 clearly explains the different results of Save Draft and Submit for Greenlight.
- Missing Greenlight requirements are shown together in the Program Workspace.
- A complete Academy Manager lifecycle was validated through all eight stages and Final Closure.
- Adds the **Curriculum Developer** Position.
- Allows **Academy Manager** and **Program Operations Executive** to create Programs.
- Stage 2 requires **Outline, Topic, Competences, and Duration**.
- Stage 3 requires **R/H, Project Based, Part / Full Time, Level, Assigned Groups, and Internal / External**.
- Launch Planning includes Instructor Shooting, Supplement Change, the requested workshop planning dataset, P&L, and minimum participants.
- The Academy Manager Dashboard includes Launch Go / No Go decisions and all-crew task assignment and monitoring.
- Former Stages 4, 5, 6, and Finance are combined as **Launch, Commercial, Operations & Finance**.
- Former Stages 7, 8, and 9 remain combined as **Readiness, Delivery & Assessment**.
- The Academy Manager can enter, save, review, approve, and complete every stage and every Position-owned section.
- The Academy Manager can complete open workflow assignments directly from the selected stage's **Stage Work** panel.
- Manager-completed assignments update their linked follow-up, incident, or improvement-action record and leave an audit entry.
- The sidebar has one **Planner** entry; Weekly, Monthly, and Quarterly remain available as tabs inside it.
- The sidebar includes **Finance**, with an all-Program finance portfolio covering PMB and Treasury information.
- The sidebar includes **Schedule**, showing timed sessions for today and future planned dates.
- The manager dashboard presents Launch Planning and Academy Crew Tasks as two compact command cards.
- Both command cards show five records by default, with **See All / Show 5** controls and their own bounded scrolling areas.
- Crew assignment opens only when **Assign Task** is selected, keeping the dashboard focused on decisions and active work.
- **My Work** has been removed from desktop, mobile, dashboard, profile-default, and Position-rule navigation because **My Tasks** is the single personal-work destination.
- The dashboard is tuned for both 1920×1080 HD and 1280×720 displays without horizontal page overflow.

## Eight-stage lifecycle

1. Request & Greenlight
2. Curriculum
3. Instructor Setup
4. Launch, Commercial, Operations & Finance
   - 4A Launch Planning and Academy Manager Go / No Go
   - 4B B2C / B2B Commercial
   - 4C Four parallel Operational Activities and supervisor approval
   - 4D Finance with separate PMB and Treasury responsibilities
5. Readiness, Delivery & Assessment
   - 5A Readiness and Academy Manager decision
   - 5B Delivery, sessions, attendance, evidence, and incidents
   - 5C Assessment, results, and certificates
6. Graduate Outcomes
7. Reporting & Improvement
8. Final Closure

The combined sections remain sequential. Finance opens after Operational Activities are supervisor-approved. Completing Finance closes Stage 4 and opens Readiness.

## Finance controls inside Stage 4

- **Finance — PMB:** actual revenue, actual cost, and final P&L closure.
- **Finance — Treasury:** sponsorship collection, instructor payments, vendor payments, and payment evidence.
- Both Position-owned Finance requirements must be complete before the lifecycle can proceed to Stage 5.

## Academy Manager full-stage authority

When **Academy Manager** is an active Position, the manager can create a Program, fill and submit its request, approve Greenlight, and continue through every lifecycle stage. The Program Workspace displays a full-stage authority notice and enables the active controls for all stage owners. The manager may perform Curriculum drafting and QA, Instructor Setup, all four Stage 4 sections, Readiness preparation and decision, Delivery, Assessment, Graduate Outcomes, Reporting & Improvement, and Final Closure. Stages 4–8 also provide one clear manager completion button that runs the correct existing completion workflow. Required fields, financial separation, count checks, evidence requirements, incidents, handover gates, and Go / No Go rules remain enforced.

## Request & Greenlight actions

- **Save Draft:** keeps the request editable, saves partial information, updates draft progress, and creates no manager approval.
- **Submit for Greenlight:** requires Program Name, Expected Attendees above zero, Preliminary Budget above zero, Objective, and Demand Evidence.
- A successful submission changes Stage 1 to **Pending Approval**, locks its fields, completes the submitter's request assignment, and creates one Academy Manager approval assignment.
- Submission no longer runs or records the Save Draft action first.

## Academy Manager dashboard

- **Launch Planning:** five priority Programs initially, compact planning evidence, direct Program access, reason entry, and Go / No Go actions.
- **Academy Crew Tasks:** five urgent assignments initially, status, owner, stage, due date, priority, assigning manager, and direct task access.
- **Assign Task:** a deliberate expandable panel, available only to Academy Manager.
- **See All / Show 5:** independently controlled for Launch Planning and Crew Tasks.

## Sidebar workspaces

- **Planner:** one navigation entry with Weekly, Monthly, and Quarterly tabs.
- **Instructors:** live Stage 3 instructor assignments plus available Instructor master-data records, engagement fields, readiness controls, search, filters, and direct Program access.
- **Finance:** Program, combined-stage status, finance status, actual revenue, actual cost, sponsorship collected, net result, settlements, P&L, evidence, and Program link.
- **Schedule:** delivery-session date, time, Program, instructor, region, status, and direct Program link, with Today, Planned, and All filters.
- Delivery session date and time are maintained inside **Stage 5 — Readiness, Delivery & Assessment**. Former Delivery and Assessment stages remain combined in this controlled stage.

## Test program

Profile → **Add Stage 2–8 Test Program** creates a clean Program after approved Greenlight and starts at Curriculum.

## Local architecture

- Existing Andalusia UI/UX
- Collapsible sidebar and compact blended Andalusia top bar for HD and 720p desktop displays
- Python local server
- SQLite primary local database
- JSON backup snapshot
- Excel personal-task mirror
- Documents, Search, Reports, Administration, Position Rules, Audit, and Training Mode retained

## Run

Windows: `run.bat`

macOS/Linux: `./run.sh`

Local URL: `http://127.0.0.1:8765`

## Revision 12 — Pinterest-inspired unified UI

Revision 12 applies a unified design language across all primary workspaces using recurring patterns from education, task management, finance, calendar, document management, analytics, LMS, profile, and admin-settings inspiration found on Pinterest.

The Instructors workspace has been redesigned from a wide 13-column table into a responsive people-first card directory. Every instructor now has a dedicated Instructor Profile workspace generated from the existing master-data and Program engagement records.

See `PINTEREST_UI_REFERENCE_MAP.md` for the screen-by-screen design decisions.

## Revision 16 — Manager Completion & Team Workflow

Revision 16 adds the fixed blended Academy sidebar with bottom collapse control, the selected Insight card design on the Command Dashboard, a dedicated Team Members → Team Member Profile task workflow, and a universal Academy Manager completion panel across all eight program lifecycle stages. See `REVISION_16_MANAGER_COMPLETION_REPORT.md` and `REVISION_16_VALIDATION.md` for details.

## Revision 16.2 — Role Governance

Revision 16.2 makes the **Manager Dashboard, Team Members management, Administration, and Academy Manager Control manager-only**. Non-manager users land on My Tasks, see only tasks assigned to their active Position(s), and complete Position-owned deliverables without closing lifecycle stages. Final lifecycle-stage completion and handoff are reserved for the Academy Manager. See `REVISION_16_2_ROLE_GOVERNANCE.md` for the complete access matrix and `REVISION_16_2_VALIDATION.md` for validation details.

## Revision 16.4 update

Revision 16.4 adds a unified internal SVG icon system and Academy Manager instructor-directory controls: manual add, validated XLSX/CSV import with preview, downloadable Excel template, and optional test instructor data. See `REVISION_16_4_SVG_INSTRUCTOR_MANAGEMENT.md` and `REVISION_16_4_VALIDATION.md`.

## Revision 18 — Live Themes

The clear Revision 17 interface now supports live application themes end-to-end. Use **Theme** in the fixed sidebar, the top-bar selector, or the Profile theme choices. Available themes are Terracotta, Ocean, Forest, Plum, Midnight, Sandstone, and Rose. Theme preference persists locally and in the employee profile.


## Revision 19 — Executive UI

Revision 19 implements the approved Executive UI direction across the real application while preserving Revision 18 live themes, the original Academy logo assets, manager-only governance, Team Members drill-down, instructor management/import, and the complete eight-stage Academy Manager lifecycle. The Manager Dashboard now uses Executive insights with targets, variance, compact charts, and strategic performance summaries. Programs, Tasks, Team Members, Instructors, Program Workspace, Schedule, Finance, Documents, Reports, Administration/Profile, planners, and responsive/mobile surfaces share the same tighter executive design system.

See `REVISION_19_EXECUTIVE_UI.md` and `REVISION_19_VALIDATION.md`.
