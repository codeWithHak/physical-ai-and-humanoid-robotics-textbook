# Implementation Plan: Visual Identity & Landing Page Overhaul

**Branch**: `003-visual-identity-overhaul` | **Date**: 2025-12-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-visual-identity-overhaul/spec.md`

## Summary

Completely re-theme the Docusaurus application to match the "RoboLearn" dark aesthetic. This involves implementing a new typography engine (Space Grotesk), a global dark-mode color palette (Lime Green #BFE600 accents), and restructuring the landing page (`src/pages/index.tsx`) to follow a specific "Left Text / Right Diagram" layout.

## Technical Context

**Language/Version**: TypeScript 5.x / React 18+
**Primary Dependencies**: Docusaurus v3+ (Infima styling system), Custom CSS
**Storage**: N/A (Frontend Styles)
**Testing**: Manual Visual Inspection, Mobile Responsiveness Check
**Target Platform**: Vercel (Web)
**Project Type**: Web Application (Docusaurus)
**Performance Goals**: Font loading < 100ms (using `font-display: swap`), CLS < 0.1
**Constraints**: Must enforce Dark Mode by default.
**Scale/Scope**: Global CSS overrides and Landing Page component.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **The Triad Architecture**: N/A (Visual Style)
- [x] **Software-to-Hardware Causality**: N/A (Visual Style)
- [x] **Tech Stack Isolation**:
    - ROS 2: N/A
    - Gazebo/Unity: N/A
    - NVIDIA Isaac: N/A
    - *Exception*: Docusaurus usage is compliant.
- [x] **Compute-Aware Deployment**: N/A
- [x] **Global Constraints**:
    - Framework: Docusaurus (Correct)
    - Deployment: Vercel (Correct)
    - Tech Stack: React/TypeScript/CSS (Correct)

## Project Structure

### Documentation (this feature)

```text
specs/003-visual-identity-overhaul/
├── plan.md              # This file
├── research.md          # Phase 0 output (N/A - No unknowns)
├── data-model.md        # Phase 1 output (N/A - Styles only)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── css/
│   │   ├── custom.css       # Global overrides (Infima variables, Google Fonts import)
│   ├── pages/
│   │   ├── index.tsx        # Landing Page Layout
│   │   └── index.module.css # Landing Page specific styles
│   └── components/          # (Existing components)
└── docusaurus.config.ts     # Font config reference
```

**Structure Decision**: Standard Docusaurus styling structure. Styles will be centralized in `custom.css` for global themes, and module CSS for the landing page layout. Fonts loaded via CSS import.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |