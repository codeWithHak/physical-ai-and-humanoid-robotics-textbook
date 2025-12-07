# Research: Global RAG Chat with Contextual Ask

**Status**: Complete
**Date**: 2025-12-07

## Technical Context

**Language/Version**: TypeScript 5.x, React 18+
**Framework**: Docusaurus v3+
**State Management**: React Context API
**DOM API**: `window.getSelection()`

## Decisions & Rationale

### 1. Global State Architecture
- **Decision**: Use `src/theme/Root.tsx` to wrap the entire Docusaurus app with `ChatProvider`.
- **Rationale**: This is the standard Docusaurus way to introduce global state without Swizzling `Layout`, ensuring persistence across client-side navigation.

### 2. Chat Context
- **Decision**: Lift `isOpen`, `messages`, and `isLoading` from `<RagChat />` to `ChatContext`.
- **Rationale**: Allows multiple triggers (Floating Button, Selection Tooltip) to control the chat.

### 3. Selection Tooltip Logic
- **Decision**: Listen to `mouseup` events globally (on `document`).
- **Rationale**: Captures selection anywhere.
- **Filtering**: Ignore selections inside the chat window itself or < 5 chars.
- **Positioning**: Use `range.getBoundingClientRect()` to position the tooltip absolutely near the selection.

### 4. Mobile Handling
- **Decision**: Disable tooltip on touch devices for MVP.
- **Rationale**: Conflicts with OS native copy/paste menus are complex to resolve reliably without custom touch handling libraries.

## Open Questions Resolved

- **Docusaurus Integration**: `Root.tsx` confirmed as the correct extension point.
- **Event Handling**: `document.addEventListener('mouseup', ...)` inside the Tooltip component (mounted at Root) is sufficient.