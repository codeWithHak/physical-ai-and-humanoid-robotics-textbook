# Implementation Plan: Preface and User Guide

**Branch**: `002-preface-and-user-guide` | **Date**: 2025-12-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-preface-and-user-guide/spec.md`

## Summary

Implement the "Preface" page (`docs/intro.md` or a new file if necessary) using Docusaurus Markdown. This page serves as the critical entry point for the course, detailing the "Triad Architecture," strict hardware requirements (with visual warnings), and the 13-week learning path. It will also briefly introduce the interactive features (Translation/Chatbot) to onboard users.

## Technical Context

**Language/Version**: Markdown / MDX (Docusaurus v3+)
**Primary Dependencies**: Docusaurus v3+ (Standard Admonitions)
**Storage**: N/A (Static Content)
**Testing**: Manual Review / Vercel Preview
**Target Platform**: Vercel (Web)
**Project Type**: Documentation Content
**Performance Goals**: N/A (Static Content)
**Constraints**: Must be the first item in the sidebar (`sidebar_position: 0` or similar).
**Scale/Scope**: Single MDX file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **The Triad Architecture**: The content explicitly *explains* this architecture to the user.
- [x] **Software-to-Hardware Causality**: The "Hardware Reality Check" section directly addresses the physical hardware requirements needed for this principle.
- [x] **Tech Stack Isolation**:
    - ROS 2: N/A (Content)
    - Gazebo/Unity: N/A (Content)
    - NVIDIA Isaac: N/A (Content)
    - *Exception*: Docusaurus usage is compliant.
- [x] **Compute-Aware Deployment**: The hardware requirements section explicitly segregates "Workstation" vs "Edge" specs.
- [x] **Global Constraints**:
    - Framework: Docusaurus (Correct)
    - Deployment: Vercel (Correct)
    - Tech Stack: Markdown/MDX (Correct)

## Project Structure

### Documentation (this feature)

```text
specs/002-preface-and-user-guide/
├── plan.md              # This file
├── research.md          # Phase 0 output (N/A - No unknowns)
├── data-model.md        # Phase 1 output (N/A - Static Content)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
frontend/
├── docs/
│   ├── 00-preface.md    # NEW: The Preface Content
│   ├── intro.md         # EXISTING: To be removed or repurposed
│   └── ...
├── sidebars.ts          # CONFIG: Update sidebar order
```

**Structure Decision**: Create `00-preface.md` to ensure alphabetic sorting puts it first, or explicitly configure `sidebars.ts` to place it at the top. Using standard Docusaurus `docs/` directory.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |