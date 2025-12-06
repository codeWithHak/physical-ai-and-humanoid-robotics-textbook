# Task List: Refine Chapter 1 Content & Hierarchy

**Feature**: Refine Chapter 1 Content & Hierarchy
**Spec**: [spec.md](spec.md)
**Version**: 1.0

This task list is structured to ensure that each user story from the specification is addressed and independently testable.

---

## Phase 1: Setup

*No setup tasks are required for this content-focused feature. The existing Docusaurus structure will be used.*

---

## Phase 2: User Story 1 - Content Depth and Structure

**Goal**: As a reader, I want to read in-depth technical explanations with clear hierarchical headings (H1 -> H2 -> H3) so I can understand the nuance of topics without getting lost in repetitive titles.
**Independent Test**: Open each of the 4 files. Verify H1 is unique. Verify H2s are distinct concepts. Check word count is significantly increased.

- [x] T001 [US1] Overwrite content in `frontend/docs/chapter-01-foundations/01-great-transition.mdx` with ~800 words detailing "Beyond the Screen", "Moravec's Paradox", and "The Physics Barrier".
- [x] T002 [US1] Overwrite content in `frontend/docs/chapter-01-foundations/02-triad-architecture.mdx` with ~800 words detailing "Human Commander", "Artificial Brain", and "Mechanical Body".
- [x] T003 [US1] Overwrite content in `frontend/docs/chapter-01-foundations/03-hardware-nervous-system.mdx` with ~1,000 words detailing "Digital Twin Workstation" and "Edge Brain", focusing on VRAM bottlenecks.
- [x] T004 [US1] Overwrite content in `frontend/docs/chapter-01-foundations/04-senses-of-the-machine.mdx` with ~800 words detailing "Visual (RGB-D)", "Vestibular (IMU)", and "Auditory (Whisper)" perception.

---

## Phase 3: User Story 2 - Component and Citation Preservation

**Goal**: As a student, I want the interactive Hardware Check and the citation system to remain functional after the content rewrite, so I don't lose access to tools and references.
**Independent Test**: Navigate to `03-hardware-nervous-system.mdx` and use the validator. Navigate to any page and check citation links `[1]` and the `## References` section.

- [x] T005 [US2] Verify that the `<HardwareCheck />` component is present and its import statement exists in `frontend/docs/chapter-01-foundations/03-hardware-nervous-system.mdx`.
- [x] T006 [P] [US2] Verify that `<TermTooltip />` components are used and their import statements exist in all 4 chapter files.
- [x] T007 [P] [US2] Verify that the Mermaid diagram and its import statement are present in `frontend/docs/chapter-01-foundations/02-triad-architecture.mdx`.
- [x] T008 [P] [US2] Verify that a `## References` section exists and is correctly formatted in all 4 chapter files.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Goal**: Ensure the final output meets all success criteria defined in the specification.
**Independent Test**: Perform a final review of all 4 files together.

- [x] T009 Validate total word count for all 4 files in `frontend/docs/chapter-01-foundations/` is > 3,000.
- [x] T010 [P] Manually review all 4 files to confirm no H2 titles are duplicates of H1 titles.
- [x] T011 [P] Manually review all 4 files to confirm at least 3 Docusaurus Admonitions (`:::info`, `:::warning`) are used across the chapter.
- [x] T012 [P] Manually check for any broken internal links (if any were added).

---

## Dependencies

- **Phase 2 (US1)** must be completed before **Phase 3 (US2)** and **Phase 4 (Polish)** can begin.
- Tasks within Phase 3 can be run in parallel.
- Tasks within Phase 4 can be run in parallel.

## Parallel Execution Examples

- **During Phase 3**: While one person verifies the `<HardwareCheck>` component (`T005`), another can simultaneously check for `<TermTooltip>` usage (`T006`) and reference sections (`T008`).
- **During Phase 4**: Word count validation (`T009`) can happen at the same time as the manual hierarchy review (`T010`).

## Implementation Strategy

The implementation will proceed by completing all tasks in Phase 2 first, which involves replacing the content of the four MDX files. Once the new content is in place, Phase 3 and Phase 4 tasks will be executed to verify that all components, formatting, and cross-cutting requirements have been met. This ensures the core content is delivered first, followed by validation.
