# Feature Specification: Refine Chapter 1 Content & Hierarchy

**Feature Branch**: `008-refine-chapter-1-content-and-hierarchy`  
**Created**: 2025-12-04  
**Status**: Draft  
**Input**: User description: "Refine Chapter 1: Expand Content & Fix Hierarchy Intent: Overwrite the existing Chapter 1 files to resolve heading redundancy and significantly expand technical depth. Each file must follow a strict "Drill-Down" structure (H1 Title -> H2 Concept -> H3 Detail) to ensure unique headings and roughly 800-1,000 words per file. Feature Scope (Content Expansion by File): 1. `01-great-transition.mdx` (~800 words): - H1: The Great Transition - H2: Beyond the Screen (Concept: Why Chatbots are easy, Robots are hard). - H2: Moravec's Paradox Explained (Concept: The counter-intuitive difficulty of motor skills vs. logic). - H2: The Physics Barrier (Concept: Gravity, Friction, and Inertia as "Adversaries"). - H3: Case Study: A ChatGPT generated code vs. Real World deployment failure. 2. `02-triad-architecture.mdx` (~800 words): - H1: The Triad Architecture - H2: The Human Commander (Role: Intent, Voice, Oversight). - H2: The Artificial Brain (Role: Planning, Reasoning, VLA Models). - H2: The Mechanical Body (Role: Actuation, Feedback loops). - H3: The Feedback Loop (How the Body tells the Brain it failed). 3. `03-hardware-nervous-system.mdx` (~1,000 words): - H1: The Hardware Nervous System - H2: The Digital Twin Workstation (The Simulation Rig). * Detail: Why RTX 4070 Ti is the minimum. * Detail: The "VRAM Bottleneck" explained (USD Assets + LLM weights). - H2: The Edge Brain (The Inference Unit). * Detail: Jetson Orin Nano specs (8GB vs 16GB). * Detail: "Sim-to-Real" workflow (Train on PC -> Deploy to Edge). - *Keep the <HardwareCheck /> component here.* 4. `04-senses-of-the-machine.mdx` (~800 words): - H1: Senses of the Machine - H2: Visual Perception (RGB-D). * Detail: How RealSense D435i measures depth vs. standard webcams. - H2: Vestibular System (IMU). * Detail: Accelerometers and Gyroscopes for balance. - H2: Auditory Perception (Whisper). * Detail: ReSpeaker arrays and Voice-to-Action. Success Criteria (SMART): - Hierarchy: H1 titles must NEVER match H2 subtitles. - Length: Total chapter word count exceeds 3,000 words. - Formatting: Use bolding for key terms, blockquotes for definitions, and Admonitions for hardware warnings. - Citations: Ensure IEEE citations are preserved and accurate. User Stories: - "As a reader, I want distinct sub-headings that tell me what the paragraph is about, not just a repeated chapter title.""

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Content Depth and Structure (Priority: P1)

As a reader, I want to read in-depth technical explanations with clear hierarchical headings (H1 -> H2 -> H3), so I can understand the nuance of topics like "The Physics Barrier" without getting lost in repetitive titles.

**Why this priority**: The current content is too shallow and repetitive. This upgrade establishes the textbook's quality standard.

**Independent Test**: Open each of the 4 files. Verify H1 is unique. Verify H2s are distinct concepts (e.g., "Beyond the Screen", not just "The Great Transition" again). Check word count is significantly increased.

**Acceptance Scenarios**:

1. **Given** page `01-great-transition.mdx`, **When** I scroll, **Then** I see H2s "Beyond the Screen", "Moravec's Paradox Explained", and "The Physics Barrier".
2. **Given** page `03-hardware-nervous-system.mdx`, **When** I read the Workstation section, **Then** I see a detailed explanation of the "VRAM Bottleneck" and USD assets.
3. **Given** the full Chapter 1, **When** I sum the word counts, **Then** the total exceeds 3,000 words.

---

### User Story 2 - Component and Citation Preservation (Priority: P1)

As a student, I want the interactive Hardware Check and the citation system to remain functional after the content rewrite, so I don't lose access to tools and references.

**Why this priority**: Regression testing. Rewriting content often accidentally deletes imports or reference anchors.

**Independent Test**: Navigate to `03-hardware-nervous-system` and use the validator. Navigate to any page and check citation links `[1]`.

**Acceptance Scenarios**:

1. **Given** the Hardware page, **When** I select a GPU, **Then** the Validator component gives correct feedback.
2. **Given** the bottom of any page, **When** I look for references, **Then** I see the `## References` section with IEEE formatted citations.

### Edge Cases

- **Broken Links**: Internal links between sections (e.g., "See Section 1.2") must be updated if the H2 text changes.
- **Formatting Consistency**: Ensure all bold terms and blockquotes follow the Docusaurus markdown syntax correctly.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST replace the content of `frontend/docs/chapter-01-foundations/01-great-transition.mdx` with ~800 words detailing "Beyond the Screen", "Moravec's Paradox", and "The Physics Barrier".
- **FR-002**: The system MUST replace `frontend/docs/chapter-01-foundations/02-triad-architecture.mdx` with ~800 words detailing "Human Commander", "Artificial Brain", and "Mechanical Body", preserving the Mermaid diagram.
- **FR-003**: The system MUST replace `frontend/docs/chapter-01-foundations/03-hardware-nervous-system.mdx` with ~1,000 words detailing "Digital Twin Workstation" (VRAM focus) and "Edge Brain", preserving the `<HardwareCheck />` component.
- **FR-004**: The system MUST replace `frontend/docs/chapter-01-foundations/04-senses-of-the-machine.mdx` with ~800 words detailing "Visual (RGB-D)", "Vestibular (IMU)", and "Auditory (Whisper)" perception, preserving `<TermTooltip />` usage.
- **FR-005**: The heading hierarchy MUST follow H1 -> H2 -> H3 logic, ensuring no H2 duplicates the H1 title.
- **FR-006**: All files MUST retain the `## References` section with valid IEEE citations relevant to the new content.

### Key Entities *(include if feature involves data)*

*None (Static Content)*

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Word Count**: Total word count for the 4 files > 3,000 words.
- **SC-002**: **Hierarchy**: Zero instances of H2 text matching H1 text.
- **SC-003**: **Component Functionality**: `<HardwareCheck />` and `<TermTooltip />` render without errors.
- **SC-004**: **Formatting**: At least 3 instances of Docusaurus Admonitions (`:::info`, `:::warning`) used appropriately across the chapter.