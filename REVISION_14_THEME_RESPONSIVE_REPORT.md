# Revision 14 — Unified Themes & Responsive Scale

## Goal

Apply the application's existing theme choices consistently to every workspace and review the complete UI size system across common device widths without changing the Revision 13 workflow decisions.

## Existing themes applied

1. Terracotta
2. Ocean
3. Forest
4. Plum
5. Midnight
6. Sandstone
7. Rose

The live theme now controls the shared background, surface tint, borders, primary accent, secondary accent, focus states, sidebar/hero gradient, card shadows, tabs, filter controls, stage indicators, command-center accents, Schedule accents, Finance bars, and reusable UI states. Semantic green/amber/red statuses remain semantic so changing theme does not change the meaning of success, warning, or error.

## Workspaces covered

- Dashboard — Command + Balanced
- Tasks — Hybrid Manager View
- Weekly Planner
- Monthly Planner
- Quarterly Planner
- Programs
- Program Workspace / all eight stages
- Instructors
- Instructor Profile
- Operations
- Finance
- Schedule
- Documents
- Reports
- History
- Training
- Administration
- Profile

## Responsive sizing changes

- Fluid main-content padding with a large-desktop content cap.
- Six-column KPI grids collapse to three, two, and one columns as space reduces.
- Program and Instructor card grids collapse from four columns to three, two, and one.
- Team-member cards become a horizontal snap row on mobile.
- Program stages become a horizontal snap strip on mobile.
- Schedule and report tables remain inside explicit horizontal scroll containers.
- Task filters collapse before they can overflow at tablet widths.
- Reports switch to a single-column control/preview layout at narrower widths.
- Forms and controls use 42 px desktop sizing and 46 px mobile sizing.
- Coarse-pointer devices enforce 44 px interaction targets.
- Tiny 7–9 px labels in Command Center, stages, instructor cards/profile, Schedule and Finance were raised to a minimum readable scale.
- Reduced-motion preference remains supported.

## Theme implementation approach

Revision 14 rebinds the older Revision 12 and Revision 13 design tokens to the application's existing live theme variables. This avoids maintaining separate visual palettes per module and prevents new screens from drifting back to hard-coded blue/terracotta styling.

The system therefore preserves one design language while still allowing the user to switch the overall visual theme from the existing theme selector.
