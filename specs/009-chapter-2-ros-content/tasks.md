# Task List: Chapter 2 Content - The Robotic Nervous System

**Feature**: Chapter 2 Content - The Robotic Nervous System
**Spec**: [spec.md](spec.md)
**Version**: 1.0

This task list is structured to ensure that each user story from the specification is addressed and independently testable.

---

## Phase 1: Setup

- [x] T001 Create directory `frontend/docs/chapter-02-robotic-nervous-system/`.
- [x] T002 Create file `frontend/docs/chapter-02-robotic-nervous-system/_category_.json`.
- [x] T003 Create directory `frontend/src/components/RosTerminal/`.
- [x] T004 Create file `frontend/src/components/RosTerminal/index.tsx`.
- [x] T005 Create file `frontend/src/components/RosTerminal/styles.module.css`.
- [x] T006 Create directory `frontend/src/components/ConceptCard/`.
- [x] T007 Create file `frontend/src/components/ConceptCard/index.tsx`.
- [x] T008 Create file `frontend/src/components/ConceptCard/styles.module.css`.

---

## Phase 2: User Story 1 - Interactive ROS Terminal

**Goal**: As a student, I want to try typing a ROS command right in the browser to build muscle memory before I install Linux.
**Independent Test**: The `<RosTerminal />` component can be developed and tested in isolation. It requires no backend and can be validated by checking if the simulated input correctly produces the expected mock output.

- [x] T009 [US1] Implement the `<RosTerminal />` React component in `frontend/src/components/RosTerminal/index.tsx`, including basic UI and logic for simulating ROS commands.
- [x] T010 [US1] Implement "Auto-Type" buttons for supported commands as separate, labeled buttons displayed next to or below the terminal input in `frontend/src/components/RosTerminal/index.tsx`.
- [x] T011 [US1] Create file `frontend/docs/chapter-02-robotic-nervous-system/01-why-middleware.mdx` and add an instance of the `<RosTerminal />` component.

---

## Phase 3: User Story 2 - Conceptual Understanding for AI Engineers

**Goal**: As an AI engineer, I want to see exactly how Python code injects data into the robot's nervous system, with clear analogies and diagrams.
**Independent Test**: The four content sections (2.1-2.4) and the `<ConceptCard />` can be written and reviewed independently. The test is to ensure the content is technically accurate, easy to understand for an AI expert, and meets the specified word count and citation requirements.

- [x] T012 [US2] Implement the `<ConceptCard />` React component in `frontend/src/components/ConceptCard/index.tsx`, including logic to toggle between conceptual and technical views.
- [x] T013 [US2] Write content for Section 2.1 "Why Middleware? (The 'Nervous System' Analogy)" in `frontend/docs/chapter-02-robotic-nervous-system/01-why-middleware.mdx`.
- [x] T014 [US2] Write content for Section 2.2 "The Atomic Unit (Nodes & Graphs)" in `frontend/docs/chapter-02-robotic-nervous-system/02-atomic-unit.mdx`.
- [x] T015 [US2] Add at least one Mermaid Diagram illustrating a ROS 2 node graph in `frontend/docs/chapter-02-robotic-nervous-system/02-atomic-unit.mdx`.
- [x] T016 [US2] Write content for Section 2.3 "The Python Bridge (`rclpy`)" in `frontend/docs/chapter-02-robotic-nervous-system/03-python-bridge.mdx`.
- [x] T017 [US2] Include a minimal Python Publisher node code example in `frontend/docs/chapter-02-robotic-nervous-system/03-python-bridge.mdx`.
- [x] T018 [US2] Write content for Section 2.4 "Workspace Hygiene" in `frontend/docs/chapter-02-robotic-nervous-system/04-workspace-hygiene.mdx`.
- [x] T019 [US2] Add an instance of the `<ConceptCard />` component in a relevant content section (e.g., `frontend/docs/chapter-02-robotic-nervous-system/02-atomic-unit.mdx`).

---

## Phase 4: Polish & Cross-Cutting Concerns

- [x] T020 Validate total word count for Chapter 2 content sections is >= 2,500 words.
- [x] T021 Validate content explicitly states that ROS 2 nodes run on Edge Kit (Jetson) and visualization tools on Workstation.
- [x] T022 Validate 8-10 IEEE-formatted citations are present across Chapter 2 content.
- [x] T023 Validate content focuses exclusively on Python (`rclpy`) and not C++ (`rclcpp`).
- [x] T024 Perform a final review of Chapter 2 content for clarity, accuracy, and adherence to Docusaurus formatting.

---

## Dependencies

- **Phase 1 (Setup)** must be completed before **Phase 2 (US1)** and **Phase 3 (US2)**.
- **Phase 2 (US1)** and **Phase 3 (US2)** can be developed in parallel after Phase 1.
- **Phase 4 (Polish)** requires completion of **Phase 2** and **Phase 3**.

## Parallel Execution Examples

- After setup, one developer can work on the `<RosTerminal />` component and its integration into `01-why-middleware.mdx` (Phase 2), while another works on writing initial content for Sections 2.1-2.4 and implementing the `<ConceptCard />` (Phase 3).
- Within Phase 3, multiple content sections can be written concurrently by different team members.

## Implementation Strategy

The implementation will begin with setting up the necessary directory structure and component files. Following this, the development of the interactive `<RosTerminal />` component and the core content sections will proceed in parallel, enabling rapid iteration on the user experience and technical explanations. A final polish phase will ensure all success criteria and cross-cutting concerns are met.
