---
description: >
  Break down the plan into small, testable tasks for implementation.
  Each task must be an atomic step (setup -> config -> implementation -> verify).
---

# Checklist: Chapter 1 Content & Micro-Interactions

## Phase 1: Component Setup (Micro-Interactions)
- [x] T001 Create HardwareCheck Component Structure
  - **Description**: Create files for the GPU validator.
  - **Context**: FR-002, FR-003.
  - **Steps**:
    - Create `frontend/src/components/HardwareCheck/index.tsx`.
    - Create `frontend/src/components/HardwareCheck/styles.module.css`.
    - Create `frontend/src/components/HardwareCheck/data.json` (Static GPU list).
  - **Test**: `test -f frontend/src/components/HardwareCheck/index.tsx` returns 0.

- [x] T002 [US1] Implement HardwareCheck Logic
  - **Description**: Build the validator form and logic.
  - **Context**: FR-003.
  - **Steps**:
    - Import JSON data.
    - Add state for selected GPU and RAM.
    - Add validation logic:
        - **Red**: Non-RTX card.
        - **Yellow**: RTX card but <12GB VRAM.
        - **Green**: RTX card and >=12GB VRAM.
    - Render specific messages (Green/Red/Yellow) based on result.
  - **Test**: `grep "RTX" frontend/src/components/HardwareCheck/index.tsx` returns match.

- [x] T003 Create TermTooltip Component
  - **Description**: Create the glossary tooltip component.
  - **Context**: FR-005.
  - **Steps**:
    - Create `frontend/src/components/TermTooltip/index.tsx`.
    - Create `frontend/src/components/TermTooltip/styles.module.css`.
    - Add an internal `GLOSSARY` dictionary object.
    - Implement hover logic (simple CSS tooltip or React state).
  - **Test**: `test -f frontend/src/components/TermTooltip/index.tsx` returns 0.

## Phase 2: Content Writing (Sections 1.1 & 1.2)
- [x] T004 [US2] Write Section 1.1 & 1.2
  - **Description**: Author the first half of Chapter 1.
  - **Context**: FR-001, FR-007.
  - **Steps**:
    - Create `frontend/docs/01-chapter-1.mdx`.
    - Add frontmatter: `title: "Chapter 1: The Age of Embodied Intelligence"`.
    - Write "1.1 The Great Transition" (Moravec's Paradox).
    - Write "1.2 The Triad Architecture" (Partnership).
  - **Test**: `grep "Moravec" frontend/docs/01-chapter-1.mdx` returns match.

- [x] T005 [US2] Add Triad Mermaid Diagram
  - **Description**: Insert the architectural diagram.
  - **Context**: FR-004.
  - **Steps**:
    - Add ````mermaid` block in Section 1.2.
    - Define graph: `Human --> Agent --> Robot`.
  - **Test**: `grep "mermaid" frontend/docs/01-chapter-1.mdx` returns match.

## Phase 3: Content Writing (Sections 1.3 & 1.4)
- [x] T006 [US1] Write Section 1.3 & Hardware Integration
  - **Description**: Author Hardware section and embed validator.
  - **Context**: FR-002.
  - **Steps**:
    - Write "1.3 The Hardware Nervous System".
    - Import `HardwareCheck`.
    - Embed `<HardwareCheck />` in the MDX file.
  - **Test**: `grep "<HardwareCheck />" frontend/docs/01-chapter-1.mdx` returns match.

- [x] T007 [US3] Write Section 1.4 & Tooltips
  - **Description**: Author Senses section with tooltips.
  - **Context**: FR-005.
  - **Steps**:
    - Write "1.4 Senses of the Machine".
    - Import `TermTooltip`.
    - Wrap terms like `<TermTooltip term="SLAM">SLAM</TermTooltip>`.
  - **Test**: `grep "TermTooltip" frontend/docs/01-chapter-1.mdx` returns match.

- [x] T008 Add Hardware Topology Diagram
  - **Description**: Insert the second Mermaid diagram.
  - **Context**: FR-004.
  - **Steps**:
    - Add ````mermaid` block in Section 1.3.
    - Define topology: `Workstation --Ethernet--> Jetson`.
  - **Test**: Check file content.

## Phase 4: Verification & Polish
- [x] T009 Add Citations
  - **Description**: Ensure IEEE style references.
  - **Context**: FR-006.
  - **Steps**:
    - Add `[1]`, `[2]` markers throughout text.
    - Add `## References` section at the bottom.
  - **Test**: `grep "References" frontend/docs/01-chapter-1.mdx` returns match.

- [x] T010 Verify Content & Features
  - **Description**: Final check against success criteria.
  - **Steps**:
    - Check word count > 2500 (visual estimate/wc).
    - Verify HardwareCheck interactive logic.
    - Verify Mermaid diagrams render.

## Dependencies
- **T006** depends on **T001 & T002**.
- **T007** depends on **T003**.

## Implementation Strategy
1.  **Components First**: Build the interactive elements.
2.  **Content Second**: Write the MDX and embed components as we go.
3.  **Polish**: Diagrams and citations last.