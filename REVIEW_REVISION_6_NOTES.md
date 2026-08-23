# Prototype V5 — Review Revision 6 Notes

Revision 6 focuses the Academy Manager workspace on the two decisions that need the clearest daily attention: Launch Planning and Academy Crew Tasks.

## Manager dashboard presentation

- Launch Planning is a compact decision card instead of a wide table.
- Academy Crew Tasks is a compact crew-control card beside Launch Planning on desktop displays.
- Each card initially shows exactly five records.
- Each card has an independent **See All / Show 5** button.
- Each list uses a bounded internal scroll area so the rest of the dashboard remains reachable.
- Launch items surface Month, Priority, Go / No Go status, Program, specialty, level, audience, date, estimated fee, P&L, minimum/plan readiness, reason, and direct actions.
- Crew items surface task, Program, Position, status, stage, due date, priority, assigning manager, and direct access.
- Crew assignment is collapsed by default and opens from **Assign Task**.

## Display support

- Two-column command layout on 1920×1080 and 1280×720 displays.
- More compact top spacing, hero area, and manager lists on screens up to 760 pixels high.
- No horizontal page overflow at either validated display size.
- Manager cards stack on narrower desktop/tablet widths below the 1180-pixel breakpoint.

## Personal work navigation

- **My Work** is removed from the desktop sidebar, mobile navigation, dashboard actions, Profile default-view choices, and Position-rule module display.
- **My Tasks** is the one personal-work destination.
- A legacy `mywork` saved default or internal route is redirected to **My Tasks** so existing local profiles remain usable.

## Academy Manager authority

- Academy Manager can create a Program.
- Academy Manager can fill and submit the Program request, approve Greenlight, and continue into Curriculum.
- Academy Manager retains full fill, submit, review, and completion authority across all eight stages.
- Specialist ownership labels, field validation, approval gates, and lifecycle sequence remain visible and enforced.
