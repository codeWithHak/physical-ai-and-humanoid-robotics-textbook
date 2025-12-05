# Feature Specification: Chapter 1 Content & Micro-Interactions

**Feature Branch**: `006-chapter-1-content-and-micro-interactions`  
**Created**: 2025-12-04  
**Status**: Draft  
**Input**: User description: "Feature: Chapter 1 Content & Micro-Interactions Intent: Write "Chapter 1: The Age of Embodied Intelligence" with integrated "Micro-Interactions." The goal is to transform passive reading into active verification, specifically regarding the strict hardware requirements. Feature Scope (Content): 1. Section 1.1: The Great Transition. Define "Physical AI" vs "Generative AI" and "Moravec's Paradox." 2. Section 1.2: The Triad Architecture. Explain the "Partnership" (Human -> Agent -> Robot). 3. Section 1.3: The Hardware Nervous System. Detailed breakdown of Workstations (RTX) and Edge Kits (Jetson). 4. Section 1.4: Senses of the Machine. Vision (RealSense), Balance (IMU), Voice (Whisper). Feature Scope (Micro-Interactions): 1. Component: `<HardwareCheck />`. A simple React component embedded in Section 1.3. - Logic: User selects their GPU (e.g., "RTX 3060", "RTX 4090", "M2 Mac") and RAM amount. - Output: Returns "Ready for Isaac Sim" (Green) or "Insufficient VRAM" (Red) based on the 12GB VRAM / RTX requirement. 2. Component: `<TermTooltip />`. A hoverable span that defines jargon (e.g., "SLAM", "URDF", "VLA") without forcing the user to leave the page. Success Criteria (SMART): - Content Depth: 2,500+ words total. - Interactive Element: The `<HardwareCheck />` is fully functional (client-side logic) and correctly identifies that non-RTX cards fail. - Visuals: 2 Mermaid Diagrams (Triad Flow, Hardware Topology). - Citations: 8-10 IEEE citations. - Formatting: Use Docusaurus Admonitions for warnings. Non-Goals: - NOT connecting the Hardware Check to a backend (keep logic local/in-browser). - NOT writing Chapter 2 yet. User Stories: - "As a student, I want to select 'MacBook Air' in the interactive tool and immediately see WHY it won't work (No RTX, No CUDA), so I stop guessing.""

## Clarifications

### Session 2025-12-04
- Q: Where should the GPU compatibility data be sourced from? → A: Static JSON object within the component/file.
- Q: How should Mermaid diagrams be implemented? → A: Use standard Docusaurus MDX `mermaid` code blocks.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Interactive Hardware Verification (Priority: P1)

As a student, I want to select my specific hardware (e.g., "MacBook Air" or "RTX 3060") in an interactive tool and immediately see a pass/fail result with an explanation, so I can stop guessing about compatibility.

**Why this priority**: Hardware confusion is the #1 friction point for new students. Passive text warnings are often ignored.

**Independent Test**: Render the `<HardwareCheck />` component. Select "MacBook Air" -> Verify "Insufficient" result. Select "RTX 4090" -> Verify "Ready" result.

**Acceptance Scenarios**:

1. **Given** the Hardware Check component, **When** I select "M2 Mac" from the dropdown, **Then** I see a Red warning stating "No CUDA Support / Insufficient VRAM".
2. **Given** the Hardware Check component, **When** I select "RTX 4070 Ti" and "64GB RAM", **Then** I see a Green success message "Ready for Isaac Sim".
3. **Given** the Hardware Check component, **When** I select "RTX 3060 (12GB)", **Then** I see a "Yellow/Caution" message (Borderline for heavy sims).

---

### User Story 2 - Understanding The Triad Architecture (Priority: P1)

As a learner, I want to visualize the "Human -> Agent -> Robot" flow through a clear diagram so I understand the core architectural pattern of the course.

**Why this priority**: This concept is the foundation of the entire textbook's methodology.

**Independent Test**: Verify Section 1.2 contains a rendered Mermaid diagram depicting the flow.

**Acceptance Scenarios**:

1. **Given** Section 1.2, **When** the page loads, **Then** a Mermaid diagram renders showing nodes for "Human", "AI Agent", and "Robot" with directional arrows.

---

### User Story 3 - Jargon-Free Reading (Priority: P2)

As a beginner, I want to hover over complex terms like "SLAM" or "URDF" to see their definitions instantly, so I don't have to lose context by switching tabs to Google them.

**Why this priority**: Improves readability and retention for technical content.

**Independent Test**: Hover over a `<TermTooltip>` element and verify the overlay appears.

**Acceptance Scenarios**:

1. **Given** the text contains "SLAM", **When** I hover over the word, **Then** a tooltip appears defining it as "Simultaneous Localization and Mapping".

### Edge Cases

- **Mobile Tooltips**: On mobile, hovering isn't possible. The tooltip should activate on tap (click) instead.
- **No JS**: If JavaScript is disabled, the tooltips should fallback to regular text or links to a glossary.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST render "Chapter 1" content (`docs/01-chapter-1.md`) with 4 distinct sections (1.1 to 1.4).
- **FR-002**: Section 1.3 MUST embed the custom React component `<HardwareCheck />`.
- **FR-003**: The `<HardwareCheck />` logic MUST validate against a static local JSON object containing GPU specs (Name, VRAM, CUDA support) to determine compatibility: NVIDIA RTX required, VRAM >= 12GB (Preferred), RAM >= 32GB.
- **FR-004**: The content MUST include at least 2 Mermaid diagrams (Triad Flow, Hardware Topology) implemented using Docusaurus native ````mermaid` code blocks.
- **FR-005**: Technical terms (SLAM, URDF, VLA) MUST be wrapped in `<TermTooltip term="...">` components.
- **FR-006**: The content MUST include 8-10 IEEE style citations (e.g., `[1]`).
- **FR-007**: Section 1.1 MUST define "Moravec's Paradox" and contrast "Physical AI" vs "Generative AI".

### Key Entities *(include if feature involves data)*

- **HardwareProfile**: `{ gpu: string, vram: number, ram: number, os: string }` (Client-side state).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Interactive Success**: The `<HardwareCheck />` component correctly flags "MacBook" as incompatible and "RTX 4090" as compatible 100% of the time.
- **SC-002**: **Content Volume**: The rendered Chapter 1 page contains >2,500 words of text.
- **SC-003**: **Diagram Rendering**: Both Mermaid diagrams render successfully without syntax errors.
- **SC-004**: **Tooltip Usability**: Tooltips open on hover (desktop) or click (mobile) and display correct definitions.