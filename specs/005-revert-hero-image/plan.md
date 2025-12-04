# Implementation Plan: Revert Hero Image

**Branch**: `005-revert-hero-image` | **Date**: 2025-12-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-revert-hero-image/spec.md`

## Summary

Revert the Hero section on the landing page to use the static `undraw_docusaurus_mountain.svg` image instead of the `RobotBody` React component. This restores the simpler visual design requested by the stakeholder. The implementation involves modifying `src/pages/index.tsx` to remove the component import and usage, restoring the `<img>` tag, and cleaning up unused code.

## Technical Context

**Language/Version**: React 18+ / TypeScript 5.x
**Primary Dependencies**: Docusaurus v3+
**Storage**: N/A (Frontend only)
**Testing**: Manual Visual Inspection
**Target Platform**: Vercel (Web)
**Project Type**: Web Application (Frontend Revert)
**Performance Goals**: N/A (Reverting to static image)
**Constraints**: Must preserve the "Text Left, Image Right" layout.
**Scale/Scope**: Single Page Update.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **The Triad Architecture**: N/A (Visual Revert)
- [x] **Software-to-Hardware Causality**: N/A (Visual Revert)
- [x] **Tech Stack Isolation**: N/A
- [x] **Compute-Aware Deployment**: N/A
- [x] **Global Constraints**:
    - Framework: Docusaurus (Correct)
    - Deployment: Vercel (Correct)
    - Tech Stack: React/TypeScript (Correct)

## Project Structure

### Documentation (this feature)

```text
specs/005-revert-hero-image/
├── plan.md              # This file
├── research.md          # Phase 0 output (N/A - Revert)
├── data-model.md        # Phase 1 output (N/A - Revert)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   └── RobotBody/   # TO BE REMOVED/UNUSED
│   └── pages/
│       ├── index.tsx    # Update to remove RobotBody
│       └── index.module.css # Ensure styles support image
```

**Structure Decision**: Standard Docusaurus structure.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |