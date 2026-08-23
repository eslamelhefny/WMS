# Revision 20.1 — Program Stage Flow UI/UX Fix

## Scope

Focused correction of `id="programStageFlow"` in the Program Workspace.

## Problems identified

The previous lifecycle strip had several design/UX problems:

- multiple historical `.stage-flow` / `.stage-node` CSS definitions competed with one another;
- the final override compressed eight real Academy stages into a very small horizontal strip;
- stage names and states were too small to scan comfortably;
- selected stage and actual current stage used the same visual treatment, which could mislead the user after clicking another stage;
- the stage progress indicator was visually weak and could be hidden by older overrides;
- the component did not give the manager a concise lifecycle summary before the eight stages;
- tablet/phone behavior depended too heavily on horizontal scrolling.

## New design

`programStageFlow` is now a scoped lifecycle component with:

- Program Lifecycle header;
- explicit current stage;
- completed-stage count (`x of 8 stages completed`);
- overall readiness and progress bar;
- eight readable stage steps;
- separate visual states for Completed, Current, Selected, Pending Approval, Returned, and Upcoming;
- per-stage progress percentage and progress bar;
- semantic stage icons plus visible stage numbers;
- full stage name retained in tooltip and accessible label;
- `aria-current="step"` for the actual current lifecycle stage;
- `aria-pressed` for the stage the user is inspecting.

## Responsive behavior

- Desktop / laptop / tablet landscape: horizontal lifecycle stepper.
- Phone and tablet portrait (<= 820 px): vertical lifecycle timeline.
- No document-level horizontal overflow is introduced.
- Stage rows on touch layouts are 72 px high, comfortably above the 44 px touch target minimum.

## Interaction behavior

Clicking a stage still opens that stage's details and evidence. The selected stage is highlighted independently from the actual current stage, so browsing an upcoming/completed stage no longer makes it appear to be the Program's current stage.

## Theme behavior

The redesign uses the existing application theme variables (`--app-accent`, surfaces, borders, semantic green/red/amber) and therefore continues to work with Terracotta, Ocean, Forest, Plum, Midnight, Sandstone, and Rose themes.

## Validation

- Python syntax: passed.
- JavaScript syntax (`node --check`): passed.
- Component tested at 390, 430, 768, 1024, 1366, 1440, and 1920 px widths.
- Root horizontal overflow in component audit: 0 at every tested width.
- 390/430/768 portrait lifecycle uses vertical timeline.
- 1024+ lifecycle uses horizontal stepper.
- Clean data baseline restored before packaging: no user, Programs, tasks, assignments, or documents.
