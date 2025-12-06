# Implementation Plan: Refine Chapter 1 Content & Hierarchy

**Branch**: `008-refine-chapter-1-content-and-hierarchy` | **Date**: 2025-12-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/008-refine-chapter-1-content-and-hierarchy/spec.md`

## Summary

Refine Chapter 1 content by expanding technical depth (>3,000 words total) and enforcing a strict "Drill-Down" hierarchy (H1 -> H2 -> H3) to eliminate redundant headings. This involves overwriting the 4 existing MDX files in `docs/chapter-01-foundations/` with detailed explanations of Moravec's Paradox, Triad Architecture, Hardware bottlenecks (VRAM focus), and Sensor physics, while preserving existing interactive components (`HardwareCheck`, `TermTooltip`, Mermaid diagrams).

## Technical Context

**Language/Version**: Markdown / MDX (Docusaurus v3+)
**Primary Dependencies**: Docusaurus Admonitions, Mermaid, React Components
**Storage**: N/A (Static Content)
**Testing**: Manual Review (Content/Structure) + Component Functionality Check
**Target Platform**: Vercel (Web)
**Project Type**: Content Update
**Performance Goals**: N/A
**Constraints**: Must preserve existing component imports and relative paths.
**Scale/Scope**: 4 MDX Files (~3,000 words).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **The Triad Architecture**: Content explicitly details this (Section 1.2).
- [x] **Software-to-Hardware Causality**: Hardware section (1.3) focuses on the "why" (VRAM bottleneck).
- [x] **Tech Stack Isolation**: Content discusses the approved stack (ROS 2, Isaac Sim, Jetson).
- [x] **Compute-Aware Deployment**: Content differentiates Workstation vs Edge.
- [x] **Global Constraints**:
    - Framework: Docusaurus (Correct)
    - Deployment: Vercel (Correct)
    - Tech Stack: Markdown/MDX (Correct)

## Project Structure

### Documentation (this feature)

```text
specs/008-refine-chapter-1-content-and-hierarchy/
├── plan.md              # This file
├── research.md          # Phase 0 output (N/A - Content only)
├── data-model.md        # Phase 1 output (N/A - Static Content)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
frontend/
├── docs/
│   └── chapter-01-foundations/
│       ├── 01-great-transition.mdx      # Updated Content
│       ├── 02-triad-architecture.mdx    # Updated Content
│       ├── 03-hardware-nervous-system.mdx # Updated Content
│       └── 04-senses-of-the-machine.mdx # Updated Content
```

**Structure Decision**: No structural changes; overwriting existing files in place.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |