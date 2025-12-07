# Implementation Plan: Global RAG Chat with Contextual Ask

**Branch**: `015-global-context-chat` | **Date**: 2025-12-07 | **Spec**: [specs/015-global-context-chat/spec.md](../spec.md)
**Input**: Feature specification from `specs/015-global-context-chat/spec.md`

## Summary

Implement a global `ChatProvider` to persist chat state across navigation and enable a "Contextual Ask" feature. This involves wrapping the application in `src/theme/Root.tsx`, refactoring `<RagChat />` to use the context, and creating a new `<SelectionTooltip />` component.

## Technical Context

**Language/Version**: TypeScript 5.x, React 19
**Primary Dependencies**:
- React Context API
- DOM API (`window.getSelection`)
**Target Platform**: Docusaurus v3
**Project Type**: Web Application (Frontend)
**Performance Goals**: No lag on selection; smooth transition to chat.
**Constraints**: Must handle mobile touch conflicts.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **The Triad Architecture**: Enhances "Human Intent" via seamless query injection.
- **Tech Stack Isolation**: Compliant.
- **Compute-Aware Deployment**: Client-side logic.
- **Documentation Strategy**: N/A.
- **Success Criteria**: Directly supports "RAG Agent" highlighting requirement.

## Project Structure

### Documentation (this feature)

```text
specs/015-global-context-chat/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── tasks.md
```

### Source Code (repository root)

```text
frontend/
└── src/
    ├── theme/
    │   └── Root.tsx                 # NEW: Global Wrapper
    ├── context/
    │   └── ChatContext.tsx          # NEW: Context Provider
    ├── components/
    │   ├── RagChat/
    │   │   ├── index.tsx            # MOD: Consume Context
    │   │   └── ...
    │   └── SelectionTooltip/        # NEW: Feature
    │       ├── index.tsx
    │       └── styles.module.css
    └── pages/
        └── index.tsx                # MOD: Remove local RagChat mount (moved to Root)
```

**Structure Decision**: Option 2 (Web application - Frontend). Extending Docusaurus theme architecture.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Global Wrapper | Persistence | Swizzling `Layout` is more brittle and complex to maintain. `Root` is the standard extension point. |