# Prototype V5 — Review Revision 7 Notes

Revision 7 corrects Stage 1 and confirms that the complete Academy Training Life Cycle works as one connected workflow.

## Save Draft and Submit for Greenlight

- The two buttons now use a shared field collector but perform separate workflow actions.
- **Save Draft** keeps Stage 1 Active or Returned, leaves fields editable, creates no approval, and records only `Program request draft saved`.
- **Submit for Greenlight** validates the completed request, changes Stage 1 to Pending Approval, locks the fields, closes the submitter's request assignment, creates one Academy Manager approval, and records only `Program request submitted for Greenlight`.
- Required submission data is Program Name, Expected Attendees above zero, Preliminary Budget above zero, Objective, and Demand Evidence.
- All missing requirements appear together in a warning panel.
- Repeated submission logic is protected from creating duplicate open Greenlight approvals.

## Complete lifecycle validation

One clean Academy Manager Program was created and completed through:

1. Request & Greenlight
2. Curriculum
3. Instructor Setup
4. Launch, Commercial, Operations & Finance
5. Readiness, Delivery & Assessment
6. Graduate Outcomes
7. Reporting & Improvement
8. Final Closure

The Program reached **Program Lifecycle Completed** with all eight stages marked Completed. Required evidence, numeric validation, approval gates, four operational lanes, PMB/Treasury Finance separation, readiness decision, session completion, assessment evidence, outcome-count validation, course review, and closure approvals were all exercised.
