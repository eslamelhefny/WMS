# Prototype V5 — Review Revision 9 Notes

Revision 9 improves workspace visibility and makes the Academy Manager's Stage 4–8 completion authority explicit while preserving the existing UI/UX, lifecycle rules, and Position ownership model.

## Sidebar show and hide

- **Hide Sidebar** collapses the navigation without changing the current view or Program stage.
- A fixed **Show sidebar** control restores the navigation.
- The selected visibility is remembered on the same device.
- When hidden, the released width is used by the main workspace, including at 1280×720.
- Both controls include accessible sidebar state and target attributes.

## Blended Andalusia identity

- The compact top-bar wordmark remains the main readable identity.
- A low-opacity Andalusia emblem is blended into the top-bar background.
- The logo treatment does not block search, theme, notifications, Today's Tasks, or add-task controls.
- The sidebar remains visually clean and contains navigation only.

## Academy Manager completion for Stages 4–8

- Active Stages 4, 5, 6, 7, and 8 display a dedicated manager validation-and-completion control.
- The control calls the existing stage completion workflow and does not skip evidence or validation.
- Stage 4 still requires Launch Go, completed Commercial routes, all four Operational Activities, supervisor approval, and both PMB and Treasury Finance controls.
- Stage 5 still requires readiness authorization, completed Delivery, resolved incidents, and valid assessment/certificate evidence.
- Stages 6 and 7 retain outcome, report, review, and improvement-action rules.
- Stage 8 retains all lifecycle prerequisite, operational closure, financial closure, open-work, and lessons-learned rules.
- Completed stages display a clear completed state instead of an active completion button.

## Combined-stage work visibility

- Assignment filtering now normalizes legacy subsection stage names into combined Stage 4 and Stage 5.
- Open-work counts and Final Closure checks use the same normalized lifecycle names.
- Academy Managers can therefore see and close the correct crew assignments from the selected combined stage.

## Validation result

- Sidebar hide, restore, and persistence passed.
- 1920×1080 and 1280×720 browser layouts passed visual review.
- Academy Manager completion passed for Stage 4 and for the full Stage 5–8 route through lifecycle completion.
