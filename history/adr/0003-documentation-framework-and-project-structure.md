# ADR-0003: Documentation Framework and Project Structure

> **Scope**: Architecture and Repository Organization

- **Status:** Accepted
- **Date:** 2025-12-04
- **Feature:** 001-platform-foundation-setup
- **Context:** The project's primary output is a "textbook" (structured documentation). We also anticipate future code components (Python/ROS) to sit alongside the text. We need a repository structure and framework that supports high-quality documentation without cluttering the root or blocking future expansion into software modules.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? Yes.
     2) Alternatives: Multiple viable options considered with tradeoffs? Yes.
     3) Scope: Cross-cutting concern (not an isolated detail)? Yes.
-->

## Decision

We will use **Docusaurus v3 (TypeScript)** located in a **`frontend/` subdirectory**.

- **Framework**: Docusaurus v3+
- **Language**: TypeScript
- **Location**: `repo-root/frontend/`

## Consequences

### Positive

- **Content Optimized**: Docusaurus is purpose-built for documentation (versioning, sidebars, i18n, markdown-centric).
- **Clean Architecture**: Putting the site in `frontend/` prevents configuration pollution (tsconfig, package.json, etc.) in the root, keeping it clear for future Robotics/Python code.
- **Extensibility**: React/TypeScript allows us to build custom interactive components (e.g., visualizations) for the textbook.
- **Type Safety**: TypeScript config prevents common regressions in customization code.

### Negative

- **Workflow Friction**: Developers must `cd frontend` to run web-related commands (`npm start`).
- **CI Complexity**: CI workflows must define `working-directory: ./frontend`.

## Alternatives Considered

### Root-level Docusaurus
- **Pros**: Simpler initial setup, standard Docusaurus layout.
- **Cons**: Pollutes the root directory. Makes it harder to add a separate "backend" or "robotics-sdk" folder later without naming conflicts or clutter.
- **Rationale**: Rejected to support the "Triad Architecture" (Mental/Sim/Real) concept where web is just one interface.

### MkDocs (Material)
- **Pros**: Python-based (aligns with Robotics), very popular, easy to set up.
- **Cons**: Limited interactivity compared to React. Harder to build custom complex visualizations for "Physical AI".
- **Rationale**: Rejected because the interactive nature of the textbook benefits from the React ecosystem.

## References

- Feature Spec: specs/001-platform-foundation-setup/spec.md
- Implementation Plan: specs/001-platform-foundation-setup/plan.md