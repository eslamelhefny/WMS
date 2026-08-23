# Andalusia Academy Work Management System
## Master Application Plan — Draft for Review

**Project status:** Planning / Architecture  
**Primary goal:** Combine the Andalusia Academy Task Planner and the Andalusia Academy Operational App into one position-driven work management system.  
**UI/UX direction:** Keep the existing Andalusia Task Planner UI/UX as the visual foundation. The Operational App contributes workflow rules, stages, responsibilities, operational records, and business logic — not its visual design.

---

# 1. Product Vision

The **Andalusia Academy Work Management System (AAWMS)** will be one application that connects:

- Academy programs
- Position-specific responsibilities
- Work assignments
- Employee tasks
- Daily / weekly / monthly / quarterly planning
- Operational activities
- Follow-ups
- Approvals
- Documents
- Notifications
- Reports
- Audit history

The core idea is:

```text
PROGRAM WORKFLOW
      ↓
POSITION RULE
      ↓
WORK ASSIGNMENT
      ↓
EMPLOYEE TASK
      ↓
MY WORK / TODAY / PLANNER
      ↓
COMPLETION / REVIEW / APPROVAL
      ↓
PROGRAM WORKFLOW UPDATED
```

The employee should not enter the same information twice.

---

# 2. Fundamental Design Principles

## 2.1 Keep Our Existing UI/UX

The new application should continue the visual and interaction language already developed in the Task Planner:

- Andalusia branding
- Fixed desktop sidebar
- Responsive mobile navigation
- Dashboard hero
- Large cards and clear spacing
- Terracotta-led visual identity
- Multiple user-selectable themes
- Profile image
- SVG interface icons
- Today's Tasks
- Mouse-friendly progress controls
- Weekly / monthly / quarterly planners
- Excel and PDF reporting
- Local-first prototype behavior
- Empty first-login experience

The Operational App should **not replace this design**.

Its workflow logic will be integrated into our interface.

## 2.2 Position-Driven Rules

The application must not use a generic:

```text
Employee → Supervisor → Manager
```

permission model.

Every Academy position has its own rules.

Each employee is connected to one or more **Positions**, and each Position determines:

- Which modules are visible
- Which programs are visible
- Which stages can be opened
- Which actions can be performed
- Which fields can be edited
- Which approvals can be made
- Which documents can be uploaded
- Which work assignments are created
- Which notifications are received
- Which reports can be viewed
- Which handovers are required

## 2.3 Separate Workflow State from Personal Task Progress

These must remain different:

```text
Program Stage Status
Activity Status
Work Assignment Status
Employee Task Progress
```

Example:

```text
Program Stage       Operational Activities
Stage Status        In Progress

Activity            Instructor Coordination
Activity Status     Ready for Review

Employee Task       Finalize instructor agenda
Task Progress       75%
```

The employee task must never incorrectly control the whole program stage unless the workflow rule explicitly says so.

## 2.4 Keep the Employee Task Form Simple

The normal employee task form should stay easy to use.

### Visible Task Fields

- Task Title
- Project
- Task Category
- Deliverable Type
- Priority
- Status
- Progress
- Start Date
- Due Date
- Estimated Hours
- Actual Hours
- Recurrence
- Link
- Notes

### Do Not Reintroduce into the normal Create Task form

- Impact
- Blocker Status
- Delivery Status
- Action Status
- Notification Status

Operational complexity should exist inside the workflow modules, not inside the normal personal task form.

---

# 3. Main Application Architecture

```text
ANDALUSIA ACADEMY WORK MANAGEMENT SYSTEM
│
├── Identity & Position Rules
│   ├── Employees
│   ├── Positions
│   └── Position Rule Engine
│
├── Personal Work
│   ├── Home
│   ├── My Work
│   ├── My Tasks
│   ├── Today
│   └── Planner
│       ├── Week
│       ├── Month
│       └── Quarter
│
├── Program Operations
│   ├── Programs
│   ├── Program Workspace
│   ├── Operational Activities
│   ├── Visits
│   ├── Follow-Ups
│   ├── Approvals
│   ├── Exceptions
│   └── Documents
│
├── Communication
│   ├── Notifications
│   └── Activity Feed
│
├── Reporting
│   ├── Personal Reports
│   ├── Program Reports
│   └── Management Reports
│
├── Administration
│   ├── Employees
│   ├── Positions
│   ├── Position Rules
│   ├── Workflow Rules
│   ├── Master Data
│   └── System Settings
│
└── Profile
    ├── Employee Information
    ├── Profile Image
    ├── Theme
    ├── Default View
    └── Test / Sample Data
```

---

# 4. Source Operational Model to Preserve

The Operational App currently defines the following Academy positions.

## 4.1 Positions

1. Academy Manager
2. Academy Operations Supervisor
3. Program Operations Executive
4. MBA/DBA Program Executive
5. Academy Curriculum Development Manager
6. Curriculum Developer
7. Academy BD & Partnerships Head
8. Business Developer
9. Operations Specialist — Instructor Coordination
10. Operations Specialist — Logistics
11. Operations Specialist — Registration
12. Operations Specialist — Partnerships Support
13. Program Coordinator
14. Finance — PMB
15. Finance — Treasury
16. Legal
17. Marketing Account Manager
18. Studio Account Manager
19. Recruitment Head
20. Instructor / SME

These should become formal Position records in the new system.

---

# 5. Program Lifecycle

The Academy program lifecycle should preserve the 13 operational stages currently modeled:

1. Request & Greenlight
2. Curriculum
3. Instructor Setup
4. Launch Planning
5. Commercial
6. Operational Activities
7. Readiness
8. Delivery
9. Assessment & Certification
10. Finance
11. Graduate Outcomes
12. Reporting & Improvement
13. Final Closure

Each stage will have:

- Stage owner positions
- View rules
- Edit rules
- Required information
- Required documents
- Completion conditions
- Approval conditions
- Generated work assignments
- Notifications
- Audit events
- Handover rules

---

# 6. Position Rule Engine

Every Position requires a structured rule profile.

## 6.1 Position Rule Structure

```text
Position
│
├── Module Access
├── Program Visibility
├── Stage Access
├── Action Permissions
├── Field Permissions
├── Approval Permissions
├── Document Permissions
├── Work Assignment Rules
├── Notification Rules
├── Report Access
└── Handover Rules
```

The system should support rules at several levels:

- **Module-level:** can the position open the module?
- **Program-level:** which programs are visible?
- **Stage-level:** which stages are visible/editable?
- **Action-level:** create, edit, submit, review, approve, return, close, reopen.
- **Field-level:** which individual fields are editable?
- **Record-level:** which activity, document, visit, follow-up, or approval records are allowed?
- **Report-level:** which personal, program, financial, and management reports are visible?

---

# 7. Draft Position Rules Matrix

This is the starting rule model and must be reviewed with Academy stakeholders before final implementation.

## 7.1 Academy Manager

### Primary Responsibility
Governance, major decisions, readiness authorization, and final closure.

### Primary Modules
- Executive Dashboard
- My Work
- Programs
- Approvals
- Readiness
- Operations
- Reports
- Profile

### Core Actions
- Review program request
- Approve / return Greenlight
- Approve instructor fee where required
- Review Academy readiness
- Record Go
- Record Conditional Go
- Record No-Go
- Approve final program closure
- Review Academy-level exceptions
- Review management reports

### Generated Work
Examples:
- Approve program Greenlight
- Review readiness decision
- Approve instructor commercial terms
- Review final closure

## 7.2 Academy Operations Supervisor

### Primary Responsibility
Operational coordination, assignment, monitoring, review, and readiness preparation.

### Primary Modules
- Home
- My Work
- Programs
- Operations
- Readiness
- Planner
- Reports
- Profile

### Core Actions
- Assign operational activity owners
- Set Program Coordinator
- Monitor the four operational activities
- Review operational activity completion
- Return incomplete operational work
- Approve operational review
- Maintain readiness checklist items allowed by position
- Monitor operational exceptions
- Participate in launch planning
- Participate in reporting and improvement

### Generated Work
Examples:
- Assign operational owners
- Review completed logistics activity
- Review operational activity package
- Prepare readiness for manager decision
- Complete program review

## 7.3 Program Operations Executive

### Primary Responsibility
Program creation, program coordination, setup, and operational preparation.

### Core Actions
- Create program request
- Edit request
- Submit request for Greenlight
- Participate in instructor setup
- Participate in launch planning
- Manage applicable program data
- Coordinate applicable commercial and operational preparation

### Generated Work
Examples:
- Complete new program request
- Prepare instructor shortlist
- Confirm launch schedule
- Complete program setup information

## 7.4 MBA/DBA Program Executive

### Primary Responsibility
MBA/DBA program operations and applicable learner/commercial coordination.

### Core Actions
- Create / edit applicable program requests
- Manage applicable B2C operational records
- Monitor assigned program tasks
- Maintain MBA/DBA program operational information

### Notes
Detailed MBA/DBA-specific rules require stakeholder confirmation.

## 7.5 Academy Curriculum Development Manager

### Primary Responsibility
Curriculum development, academic QA, curriculum lock, assessment, and certification.

### Primary Modules
- Home
- My Work
- Planner
- Programs
- Curriculum
- Assessment & Certification
- Reports
- Profile

### Core Actions
- Define learning outcomes
- Define program structure
- Define assessment blueprint
- Upload curriculum package
- Perform curriculum QA
- Lock approved curriculum version
- Participate in instructor selection
- Record assessment completion
- Record approved results
- Record certificate issuance

### Generated Work
Examples:
- Build curriculum draft
- Complete curriculum QA
- Lock curriculum
- Validate assessment results
- Complete certificate record

## 7.5A Curriculum Developer

### Primary Responsibility
Prepare and maintain the curriculum draft under the Academy Curriculum Development Manager's academic governance.

### Core Actions
- Complete curriculum Outline
- Record Topic and Competences
- Define Duration
- Maintain learning outcomes, program structure, assessment blueprint, and curriculum pack reference
- Submit the completed curriculum draft for academic QA

### Governance
The Curriculum Developer can edit and save the Stage 2 draft. Academic QA approval and Lock & Release remain restricted to the Academy Curriculum Development Manager.

## 7.6 Academy BD & Partnerships Head

### Primary Responsibility
B2B opportunities, partnerships, commercial development, and sponsorship oversight.

### Core Actions
- Participate in eligible program requests
- Manage B2B account
- Manage opportunity stage
- Upload proposal
- Record contract information
- Manage commercial value
- Oversee partnership-related work

### Generated Work
Examples:
- Prepare B2B proposal
- Follow up institutional account
- Complete commercial record
- Review partnership opportunity

## 7.7 Business Developer

### Primary Responsibility
Execution of B2B commercial opportunities.

### Core Actions
- Maintain assigned B2B opportunities
- Update opportunity stage
- Prepare or upload proposal
- Record commercial follow-ups
- Support contract progression

## 7.8 Operations Specialist — Instructor Coordination

### Primary Responsibility
Instructor operational readiness.

### Primary Operational Lane
**Instructors**

### Core Actions
- Manage instructor coordination activity
- Record instructor type
- Record agreed fee where permitted
- Record instructor visits / interactions
- Record objectives and outcomes
- Record follow-up dates
- Upload evidence
- Upload final agenda
- Complete instructor operational activity

### Generated Work
Examples:
- Confirm instructor availability
- Follow up instructor
- Upload final agenda
- Complete instructor activity

## 7.9 Operations Specialist — Logistics

### Primary Responsibility
Venue, materials, logistics readiness, and operational evidence.

### Primary Operational Lane
**Logistics & Place**

### Core Actions
- Select venue
- Select required materials
- Record logistics budget
- Record visits / coordination
- Upload evidence
- Complete logistics activity

### Generated Work
Examples:
- Confirm venue
- Prepare materials
- Complete venue inspection
- Close logistics activity

## 7.10 Operations Specialist — Registration

### Primary Responsibility
Attendee registration and participation readiness.

### Primary Operational Lane
**Attendees**

### Core Actions
- Select B2B / B2C attendee classification
- Select attendee subtype
- Record course fee
- Record payment method
- Record expected count
- Upload attendee list
- Record communication / visits
- Complete attendee activity

### Generated Work
Examples:
- Update attendee list
- Confirm expected count
- Follow up registration
- Close attendee activity

## 7.11 Operations Specialist — Partnerships Support

### Primary Responsibility
Operational sponsorship coordination.

### Primary Operational Lane
**Sponsorships**

### Core Actions
- Select sponsor
- Record sponsorship amount
- Record meetings / visits
- Record outcomes
- Record follow-ups
- Upload evidence
- Complete sponsorship activity

## 7.12 Program Coordinator

### Primary Responsibility
Program execution and delivery coordination.

### Core Actions
- Work on readiness checklist where allowed
- Manage delivery
- Update session status
- Record actual attendance
- Record instructor arrival
- Upload execution evidence
- Record execution comments
- Record incidents
- Coordinate assigned program tasks

### Generated Work
Examples:
- Prepare delivery schedule
- Confirm session readiness
- Record attendance
- Close delivery evidence
- Resolve execution incident

## 7.13 Finance — PMB

### Primary Responsibility
Financial program results and P&L.

### Core Actions
- Record actual revenue
- Record actual cost
- Review program financial performance
- Participate in launch financial planning where required
- Close final P&L

### Generated Work
Examples:
- Review final program cost
- Record actual revenue
- Complete P&L
- Close financial record

## 7.14 Finance — Treasury

### Primary Responsibility
Payments, settlements, and collected funds.

### Core Actions
- Record sponsorship collected
- Record instructor payment completion
- Record vendor payment completion
- Upload payment evidence where required

### Generated Work
Examples:
- Settle instructor payment
- Confirm vendor payment
- Confirm sponsorship collection

## 7.15 Legal

### Primary Responsibility
Legal documents and contractual completion.

### Core Actions
- Review instructor contract
- Record contract signed status where allowed
- Review assigned legal documents
- Complete legal work assignments

### Generated Work
Examples:
- Finalize instructor agreement
- Confirm signed contract
- Review legal document

## 7.16 Marketing Account Manager

### Primary Responsibility
Marketing launch readiness.

### Core Actions
- Participate in launch planning
- Upload / maintain marketing brief
- Update assigned marketing deliverables
- Complete marketing work assignments

### Generated Work
Examples:
- Prepare marketing brief
- Confirm campaign readiness
- Complete launch asset

## 7.17 Studio Account Manager

### Primary Responsibility
Studio production and creative operational readiness.

### Core Actions
- Receive studio request
- Update studio production status
- Manage assigned production work
- Confirm studio output readiness

### Generated Work
Examples:
- Produce program assets
- Update studio status
- Confirm production completion

## 7.18 Recruitment Head

### Primary Responsibility
Graduate outcomes and post-program recruitment handoff.

### Core Actions
- Mark graduate outcome applicability
- Record eligible graduates
- Record consent
- Record job-ready count
- Record placement pool
- Record shortlisted count
- Record placed count
- Upload outcome evidence
- Complete graduate outcome stage

### Generated Work
Examples:
- Review eligible graduates
- Complete placement handoff
- Update recruitment outcome
- Close graduate outcomes

## 7.19 Instructor / SME

### Primary Responsibility
Academic / subject-matter contribution.

### Initial Proposed Access
- View assigned programs
- View assigned tasks
- View relevant curriculum
- View relevant delivery schedule
- Upload requested instructor evidence
- Complete assigned actions

### Important
The source prototype does not define enough detailed Instructor / SME permissions to finalize this rule set. These rules require Academy review.

---

# 8. Position Rule Configuration

The system should include an administrative **Position Rules** screen.

For each Position:

```text
POSITION: Academy Operations Supervisor

Modules
☑ Programs
☑ Operations
☑ Readiness
☑ Reports

Stages
☑ Launch Planning
☑ Operational Activities
☑ Readiness
☑ Reporting & Improvement

Actions
☑ Assign
☑ Edit
☑ Review
☑ Return
☑ Approve Operational Review

Fields
☑ Coordinator
☑ Activity Owner
☑ Review Status

Approvals
☐ Greenlight
☐ Final Closure
```

Critical governance rules should require administrator rights and audit logging.

---

# 9. Employee Model

Each employee record should include:

- Employee ID
- Full Name
- Academy Email
- Department
- Job Title
- Primary Position
- Additional Positions
- Profile Image
- Phone
- Active / Inactive
- Default View
- Selected Theme
- Created Date
- Last Login

Academy email format:

```text
username@andalusia.net
```

---

# 10. Multiple Positions per Employee

The architecture should support one employee holding more than one Position.

Example:

```text
Employee: Ahmed Ali

Primary Position:
Program Operations Executive

Additional Position:
Program Coordinator
```

When work is assigned, the system records which Position the employee is acting under.

Example:

```text
Task
Prepare delivery schedule

Assigned Employee
Ahmed Ali

Position Context
Program Coordinator
```

---

# 11. Login and First-Time Experience

## First Login Must Be Empty

A new installation / new workspace should contain:

- No employee data
- No tasks
- No programs
- No sample data
- Empty dashboard
- No default department
- No fake KPIs

The application should show:

```text
Your workspace is ready.

No tasks or programs have been added yet.
```

### Primary Actions

- Add First Task
- Create Program
- Open Profile

For a real multi-user deployment, employees should not be allowed to assign themselves unrestricted Positions. Positions are assigned by an authorized administrator. A prototype-only Position switcher may exist in Training/Test Mode.

---

# 12. Profile

Profile will preserve the current Task Planner UX.

## Fields

- Profile Image
- Full Name
- Employee ID
- Academy Email
- Department
- Job Title
- Phone
- Primary Position
- Additional Position(s)
- Default View
- Theme

## Profile Image

- Upload PNG
- Upload JPG
- Upload WebP
- Preview
- Remove
- Resize locally before save

## Test / Development Tools

- Add Sample Tasks
- Add Test Tasks
- Add Sample Program
- Add Full Workflow Test Program
- Clear All Local Data

These tools should be clearly marked as testing features in the prototype.

---

# 13. Theme System

Keep the existing theme engine.

Themes:

1. Terracotta
2. Ocean
3. Forest
4. Plum
5. Midnight
6. Sandstone
7. Rose

Theme selection should remain available from:

- Top bar
- Registration
- Profile

Do not place a second theme control in the sidebar.

Themes must update:

- Sidebar gradient
- Dashboard hero
- Page background
- Cards
- Forms
- Buttons
- Borders
- Navigation states
- Progress controls
- Planner
- Reports preview
- Modal surfaces
- Browser theme color

---

# 14. Branding

## Sidebar

- Fixed while page scrolls
- Andalusia full logo centered
- Low-opacity white emblem watermark
- No sidebar theme selector

## Browser Tab

- Andalusia emblem only
- No text inside favicon image

## Dashboard Hero

- Position-aware greeting
- Low-opacity white emblem watermark
- No decorative circle

---

# 15. Main Navigation Strategy

The application uses the same overall shell, but navigation changes based on Position.

## Common Modules

Most positions can access:

- Home
- My Work
- My Tasks
- Today
- Planner
- Programs
- Reports
- Profile

## Position Modules

Examples:

### Academy Manager
- Executive Dashboard
- My Work
- Programs
- Approvals
- Readiness
- Operations
- Reports
- Profile

### Operations Specialist — Logistics
- Home
- My Work
- My Tasks
- Planner
- Programs
- Logistics
- Reports
- Profile

### Curriculum Development Manager
- Home
- My Work
- Planner
- Programs
- Curriculum
- Assessment
- Reports
- Profile

### Finance — PMB
- Home
- My Work
- Planner
- Programs
- Finance
- Reports
- Profile

Navigation visibility is controlled by the Position Rule Engine.

---

# 16. Home Dashboard

The dashboard should combine personal execution with relevant operational visibility.

## Common Personal KPIs

- Today's Tasks
- Total Open Tasks
- Completed
- In Progress
- Overdue
- Actual Hours
- Completion Rate

## Position-Specific Operational KPIs

The second dashboard area changes based on Position.

### Academy Manager
- Active Programs
- Pending Approvals
- Pending Readiness Decisions
- Programs at Risk
- Operational Exceptions
- Upcoming Programs

### Academy Operations Supervisor
- Active Operational Activities
- Activities Awaiting Review
- Open Follow-Ups
- Unassigned Activities
- Programs Near Delivery
- Operational Exceptions

### Instructor Coordination
- Active Instructor Tasks
- Upcoming Instructor Follow-Ups
- Missing Agendas
- Instructors Awaiting Confirmation

### Finance
- Open Financial Records
- Pending Settlements
- Programs Awaiting P&L Closure

The dashboard should never show operational cards that the Position cannot access.

---

# 17. My Work

**My Work** is the bridge between operational workflow and the personal planner.

It contains work generated by:

- Program stages
- Activity ownership
- Follow-ups
- Approvals
- Exceptions
- Reviews
- Handovers

## My Work Sections

- Needs Action
- Due Today
- High Priority
- Overdue
- Awaiting Review
- Waiting on Someone Else
- Recently Completed

## Work Card

```text
HIGH

Complete Instructor Contract

Clinical Leadership Certificate
Instructor Setup

Assigned as:
Legal

Due:
18 Aug

[Open Task] [Open Program]
```

---

# 18. My Tasks

My Tasks contains both:

## Manual Tasks

Created directly by the employee.

## Workflow Tasks

Created by Program / Activity / Follow-Up / Exception / Approval logic.

Workflow tasks should show:

- Source Program
- Stage
- Activity
- Position Context
- Assignment ID

These workflow metadata fields should not clutter the normal Create Task form.

---

# 19. Task Types

The system should support:

1. Manual Task
2. Program Task
3. Activity Task
4. Follow-Up Task
5. Exception Task
6. Approval Task
7. Review Task

All task types use the same personal execution engine.

---

# 20. Task Status and Progress

Recommended personal task statuses:

- Not Started
- In Progress
- Completed
- On Hold
- Cancelled

Progress:

- 0–100%
- Mouse-friendly slider
- Quick presets:
  - 0%
  - 25%
  - 50%
  - 75%
  - 100%

Rules:

- 100% → Completed
- Reducing a Completed task below 100% reopens it
- Completion can optionally trigger workflow completion checks

---

# 21. Today

Today's Tasks should show:

- Active today
- Due today
- Overdue
- High priority
- Workflow source
- Quick progress
- Complete action
- Open Program action

Features:

- Dedicated Today's Tasks dashboard button
- Daily task modal/panel
- Print Daily Report
- Add Task for Today

---

# 22. Planner

One Planner module with tabs:

- Week
- Month
- Quarter

## Weekly Planner

Sunday–Thursday.

Features:

- Previous
- Current Week
- Next
- Day columns
- Project filter
- Status filter
- Priority filter
- Workflow source label

## Monthly Planner

Features:

- Previous
- Current Month
- Next
- Clickable days
- Task counts
- Today highlight

## Quarterly Planner

Features:

- Previous Quarter
- Current Quarter
- Next Quarter
- Three month cards
- Completion summary
- Hours
- Program workload

---

# 23. Programs

Programs are the primary Academy operational records.

## Programs Page

Views:

- Pipeline
- Cards
- Table
- Search
- Filters

Filters:

- Status
- Program Type
- Route
- Region
- Stage
- Owner
- Start Date
- Position involvement

Program card:

```text
Clinical Leadership Certificate

Certificate Program
Mixed
Egypt

Current Stage:
Operational Activities

Overall Readiness:
64%

Start:
14 Sep

[Open Program]
```

---

# 24. Program Workspace

Each Program has one workspace.

## Program Header

- Program Name
- Program ID
- Type
- Route
- Region
- Owner
- Start / End
- Status
- Overall Readiness
- Current Stage

## Stage Flow

Display all 13 stages horizontally / responsively.

Each stage shows:

- Stage number
- Stage name
- Status
- Completion %
- Active indicator

Clicking a stage opens its work area.

---

# 25. Stage Data Model

Each program stage contains:

- Stage Status
- Stage Owner Position(s)
- Stage Progress
- Required Fields
- Required Documents
- Required Checks
- Work Assignments
- Approvals
- Exceptions
- Comments
- Audit History
- Completion Date

---

# 26. Request & Greenlight

## Data

- Program Name
- Program Type
- Route
- Specialty
- Region
- Start Date
- End Date
- Expected Attendees
- Preliminary Budget
- Objective
- Target Audience
- Demand Evidence
- Delivery Mode
- Priority

## Workflow

```text
Program Operations
      ↓ Submit
Academy Manager
      ↓
Approve / Return
```

---

# 27. Curriculum

## Data

- Curriculum Status
- Owner
- Learning Outcomes
- Program Structure
- Assessment Blueprint
- Curriculum File
- QA Checks
- Version
- Lock Status

## Workflow

```text
Approved Greenlight
      ↓
Curriculum Development
      ↓
QA
      ↓
Lock Final Version
```

---

# 28. Instructor Setup

## Data

- Shortlist
- Evaluation
- Selected Instructor
- Fee Approval
- Contract Signed
- Onboarding Complete
- Comment

## Position Collaboration

- Program Operations
- Curriculum
- Academy Manager
- Legal
- Operations Supervisor

---

# 29. Launch Planning

## Data

- Price
- Capacity
- Budget
- Expected Revenue
- Contribution / Margin
- Schedule Confirmed
- Marketing Brief
- Studio Request
- Studio Status
- Comment

## Position Collaboration

- Program Operations
- Operations Supervisor
- Marketing
- Studio
- Finance PMB

---

# 30. Commercial

Two independent routes depending on program type.

## B2C

- Course Fee
- Payment Method
- Leads
- Registered
- Paid
- Waitlist

## B2B

- Account
- Opportunity Stage
- Proposal
- Contract
- Contract Value
- Participants

Applicable route rules depend on:

- B2C
- B2B
- Mixed

---

# 31. Operational Activities

Four operational lanes remain parallel.

## 31.1 Instructors
Owner: Operations Specialist — Instructor Coordination

## 31.2 Logistics & Place
Owner: Operations Specialist — Logistics

## 31.3 Attendees
Owner: Operations Specialist — Registration

## 31.4 Sponsorships
Owner: Operations Specialist — Partnerships Support

These activities must not lock each other.

---

# 32. Operational Activity Record

Each activity contains:

- Owner Position
- Assigned Employee
- Status
- Progress
- Saved / Draft State
- Completion State
- Activity-Specific Fields
- Visits
- Follow-Ups
- Documents
- Comments
- Review Status

---

# 33. Visits / Interaction Records

A visit / interaction should contain:

- Activity
- Target
- Date
- Type
- Objective
- Outcome
- Follow-Up Date
- Evidence
- Created By
- Created Date

Visit types initially include:

- Physical Location
- Online Meeting
- Phone Call

---

# 34. Follow-Up Engine

When a Follow-Up Date is entered:

```text
Visit
  ↓
Follow-Up Rule
  ↓
Work Assignment
  ↓
Employee Task
```

Example:

```text
Follow up with Dr. Mona Adel
Due 18 Aug
Source: Instructor Activity
```

When the task is completed, the follow-up record can be marked completed.

---

# 35. Readiness

Readiness is a controlled workflow, not a normal task field.

## Readiness Checklist

Examples from the current workflow:

- Agenda
- Instructor Contract
- Venue
- Materials
- Attendee Communication
- Sponsor Confirmation
- Finance Clearance
- AV Test

## Decision

Allowed values:

- Pending
- Go
- Conditional Go
- No-Go

The Academy Manager owns the final delivery decision.

---

# 36. Delivery

## Data

- Delivery Status
- Actual Attendees
- Instructor Arrived
- Sessions
- Execution Evidence
- Comments
- Incidents

## Session Status

- Not Started
- In Progress
- Completed
- Delayed
- Cancelled

---

# 37. Incidents

Delivery incidents should contain:

- Category
- Severity
- Description
- Owner
- Action Required
- Resolution
- Status
- Evidence
- Created Date
- Closed Date

Severity:

- Low
- Medium
- High
- Critical

Incidents may create tasks automatically.

---

# 38. Assessment & Certification

## Data

- Assessment Completed
- Pass Count
- Feedback Score
- Approved Result File
- Certificates Issued
- Certificate Evidence
- Comments

Validation:

- Certificates Issued must not exceed Pass Count

---

# 39. Finance

## Financial Results

- Actual Revenue
- Actual Cost
- Sponsorship Collected
- Profit / Loss

## Settlement

- Instructor Paid
- Vendor Paid
- Payment Evidence

## Closure

- Final P&L Closed

Finance permissions must remain separated between PMB and Treasury.

---

# 40. Graduate Outcomes

## Data

- Applicable / Not Applicable
- Eligible
- Consented
- Job Ready
- Placement Pool
- Shortlisted
- Placed
- Evidence
- Comment

Validation rules must prevent inconsistent counts.

---

# 41. Reporting & Improvement

## Course Review

- Performance Report
- Review Completed
- Review Comment

## Improvement Actions

- Action
- Owner
- Due Date
- Status
- Evidence

Improvement actions should create personal tasks for the assigned Position / employee.

---

# 42. Final Closure

## Preconditions

- Finance Closed
- Graduate Outcomes Complete / N/A
- Course Review Complete
- Required workflow stages completed

## Closure

- Operational Closure Approved
- Financial Closure Approved
- Lessons Learned
- Closed By
- Closed Date

---

# 43. Work Assignment Engine

A Work Assignment is the bridge between operational workflow and personal tasks.

## Data

- Assignment ID
- Program
- Stage
- Activity
- Action
- Owner Position
- Assigned Employee
- Priority
- Start Date
- Due Date
- Status
- Required Evidence
- Completion Checks
- Can Delegate
- Review Position
- Approval Position
- Generated Task ID

---

# 44. Work Assignment Lifecycle

```text
Rule Triggered
    ↓
Assignment Created
    ↓
Employee Assigned
    ↓
Task Created
    ↓
Employee Works
    ↓
Completion Requested
    ↓
System Validation
    ↓
Review / Approval if required
    ↓
Assignment Closed
    ↓
Workflow Updated
```

---

# 45. Handovers

Every workflow action should support a defined next responsible Position.

Example:

```text
Program Operations Executive
      ↓
Submit Greenlight

Academy Manager
      ↓
Approve

Curriculum Development Manager
      ↓
Build Curriculum

Program Operations / Curriculum
      ↓
Instructor Setup
```

Handovers should create notifications and Work Assignments automatically.

---

# 46. Approvals

Approval record:

- Approval ID
- Program
- Stage
- Action
- Requested By
- Requested Position
- Approver Position
- Approver Employee
- Decision
- Comment
- Date
- Evidence
- Audit Entry

Possible decisions vary by workflow.

Examples:

- Approve
- Return
- Reject
- Go
- Conditional Go
- No-Go

---

# 47. Exceptions

The system should detect operational conditions requiring attention.

Examples:

- No owner assigned
- Overdue follow-up
- Required document missing
- Activity completed without required interaction
- Program date approaching while readiness incomplete
- Missing delivery evidence
- Invalid certificate count
- Financial closure incomplete
- Improvement action overdue

Exceptions can:

- Show alert
- Notify Position
- Generate Work Assignment
- Generate Task
- Require review

---

# 48. Notifications

Do not add Notification Status back into Create Task.

Notifications should be system events.

## Notification Types

- Task assigned
- Task due tomorrow
- Task overdue
- Follow-up due
- Program assigned
- Stage handover
- Approval requested
- Approval completed
- Work returned
- Exception created
- Comment added
- Document uploaded
- Program stage changed

## Notification Center

Top bar bell icon:

```text
Notifications  4

Approval requested
Clinical Leadership Certificate

Task due today
Finalize instructor agenda

Follow-up overdue
Dr. Mona Adel
```

---

# 49. Documents

Documents should be proper system records.

## Document Record

- Document ID
- Program
- Stage
- Activity
- Task
- Type
- File Name
- Version
- Uploaded By
- Uploaded Date
- Status

## Common Document Types

- Curriculum
- Instructor Contract
- Agenda
- Marketing Brief
- Proposal
- Signed Contract
- Attendance List
- Delivery Evidence
- Results
- Certificates
- Payment Evidence
- Performance Report
- Recruitment Evidence

---

# 50. Global Search

Search across:

- Programs
- Tasks
- Work Assignments
- Employees
- Instructors
- Documents
- Activities
- Follow-Ups

Example:

```text
Search: Clinical

PROGRAM
Clinical Leadership Certificate

TASK
Finalize Clinical Leadership Agenda

DOCUMENT
Clinical Leadership Curriculum v3
```

---

# 51. Reports

Three report layers.

## 51.1 Personal Reports

- Weekly
- Monthly
- Quarterly
- Task Completion
- Hours
- Overdue Tasks
- Project Workload

## 51.2 Program Reports

- Program Overview
- Stage Progress
- Operational Activities
- Follow-Ups
- Readiness
- Delivery
- Assessment
- Finance
- Graduate Outcomes
- Improvement
- Audit History

## 51.3 Management Reports

Position-controlled access.

Examples:

- Active Programs
- Program Pipeline
- Programs at Risk
- Team Workload
- Operational Exceptions
- Pending Approvals
- Upcoming Deliveries
- Activity Completion
- Financial Status
- Graduate Outcomes
- Program Closure

---

# 52. Excel Export

The combined application should preserve the improved, user-friendly export philosophy.

## Personal Export

Visible sheets:

- Overview
- Employee Profile
- Tasks
- Weekly Report
- Monthly Report
- Quarterly Report

No visible Lists sheet.

## Program Export

Potential sheets:

- Program Overview
- Stage Status
- Assigned Work
- Operational Activities
- Follow-Ups
- Documents
- Readiness
- Delivery
- Assessment
- Finance
- Outcomes
- Improvement
- Audit

Exports should only include information the current Position is allowed to view.

---

# 53. PDF Export

PDF reports:

- Today Report
- Weekly Personal Report
- Monthly Personal Report
- Quarterly Personal Report
- Program Status Report
- Operations Report
- Readiness Report
- Management Summary

---

# 54. History and Audit

Every important action should create an audit record.

Audit record:

- Date / Time
- Employee
- Position
- Module
- Program
- Stage
- Record
- Action
- Previous Value
- New Value
- Comment

Examples:

```text
14 Aug 10:32
Ahmed Ali
Program Coordinator
Updated task progress
40% → 75%

14 Aug 11:10
Legal
Uploaded instructor contract

14 Aug 13:25
Academy Manager
Approved Greenlight
```

---

# 55. Setup & Configuration

Administrative modules:

## Employees
Manage employee accounts.

## Positions
Manage Academy positions.

## Position Rules
Manage allowed modules, actions, fields, approvals, and reports.

## Workflow Rules
Manage stage requirements, handovers, and assignment generation.

## Program Types
- Certificate Program
- Workshop
- Corporate Program
- Webinar

## Specialties
Initial values from the current prototype can be migrated and later maintained as master data.

## Regions
Initial:
- Egypt
- KSA

## Instructors
Reference instructor records.

## Venues
Reference venue records.

## Materials
Reference material records.

## Sponsors
Reference sponsor records.

## Attendee Types
B2B / B2C subtypes.

## Payment Methods
Initial:
- Online Payment
- Bank Transfer
- Corporate Invoice
- Cash

## Visit Types
Initial:
- Physical Location
- Online Meeting
- Phone Call

---

# 56. Dashboard Empty-State Rules

When there is no data:

## No Tasks

Do not show fake performance.

Show:

```text
No tasks yet.
Create your first task or open Profile to add test data.
```

## No Programs

Show:

```text
No programs yet.
Create the first Academy program when ready.
```

KPIs should show `0`, not sample values.

---

# 57. Sample and Test Data

Testing should always be explicit.

## Profile Actions

- Add Sample Tasks
- Add Test Tasks
- Add Sample Program
- Add Full Workflow Test Program

These should add records without silently replacing real work.

## Clear All Local Data

Returns the system to:

```text
User: None
Tasks: 0
Programs: 0
Assignments: 0
```

---

# 58. Local Prototype Technical Architecture

For the combined system, move beyond a single JSON file.

## Recommended Local Architecture

```text
Browser UI
    ↓
Local Python Server
    ↓
SQLite Database
    │
    ├── Profile Images
    ├── Documents
    ├── Excel Exports
    └── Backups
```

SQLite should become the main local database.

JSON can remain as:

- Backup format
- Import / export format
- Debug format

---

# 59. Proposed Local Database Tables

## Identity

- employees
- positions
- employee_positions

## Rules

- position_module_rules
- position_stage_rules
- position_action_rules
- position_field_rules
- position_report_rules
- workflow_rules
- workflow_requirements
- workflow_handovers

## Program Operations

- programs
- program_stages
- activities
- visits
- followups
- incidents
- approvals
- exceptions
- documents

## Work

- work_assignments
- tasks
- task_history

## Communication

- notifications

## Governance

- audit_log

## Configuration

- instructors
- venues
- materials
- sponsors
- attendee_types
- payment_methods
- visit_types
- program_types
- specialties
- regions

---

# 60. Key Relationships

```text
Employee
   │
   ├── Employee Position
   │       └── Position
   │             └── Position Rules
   │
   └── Task

Program
   │
   ├── Program Stage
   │      ├── Work Assignment
   │      │       └── Task
   │      ├── Approval
   │      └── Document
   │
   ├── Activity
   │      ├── Visit
   │      │     └── Follow-Up
   │      │             └── Work Assignment
   │      └── Document
   │
   ├── Exception
   │      └── Work Assignment
   │
   └── Audit Log
```

---

# 61. API Structure for Local Prototype

Recommended endpoints:

## Identity

```text
GET    /api/profile
POST   /api/profile
GET    /api/positions
```

## Tasks

```text
GET    /api/tasks
POST   /api/tasks
PUT    /api/tasks/:id
DELETE /api/tasks/:id
```

## Programs

```text
GET    /api/programs
POST   /api/programs
GET    /api/programs/:id
PUT    /api/programs/:id
```

## Stages

```text
GET    /api/programs/:id/stages
PUT    /api/programs/:id/stages/:stage
```

## Assignments

```text
GET    /api/my-work
POST   /api/assignments
PUT    /api/assignments/:id
```

## Activities

```text
GET    /api/programs/:id/activities
PUT    /api/activities/:id
```

## Visits / Follow-Ups

```text
POST   /api/activities/:id/visits
PUT    /api/visits/:id
GET    /api/followups
```

## Approvals

```text
GET    /api/approvals
POST   /api/approvals/:id/decision
```

## Documents

```text
POST   /api/documents
GET    /api/documents/:id
```

## Reports

```text
GET    /api/reports/personal
GET    /api/reports/program/:id
GET    /api/reports/management
```

---

# 62. Permission Enforcement

Permissions must be checked in two places.

## UI

Hide actions the employee cannot perform.

## Server

Always validate Position permissions again before changing data.

The UI alone must never be considered security.

---

# 63. Production Architecture

After the combined workflow is approved:

```text
Frontend
Next.js / TypeScript / PWA

Database
PostgreSQL

Backend
Supabase

Authentication
Academy Employee Accounts

File Storage
Supabase Storage

Permissions
Database + Row Level Security

Reports
Excel + PDF

Hosting
Vercel + Supabase
```

Production migration should happen only after workflow and Position Rules are approved.

---

# 64. Mobile Strategy

The application must remain usable on mobile.

## Mobile Bottom Navigation

Position-aware subset such as:

- Home
- My Work
- Tasks
- Planner
- More

Program details and operational modules can be available under **More**.

## Mobile Priority

Optimize first for:

- Today
- My Work
- Progress updates
- Follow-ups
- Approvals
- Task completion
- Quick comments

Complex setup/configuration remains desktop-first.

---

# 65. Notifications and Reminder Strategy

Prototype:

- In-app notifications
- Due / overdue indicators

Production later:

- In-app
- Email
- Optional push notifications

Notification rules should be configurable by Position and event.

---

# 66. Search, Filter, and Sorting Standards

Every major list should support:

- Search
- Status filter
- Priority filter where relevant
- Position filter where permitted
- Program filter
- Stage filter
- Date range
- Sort by due date
- Sort by priority
- Sort by progress
- Clear filters

Filters should remember the user's selection during the session.

---

# 67. UX Standards

## All Pages

- Clear page title
- One-line description
- Primary action on the right
- No overcrowded toolbars
- Consistent cards
- Consistent status chips
- Consistent empty states
- Consistent error messages
- Responsive forms
- Keyboard accessible controls
- SVG interface icons

## Forms

Group fields into:

- Details
- Schedule
- Responsibility
- Evidence
- Notes

Do not show irrelevant fields to Positions that cannot edit them.

---

# 68. Status Color System

Use consistent semantic meaning across all themes.

- Green → Completed / Approved / Ready
- Blue → In Progress / Active
- Amber → Pending / Warning / Conditional
- Red → Overdue / Exception / Rejected / Critical
- Gray → Not Started / Cancelled / N/A

Theme colors change the brand surfaces, not semantic meaning.

---

# 69. Audit and Data Integrity Rules

Important controls:

- No silent deletion
- Critical delete requires confirmation
- Approval decisions recorded permanently
- Position used for action recorded
- Program stage changes audited
- Workflow-generated tasks retain source reference
- Completed workflow assignments remain in history
- Attachments retain uploader and date
- Financial and closure records require audit events

---

# 70. Migration from the Existing Task Planner

Reuse:

- UI shell
- Sidebar
- Brand treatment
- Theme engine
- Profile
- Profile image
- Academy email behavior
- My Tasks
- Today
- Weekly Planner
- Monthly Planner
- Quarterly Planner
- Progress slider
- Reports
- Excel exports
- Local backup tools

Upgrade:

- JSON → SQLite
- Single profile → Employee / Position model
- Manual tasks → Manual + Workflow tasks
- Personal projects → Linked Program context
- Personal history → Full audit history

---

# 71. Migration from the Operational App

Reuse the operational concepts:

- 20 Positions
- 13 Program Stages
- Program lifecycle
- Program pipeline
- My Work concept
- Position-specific actions
- Stage completion rules
- Parallel operational activities
- Visits
- Follow-Ups
- Readiness
- Delivery
- Assessment
- Finance
- Graduate Outcomes
- Improvement
- Closure
- Master data
- Guided workflow concepts

Do not reuse the Operational App visual design.

---

# 72. Training Mode

The Operational App's guided simulation idea should be retained as **Training Mode**.

Training Mode should:

- Create isolated test program
- Walk through all 13 stages
- Change the acting Position at each step
- Explain required inputs
- Explain completion checks
- Explain system result
- Explain next handover

Training data must never mix with live operational data.

---

# 73. Development Phases

## Phase 1 — Foundation

Build:

- New project structure
- Existing Task Planner UI shell
- Branding
- Themes
- Profile
- Profile image
- Empty first login
- SQLite
- Employees
- Positions
- Position assignment
- Permission engine

### Acceptance
Position controls visible navigation and allowed actions.

## Phase 2 — Personal Work

Build:

- Home
- My Work shell
- My Tasks
- Today
- Weekly Planner
- Monthly Planner
- Quarterly Planner
- Progress controls
- Hours
- Links
- Reports

### Acceptance
Manual employee task workflow works completely.

## Phase 3 — Programs

Build:

- Program Pipeline
- Program creation
- Program Workspace
- 13 Stage Flow
- Program documents
- Stage status
- Audit

### Acceptance
A program can move through the stage model with Position restrictions.

## Phase 4 — Work Assignment Integration

Build:

- Work Assignment engine
- Position rule triggers
- Assignment → Task generation
- Task → Workflow completion
- Handovers

### Acceptance
A program action automatically becomes the correct employee's work.

## Phase 5 — Operational Activities

Build:

- Instructors
- Logistics & Place
- Attendees
- Sponsorships
- Activity ownership
- Visits
- Follow-Ups
- Activity completion
- Supervisor review

### Acceptance
Four operational lanes work independently and generate employee tasks.

## Phase 6 — Readiness and Delivery

Build:

- Readiness checklist
- Go / Conditional Go / No-Go
- Delivery
- Sessions
- Attendance
- Incidents
- Evidence

### Acceptance
Delivery is gated correctly by the workflow.

## Phase 7 — Academic / Finance / Outcomes

Build:

- Assessment
- Certificates
- Finance PMB
- Treasury
- Graduate Outcomes
- Reporting & Improvement
- Final Closure

### Acceptance
A complete program can reach final closure.

## Phase 8 — Notifications, Exceptions, Reports

Build:

- Notification center
- Exception engine
- Personal reports
- Program reports
- Management reports
- Excel export
- PDF export

## Phase 9 — Administration

Build:

- Employee management
- Position Rules UI
- Workflow Rules UI
- Master data
- System settings
- Audit viewer

## Phase 10 — Training and Testing

Build:

- Training Mode
- Sample programs
- Test programs
- Test Position switching
- Workflow validation scenarios
- Error / edge case testing

---

# 74. Core Prototype Success Scenario

The first combined prototype must prove this full cycle:

```text
1. Program Operations Executive creates Program
2. Program is submitted for Greenlight
3. Academy Manager receives approval work
4. Manager approves
5. Curriculum Position receives work
6. Curriculum is completed and locked
7. Instructor Setup assignments are generated
8. Launch work is assigned
9. Operational Activities start in parallel
10. Each Specialist receives their own My Work items
11. Visits can generate Follow-Up Tasks
12. Supervisor reviews all four activities
13. Readiness work is created
14. Academy Manager records delivery decision
15. Program Coordinator receives Delivery work
16. Assessment work is generated
17. Finance assignments are generated
18. Graduate Outcomes work is generated where applicable
19. Improvement work is generated
20. Final Closure is approved
21. Program is completed
22. Full audit and reports remain available
```

If this scenario works correctly, the core system architecture is successful.

---

# 75. Key Review Decisions Required Before Building

The Academy should approve the following before implementation:

1. Exact rules for all 20 Positions
2. Employees allowed to hold multiple Positions
3. Program visibility by Position
4. Field-level edit permissions
5. Approval authority
6. Delegation rules
7. Backup Position rules
8. Required evidence by stage
9. Workflow completion requirements
10. Automatic task generation rules
11. Follow-Up assignment rules
12. Exception assignment rules
13. Notification rules
14. Report visibility
15. Financial visibility
16. Instructor / SME permissions
17. MBA/DBA-specific responsibilities
18. Which Position may create Programs
19. Who may cancel a Program
20. Who may reopen a completed Stage
21. Who may override workflow gates
22. Whether overrides require a comment / approval

---

# 76. Recommended Review Order

Review the system in this order:

```text
1. Positions
2. Position Rules
3. Program Lifecycle
4. Stage Requirements
5. Operational Activities
6. Work Assignment Rules
7. Handovers
8. Approvals
9. Task Integration
10. Dashboard / My Work
11. Reports
12. Administration
13. Training Mode
14. Technical Architecture
```

The most important document after this Master Plan should be the detailed **Position Rules Matrix**.

---

# 77. Final Product Definition

The Andalusia Academy Work Management System should become:

> A position-driven Academy operations and employee execution platform where every program action is assigned to the correct Position, every employee sees only the work relevant to their responsibilities, operational workflow automatically generates personal work, and the existing Andalusia Task Planner UI/UX remains the main employee experience.

The system should feel simple to the employee even though the workflow behind it is detailed.

The complexity belongs in the **rules engine**, not in the employee's task form.

---

# 78. Source Inputs Used for This Plan

This plan combines:

1. The existing Andalusia Academy Task Planner project and its current UI/UX decisions.
2. The uploaded **Workflow Group AHQ — andalusia_academy_operational_app_v16** prototype.
3. The existing operational positions, 13-stage lifecycle, operational activity lanes, role-specific action logic, visit/follow-up model, readiness, delivery, assessment, finance, graduate outcomes, improvement, closure, master data, and guided simulation concepts.
4. The requirement that every Position has its own rules rather than a generic management hierarchy.

---

# 79. Proposed Next Design Artifact

After approval of this master plan, create:

**Andalusia Academy — Position Rules Matrix.md**

For each Position it should document:

- Visible modules
- Visible programs
- Stages
- View permissions
- Create permissions
- Edit permissions
- Field permissions
- Approval permissions
- Required actions
- Required evidence
- Generated tasks
- Notifications
- Reports
- Handovers
- Delegation
- Overrides

That matrix should become the functional specification for the permission and workflow engine.


---

# Prototype V4 Completion Status

Prototype V4 implements the complete local prototype scope: 13-stage lifecycle, Position-driven work, personal planner, documents, global search, reports, audit, administration, master data, isolated training mode, and SQLite-backed local persistence. Microsoft 365 live integration and production multi-user authentication remain deployment-phase work rather than simulated prototype features.

# Prototype V5 — Detailed Stage Execution Status

Prototype V5 builds on the V4 local prototype and makes the lifecycle review explicitly stage-by-stage. The employee UI/UX remains the Andalusia Task Planner experience, while every Academy program stage exposes its Position owners, prerequisite, completion requirement, next handover, and open work.

## V5 detailed implementation

- Stage 1 — Request & Greenlight: retained as the program initiation and Academy Manager approval gate.
- Stage 2 — Curriculum: separated into Curriculum Draft, Academic QA, and Lock & Release. Outline, Topic, Competences, Duration, the existing academic fields, a curriculum pack/reference, and four QA checks are required before release.
- Stage 3 — Instructor Setup: separated into shortlist, evaluation, selection, R/H, project basis, Part / Full Time, Level, Assigned Groups, Internal / External, agreed fee, Academy Manager fee approval, Legal contract/reference, and Operations Supervisor onboarding/reference.
- Stage 4 — Launch Planning: validates the complete workshop planning record—month, workshop, specialty, level, target audience, duration, teaching method, hands-on, instructor shooting, supplement changes, estimated fee, date, priority, research, brief, link, P&L, minimum participants, capacity, schedule, and Studio readiness—before the Academy Manager records Go or No Go.
- Stage 5 — Commercial: validates the applicable B2C/B2B routes, including B2C registration/payment count consistency and B2B proposal/contract progression.
- Stage 6 — Operational Activities: preserves the four parallel lanes with specialist Position ownership, activity-specific inputs, visits, follow-ups, evidence, and Academy Operations Supervisor review.
- Stage 7 — Readiness: can refresh evidence from completed program records, maintains the readiness checklist, and remains gated by the Academy Manager Go / Conditional Go / No-Go decision.
- Stage 8 — Delivery: manages session execution, attendance, instructor check-in, evidence, and incidents; unresolved incidents block completion.
- Stage 9 — Assessment & Certification: validates pass count against actual attendance and certificate count against pass count, with approved results and certificate evidence required.
- Stage 10 — Finance: preserves Finance — PMB and Finance — Treasury separation; settlement evidence and P&L closure are required.
- Stage 11 — Graduate Outcomes: validates the outcome funnel Eligible → Consented → Job Ready → Placement Pool → Shortlisted → Placed.
- Stage 12 — Reporting & Improvement: requires the performance report, course review, and completion of all Position-owned improvement actions.
- Stage 13 — Final Closure: requires all prior stages complete, Finance closed, outcomes completed/N/A, improvement complete, no open workflow assignments, both closure approvals, and lessons learned.

## V5 testing

Profile includes **Add Stage 2–13 Test Program**, which creates a program immediately after an approved Greenlight and activates Curriculum. This is the preferred test route for reviewing all remaining lifecycle stages without repeating Stage 1 for every test cycle.

# Prototype V5 — Review Revision 1

Review Revision 1 adds Curriculum Developer as the twentieth Position, grants Program creation to Academy Manager while retaining Program Operations Executive creation, expands Stage 2 and Stage 3 completion data, and preserves the existing Andalusia UI/UX and Position-driven governance.

# Prototype V5 — Review Revision 2

Review Revision 2 makes Launch Planning an Academy Manager approval gate. All requested workshop planning information is shown in a dedicated manager dashboard table. No Go requires a recorded reason and generates corrective work; Go is blocked until the plan is complete and then activates Commercial.

# Prototype V5 — Review Revision 3

Review Revision 3 gives the Academy Manager an all-crew work dashboard and the ability to assign general or Program-linked tasks to any Academy Position. The dashboard shows every crew assignment with status totals, due dates, priorities, ownership, and assigning manager.

The Academy Training Life Cycle is consolidated from thirteen to nine visible stages. Former Stages 4–6 are preserved as gated sections inside **Stage 4 — Launch, Commercial & Operations**. Former Stages 7–9 are preserved as gated sections inside **Stage 5 — Readiness, Delivery & Assessment**. Finance, Graduate Outcomes, Reporting & Improvement, and Final Closure become Stages 6–9. Existing 13-stage local records and stage references migrate to the new combined-stage structure when loaded.

# Prototype V5 — Review Revision 4

Review Revision 4 combines Finance into **Stage 4 — Launch, Commercial, Operations & Finance** as Section 4D. Finance — PMB and Finance — Treasury remain separate Position-controlled lanes. Finance is unlocked after the Academy Operations Supervisor approves all Operational Activities; completing both Finance responsibilities closes Stage 4 and activates Readiness.

The Academy Training Life Cycle now contains eight visible stages. Readiness, Delivery & Assessment remains Stage 5. Graduate Outcomes, Reporting & Improvement, and Final Closure become Stages 6–8. Existing standalone Finance stages, assignments, tasks, and document references migrate into the combined Stage 4 when local records are loaded.

# Prototype V5 — Review Revision 5

Review Revision 5 grants the Academy Manager full lifecycle completion authority. With Academy Manager active, every Position-owned stage control is available from the Program Workspace, including Curriculum drafting and QA, Instructor Setup, all Stage 4 operational and financial lanes, Readiness preparation, Delivery, Assessment, Graduate Outcomes, and improvement actions. The Manager can also complete outstanding Stage Work assignments, with linked follow-ups, incidents, and improvement actions updated automatically.

Specialist ownership and the Position-driven handover model remain visible and unchanged for other users. Manager authority does not bypass required data, evidence, count validation, sequential handovers, financial controls, or Go / No Go decision rules.

Revision 5 also consolidates the sidebar planner links into one Planner workspace, adds an all-Program Finance portfolio, and adds a timed session Schedule for today and planned dates. The manager dashboard limits Launch Planning and Academy Crew Tasks to five visible records by default and provides See All / Show 5 expansion. Delivery session date and time are stored in the combined Stage 5, where Delivery and Assessment remain sequential sections of one lifecycle stage.

# Prototype V5 — Review Revision 6

Review Revision 6 turns the Academy Manager's Launch Planning and Academy Crew Tasks areas into two compact command cards. Each card displays five priority records first, provides independent See All / Show 5 behavior, and uses a bounded internal list so high record counts do not push the rest of the dashboard out of reach. Crew assignment is collapsed until the manager selects Assign Task.

The desktop layout is tuned for 1920×1080 and 1280×720 displays. The two command cards remain side-by-side at both target sizes, spacing and list heights compress on 720-pixel-high screens, and the page avoids horizontal overflow. Below 1180 pixels wide the cards stack for narrower screens.

Revision 6 removes My Work from current navigation and Profile choices because My Tasks is the single personal-work workspace. Existing saved `mywork` values are redirected to My Tasks for backward compatibility. Academy Manager retains the ability to create Programs and retains full fill, submit, review, and completion authority through all eight lifecycle stages.

# Prototype V5 — Review Revision 7

Review Revision 7 separates Stage 1 draft persistence from workflow submission. Save Draft now keeps Request & Greenlight editable and does not create approval work. Submit for Greenlight collects the current form directly, validates all required request data, changes the stage to Pending Approval, locks the request, closes the submitter assignment, creates one Academy Manager approval, and records only the submission audit event. A visible explanation and consolidated validation warning make the two outcomes clear.

Revision 7 was validated with one clean Program completed through the full eight-stage lifecycle. Academy Manager created and submitted the request, approved Greenlight, completed Curriculum and Instructor Setup, completed every Section 4 lane including all four operational activities and Finance, authorized and completed Stage 5, recorded Graduate Outcomes, completed Reporting & Improvement, and approved Final Closure. The Program reached Completed with all eight lifecycle stages closed and no browser console errors.
