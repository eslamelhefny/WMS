# Revision 16 — Manager Completion & Team Workflow

## Scope

Revision 16 implements the UI/workflow decisions approved after Revision 15. The goal is to make the Academy Manager's daily control flow clearer while preserving the existing eight-stage Academy lifecycle and the seven existing themes.

## Implemented UI decisions

### Fixed Academy sidebar
- Desktop sidebar is fixed to the viewport and no longer moves with page content.
- Academy emblem and product name are integrated into the same sidebar surface rather than appearing as a separate floating header.
- The profile/footer area is anchored to the bottom.
- **Hide Sidebar** is the final control at the bottom of the sidebar.
- The content area reflows correctly when the sidebar is hidden or restored.

### Dashboard — Insight card system
The six Command Dashboard summary cards now use the selected **Insight** design. Each card combines:
- a large operational metric;
- short context explaining the metric;
- state/attention messaging;
- progress or health indication;
- a direct action destination.

Cards cover Active Programs, Open Tasks, Overdue, Upcoming Sessions, Instructor Readiness, and Financial Position.

### Tasks — dedicated Team workflow
The manager workflow is now separated into three levels:
1. **Tasks Dashboard** — team-level work control.
2. **Team Members** — dedicated directory with member workload, assigned-task counts, overdue work, completion, and workload state.
3. **Team Member Profile** — member details plus every assigned task and full filtering.

The Team Member Profile task filters include:
- Search
- Program / Project
- Stage
- Status
- Priority
- Due date
- Task type

Creating a task from a Team Member Profile assigns the task to that member's Position context. The current prototype's local data model contains one local employee profile and Position-based task ownership; where a configured team directory is available, the UI uses the real member name/profile and otherwise safely falls back to the Position name.

## Academy Manager lifecycle completion

The Academy Manager now receives one consistent **Academy Manager Control** panel on every stage in the consolidated lifecycle:

1. Request & Greenlight
2. Curriculum
3. Instructor Setup
4. Launch, Commercial, Operations & Finance
5. Readiness, Delivery & Assessment
6. Graduate Outcomes
7. Reporting & Improvement
8. Final Closure

For every stage the Manager Control panel exposes:
- stage number and current state;
- completion requirements;
- missing/blocking requirements;
- completed requirement count;
- explicit **Complete Stage** action when requirements are satisfied;
- progression into the next lifecycle stage;
- existing audit trail recording through the stage completion functions.

The Academy Manager can exercise the required authority across all lifecycle stages while the underlying evidence and validation rules remain enforced. The manager override does not silently bypass required curriculum, instructor, launch, finance, assessment, graduate outcome, reporting, or closure evidence.

## Data integrity
- No representative review/test data is stored in the packaged application.
- The packaged JSON store contains 0 tasks, 0 programs, 0 assignments, 0 documents, and no user profile.
- The packaged SQLite baseline contains no profile, task, program, assignment, notification, audit, or document rows.
