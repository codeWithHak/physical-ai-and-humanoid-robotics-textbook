# Implementation Plan: Chapter 1 Content & Micro-Interactions

**Branch**: `006-chapter-1-content-and-micro-interactions` | **Date**: 2025-12-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/006-chapter-1-content-and-micro-interactions/spec.md`

## Summary

Implement "Chapter 1: The Age of Embodied Intelligence" as a Docusaurus MDX page with two embedded React micro-interactions: `<HardwareCheck />` for GPU validation and `<TermTooltip />` for glossary definitions. The content will cover the "Great Transition," "Triad Architecture," and "Hardware Nervous System," supported by Mermaid diagrams and IEEE citations.

## Technical Context

**Language/Version**: React 18+ / TypeScript 5.x / MDX
**Primary Dependencies**: Docusaurus v3+, Mermaid (Native support)
**Storage**: N/A (Static Content + Client-side State)
**Testing**: Manual Component Verification
**Target Platform**: Vercel (Web)
**Project Type**: Web Application (Content + Components)
**Performance Goals**: Components must be lightweight and not block First Paint.
**Constraints**: Hardware check logic is client-side only (no backend).
**Scale/Scope**: 1 MDX File + 2 React Components.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **The Triad Architecture**: Chapter 1 explicitly defines and teaches this architecture.
- [x] **Software-to-Hardware Causality**: The `<HardwareCheck />` component enforces the hardware reality required for this causality.
- [x] **Tech Stack Isolation**:
    - ROS 2: N/A (Content)
    - Gazebo/Unity: N/A (Content)
    - NVIDIA Isaac: N/A (Content)
    - *Exception*: Docusaurus usage is compliant.
- [x] **Compute-Aware Deployment**: The content differentiates Workstation vs Edge compute.
- [x] **Global Constraints**:
    - Framework: Docusaurus (Correct)
    - Deployment: Vercel (Correct)
    - Tech Stack: React/TypeScript (Correct)

## Project Structure

### Documentation (this feature)

```text
specs/006-chapter-1-content-and-micro-interactions/
├── plan.md              # This file
├── research.md          # Phase 0 output (N/A - No unknowns)
├── data-model.md        # Phase 1 output (N/A - Client state only)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── HardwareCheck/
│   │   │   ├── index.tsx        # Logic + UI
│   │   │   ├── data.json        # GPU Database
│   │   │   └── styles.module.css
│   │   └── TermTooltip/
│   │       ├── index.tsx
│   │       └── styles.module.css
├── docs/
│   └── 01-chapter-1.mdx         # The Content File
```

**Structure Decision**: Standalone components in `src/components` imported into MDX.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |