# Revision 16.2 — Role Governance Re-evaluation

## Governance principle

Revision 16.2 separates **manager governance** from **team execution**.

- Contributors complete the work owned by their Position.
- The **Academy Manager alone** owns the Manager Dashboard, all-team management, the Academy Manager Control panel, and final lifecycle-stage completion / handoff.
- The Academy Manager retains override authority to fill or perform Position-owned work when necessary so a Program can still be completed end-to-end.

## Manager-only capabilities

Only a user whose active Position set contains **Academy Manager** can access:

- Manager Dashboard.
- Dashboard manager launch / crew controls.
- Team Members directory.
- Team Member Profile and all-team workload views.
- Assignment of tasks directly to another team member / Position from the Team Member Profile.
- Administration workspace.
- Academy Manager Control on every Program lifecycle stage.
- Final **Complete Stage** / handoff action for Stages 1–8.
- Final Program Closure.

Direct navigation attempts to manager-only views are redirected to **My Tasks**.

## Non-manager experience

Non-manager users:

- Land on **My Tasks** instead of the Manager Dashboard.
- Do not see Manager Dashboard navigation on desktop or mobile.
- Do not see Team Member / All Team filters, Team Members cards, or Team Member profiles.
- See only task records assigned to their active Position(s).
- Can complete only workflow assignments owned by one of their active Position(s).
- Can perform the Program-stage fields/actions owned by their Position.
- Can finish a section/deliverable and submit it for manager completion, but cannot advance the lifecycle stage themselves.

## Lifecycle completion model

| Stage | Contributor responsibility | Academy Manager responsibility |
|---|---|---|
| 1. Request & Greenlight | Prepare and submit a valid request | Approve/return Greenlight and close Stage 1 |
| 2. Curriculum | Draft, QA and lock the curriculum package | Finalize Stage 2 and hand off to Instructor Setup |
| 3. Instructor Setup | Complete selection, engagement, contract and onboarding evidence | Finalize Stage 3 and open Stage 4 |
| 4. Launch, Commercial, Operations & Finance | Complete Launch inputs, Commercial routes, Operations lanes, Finance settlement/P&L | Record required manager decisions and finalize Stage 4 handoff |
| 5. Readiness, Delivery & Assessment | Complete readiness inputs, delivery sessions/incidents, assessment/certificate evidence | Record readiness decision and finalize Stage 5 handoff |
| 6. Graduate Outcomes | Complete outcome counts/evidence or provide N/A basis | Finalize Stage 6 / N/A handoff |
| 7. Reporting & Improvement | Complete report, review and improvement actions | Finalize Stage 7 and open Final Closure |
| 8. Final Closure | No contributor can close the Program | Academy Manager alone closes the Program |

## Stage behavior changes

The following contributor actions no longer close the lifecycle stage on their own:

- Curriculum lock.
- Instructor Setup validation.
- Finance section close.
- Assessment & Certification completion.
- Graduate Outcomes completion.
- Reporting & Improvement completion.

They now mark the underlying section/deliverable ready and leave the lifecycle stage active until the Academy Manager completes it through **Academy Manager Control**.

Commercial, Operations, Delivery, Finance, Assessment and similar internal sections remain Position-owned operational work; they are not themselves the final lifecycle-stage approval.

## Prototype security note

This prototype stores one local employee profile and applies role checks in the client application. A production deployment should enforce the same permissions server-side using organizational identity (for example Microsoft Entra ID / SSO) and immutable role claims; UI hiding alone must not be treated as production authorization.
