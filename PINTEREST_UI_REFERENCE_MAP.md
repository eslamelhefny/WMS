# Pinterest UI Reference Map — Revision 12

This revision uses Pinterest as an inspiration library, then translates recurring patterns into the Andalusia Academy brand instead of copying a single design.

## Screen-by-screen direction

| Andalusia screen | Pinterest inspiration category | Selected pattern | Applied in Revision 12 |
|---|---|---|---|
| Dashboard | Education dashboard / school admin dashboard | Editorial hero + compact KPIs + clear content zones | Kept strong hero, softened cards, reduced visual noise, unified spacing |
| My Tasks | Task management dashboard | Focused task list with predictable filters and clear status chips | Unified filters, table hierarchy, buttons, badges, and card spacing |
| Weekly Planner | Project/task planner | Segmented view controls + simple date navigation | Restyled planner tabs and controls into a compact segmented system |
| Monthly Planner | Calendar UI | Familiar calendar grid with low-noise controls | Unified tabs, cards, borders, and active states |
| Quarterly Planner | Project timeline / planning dashboard | Summary-first planning view | Unified KPI and card treatment |
| Programs | Program/project management dashboard | Card-based program portfolio with progress + status | Unified program cards, hover behavior, progress visuals, and page header |
| Program Workspace | Project detail dashboard | Stage flow + detail panel + side activity rail | Retained lifecycle logic while standardizing page hierarchy and cards |
| Instructors | Teacher dashboard / instructor management | People-first profile cards instead of spreadsheet-first presentation | Replaced 13-column directory with responsive instructor profile cards |
| Instructor Profile | LMS instructor details | Profile hero + KPIs + engagement details + courses/programs + activity | Added a new dedicated profile page for every instructor |
| Operations | Workflow/operations dashboard | Compact operational cards with progress and ownership | Unified operational cards, spacing, and progress visuals |
| Finance | Financial dashboard | Summary KPIs above detailed records | Refined KPI language and table hierarchy |
| Schedule | Calendar/schedule dashboard | Metric-first schedule + structured records | Unified page header, filters, KPIs, and table styling |
| Documents | Document management dashboard | Search/filter bar + card/file presentation | Standardized filters, cards, empty states, and action controls |
| Reports | Analytics/report dashboard | Segmented report mode + controls + clean report canvas | Restyled report tabs, control panel, preview surface, and tables |
| History | Activity log / audit trail UI | Simple chronological scan pattern | Unified tabs, filters, row hierarchy, and neutral surface styling |
| Training | LMS/course dashboard | Guided content + progress map | Standardized cards, page hero, and content surfaces |
| Administration | Admin settings UI | Sectioned settings rather than flat utility wall | Unified settings navigation, panels, controls, and system cards |
| Profile | Admin/profile settings | Profile summary + grouped settings/tools | Unified surface hierarchy, forms, cards, and tool groups |
| Add Task / Drawers | SaaS form/modal UI | Clear field grouping + sticky actions | Preserved good form flow and aligned it with Revision 12 components |
| Mobile More | Mobile overflow navigation | Bottom sheet for secondary modules | Preserved existing strong pattern and aligned colors/spacings |

## Design system selected

- Brand direction: warm terracotta Andalusia identity, not generic blue SaaS.
- Navigation: dark brand sidebar, high-contrast selected item, quiet hover states.
- Surfaces: white cards on a warm neutral canvas with low shadow and light borders.
- Radius: 16–22px depending on hierarchy.
- Page headers: consistent title, eyebrow, supporting description, and optional action.
- Filters: one reusable control language across all workspaces.
- Tabs: segmented controls rather than unrelated button styles.
- KPIs: compact, editorial cards with a small accent rail and strong numbers.
- Tables: softer headers, more breathing room, clearer hover, less spreadsheet feel.
- Empty states: dashed neutral panel with concise message and contextual CTA where available.
- People: instructor cards and dedicated profile workspace rather than forcing personnel data into a wide table.
- Mobile: single-column content, two-column KPI grids, touch-friendly actions, no document-level horizontal overflow target.

## Instructor Profile functionality

Every instructor from master data now has a profile route inside the single-page application. The profile aggregates existing program-linked instructor records and shows:

- status and engagement source
- level and work schedule
- assigned groups
- linked Programs
- scheduled sessions
- recorded engagement fees
- average program feedback where available
- contract readiness
- onboarding readiness
- Program-linked instructor activity
- direct links back to the relevant Program workspace

No fake personal contact information is generated. If contact data is not present in the current data model, the profile states that it is not recorded.
