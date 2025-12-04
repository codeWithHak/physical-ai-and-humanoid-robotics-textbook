---
id: 0001
title: Spec Creation - Revert Hero Image
stage: spec
date: 2025-12-04
surface: agent
model: gemini
feature: 005-revert-hero-image
branch: 005-revert-hero-image
user: codeWithHak
command: /sp.specify
labels: ["spec", "revert", "frontend"]
links:
  spec: specs/005-revert-hero-image/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-revert-hero-image/spec.md
 - specs/005-revert-hero-image/checklists/requirements.md
tests:
---

## Prompt

can we rewert back and use the image in hero section as we wer usig before

## Response snapshot

Created spec `specs/005-revert-hero-image/spec.md`.
- **Intent**: Revert landing page visual to static SVG.
- **Requirements**: Restore `undraw_docusaurus_mountain.svg`, remove `RobotBody` usage.
- **Success Criteria**: Visual match with original design.

Created checklist.

## Outcome

- ✅ Impact: Defined revert operation requirements.
- 🧪 Tests: N/A
- 📁 Files: spec.md, requirements.md created.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: Simple revert request handled as a formal feature to maintain process discipline.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A