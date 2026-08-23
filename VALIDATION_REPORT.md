# Prototype V5 Review Revision 9 — Validation Report

Validated on 17 August 2026 with disposable Academy Manager Programs. Revision 9 was exercised through the browser at 1920×1080 and 1280×720, including sidebar persistence, Stage 4 completion, and the complete manager path across Stages 5–8. Generated validation data was removed before packaging.

## Build checks passed

- Embedded frontend JavaScript syntax
- Python server syntax
- Clean local server start and HTTP data access
- Revision 9 page title, local build identifier, and server title
- Eight-stage lifecycle displayed in the Program Workspace

## Revision 9 interface passed

- **Hide Sidebar** removed the sidebar and returned its width to the Program Workspace.
- The fixed **Show sidebar** control restored the sidebar at 1280×720 and 1920×1080.
- Hidden state persisted through reload and could be reopened normally.
- The top bar retained the compact Andalusia wordmark and displayed the low-opacity blended emblem background.
- The 1280×720 hidden-sidebar view kept the manager completion control and Stage Work panel readable.
- Existing Planner, Programs, Instructors, Operations, Finance, Schedule, Documents, Reports, History, Training, Administration, and Profile navigation remained present.

## Academy Manager Stage 4–8 completion passed

- Each lifecycle Stage from 4 through 8 displayed a dedicated Academy Manager completion panel.
- Stage 4 correctly refused completion until all four Operational Activities were finished and supervisor-approved.
- Combined-stage assignments, interactions, and follow-ups appeared in Stage 4 **Stage Work** after stage-name normalization.
- The Academy Manager completed Instructor, Logistics, Attendee, and Sponsorship operational lanes, recorded evidence, and closed follow-ups.
- Operational supervisor approval unlocked Finance.
- PMB revenue, cost, and P&L plus Treasury sponsorship, settlements, and payment evidence passed Stage 4 validation.
- Completing Stage 4 activated **Readiness, Delivery & Assessment**.
- Stage 5 correctly refused completion before readiness authorization, then completed after Go, three completed sessions, attendance, delivery evidence, and valid assessment/certificate evidence.
- Stage 6 accepted valid Graduate Outcome counts and evidence.
- Stage 7 accepted the report reference and completed review with no open improvement actions.
- Stage 8 required all prior stages, operational closure, financial closure, and lessons learned, then marked the lifecycle complete.
- Manager completion controls dispatched through the standard completion handlers; validation rules remained enforced.

## Save Draft versus Submit for Greenlight passed

- Submit with missing Demand Evidence remained Active and created no approval
- The workspace displayed the consolidated Greenlight requirements warning
- Save Draft kept Request & Greenlight Active and editable
- Save Draft created one `Program request draft saved` audit event
- Save Draft created no Academy Manager approval
- Valid Submit changed the stage to Pending Approval and locked the fields
- Valid Submit created the Academy Manager approval
- Valid Submit created one `Program request submitted for Greenlight` audit event
- The prior draft audit count remained unchanged after submission
- Duplicate-open-approval protection is present

## Full eight-stage lifecycle retained

1. **Request & Greenlight:** created, drafted, submitted, and approved by Academy Manager.
2. **Curriculum:** all required curriculum fields, four QA checks, QA approval, lock, and release completed.
3. **Instructor Setup:** shortlist, evaluation, selection, R/H, project basis, Part Time, level, groups, source, fee approval, Legal contract, and onboarding completed.
4. **Launch, Commercial, Operations & Finance:** complete launch plan submitted and approved Go; B2C Commercial completed; Instructor, Logistics, Attendee, and Sponsorship activities each completed with an interaction and no open follow-up; supervisor review approved; PMB and Treasury Finance completed.
5. **Readiness, Delivery & Assessment:** all eight readiness checks refreshed and saved; Academy Manager recorded Go; all three timed sessions completed; delivery evidence recorded with no open incidents; assessment results and certificate evidence completed.
6. **Graduate Outcomes:** valid descending outcome counts and evidence completed.
7. **Reporting & Improvement:** report reference and completed course review recorded with no open actions.
8. **Final Closure:** all prerequisite checks passed, operational and financial closure approved, and lessons learned recorded.

## Completion result

- All eight lifecycle stage buttons displayed Completed
- Program Lifecycle Completed banner displayed
- Final closure audit recorded Academy Manager completion
- No browser console errors were recorded during the final lifecycle run

## Revision 8 regression retained

- My Work remains removed in favor of My Tasks
- Launch Planning and Academy Crew Tasks remain limited to five items with See All / Show 5
- Finance and Schedule sidebar workspaces remain present
- Responsive HD and 1280×720 manager dashboard behavior remains available with the new compact top bar
- Academy Manager retains full-stage completion authority
- Save Draft and Submit for Greenlight remain separate workflow actions
- The complete eight-stage lifecycle validation remains preserved
- Instructors remains available directly after Programs with Stage 3 engagement and readiness information
- The 52 px compact top bar remains available, now with blended brand treatment

## Packaging state

- No validation employee, Program, assignments, generated SQLite database, or generated Excel mirror is included
- Original V5 and Review Revisions 1–8 remain unchanged
