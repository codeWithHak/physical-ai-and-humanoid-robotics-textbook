# Feature Specification: Refactor Chapter 1: Modular File Structure

**Feature Branch**: `007-refactor-chapter-1-modular-structure`  
**Created**: 2025-12-04  
**Status**: Draft  
**Input**: User description: "Refactor Chapter 1: Modular File Structure Intent: Refactor the existing monolithic "Chapter 1" content into a modular Docusaurus folder structure. This improves navigation and maintainability by treating each major section as a distinct page within the "Chapter 1" category. Feature Scope (File Architecture): 1. Directory Structure: - Create directory: `docs/chapter-01-foundations/`. - Create Sidebar Config: `docs/chapter-01-foundations/_category_.json` with label "Chapter 1: Embodied Intelligence" and `collapsible: true`. 2. Content Splitting (Migrate existing text): - `01-great-transition.mdx`: Contains Section 1.1 (Moravec's Paradox, etc.). - `02-triad-architecture.mdx`: Contains Section 1.2 (Human->AI->Robot diagram). - `03-hardware-nervous-system.mdx`: Contains Section 1.3 (Workstations/Edge Kits). *MUST include the <HardwareCheck /> import.* - `04-senses-of-the-machine.mdx`: Contains Section 1.4 (Sensors). 3. Cleanup: - Delete the original monolithic file. Success Criteria (SMART): - Sidebar Navigation: "Chapter 1" appears as a folder in the left sidebar. Clicking it reveals the 4 sub-pages. - Component Integrity: The `<HardwareCheck />` component still functions correctly inside the new `03-hardware-nervous-system.mdx` file. - Link Integrity: Previous citations/links are preserved. Non-Goals: - NOT rewriting the text (just moving it). - NOT changing the visual design. User Stories: - "As a reader, I prefer reading short, focused pages rather than scrolling through one giant wall of text.""

## Clarifications

### Session 2025-12-04
- Q: How should file ordering be enforced within the new category? → A: Use `sidebar_position` frontmatter in each MDX file.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Focused Reading Experience (Priority: P1)

As a reader, I prefer reading short, focused pages rather than scrolling through one giant wall of text, so that I can maintain focus and easily track my progress through the chapter.

**Why this priority**: Improves readability and cognitive load for complex technical topics.

**Independent Test**: Open the documentation sidebar and verify "Chapter 1: Embodied Intelligence" is a folder containing 4 distinct sub-pages. Click each page and verify it loads only the relevant section content.

**Acceptance Scenarios**:

1. **Given** the sidebar, **When** I expand "Chapter 1: Embodied Intelligence", **Then** I see "1.1 The Great Transition", "1.2 The Triad Architecture", "1.3 The Hardware Nervous System", and "1.4 Senses of the Machine" as child links.
2. **Given** I click "1.3 The Hardware Nervous System", **When** the page loads, **Then** I see the Hardware Check component and *only* the hardware-related text.

---

### User Story 2 - Component Persistence (Priority: P1)

As a student, I want the interactive Hardware Check to function exactly as it did before the refactor, so I can still validate my GPU setup.

**Why this priority**: Regression testing. Moving files often breaks relative import paths for components.

**Independent Test**: Navigate to the new `03-hardware-nervous-system` page and interact with the Hardware Validator.

**Acceptance Scenarios**:

1. **Given** the "Hardware Nervous System" page, **When** I use the `<HardwareCheck />` dropdown, **Then** it correctly validates my selection (Green/Red logic works).
2. **Given** the page source, **When** I verify the import path, **Then** it points correctly to `@site/src/components/HardwareCheck`.

### Edge Cases

- **Broken Relative Links**: If the original content linked to "Section 1.2" via anchor tags (`#section-12`), these links must now point to the new file (`./02-triad-architecture.mdx`).
- **Broken Image Paths**: If diagrams or images were referenced relatively, their paths must be updated to account for the new directory depth (though mostly using Mermaid/Components here).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST organize Chapter 1 content into a subdirectory `docs/chapter-01-foundations/`.
- **FR-002**: The directory MUST contain a `_category_.json` file configuring the sidebar label as "Chapter 1: Embodied Intelligence" and enabling collapsibility.
- **FR-003**: The monolithic content from `docs/01-chapter-1.mdx` MUST be split into four separate MDX files: `01-great-transition.mdx`, `02-triad-architecture.mdx`, `03-hardware-nervous-system.mdx`, `04-senses-of-the-machine.mdx`.
- **FR-004**: The `03-hardware-nervous-system.mdx` file MUST import and render the `<HardwareCheck />` component.
- **FR-005**: The `02-triad-architecture.mdx` file MUST contain the Triad Mermaid diagram.
- **FR-006**: The original file `docs/01-chapter-1.mdx` MUST be deleted to prevent duplication.
- **FR-007**: Sidebar ordering MUST follow the file numbering (01, 02, 03, 04) by adding `sidebar_position: [1-4]` to each file's frontmatter.

### Key Entities *(include if feature involves data)*

*None (File Structure Refactor)*

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Navigation Structure**: The sidebar renders a collapsible group for Chapter 1 with 4 children.
- **SC-002**: **No Broken Imports**: The build process (`npm run build`) completes with zero errors regarding missing components or modules.
- **SC-003**: **Content Parity**: The total word count across the 4 new files equals the word count of the original monolithic file (minus headers).
- **SC-004**: **Interactive Integrity**: The Hardware Check component renders and functions on the new page.