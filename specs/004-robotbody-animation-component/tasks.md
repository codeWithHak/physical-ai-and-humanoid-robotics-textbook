---
description: >
  Break down the plan into small, testable tasks for implementation.
  Each task must be an atomic step (setup -> config -> implementation -> verify).
---

# Checklist: RobotBody Animation Component

## Phase 1: Setup & Structure
- [x] T001 Create Component Structure
  - **Description**: Create `src/components/RobotBody/` directory and files.
  - **Context**: FR-001.
  - **Steps**:
    - Create `frontend/src/components/RobotBody/index.tsx`.
    - Create `frontend/src/components/RobotBody/styles.module.css`.
  - **Test**: `test -f frontend/src/components/RobotBody/index.tsx` returns 0.

- [x] T002 [US1] Implement CSS Grid Layout
  - **Description**: Define the grid structure for the humanoid shape.
  - **Context**: FR-002, FR-003.
  - **Steps**:
    - In `styles.module.css`, define `.robotContainer` with `display: grid`.
    - Define grid areas: `head`, `torso`, `hips`, `lArm`, `rArm`, `lLeg`, `rLeg`.
    - Style the `.card` class with black bg and neon lime border.
  - **Test**: `grep "grid-template-areas" frontend/src/components/RobotBody/styles.module.css` returns match.

## Phase 2: User Story 1 - Visualizing the Robotic Nervous System (P1)
**Goal**: Render the schematic with static connections.

- [x] T003 [US1] Implement RobotBody Component Logic
  - **Description**: Build the React component with the grid items.
  - **Context**: FR-001, FR-002.
  - **Steps**:
    - In `index.tsx`, return a `div` with the grid items mapping to the body parts.
    - Wrap the return in `<BrowserOnly>` (FR-001).
  - **Test**: `grep "BrowserOnly" frontend/src/components/RobotBody/index.tsx` returns match.

- [x] T004 [US1] Add SVG Connections Overlay
  - **Description**: Add the SVG lines behind the grid.
  - **Context**: FR-004.
  - **Steps**:
    - Add an absolute positioned `<svg>` inside the container (z-index: -1).
    - Add `<path>` elements connecting Torso to Head, Arms, Hips, Legs.
    - Style paths with neon lime stroke.
  - **Test**: `grep "<svg" frontend/src/components/RobotBody/index.tsx` returns match.

- [x] T005 [US1] Integrate Component into Landing Page
  - **Description**: Replace the old image with RobotBody.
  - **Context**: Integration constraint.
  - **Steps**:
    - Edit `frontend/src/pages/index.tsx`.
    - Import `RobotBody`.
    - Replace the `<img>` in the Hero section with `<RobotBody />`.
  - **Test**: `grep "RobotBody" frontend/src/pages/index.tsx` returns match.

## Phase 3: Animation & Polish (P1)
**Goal**: Add the "energy pulse" animation.

- [x] T006 [US1] Implement Energy Pulse Animation
  - **Description**: Add pure CSS animation for data flow.
  - **Context**: FR-005, FR-007.
  - **Steps**:
    - In `styles.module.css`, define `@keyframes pulse`.
    - Animate `stroke-dashoffset`.
    - Apply class to SVG paths.
  - **Test**: `grep "@keyframes" frontend/src/components/RobotBody/styles.module.css` returns match.

## Phase 4: User Story 2 - Responsive & Performant Design (P2)
**Goal**: Ensure mobile compatibility and performance.

- [x] T007 [US2] Implement Responsive Scaling
  - **Description**: Add media queries for mobile layout.
  - **Context**: FR-008.
  - **Steps**:
    - In `styles.module.css`, add `@media (max-width: 768px)`.
    - Adjust grid gap and cell size (scale down).
  - **Test**: `grep "@media" frontend/src/components/RobotBody/styles.module.css` returns match.

- [x] T008 [US2] Handle Reduced Motion
  - **Description**: Disable animation for accessibility.
  - **Context**: FR-006.
  - **Steps**:
    - Add `@media (prefers-reduced-motion: reduce)` block.
    - Set `animation: none` for paths.
  - **Test**: `grep "prefers-reduced-motion" frontend/src/components/RobotBody/styles.module.css` returns match.

## Phase 5: Verification
- [x] T009 Verify Success Criteria
  - **Description**: Final check.
  - **Steps**:
    - Check SC-003 (Visual Accuracy).
    - Check SC-004 (Stability/Hydration).

## Dependencies
- **Phase 2 & 3** depend on **Phase 1**.
- **T005** depends on **T003 & T004**.

## Implementation Strategy
1. **Skeleton**: Build the static Grid layout first.
2. **Integration**: Place it on the homepage to verify layout context.
3. **Visuals**: Add the SVG lines and styles.
4. **Animation**: Add the CSS keyframes last.