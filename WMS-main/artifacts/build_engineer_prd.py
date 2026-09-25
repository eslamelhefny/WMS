"""Technology-agnostic functional requirements for engineering handoff (Power Apps build)."""
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts' / 'Andalusia_Academy_Engineering_Requirements.docx'
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.27), Inches(11.69)
sec.top_margin, sec.bottom_margin = Inches(.73), Inches(.65)
sec.left_margin = sec.right_margin = Inches(.73)
sec.header_distance = sec.footer_distance = Inches(.3)
PRIMARY, DARK, SOFT, INK = 'C17A62', '8F4F3B', 'F3E4DF', '55372F'

for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','Caption']:
    st = doc.styles[name]
    st.font.name = 'Calibri'
    st.font.color.rgb = RGBColor.from_string('000000')
    for border in list(st.element.iter(qn('w:pBdr'))):
        border.getparent().remove(border)
normal = doc.styles['Normal']
normal.font.size = Pt(10.5)
normal.paragraph_format.space_after = Pt(7)
normal.paragraph_format.line_spacing = 1.1
for name, size, before, after in [('Title',27,6,12),('Subtitle',14,0,12),('Heading 1',20,0,14),('Heading 2',12,10,5),('Heading 3',11,7,4)]:
    st=doc.styles[name];st.font.size=Pt(size)
    st.paragraph_format.space_before=Pt(before);st.paragraph_format.space_after=Pt(after)
    st.paragraph_format.keep_with_next=True
doc.styles['Caption'].font.size=Pt(9)
doc.styles['Caption'].font.color.rgb=RGBColor.from_string('7D6A63')

header=sec.header.paragraphs[0]
header.text='ANDALUSIA ACADEMY    /    FUNCTIONAL REQUIREMENTS'
header.runs[0].font.size=Pt(8)
header.runs[0].font.bold=True
footer=sec.footer.paragraphs[0]
footer.paragraph_format.space_before=Pt(5)
footer.add_run('WMS Functional Requirements  |  Version 1.0  |  8 September 2026').font.size=Pt(8)
footer.add_run(' '*8+'Page ').font.size=Pt(8)
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
for run in footer.runs:run.font.color.rgb=RGBColor.from_string(DARK)

def p(text='',bold=False,style=None):
    para=doc.add_paragraph(style=style)
    run=para.add_run(text);run.bold=bold
    return para
def h(text):doc.add_heading(text,2)
def h3(text):doc.add_heading(text,3)
def bullet(text):
    para=p(text,style='List Bullet');para.paragraph_format.space_after=Pt(5)
def page(number,title):
    doc.add_page_break()
    e=p(f'{number:02d}   ANDALUSIA ACADEMY')
    e.runs[0].font.color.rgb=RGBColor.from_string(DARK);e.runs[0].font.size=Pt(9);e.runs[0].bold=True
    doc.add_heading(title,1)
def req(id,title,text):
    para=doc.add_paragraph();para.add_run(f'{id}  {title}  ').bold=True;para.add_run(text)
def note(text,label='Note'):
    para=doc.add_paragraph();r=para.add_run(f'{label}.  ');r.bold=True;r.font.color.rgb=RGBColor.from_string(DARK)
    para.add_run(text)
def oos(text):
    note(text,'Out of scope')
def table(headers, rows, widths, size=9.5):
    t=doc.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    for c,w in zip(t.columns,widths):c.width=Inches(w)
    pr=t._tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        b=OxmlElement('w:'+edge);b.set(qn('w:val'),'single');b.set(qn('w:sz'),'5');b.set(qn('w:color'),'D9D9D9');borders.append(b)
    pr.append(borders)
    for index, vals in enumerate([headers]+rows):
        row=t.rows[0] if index==0 else t.add_row()
        trPr=row._tr.get_or_add_trPr();cant=OxmlElement('w:cantSplit');trPr.append(cant)
        if index==0:
            rep=OxmlElement('w:tblHeader');trPr.append(rep)
        for j,(cell,value,width) in enumerate(zip(row.cells,vals,widths)):
            cell.width=Inches(width);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cp=cell._tc.get_or_add_tcPr();shade=OxmlElement('w:shd');shade.set(qn('w:fill'),DARK if index==0 else ('FFF9F6' if index%2 else 'FFFFFF'));cp.append(shade)
            margins=OxmlElement('w:tcMar')
            for side in ['top','left','bottom','right']:
                m=OxmlElement('w:'+side);m.set(qn('w:w'),'95');m.set(qn('w:type'),'dxa');margins.append(m)
            cp.append(margins)
            para=cell.paragraphs[0];para.paragraph_format.space_after=Pt(1);para.paragraph_format.line_spacing=1.05
            r=para.add_run(str(value));r.font.size=Pt(size);r.bold=index==0;r.font.color.rgb=RGBColor.from_string('FFFFFF' if index==0 else INK)
    p().paragraph_format.space_after=Pt(1)
    return t

# ---------------------------------------------------------------- Cover
logo=p();logo.alignment=WD_ALIGN_PARAGRAPH.CENTER
pic=logo.add_run().add_picture(str(ROOT/'static/logo.png'),width=Inches(1.8))
pic._inline.docPr.set('descr','Original bilingual Andalusia Academy logo')
doc.add_paragraph('Andalusia Academy\nWork Management System',style='Title')
doc.add_paragraph('Functional Requirements — Engineering Handoff',style='Subtitle')
p('Version 1.0   |   8 September 2026   |   Prepared for Power Apps engineering',True)
h('How to read this document')
p('Every requirement below describes an observable behavior: what a user does, what the system checks, and what happens next. It intentionally does not prescribe how to build it. Choices such as canvas app vs. model-driven app, table design, or which piece of logic runs in a flow versus a screen are left to the implementing engineer. Requirement IDs (e.g. RQ01) exist for traceability during build and test, not for a specific implementation.')
h('Purpose and product direction')
p('Andalusia Academy runs training programs, certificate programs, workshops, corporate programs, and webinars, through a fixed eight-stage lifecycle: request, curriculum, instructor setup, launch/commercial/operations/finance, readiness/delivery/assessment, graduate outcomes, reporting and improvement, and final closure. The system exists to move a program through that lifecycle with the right person doing the right thing at the right time, with nothing skipped.')
h('Business outcomes the build must serve')
bullet('A manager can see portfolio health, what needs attention, and make Go / No-Go decisions from evidence, not memory.')
bullet('Every lifecycle stage has an owner, a completion rule, and a manager gate; no stage closes itself.')
bullet('Work created by the lifecycle (approvals, follow-ups, incidents, corrective actions) reaches the right person as a task, automatically.')
bullet('Relationships with instructors, sponsors, and partners are tracked as reusable records, not lost in email threads.')
h('Explicitly out of scope for this build')
bullet('Payment processing, bank reconciliation, or accounting-ledger entries. The system records confirmations and references, not transactions.')
bullet('Issuing certificates, grading exams, or sending them by email.')
bullet('External calendar sync, automated email/SMS delivery, or e-signature.')
bullet('A general-purpose CRM, HR system, or document-storage replacement.')

# ---------------------------------------------------------------- Chapters
page(2,'Users and roles')
p('Every user holds one primary Position and may hold additional Positions. Positions, not individual named users, own lifecycle stages, sections, and work items. A person’s visible work, navigation, and authority all derive from their active Position(s).')
table(['Position','Owns / contributes to'],[
('Academy Manager','Full contribution authority across every stage, plus exclusive manager-completion (stage-closing) authority. Manager Dashboard, Team Members, Administration, program creation, Management Summary report.'),
('Academy Operations Supervisor','Program coordination, operational-lane review and approval, onboarding, readiness, delivery support, course review, Management Summary report, program creation.'),
('Program Operations Executive / MBA-DBA Program Executive','Program creation and day-to-day program operations contribution.'),
('Academy Curriculum Development Manager / Curriculum Developer','Curriculum authoring and QA; also supports instructor setup and assessment.'),
('Academy BD & Partnerships Head / Business Developer','Corporate and partnership context, B2B commercial completion, program creation (Head only).'),
('Operations Specialist — Instructor Coordination','Owns the Instructors operational lane.'),
('Operations Specialist — Logistics','Owns the Logistics and Place operational lane.'),
('Operations Specialist — Registration','Owns the Attendees operational lane.'),
('Operations Specialist — Partnerships Support','Owns the Sponsorships operational lane.'),
('Program Coordinator','Readiness preparation, delivery sessions, attendance, incidents, assessment contribution.'),
('Finance — PMB','Actual revenue and cost, profit and loss closure.'),
('Finance — Treasury','Sponsorship collection and instructor / vendor payment confirmation.'),
('Legal','Instructor contract status and reference.'),
('Marketing Account Manager','Launch marketing brief contribution.'),
('Studio Account Manager','Studio production readiness contribution.'),
('Recruitment Head','Graduate outcomes funnel.'),
('Instructor / SME','Selectable Position for instructor-side assignment context.'),
],[2.35,4.45],9.2)
h('Access rules that apply regardless of implementation')
req('GV01','Position model','Contribution checks must consider the primary Position and any additional Positions held. Academy Manager’s authority is additive on top of every stage owner’s authority, not a separate override path.')
req('GV02','Manager boundaries','Manager Dashboard, Team Members, Team Member Profile, and Administration are visible only to Academy Manager. Management Summary is visible to Academy Manager and Academy Operations Supervisor only. A non-manager’s default landing view must never be a manager-only screen.')
req('GV03','Program creation','The "create new program" action is visible only when an active Position is one of: Academy Manager, Program Operations Executive, MBA/DBA Program Executive, Academy BD & Partnerships Head, Academy Operations Supervisor.')

page(3,'Data entities')
p('This is a data dictionary, not a schema. It states what each record must hold and how records relate, leaving table design, keys, and storage to the engineer.')
table(['Entity','Holds','Relates to'],[
('Profile','Name, employee ID, email, department, job title, phone, primary + additional Positions, theme, default view, photo','Single record per user'),
('Program','Name, type, commercial route, specialty, region, dates, expected participants, budget, objective, owner; all eight stage records; four operational-activity records','Owns stages, activities, finance, documents, sessions, audit events'),
('Task','Title, project/program link, category, priority, status, deliverable type, progress %, start/due dates, estimated/actual hours, recurrence setting, reference link, notes','Optionally mirrors an Assignment; belongs to a Position'),
('Assignment','Program, stage, action, owner Position, priority, due date, kind (approval / stage action / manager task / corrective / review / follow-up / incident / improvement), notes, assigner, timestamps','Program; optional Task mirror; optional source record'),
('Notification','Target Position, message, read flag, created-at, linked record reference','Assignment or Program'),
('Audit event','Action, actor, Position, timestamp, program reference (optional)','Program (when program-linked) or system-level'),
('Document reference','Name, program, stage, activity (optional), document type, reference/link, notes, added-by, created-at','Program; stage'),
('Instructor','Name, contact details, specialty, level, region, work schedule, availability, source, notes; per-program engagement fields','Many programs via engagement records'),
('Contact','Name (required), organization, role, email, phone, notes, created/updated timestamps','Many Networking Visits'),
('Networking visit','Contact, program (optional) or "General networking", activity, date, time, type, location/reference, purpose, outcome, notes, status, follow-up date, next steps, follow-up-completed flag','Contact; optional Program'),
('Delivery session','Date, time range, name, status','Owned by a Program’s Stage 5 delivery record'),
('Master data lists','Program types, specialties, regions, venues, materials, sponsors, attendee subtypes, payment methods, visit types; each with a label and active flag','Referenced by Programs, Visits, Operations'),
],[1.55,3.7,1.55],9.0)
note('No hard relational integrity is assumed. The reference system links records by identifier without database-level foreign keys. The engineer should decide whether the target platform enforces referential integrity or the application layer reconciles it, but every relationship above must be navigable both directions in the UI (for example, open a program from an assignment, and see all assignments from that program).')

page(4,'Cross-cutting rules')
p('These patterns repeat across almost every module. Get them right once and most of the lifecycle logic elsewhere in this document falls out of them.')
req('R-01','Contributor vs. manager gate','Every stage and section follows the same two-step pattern: a contributor, the section’s owner Position, enters and saves data, and once every required condition is met the record is "ready", but the stage or section only actually closes when Academy Manager performs a separate completion action that re-validates all requirements. A contributor can never close a stage alone.')
req('R-02','Derived program status','Status is never set directly by a user; it is computed: Completed when both operational and financial closure are set, otherwise On Hold after a readiness No-Go, otherwise Delivered after delivery completion, otherwise Ready after readiness Go/Conditional Go, otherwise Preparing when overall progress is above zero, otherwise Planned.')
req('R-03','Overall progress','A program’s overall progress is the mean of its eight stage-completion percentages.')
req('R-04','Assignment to task mirroring','Whenever an Assignment is created for a Position, and that Position does not already have a Task mirroring it, create one. The consolidated task list must never show one linked assignment twice as two independent items.')
req('R-05','No duplicate assignments','Never create a second open Assignment with the same program, stage, and action already open.')
req('R-06','Completing an assignment closes its source','Where an Assignment carries a source-record reference (a follow-up, an incident, an improvement action), completing the assignment must also resolve that source record, not just mark the assignment done.')
req('R-07','Notifications follow work','Creating an assignment, an approval request, a follow-up, a completion, an operational review, a readiness hold, or a program completion must notify the relevant target Position in-app.')
req('R-08','Stage browsing is not stage activation','A user may inspect any of the eight stages at any time. Only the actual current stage accepts input; viewing a future stage must never unlock its fields or imply it is active.')

page(5,'Profile and navigation')
p('Establishes who is using the system and how they move around it.')
req('PF01','Register','Capture full name, email, employee ID, department, job title, phone, primary Position, and theme. Registration creates the workspace with no sample data. Managers default to Manager Dashboard; everyone else defaults to My Tasks.')
req('PF02','Maintain profile','Edit personal details, primary Position, and additional Positions. Choose a default landing view from the set the user’s Position is allowed to see; a non-manager cannot default to Manager Dashboard. Work week is Sunday through Thursday.')
req('PF03','Profile photo','Upload, preview, and remove a photo. Reject files over 8 MB; downscale accepted images to a maximum dimension of 512 pixels.')
req('NV01','Navigate','A persistent, collapsible navigation surface; the collapse preference is remembered per device. Mobile exposes primary destinations plus a secondary "More" menu. The active section and page title are always evident.')
req('NV02','Theme','Seven selectable themes (Terracotta default, Ocean, Forest, Plum, Midnight, Sandstone, Rose), switchable from navigation or Profile, applied instantly and remembered.')
req('SR01','Global search','After two or more characters, search tasks, programs, assignments, documents, and audit entries together; show up to 30 results with type and context; opening a result navigates to the right record. Contacts and visits have their own dedicated search inside Visits.')

page(6,'Assignments and notifications')
p('The generic work-routing engine underneath almost every workflow in the system.')
req('AS01','Create and route work','An assignment carries program, stage, action, owner Position, priority, due date, kind, notes, assigner, and timestamps. Kinds: approval, stage action, manager task, corrective work, review, operational follow-up, incident, improvement action. Enforce R-05, no duplicates.')
req('AS02','Task sync','Apply R-04: mirror every assignment into the owning Position’s task list.')
req('AS03','Complete work','The manager or the assigned active Position can complete an assignment; this sets its mirrored task to 100 percent Completed and applies R-06. Completing an assignment never by itself authorizes a lifecycle handoff; that still requires the relevant stage’s manager-completion action.')
req('NT01','In-app notifications','Apply R-07. Show an unread count and up to 30 recent notifications scoped to the user’s active Position(s), plus untargeted records. Opening one marks it read and navigates to its assignment or program.')
oos('Authenticated multi-user sessions, server-enforced authorization, or notification delivery via email, SMS, or push. These are in-app records only; see Non-functional requirements.')

page(7,'Manager dashboard')
p('Academy Manager’s single view of portfolio health, decisions waiting, and where to intervene.')
req('DB01','Executive metrics','Average program completion, task completion rate, team utilization, current-month session count, budget utilization, portfolio margin, each with supporting counts and a target comparison.')
req('DB02','Financial and capacity formulas','Inflow equals actual revenue plus collected sponsorship. Net equals inflow minus actual cost. Margin equals net divided by inflow, only when inflow is nonzero. Budget utilization compares actual cost to portfolio budget. Team utilization equals open work divided by eight items per Position, capped at 100 percent.')
req('DB03','Operational attention','Active programs, at-risk programs, overdue work, blocked work, team members, open approvals, each clickable through to the underlying record. Also: schedule, upcoming delivery, program health, personal work, instructor readiness, finance summary, recent activity.')
req('DB04','Launch Go/No-Go','A compact launch-decision list (five rows, expandable) showing plan-completion checks and expected contribution per program. Go is enabled only for a complete launch plan. No Go requires a reason and creates corrective work. A finalized Go cannot be reopened from this control.')
req('DB05','Crew assignment','An explicit "Assign Task" action, not a permanent form, requiring title, Position, and due date, with optional program/stage context, priority, and notes. Creates a Manager Task assignment, notifies the Position, and logs a program audit event when program-linked.')
req('DB06','Crew monitoring','Totals for open, overdue, and completed assignments across the team, sorted open-first then by due date, each showing owner, program, stage, due date, priority, assigner.')
note('The reference implementation used 80 percent program progress, 90 percent task completion, 80 percent team utilization, 85 percent budget guardrail, and 20 percent margin as comparison benchmarks. Confirm actual Academy targets with the business owner before hard-coding these.')

page(8,'Tasks')
req('TK01','Consolidated view','Personal tasks and workflow assignments together, table on desktop, cards on mobile. Managers see all Positions; everyone else sees only their own active Position(s). Columns: title, project/program, owner, priority, status, due date, progress, open action.')
req('TK02','Search and filter','Text search (title, project, category, stage, owner, notes) combined with project, status, priority, due-scope (all, today, this week, overdue), and, for managers, member filters.')
req('TK03','Create and edit','Title, project, category, priority, status, deliverable type, progress, start/due dates, estimated/actual hours, recurrence, reference URL, notes. Require title and dates; block a due date before the start date. Preserve workflow links when editing a mirrored task.')
req('TK04','Classification','Status: Not Started, In Progress, Completed, On Hold, Cancelled. Priority: Low, Medium, High. Categories: curriculum, content, proposals, materials, recording, assessment, quality review, coordination, delivery, program tracking, client meetings, administration.')
req('TK05','Progress','0 to 100 slider in steps of five, with 0/25/50/75/100 presets. 100 gives Completed. Lowering a completed task to a nonzero value gives In Progress; to zero gives Not Started. "Overdue" is a computed display state, never a stored status.')
req('TK06','Complete and delete','Ordinary linked assignments can be closed from here; approval, stage-action, and review work keeps its dedicated workflow controls. Deleting a task requires confirmation and deletes only the task record, never the assignment it mirrors.')
req('TK07','Summaries','Totals, completed, overdue, blocked, due-soon, status distribution, with "show all / show less" rather than always rendering full lists.')
note('Recurrence is a stored setting only; the system does not need to generate repeating task instances from it unless confirmed as required. See Open decisions.')

page(9,'Team directory and member profiles')
req('TM01','Directory overview','Total members, active members with open work, average utilization, overloaded/underloaded counts, search, and department/workload/status filters.')
req('TM02','Workload comparison','Per member: Position, department, utilization, total/open/overdue tasks, completion percentage, workload label.')
req('TM03','Workload thresholds','High equals open work at least eight or overdue at least three. Medium equals open work at least four. Otherwise Low. Underloaded equals fewer than two open items. Utilization equals open items divided by eight, capped at 100 percent. Confirm before treating as ground truth for capacity planning.')
req('TM04','Member profile','Identity, Position, department, workload, full assigned-work list, active/completed task counts, on-time indicator, average progress.')
req('TM05','Profile filters','Text, project/program, stage, status, priority, due-scope, record type, with "clear filters".')
req('TM06','Assign from profile','"Add Task" on a member profile preselects that Position; opening a task or assignment routes to its editor.')

page(10,'Planner')
p('A calendar view of tasks, distinct from the Plan dashboard, which covers operational activities and visits instead.')
req('CL01','Weekly board','Sunday through Thursday, filterable by project, status, priority, with period navigation and a "today" jump.')
req('CL02','Day lanes','Each workday lists its active tasks (title, project, priority, status, progress, link); adding from a day prefills that date.')
req('CL03','Monthly calendar','Full month grid, current-day marker, muted Friday and Saturday, per-date task counts. A multi-day task appears on every date its range overlaps.')
req('CL04','Daily detail','Selecting a date opens its task list with status, project, priority, effort; supports opening, completing, adding, and printing.')
req('CL05','Quarterly view','Total overlapping tasks, completed count, actual hours, completion rate; three-month breakdown, up to seven items per month shown.')
req('CL06','Period membership','A task belongs to any period its start-due range overlaps; a task spanning two months is not double-counted as two unique quarterly tasks.')
req('CL07','Printing','Daily and period views must support print/PDF output via the platform’s native print path.')
oos('Outlook or Google Calendar sync, or reminders/notifications generated from recurrence.')

page(11,'Program portfolio and workspace')
req('PG01','Portfolio list','Totals by status (active, planned, completed, on-hold), average progress, search (name, type, route, region, specialty), status filter, current-stage filter; table on desktop, cards on mobile.')
req('PG02','Lifecycle intelligence','All eight stages shown together with per-stage program counts and on-track/at-risk/overdue breakdowns; first-load selection should favor a stage that actually has risk or overdue work.')
req('PG03','Create a program','Name, type (Certificate, Workshop, Corporate, Webinar), route (B2C, B2B, Mixed), specialty, region, dates, expected participants, preliminary budget, objective, owner. Creating a program initializes all eight stages and all four operational activities in their starting state.')
req('PG04','Workspace overview','Identity, dates, status, overall progress, current stage, key requirements, team, open work, and recent activity, with detailed stage forms and evidence tucked behind expandable panels.')
req('PG05','Stage navigation','All eight stages inspectable at once; the actual current stage is always visually distinct from whichever stage the user is currently viewing (R-08).')
req('PG06','Stage control panel','For the current stage: owner Position(s), prerequisite, completion rule, next handoff, open assignment count, and a manager-completion control enabled only when every requirement check passes.')
req('PG07','Derived status','Apply R-02 and R-03.')

page(12,'The eight-stage lifecycle: Stages 1 and 2')
p('Every stage follows the contributor-then-manager gate pattern from R-01. What differs per stage is who contributes, what is required, and what unlocks next.')
h('Stage 1 of 8 — Request and Greenlight')
p('Owner: program creator, then Academy Manager approval. Purpose: capture a justified program request and get manager sign-off before any academic work begins.')
req('RQ01','Draft and submit','Save Draft keeps partial data and requests nothing. Submit for Greenlight validates name, expected attendees above zero, preliminary budget above zero, objective, and demand evidence; on failure, show all missing items together and keep the form editable.')
req('RQ02','Approval and return','A valid submission moves to Pending Approval, fields lock, and one open manager approval is created. Manager Approve completes Stage 1 and activates Stage 2. Manager Return unlocks the request and creates high-priority resubmission work for the owner.')
h('Stage 2 of 8 — Curriculum')
p('Owner: Curriculum Developer / Curriculum Management, then Academy Manager handoff. Purpose: produce an academically complete, QA’d, version-locked curriculum pack.')
req('CU01','Required fields','Outline, topic, competences, duration, learning outcomes, program structure, assessment blueprint, draft-pack reference: all eight required before QA and release; partial saves as draft.')
req('CU02','QA','Requires: greenlight complete, all fields complete, and four checks passed (details, learning outcomes, structure, assessment).')
req('CU03','Lock and handoff','A QA-approved pack can be locked, recording version and release timestamp; locked fields are no longer freely editable. Locking is not the same as closing the stage; manager completion is still required to activate Stage 3.')
note('Outputs: request approval creates curriculum-drafting and QA work; curriculum completion creates instructor shortlisting/selection work, manager fee approval, Legal contract work, and supervisor onboarding work.')

page(13,'Stage 3: Instructor setup')
p('Owner: Program Operations / Curriculum Management, plus Legal and Operations Supervisor. Purpose: move a shortlisted instructor to a fully contracted, onboarded, fee-approved engagement.')
req('IS01','Selection','Shortlist, evaluations, selected instructor; the selected instructor must be among those evaluated.')
req('IS02','Engagement profile','Rate per hour, project-based flag, work schedule, level, assigned groups, source: all six required.')
req('IS03','Fee approval','Agreed fee above zero plus manager fee approval.')
req('IS04','Contract and onboarding','Signed-contract status plus reference (Legal); onboarding-complete status plus reference (Operations Supervisor). A checked status without its reference does not count.')
req('IS06','Completion gate','Completion requires: non-empty shortlist and evaluations, a selected evaluated instructor, all engagement fields, positive approved fee, signed contract with reference, completed onboarding with reference. Contributor completion prepares the stage; manager completion activates Stage 4.')

page(14,'Stage 4: Launch, Commercial, Operations and Finance')
p('The largest stage: four sub-stages that must each complete before Stage 5 opens.')
h3('4A — Launch planning and Go/No-Go')
p('Owner: Operations Supervisor / Program Operations, then Academy Manager decision.')
req('LP01–LP03','Fields','Program/offer data (month, name, specialty, level, audience, duration, teaching method, hands-on format, shooting requirement, supplement change, price, launch date, priority, min participants, capacity); evidence (demand research, reference link, marketing brief, comments, schedule confirmation, studio request and readiness); financials (budget above zero, expected revenue above zero, expected contribution equals revenue minus budget; price above zero; min participants above zero; capacity at least min participants).')
req('LP04–LP07','Decision','Submit requires all launch checks including confirmed schedule and Ready studio status. Only Academy Manager records Go or No Go. Go closes launch work and opens applicable B2C/B2B commercial work. No Go requires a reason, creates high-priority corrective work, and keeps the stage active. A finalized Go or completed stage cannot be re-decided.')
h3('4B — Commercial: B2C and B2B')
p('Owner: Program Operations (B2C), BD & Partnerships (B2B).')
req('CM01','Route applicability','B2C route requires the B2C section; B2B requires the B2B section; Mixed requires both. Requires launch Go first.')
req('CM02–CM05','Validation','B2C: registered no greater than leads; paid no greater than registered; fee and waitlist nonnegative; status must reach Completed. B2B: opportunity must reach Contracted or Won with account, proposal reference, and contract reference present; value and participants nonnegative.')
req('CM07','Complete and hand off','When every applicable route passes validation, Commercial completes and activates the four operational lanes.')
h3('4C — Operations: four parallel lanes')
p('Owner: the four Operations Specialists, then Operations Supervisor review.')
req('OP02–OP05','Per-lane requirements','Instructors: agenda/reference plus at least one interaction plus zero open follow-ups. Logistics: venue plus materials plus at least one interaction plus zero open follow-ups. Attendees: positive expected count plus attendee-list reference plus at least one interaction plus zero open follow-ups. Sponsorships: sponsor plus positive amount plus at least one interaction plus zero open follow-ups.')
req('OP06–OP08','Interaction logging','Log a visit/interaction (target, date, channel, objective, outcome, evidence, optional follow-up date) into the lane’s history. A follow-up date auto-creates a Follow-Up assignment for the lane owner (R-04); closing it auto-resolves the follow-up (R-06). All four lanes complete, then Operations Supervisor review, then approval opens Finance.')
h3('4D — Finance: PMB and Treasury')
p('Owner: Finance PMB (results) and Finance Treasury (settlements), separately.')
req('FN04–FN06','Requirements','PMB: nonnegative actual revenue plus actual cost, profit and loss closure confirmed. Treasury: nonnegative sponsorship collected, instructor-paid flag, vendor-paid flag, payment-proof reference. Finance is available only after Operations Supervisor approval; closes only when both sub-sections meet their requirements.')
req('FN07','Manager handoff','Manager completion of Stage 4 also re-verifies launch Go, Commercial completion, and Operations approval before activating Stage 5.')

page(15,'Stage 5: Readiness, Delivery and Assessment')
h3('5A — Readiness checklist and Go/No-Go')
req('RD01–RD03','Checklist','Agenda, instructor contract, venue, materials, attendee communication, sponsor confirmation, financial clearance, AV test: all eight required for Go. A "refresh from evidence" action can suggest checklist values from existing program data; these are heuristics requiring human confirmation, never auto-proof.')
req('RD05–RD07','Decision','Manager records Go or Conditional Go only when all eight items are checked. No-Go keeps the stage active, creates corrective readiness work, notifies the supervisor, and sets program status to On Hold. A positive decision opens delivery-execution work for Program Coordinator.')
h3('5B — Delivery, sessions and incidents')
req('DL01–DL02','Delivery','Track status, attendance, instructor arrival, execution evidence, and per-session date/time/status. Complete Delivery requires instructor check-in, execution evidence, every session Completed, and zero unresolved incidents.')
req('DL03–DL04','Incidents','Category, severity, description, owner, due date. High or Critical severity produces a high-priority assignment; other severities produce medium priority. Closing the linked assignment resolves the incident (R-06). Unresolved incidents block delivery completion.')
h3('5C — Assessment and certificates')
req('ASM01','Fields','Assessment-completed flag, pass count, feedback score, certificates issued, results reference, certificate reference, comments.')
req('ASM02–ASM04','Validation and completion','Zero to attendance for pass count; zero to five for feedback; zero to pass count for certificates issued; both references required. Stage 5 completes only after readiness authorization, completed delivery, and valid assessment, via the manager gate. If graduate outcomes do not apply to this program, mark that stage N/A and completed, then continue to Stage 7 directly.')

page(16,'Stages 6, 7 and 8: Outcomes, Improvement, Closure')
h('Stage 6 of 8 — Graduate Outcomes')
p('Owner: Recruitment Head. Applicable to programs flagged for graduate/placement tracking; Certificate Program is applicable by default.')
req('GO01','Fields','Eligible, consented, job-ready, placement-pool, shortlisted, placed counts, plus evidence and comments.')
req('GO02–GO03','Validation','All counts nonnegative and strictly non-increasing down the funnel: eligible ≥ consented ≥ job-ready ≥ placement-pool ≥ shortlisted ≥ placed. Outcome evidence required before completion. Non-applicable programs keep this stage visible, marked N/A and completed, never removed from the lifecycle.')
h('Stage 7 of 8 — Reporting and Improvement')
p('Owner: Operations Supervisor / Academy Manager.')
req('IM01','Fields','Performance-report reference, review-completed confirmation, comments.')
req('IM02–IM03','Improvement actions','Add an action (description, owner, due date) to create a linked Improvement assignment. Completing that assignment marks the source action Done (R-06). Stage ready only when a report exists, the review is complete, and every improvement action is Done; open actions block completion regardless of report status.')
h('Stage 8 of 8 — Final Closure')
p('Owner: Academy Manager.')
req('FC01','Review','Checks: all prior stages complete, financial closure, graduate-outcome applicability or completion, review complete, zero outstanding prior-stage assignments. A completed task mirror is never sufficient evidence on its own.')
req('FC02','Close','Confirm operational and financial closure, record lessons learned, closer plus timestamp. Sets Stage 8 to 100 percent, closes remaining program assignments, writes an audit event, and notifies the program owner.')

page(17,'Instructor directory and import')
req('IN01','Consolidated network','Combine active instructor master records with per-program shortlists, evaluations, and selections into one people-first directory, aggregated by name.')
req('IN02','Search and filter','By name, program, relationship status, internal/external, level, specialty, region, email, groups, schedule, readiness; filter to one program, all programs, or directory-only.')
req('IN03','Analytics','Unique, selected, external, and ready instructor counts, available capacity, average program load, expertise distribution, and attention counts for incomplete contracts, onboarding, or readiness.')
req('IN04','Instructor profile','Contact details, specialty, region, level, schedule, availability, notes, and every program engagement with its relationship, fee, groups, source, contract, onboarding, and readiness state.')
req('IN05','Manual add','Name (required, reject case-insensitive duplicates), email, phone, specialty, level, source, schedule, availability, region, notes. Defaults: source External, schedule Project Based, availability Available.')
req('IN06','Import preview','Accept XLSX/CSV with a downloadable template; normalize known column aliases; require Name; flag malformed emails and in-file duplicates; preview new, matching, and error rows before commit.')
req('IN07','Commit','Merge adds new names and leaves matches untouched. Replace-matching updates matches and adds new names, never deletes absent names. Report added, updated, and skipped counts.')
oos('Issuing contracts, or an instructor self-service portal. The system records references to contracts; it does not generate or send them. Instructor names are the matching key for import and aggregation, so spelling differences will fork identities.')

page(18,'Operations and Finance')
h('Operations lanes')
p('A dedicated view over the four operational lanes described under Stage 4C: useful as a cross-program work surface, not a separate data model.')
req('OP01','Program view','Select a program; see all four lanes’ owner, status, progress, interaction count, open follow-up count; totals and average progress across the four; open a lane in the program workspace.')
h('Finance')
req('FN01','Portfolio view','Recorded revenue, actual cost, sponsorship collected, net, margin, program comparisons, revenue mix, profitability, settlement/closure state, each row linking to that program’s Finance section.')
req('FN02','Per-program record','Current stage context, finance state, actual revenue/cost, sponsorship collected, net, instructor/vendor payment flags, profit and loss closure, payment evidence.')
req('FN03','Formulas','Same inflow, net, and margin definitions as R-02. No multi-currency conversion required; amounts are plain numeric values without a hard-coded currency suffix.')
oos('Bank payment execution, statement reconciliation, accounting journal entries, tax calculation, or live accounting-system integration. Payment flags are recorded confirmations only.')

page(19,'Delivery schedule and Plan dashboard')
h('Delivery schedule')
req('SC01','Source','Built entirely from each program’s Stage 5 delivery sessions (date, time range, name, status); editing a session in Stage 5 is the only way to change its schedule entry.')
req('SC02','Weekly calendar','Seven-day grid, 08:00 to 20:00 visible range, previous/next/today controls, session blocks showing time, instructor, region; wide grids scroll within their own region on small screens.')
req('SC03','Agenda view','Calendar/agenda toggle; scopes: Today plus Planned, Today Only, Planned Only, All Sessions. Planned means dated, today-forward, excluding Completed/Cancelled.')
req('SC04','Agenda record','Date/time, program name and ID, session title, instructor, region, status, open-program action; sorted by date/time; opening a session routes to that program’s Stage 5.')
oos('Appointment booking, instructor/room conflict detection, external calendar sync, invitations, or drag-and-drop rescheduling. This is a read view of configured sessions.')
h('Plan dashboard')
p('Cross-cutting operational view: combines operational activities, networking visits, and open follow-ups into one glanceable surface. Not a new task engine; a computed view over existing records.')
req('PL01','Lanes','In Progress and Upcoming, plus summary counts for In Progress, Upcoming, Overdue, Completed. Completed/Cancelled visits are excluded from the two open lanes.')
req('PL02–PL04','Entries','Activities: Not Started maps to Upcoming, In Progress stays In Progress, showing program start date as context, not a deadline. Visits: use the visit’s own status and date; an overdue Upcoming visit stays Upcoming until manually edited. Follow-ups: a visit with an open follow-up date gets its own entry; dated at or before today is In Progress, later is Upcoming; closing the follow-up removes the entry but keeps the visit’s history.')
req('PL05–PL06','Filter, search, counts','Program, activity, and text search combined; each lane sorted earliest-first, undated last. Counts computed after filters apply; "overdue" means an open item dated before today; a visit and its own open follow-up count as two separate planning items.')

page(20,'Networking and visits')
p('A reusable relationship directory, independent of but linkable to programs. Two parts: a Contact directory, and Visit records against those contacts.')
h('Contact directory')
req('NC01','Reusable contacts','Name (required), organization, role, email, phone, relationship notes; reusable across any number of visits, programs, and activities.')
req('NC02','Validation','Name, organization, and role up to 200 characters each; email up to 254 characters (format-validated when present); phone up to 60 characters; notes up to 4000 characters. Render all free text safely, never as markup.')
req('NC03','Directory view','Name, notes, organization, role, email, phone, total linked-visit count, and actions: History, Edit, Add visit.')
req('NC04','Contact history','Filter the visit list down to one contact’s visits, with a clear path back to the full list.')
req('NC06','Edit propagation','Editing a contact updates its details everywhere it is referenced; no historical snapshot of organization/role is kept per past visit unless explicitly required (see Open decisions).')
h('Visit records')
req('NV01','Create a visit','Contact (required), activity (required), program or "General networking", date (required), purpose (required); optional time, type, location/reference, outcome, notes, follow-up date, next steps.')
req('NV02','Types and statuses','Types: Physical Location, Online Meeting, Phone Call, Event, Email. Statuses: Upcoming, In Progress, Completed, Cancelled. Selecting Email never triggers an actual email send; it is a record label.')
req('NV03','Save validation','Existing contact required; program reference must resolve if non-blank; outcome required to save as Completed; follow-up date must not precede the visit date.')
req('NV05','Search and filter','Program and activity filters, contact-history scope, text search across contact, organization, email, phone, purpose, outcome, location, notes, activity, program.')
req('NV07','Operational history','Interactions logged from an operational lane appear here too, clearly labeled "Operational interaction," opening in their original activity rather than the visit editor; never silently merged or duplicated with networking visits.')
oos('Bulk contact import, duplicate merge, archive/delete, or automatic assignment creation from a networking follow-up. Only operational follow-ups auto-create assignments, per R-04.')

page(21,'Documents, reports and history')
h('Documents')
req('DC01','Register a document','Name, program, stage, document type, optional activity context, reference/link, notes, added-by, created-at. Types: curriculum, QA, evaluations, contracts, onboarding, agenda, marketing, proposals, attendance, results, certificates, payment evidence, reports, recruitment, other.')
req('DC02','Find, open, remove','Search plus program/stage/type filters. HTTP/HTTPS references open externally; other reference text displays as-is. Removal requires confirmation and logs an audit event; it deletes the reference record only, never an external file.')
note('This is a metadata register, not a document-storage system. If the build needs actual file upload and storage, confirm that as a platform decision; see Open decisions.')
h('Reports')
req('RP01','Period task reports','Weekly, Monthly, Quarterly, based on date-range overlap: totals, completed, in-progress, actual hours, and a task list with status, progress, hours, link.')
req('RP02','Program report','Status, overall progress, open work, operational follow-up count, per-stage owner, status, progress, open assignments, next handoff.')
req('RP03','Management Summary','Academy Manager and Operations Supervisor only: active/on-hold programs, open/overdue work, per-program stage, status, progress, owner. Any other Position sees a restriction message, not the report.')
req('RP04','Export','Print/PDF for reports via the platform’s native print path.')
h('History and audit')
req('HI01','Three views','Completed-task history (tasks with Completed status, openable), Program Audit (program-linked events), System Audit (everything else).')
req('HI02','Audit search','Program filter plus search across action, actor, Position, program ID; each row shows action, context, actor, Position, timestamp. Audit coverage focuses on workflow and configuration events; not every personal-task or networking edit is guaranteed a full audit trail.')

page(22,'Administration and training')
h('Administration')
req('AD01','Position rules','Academy Manager can edit a Position’s description, visible-module list, and core-action descriptions; "Reset override" reverts to the default profile. Every change logs a system audit event.')
req('AD02','Rule scope','These overrides are recorded configuration and labels; they must never be presented as, or substitute for, actual server-side permission enforcement. See Non-functional requirements.')
req('AD03','Workflow reference','A read-only reference table of all eight stages, owners, completion requirements, and handoffs; not an editable workflow designer.')
req('AD04','Master data','Manage Program Types, Specialties, Regions, Venues, Materials, Sponsors, Instructors, Attendee Subtypes, Payment Methods, Visit Types. Add (reject case-insensitive duplicates), activate/deactivate, audit-logged.')
h('Training mode')
req('TR01','Guided walkthrough','An eight-step instructional tour, one step per lifecycle stage, covering summary, responsible Position, inputs, completion checks, expected result, and next stage.')
req('TR02','Progress controls','Previous, Complete Step, Complete Training, jump-to-stage, Restart, remembered per device.')
req('TR03','Non-destructive by design','Training must never create, advance, approve, or close a real program; it is entirely separate from any sample/test-data utilities that do write real records.')

page(23,'Import, export and backup')
req('ST01','Save feedback','Every save shows Saving, Saved, or Save failed; never a silent failure.')
req('ST03','Task import','XLSX/CSV via a documented template; Replace overwrites the task list, Merge combines with existing tasks; report row-level errors rather than a false success.')
req('ST04','Workbook export','A downloadable workbook covering profile, personal tasks, and weekly/monthly/quarterly reports; instructor import has its own separate template.')
req('ST05','Full backup','Export a complete, human-readable snapshot of all data, including contacts and visits; import restores it wholesale. This is a restore operation, not a selective merge, and must warn accordingly.')
req('ST06','Test data','Sample/test record generators (tasks, programs at various lifecycle stages, instructors) live behind a clearly separated developer-tools area, distinct from Training mode, which never writes real data.')
req('ST07','Clear all data','A confirmation-gated destructive action that wipes profile, tasks, programs, assignments, notifications, documents, audit, master data, and configuration together.')

page(24,'Non-functional requirements')
p('These apply no matter which Power Platform components the engineer chooses, and are flagged because the reference implementation deliberately did not solve them; they need an explicit decision before wider rollout.')
req('NFR01','Identity and authorization','Define real authenticated users and server/platform-enforced authorization before shared use. A user’s selected Position in their profile is not a permission boundary by itself and must not be relied on as one.')
req('NFR02','Concurrency','Decide how simultaneous edits to the same record are handled. Last-write-wins is not acceptable for approval or financial data without an explicit decision to accept that risk.')
req('NFR03','Data governance','Define who may view, create, edit, export, archive, or delete records, particularly contacts, finance, and documents, and what audit trail is required for each.')
req('NFR04','Responsive UI','Every screen must work at phone, tablet, and desktop widths with no page-level horizontal scroll; wide tables and calendars scroll within their own region only.')
req('NFR05','Accessibility','Visible keyboard focus, labeled form controls, Escape-to-dismiss on dialogs, status communicated by text as well as color, minimum touch target sizing on mobile.')
req('NFR06','Operational readiness','Agree backup ownership, restore testing, expected record volumes, and response-time targets; test at the agreed volume before go-live.')

page(25,'Acceptance criteria')
p('Representative scenarios for stakeholder UAT and regression testing; not exhaustive, but each is a concrete pass/fail check per lifecycle stage.')
table(['ID','Scenario'],[
('UAT01','An incomplete request saves as a draft with no approval work created; submitting with zero expected attendees or missing demand evidence is blocked with validation; a complete submission creates exactly one open manager approval.'),
('UAT02','QA is blocked with a missing draft-pack reference or any unchecked QA item; a fully valid, QA’d curriculum can be locked, but the stage still requires manager completion to hand off.'),
('UAT03','Instructor setup stays incomplete if the selected instructor was never evaluated, or if fee approval, contract reference, or onboarding reference is missing; each condition blocks independently.'),
('UAT04','Launch No Go without a reason is rejected; a valid Go activates only the commercial routes applicable to the program’s route.'),
('UAT05','Inconsistent B2C counts and incomplete B2B contract references are both rejected; each operational lane stays incomplete until its data, one interaction, and zero open follow-ups are all true; Finance stays locked until all four lanes are supervisor-approved.'),
('UAT06','Stage 4 manager completion is blocked without both Finance sub-sections closed; readiness Go/Conditional Go is blocked with any unchecked readiness item; readiness No-Go creates corrective work and flips the program to On Hold.'),
('UAT07','Delivery completion is blocked by any incomplete session or unresolved incident; closing an incident’s linked assignment resolves it; assessment rejects invalid pass counts, certificate counts, feedback range, or missing evidence.'),
('UAT08','Graduate-outcome funnel counts that increase down the funnel are rejected; an open improvement action blocks Stage 7 completion; Final Closure requires all prior-stage completion plus financial closure plus lessons learned.'),
('UAT09','A non-manager Position cannot reach Manager Dashboard, Team Members, or Administration by any navigation path, including direct links.'),
('UAT10','Completing an eligible linked assignment from Tasks updates its source record but never independently advances a lifecycle stage.'),
('UAT11','Editing a delivery session’s date, time, or status in Stage 5 is reflected in Schedule; Completed/Cancelled sessions are excluded from Planned-only scope.'),
('UAT12','An instructor-import preview correctly separates new, matching, and error rows before commit; merge preserves existing names untouched.'),
('UAT13','Saving a visit as Completed without an outcome is rejected; a follow-up date before the visit date is rejected; operational interaction history remains distinguishable from networking visits.'),
('UAT14','A visit can be marked Completed while its follow-up remains open; completing the follow-up removes it from Plan without deleting the visit.'),
('UAT15','Training-mode steps never mutate a real program; a restored backup lands in an isolated environment and preserves record relationships.'),
],[.75,6.05],9.3)

page(26,'Open decisions')
p('Unresolved questions that shape scope regardless of platform choice. Flag these to the business owner before or during build rather than assuming an answer.')
table(['Decision','Ask'],[
('Who can view, edit, export, archive, or delete contact and finance records in production?','Academy leadership / IT owner'),
('Should Plan include personal tasks and independent activity deadlines, beyond the current program/visit sources?','Academy Manager / Operations Supervisor'),
('Should task recurrence actually generate repeating instances?','Academy Manager'),
('Should legacy operational-interaction targets be linkable to reusable contacts, and how are duplicate contacts merged?','Operations / Partnerships owners'),
('Should a networking follow-up create an assigned task or reminder the way an operational follow-up does?','Academy Manager / workflow owners'),
('Is actual document file storage required, or is a reference/metadata register sufficient?','IT owner'),
('What record volumes, response-time targets, retention period, and backup/restore objectives are required?','Business owner / IT owner'),
('Is calendar sync (Outlook/Teams) or automated email/SMS notification required for this build?','Academy Manager / IT owner'),
],[4.65,2.15],9.3)

doc.core_properties.title='Andalusia Academy Work Management System Functional Requirements'
doc.core_properties.subject='Technology-agnostic functional requirements for engineering handoff'
doc.core_properties.author='Andalusia Academy'
doc.core_properties.keywords='Andalusia Academy, WMS, requirements, Power Apps'
doc.core_properties.version='1.0'
OUT.parent.mkdir(exist_ok=True)
doc.save(OUT)
print(OUT)
