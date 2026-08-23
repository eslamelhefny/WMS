# Revision 13 UI Decisions

## Locked choices

### Main Dashboard — Command + Balanced
The first viewport prioritizes action rather than decorative analytics. The dashboard shows six critical KPIs followed by Needs Attention and Today’s Schedule, then Program Health and My Tasks, Instructor Readiness and Upcoming Delivery, and finally Finance Snapshot and Recent Activity. Existing Academy Manager launch decisions and crew controls remain available below the command panels.

### Tasks Dashboard — Hybrid Manager View
The manager sees the whole team first, including task status, overdue/blocked work, due-today work, high-priority work, overloaded team Positions, and available capacity. Team Position cards show total/open/overdue counts and workload. Selecting a card filters the detailed table to that Position. Manual personal tasks remain supported.

### Programs — Portfolio + Stage Intelligence
The underlying eight-stage lifecycle is unchanged:
1. Request & Greenlight
2. Curriculum
3. Instructor Setup
4. Launch, Commercial, Operations & Finance
5. Readiness, Delivery & Assessment
6. Graduate Outcomes
7. Reporting & Improvement
8. Final Closure

The new UI gives them shorter scanning labels (Planning, Curriculum, Instructor, Launch & Ops, Delivery, Outcomes, Evaluation, Closeout) without changing stored stage names or workflow rules. Each stage shows Program count, on-track / at-risk / overdue counts, purpose, key actions, and Programs currently in that stage.

### Instructors — Analytics + Dedicated Profile
The directory keeps people-first profile cards and adds summary analytics for total, assigned, available, ready, external, average Program load, readiness distribution, and attention items. Every instructor can open a dedicated profile with Program assignments, sessions, engagement fees, feedback, readiness, Program list, and activity history.

### Schedule — Calendar
The Schedule is now calendar-first with a seven-day week, week navigation, Today agenda, upcoming sessions, summary KPIs, and an Agenda view for the detailed table. It uses the existing delivery session records and does not invent room data that is not stored.

### Finance — Analytical
Finance now summarizes total revenue, sponsorship collections, cost, net result, margin, and open settlements. It adds Program revenue/cost comparison, cash flow, revenue mix, profitability, settlement health, and closure health while preserving the existing detailed finance table and Program links.

## Data-model constraint retained
The current prototype stores workflow ownership by **Position**, not a multi-user employee directory. Revision 13 therefore presents manager team workload by Position and uses the registered employee name for their own Position where possible. A future multi-user version can map those Position cards to actual employee records without redesigning the Tasks UI.
