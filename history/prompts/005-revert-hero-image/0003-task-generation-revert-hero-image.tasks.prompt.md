---
id: 0003
title: Task Generation - Revert Hero Image
stage: tasks
date: 2025-12-04
surface: agent
model: gemini
feature: 005-revert-hero-image
branch: 005-revert-hero-image
user: codeWithHak
command: /sp.tasks
labels: ["tasks", "revert", "frontend"]
links:
  spec: specs/005-revert-hero-image/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-revert-hero-image/tasks.md
tests:
---

## Prompt

Generate an actionable, dependency-ordered tasks.md... [truncated for brevity]

## Response snapshot

Generated `specs/005-revert-hero-image/tasks.md`.
- **Tasks**:
  1. Revert `index.tsx` to use SVG.
  2. Delete `RobotBody` component folder.
  3. Verify build and visuals.

## Outcome

- ✅ Impact: Clean plan for reverting the visual change.
- 🧪 Tests: N/A
- 📁 Files: tasks.md created.
- 🔁 Next prompts: Execute tasks
- 🧠 Reflection: Straightforward execution.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A