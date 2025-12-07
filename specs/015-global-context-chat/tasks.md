# Tasks: Global RAG Chat with Contextual Ask

**Feature**: Global RAG Chat with Contextual Ask
**Status**: Pending

## Dependencies

1. **Phase 1 (Setup)**: Prepare global directories.
2. **Phase 2 (Foundational)**: Implement Global Chat Context and Root wrapper.
3. **Phase 3 (Refactor)**: Update RagChat to use global state.
4. **Phase 4 (Contextual Ask)**: Implement Selection Tooltip.
5. **Phase 5 (Integration)**: Wire everything in Root and cleanup.

## Phase 1: Setup

*Goal: Prepare directory structure for global components.*

- [x] T001 Create directory `frontend/src/context/`
- [x] T002 Create directory `frontend/src/theme/`
- [x] T003 Create directory `frontend/src/components/SelectionTooltip/`

## Phase 2: Foundational (Global State)

*Goal: Lift state to a global provider.*

- [x] T004 [US1] Implement `ChatContext` in `frontend/src/context/ChatContext.tsx` (State: isOpen, messages, isLoading, inputQuery)
- [x] T005 [US1] Create `Root` component in `frontend/src/theme/Root.tsx` wrapping children with `ChatProvider`

## Phase 3: Refactor RagChat

*Goal: Connect the existing UI to the new global state.*

- [x] T006 [US1] Refactor `frontend/src/components/RagChat/index.tsx` to consume `ChatContext` instead of local `useState`
- [x] T007 [US1] Update `RagChat` to accept `inputQuery` from context and auto-fill/submit if set

## Phase 4: Contextual Ask (Tooltip)

*Goal: Allow users to ask about selected text.*
*Priority: P2*

- [x] T008 [P] [US2] Create styles for tooltip in `frontend/src/components/SelectionTooltip/styles.module.css` (Neon Lime, High Z-index)
- [x] T009 [US2] Implement `SelectionTooltip` logic in `frontend/src/components/SelectionTooltip/index.tsx` (MouseUp listener, Position calculation, Mobile optimization)
- [x] T010 [US2] Wire `SelectionTooltip` "Ask AI" button to `triggerAskAI` context method

## Phase 5: Integration & Cleanup

*Goal: Final wiring and cleanup.*

- [x] T011 [US1] Mount `<RagChat />` and `<SelectionTooltip />` inside `frontend/src/theme/Root.tsx`
- [x] T012 [US1] Remove `<RagChat />` mount from `frontend/src/pages/index.tsx` (Cleanup)

## Final Phase: Polish

- [x] T013 Verify persistence across page navigation (User Story 1)
- [x] T014 Verify tooltip behavior on mobile (User Story 2 - Mobile Optimization)

## Parallel Execution Examples

- T008/T009 (Tooltip) can be built in parallel with T006/T007 (RagChat Refactor).

## Implementation Strategy

1. **Lift State**: Move state to Context first.
2. **Refactor UI**: Make RagChat "dumb" (controlled by Context).
3. **Add Feature**: Implement Tooltip and connect to Context.
4. **Globalize**: Move everything to Root.