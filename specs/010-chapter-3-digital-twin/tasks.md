# Task List: Chapter 3 Content - The Digital Twin

**Feature**: Chapter 3 Content - The Digital Twin
**Spec**: [spec.md](spec.md)
**Version**: 1.0

This task list is structured to ensure that each user story from the specification is addressed and independently testable.

---

## Phase 1: Setup

- [x] T001 Create directory `frontend/docs/chapter-03-digital-twin/`.
- [x] T002 Create file `frontend/docs/chapter-03-digital-twin/_category_.json`.
- [x] T003 Create directory `frontend/src/components/UrdfExplorer/`.
- [x] T004 Create file `frontend/src/components/UrdfExplorer/index.tsx`.
- [x] T005 Create file `frontend/src/components/UrdfExplorer/styles.module.css`.

---

## Phase 2: User Story 1 - Interactive Kinematics Learning

**Goal**: As a student, I finally understand how an XML file defines a physical robot arm by playing with the interactive explorer.
**Independent Test**: The `<UrdfExplorer />` component can be tested in isolation. Verify that hovering over XML tags correctly highlights the corresponding SVG elements.

- [x] T006 [US1] Implement the `<UrdfExplorer />` component in `frontend/src/components/UrdfExplorer/index.tsx`, creating a split-view layout with code on the left and a placeholder for the diagram on the right.
- [x] T007 [US1] Implement the SVG robot arm schematic within `<UrdfExplorer />` or as a separate asset.
- [x] T008 [US1] Implement hover logic in `<UrdfExplorer />` to highlight the SVG elements when hovering over specific XML tags (links and joints) in the hardcoded snippet.
- [x] T009 [US1] Add an instance of the `<UrdfExplorer />` component to `frontend/docs/chapter-03-digital-twin/02-defining-body.mdx` (file creation in next phase).

---

## Phase 3: User Story 2 - Understanding Simulation Constraints

**Goal**: As a developer, I understand why my simulation runs slow if I don't have a strong CPU.
**Independent Test**: Review the content in Section 3.3. Verify it explicitly explains the physics engine's reliance on CPU and differentiates it from rendering (GPU).

- [x] T010 [US2] Write content for Section 3.1 "The Mirror World" in `frontend/docs/chapter-03-digital-twin/01-mirror-world.mdx`, covering the Sim-to-Real gap.
- [x] T011 [US2] Write content for Section 3.2 "Defining the Body (URDF & SDF)" in `frontend/docs/chapter-03-digital-twin/02-defining-body.mdx`, explaining XML structure and differences.
- [x] T012 [US2] Write content for Section 3.3 "The Laws of Physics (Gazebo)" in `frontend/docs/chapter-03-digital-twin/03-laws-of-physics.mdx`, explaining rigid body dynamics and CPU bottlenecks.
- [x] T013 [US2] Write content for Section 3.4 "Visualizing Reality (Unity & Isaac)" in `frontend/docs/chapter-03-digital-twin/04-visualizing-reality.mdx`.
- [x] T014 [US2] Create a Mermaid diagram showing the "Simulation Loop" (Physics Step -> Sensor Update -> Controller Update) in `frontend/docs/chapter-03-digital-twin/03-laws-of-physics.mdx`.

---

## Phase 4: Polish & Cross-Cutting Concerns

- [x] T015 Validate total word count for Chapter 3 content sections is >= 2,500 words.
- [x] T016 Validate content explicitly warns about RTX 4070 Ti+ requirement for multiple sensors.
- [x] T017 Validate 8-10 IEEE-formatted citations are present across Chapter 3 content.
- [x] T018 Perform a final review of Chapter 3 content for clarity, accuracy, and adherence to Docusaurus formatting.

---

## Dependencies

- **Phase 1 (Setup)** must be completed before **Phase 2 (US1)** and **Phase 3 (US2)**.
- **Phase 2 (US1)** and **Phase 3 (US2)** can be developed in parallel after Phase 1.
- **Phase 4 (Polish)** requires completion of **Phase 2** and **Phase 3**.

## Parallel Execution Examples

- After setup, one developer can focus on the `<UrdfExplorer />` component (Phase 2), while another writes the content sections (Phase 3).
- Within Phase 3, multiple content sections can be written concurrently.

## Implementation Strategy

The implementation will start with the basic file and directory setup. Then, we will proceed with building the interactive `<UrdfExplorer />` component to visualize URDF concepts. Concurrently, we will draft the four content sections, ensuring the technical explanations are accurate and the diagrams are correctly integrated. Finally, we will review the word count and citations to meet the success criteria.