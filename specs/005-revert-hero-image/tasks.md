---
description: >
  Break down the plan into small, testable tasks for implementation.
  Each task must be an atomic step (setup -> config -> implementation -> verify).
---

# Checklist: Revert Hero Image

## Phase 1: Component Restoration
- [x] T001 Revert `src/pages/index.tsx` Image
  - **Description**: Replace `RobotBody` with the static SVG image.
  - **Context**: FR-001, FR-002.
  - **Steps**:
    - Remove `import RobotBody` from `frontend/src/pages/index.tsx`.
    - Inside `div.heroVisual`, replace `<RobotBody />` with the `<img>` tag for `undraw_docusaurus_mountain.svg`.
    - Ensure proper className (`diagramImage` and container styling) is preserved.
  - **Test**: `grep "undraw_docusaurus_mountain.svg" frontend/src/pages/index.tsx` returns match.

- [x] T002 [US2] Cleanup Unused Component
  - **Description**: Delete the `RobotBody` component files.
  - **Context**: P2 Code Cleanup.
  - **Steps**:
    - Remove directory `frontend/src/components/RobotBody/`.
  - **Test**: `test -d frontend/src/components/RobotBody` returns 1 (false).

## Phase 2: Verification
- [ ] T003 Verify Revert Success
  - **Description**: Ensure visual layout is restored.
  - **Steps**:
    - Check SC-001 (Visual layout).
    - Check SC-002 (Build success).

## Dependencies
- **T002** depends on **T001**.

## Implementation Strategy
1. **Swap**: Change `index.tsx` first to ensure the site renders.
2. **Cleanup**: Remove the unused component code.