---
description: >
  Break down the plan into small, testable tasks for implementation.
  Each task must be an atomic step (setup -> config -> implementation -> verify).
---

# Checklist: Refactor Chapter 1 Modular Structure

## Phase 1: Setup & Configuration
- [x] T001 Create Chapter 1 Directory Structure
  - **Description**: Create the folder for the new modular chapter.
  - **Context**: FR-001.
  - **Steps**:
    - Create directory `frontend/docs/chapter-01-foundations/`.
  - **Test**: `test -d frontend/docs/chapter-01-foundations` returns 0.

- [x] T002 Configure Category Sidebar
  - **Description**: Add `_category_.json` for sidebar grouping.
  - **Context**: FR-002.
  - **Steps**:
    - Create `frontend/docs/chapter-01-foundations/_category_.json`.
    - Content: `{ "label": "Chapter 1: Embodied Intelligence", "position": 1, "collapsible": true }`.
  - **Test**: `grep "Embodied Intelligence" frontend/docs/chapter-01-foundations/_category_.json` returns match.

## Phase 2: Content Migration
- [x] T003 Migrate Section 1.1 (The Great Transition)
  - **Description**: Extract Moravec's Paradox content.
  - **Context**: FR-003, FR-007.
  - **Steps**:
    - Read `frontend/docs/01-chapter-1.mdx`.
    - Extract Section 1.1 content.
    - Write to `frontend/docs/chapter-01-foundations/01-great-transition.mdx`.
    - Add frontmatter: `sidebar_position: 1`.
  - **Test**: File exists with correct content.

- [x] T004 Migrate Section 1.2 (Triad Architecture)
  - **Description**: Extract Triad content and Diagram.
  - **Context**: FR-003, FR-005.
  - **Steps**:
    - Read `frontend/docs/01-chapter-1.mdx`.
    - Extract Section 1.2 content and Mermaid block.
    - Write to `frontend/docs/chapter-01-foundations/02-triad-architecture.mdx`.
    - Add frontmatter: `sidebar_position: 2`.
  - **Test**: `grep "mermaid" frontend/docs/chapter-01-foundations/02-triad-architecture.mdx` returns match.

- [x] T005 Migrate Section 1.3 (Hardware Nervous System)
  - **Description**: Extract Hardware content and Component.
  - **Context**: FR-003, FR-004.
  - **Steps**:
    - Read `frontend/docs/01-chapter-1.mdx`.
    - Extract Section 1.3 content.
    - Write to `frontend/docs/chapter-01-foundations/03-hardware-nervous-system.mdx`.
    - Ensure imports: `import HardwareCheck from '@site/src/components/HardwareCheck';`.
    - Add frontmatter: `sidebar_position: 3`.
  - **Test**: `grep "HardwareCheck" frontend/docs/chapter-01-foundations/03-hardware-nervous-system.mdx` returns match.

- [x] T006 Migrate Section 1.4 (Senses of the Machine)
  - **Description**: Extract Sensors content and Tooltips.
  - **Context**: FR-003.
  - **Steps**:
    - Read `frontend/docs/01-chapter-1.mdx`.
    - Extract Section 1.4 content.
    - Write to `frontend/docs/chapter-01-foundations/04-senses-of-the-machine.mdx`.
    - Ensure imports: `import TermTooltip from '@site/src/components/TermTooltip';`.
    - Add frontmatter: `sidebar_position: 4`.
  - **Test**: `grep "TermTooltip" frontend/docs/chapter-01-foundations/04-senses-of-the-machine.mdx` returns match.

## Phase 3: Cleanup & Verification
- [x] T007 Delete Original Monolith
  - **Description**: Remove the old file to prevent duplication.
  - **Context**: FR-006.
  - **Steps**:
    - Delete `frontend/docs/01-chapter-1.mdx`.
  - **Test**: File no longer exists.

- [ ] T008 Verify Refactor
  - **Description**: Run build check.
  - **Context**: SC-002.
  - **Steps**:
    - Run `cd frontend && npm run build`.
  - **Test**: Build succeeds.

## Dependencies
- **Phase 2** depends on **Phase 1** and the existence of `01-chapter-1.mdx`.
- **T007** depends on **T003, T004, T005, T006**.

## Implementation Strategy
1.  **Setup**: Create directory structure.
2.  **Migration**: Read source, split into 4 files with correct imports/frontmatter.
3.  **Cleanup**: Delete source.