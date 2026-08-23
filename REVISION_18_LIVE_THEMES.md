# Revision 18 — Live Themes

Revision 18 restores and strengthens live theme switching on top of the Revision 17 Clear & Informative UI.

## Theme choices

- Terracotta
- Ocean
- Forest
- Plum
- Midnight
- Sandstone
- Rose

## Where themes can be changed

- A new **Theme** control is available in the fixed sidebar, above the employee profile and above the bottom Hide Sidebar control.
- Desktop retains the top-bar theme selector.
- Mobile keeps a 44 px theme control in the top bar; the native selector is placed over the icon so it remains touch-friendly.
- Profile retains Application Theme and now supports direct theme-swatch selection.
- Registration retains the Application Theme field for first-time setup.

## What changes with the theme

The selected theme now drives both the older application tokens and the Revision 17 clear-UI tokens. This includes:

- sidebar gradient and glow
- active navigation state
- application/background tint
- surface and card border colors
- primary buttons and links
- table headers and soft panels
- Program lifecycle selection states
- entity avatars and stage chips
- progress accents
- focus/highlight states

Semantic colors remain semantic: completed/success stays green, attention stays amber, and blocked/overdue stays red.

## Persistence

Theme choices are saved in local storage immediately and are also written into the employee profile when a user is registered, so the selected theme is restored on later launches.

## Reliability fix

An older implementation registered profile-image event handlers from inside `applyTheme()`. Repeated theme changes could therefore duplicate those handlers. Revision 18 moves those handlers out of the theme function and registers them exactly once.

## SVG system

A reusable `palette` icon was added to the existing SVG sprite and as `static/icons/palette.svg`.
