# Prototype V5 — Review Revision 1 Notes

This package is a separate reviewed build. The original Prototype V5 package is unchanged.

## Implemented review changes

1. Added the **Curriculum Developer** Position to employee registration, Profile, Position Rules, Administration, and Curriculum assignments.
2. Added **Academy Manager** to the Program-creation permission set. **Program Operations Executive** remains permitted to create Programs.
3. Added required Stage 2 fields: **Outline, Topic, Competences, Duration**.
4. Added required Stage 3 fields: **R/H, Project Based, Part / Full Time, Level, Assigned Groups, Internal / External**.

## Position governance retained

- Curriculum Developer can prepare and save the Stage 2 curriculum draft.
- Academy Curriculum Development Manager can also edit the draft and remains the only Position that can complete academic QA and Lock & Release.
- Existing Instructor Setup fee, Legal contract, and Operations Supervisor onboarding controls remain separated by Position.

## Compatibility

Existing V5 records are upgraded in memory with safe blank defaults for the new fields. No database migration is required because program payloads are stored as JSON within the existing SQLite/store architecture.
