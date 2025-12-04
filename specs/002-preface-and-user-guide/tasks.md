---
description: >
  Break down the plan into small, testable tasks for implementation.
  Each task must be an atomic step (setup -> config -> implementation -> verify).
---

# Checklist: Preface and User Guide

## Phase 1: Setup (Project Initialization)
- [x] T001 Verify Docusaurus Environment in `frontend/`
  - **Description**: Ensure the frontend directory is ready for content creation.
  - **Context**: Prerequisite for adding new docs.
  - **Steps**:
    - Verify `frontend/docusaurus.config.ts` exists.
    - Verify `frontend/docs` directory exists.
  - **Test**: `test -d frontend/docs` returns 0.

## Phase 2: Foundational Tasks (Prerequisites)
- [x] T002 [US1] Create Preface File `frontend/docs/00-preface.md`
  - **Description**: Create the initial markdown file with frontmatter.
  - **Context**: Sets up the file and sidebar position (SC-004).
  - **Steps**:
    - Create `frontend/docs/00-preface.md`.
    - Add frontmatter: `slug: /`, `title: Preface`, `sidebar_position: 0`.
  - **Test**: File exists and contains `sidebar_position: 0`.

## Phase 3: User Story 1 - Hardware Assessment (P1)
**Goal**: Warn users about strict hardware requirements (FR-003, FR-004).

- [x] T003 [US1] Implement Hardware Reality Check in `frontend/docs/00-preface.md`
  - **Description**: Add the "Hardware Reality Check" section with a danger admonition.
  - **Context**: Critical warning for users (SC-001, SC-002).
  - **Steps**:
    - Add `:::danger Hardware Reality Check` block.
    - Inside block, add "Digital Twin Workstation" specs (RTX 4070 Ti+, 64GB RAM, Ubuntu 22.04).
    - Inside block, add "Physical AI Edge Kit" specs (Jetson Orin Nano, RealSense Camera).
    - Inside block, add "Cloud Alternative" (AWS g5.2xlarge).
  - **Test**: `grep "RTX 4070 Ti+" frontend/docs/00-preface.md` returns match.

## Phase 4: User Story 2 - Course Commitment Understanding (P2)
**Goal**: Set expectations for time and duration (FR-005).

- [x] T004 [US2] Implement Learning Path & Time in `frontend/docs/00-preface.md`
  - **Description**: Add the "Learning Path & Time" section.
  - **Context**: FR-005.
  - **Steps**:
    - Add section header `## Learning Path & Time`.
    - Add text stating "13-week structure".
    - Add text stating "~10 hours/week of effort".
  - **Test**: `grep "13-week" frontend/docs/00-preface.md` returns match.

## Phase 5: User Story 3 - Feature Onboarding (P3)
**Goal**: Explain unique platform features (FR-006).

- [x] T005 [US3] Implement Interactive Features & Target Audience in `frontend/docs/00-preface.md`
  - **Description**: Add "Who This Is For" and "Interactive Features" sections.
  - **Context**: FR-002, FR-006.
  - **Steps**:
    - Add section `## Who This Is For` targeting founders/engineers.
    - Add section `## Interactive Features`.
    - Describe "Urdu Translation" toggle.
    - Describe "Ask the Book" RAG chatbot.
  - **Test**: `grep "Urdu Translation" frontend/docs/00-preface.md` returns match.

## Phase 6: Polish & Cross-Cutting Concerns
- [x] T006 Implement Readiness Checklist & Navigation in `frontend/docs/00-preface.md`
  - **Description**: Add the final checklist and link to Chapter 1.
  - **Context**: FR-007, FR-008.
  - **Steps**:
    - Add `## Readiness Checklist` with checkboxes.
    - Add link `[Start Chapter 1](./intro.md)` (or appropriate path).
  - **Test**: `grep "Readiness Checklist" frontend/docs/00-preface.md` returns match.

## Dependencies
- **US1, US2, US3** depend on **Phase 2 (File Creation)**.
- **Phase 6** depends on **US1, US2, US3**.

## Implementation Strategy
1. **Skeleton**: Create the file with frontmatter.
2. **Critical Content**: Add Hardware Warning (US1).
3. **Informational Content**: Add Learning Path and Features (US2, US3).
4. **Polish**: Add Checklist and Navigation.
