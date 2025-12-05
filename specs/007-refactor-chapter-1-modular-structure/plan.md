# Implementation Plan: Refactor Chapter 1: Modular File Structure

**Branch**: `007-refactor-chapter-1-modular-structure` | **Date**: 2025-12-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/007-refactor-chapter-1-modular-structure/spec.md`

## Summary

Refactor the existing "Chapter 1" content from a single monolithic MDX file into a modular directory structure (`docs/chapter-01-foundations/`). This involves creating four separate MDX files for each section, configuring sidebar metadata for proper ordering, and ensuring all component imports (like `<HardwareCheck />`) and internal links are updated to function correctly in the new location.

## Technical Context

**Language/Version**: MDX / Docusaurus v3+
**Primary Dependencies**: Docusaurus Sidebar Configuration
**Storage**: N/A (File System)
**Testing**: Manual Verification (Navigation & Component Rendering)
**Target Platform**: Vercel (Web)
**Project Type**: Web Application (Content Refactor)
**Performance Goals**: No regression in build time.
**Constraints**: Must delete the original file to prevent duplicate routes.
**Scale/Scope**: 1 Directory, 4 new files, 1 deleted file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **The Triad Architecture**: Content preserved (just moved).
- [x] **Software-to-Hardware Causality**: Hardware check component preserved.
- [x] **Tech Stack Isolation**: N/A
- [x] **Compute-Aware Deployment**: N/A
- [x] **Global Constraints**:
    - Framework: Docusaurus (Correct)
    - Deployment: Vercel (Correct)
    - Tech Stack: Markdown/MDX (Correct)

## Project Structure

### Documentation (this feature)

```text
specs/007-refactor-chapter-1-modular-structure/
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
│   ├── 01-chapter-1.mdx         # TO BE DELETED
│   └── chapter-01-foundations/  # NEW DIRECTORY
│       ├── _category_.json      # Sidebar config
│       ├── 01-great-transition.mdx
│       ├── 02-triad-architecture.mdx
│       ├── 03-hardware-nervous-system.mdx
│       └── 04-senses-of-the-machine.mdx
```

**Structure Decision**: Standard Docusaurus nested category structure.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |