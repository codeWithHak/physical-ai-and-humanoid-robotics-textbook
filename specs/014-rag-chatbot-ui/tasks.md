# Tasks: RAG Frontend UI (The Chatbot)

**Feature**: RAG Frontend UI (The Chatbot)
**Status**: Pending

## Dependencies

1. **Phase 1 (Setup)**: Prepare component directory.
2. **Phase 2 (Foundational)**: Define types and base styles.
3. **Phase 3 (User Story 1)**: Implement components and logic.

## Phase 1: Setup

*Goal: Prepare the environment for the new component.*

- [x] T001 Create directory structure `frontend/src/components/RagChat/`
- [x] T002 Verify `lucide-react` is installed in `frontend/package.json` (Install if missing)

## Phase 2: Foundational

*Goal: Define data structures and visual styling.*

- [x] T003 Create types definition in `frontend/src/components/RagChat/types.ts` (`ChatMessage`, `ChatState`)
- [x] T004 Create CSS Modules styles in `frontend/src/components/RagChat/styles.module.css` (Glass-morphism, Neon Green, Mobile Responsive)

## Phase 3: User Story 1 - Ask a Question

*Goal: Enable users to open chat, ask questions, and see responses.*
*Priority: P1*

**Independent Test**:
- Open `http://localhost:3000`.
- Click the floating button.
- Send a message.
- Verify API call to `http://127.0.0.1:8000/api/chat` (or configured URL).

- [x] T005 [P] [US1] Create `ChatButton` component in `frontend/src/components/RagChat/ChatButton.tsx` (Floating trigger)
- [x] T006 [P] [US1] Create `ChatWindow` component in `frontend/src/components/RagChat/ChatWindow.tsx` (Message list, Input, Citations)
- [x] T007 [US1] Create main `RagChat` container in `frontend/src/components/RagChat/index.tsx` (State management, API integration)
- [x] T008 [US1] Mount `<RagChat />` in `frontend/src/pages/index.tsx` (Landing Page Integration)

## Final Phase: Polish

*Goal: Ensure seamless integration and robustness.*

- [x] T009 Verify mobile responsiveness (100% width/height on small screens)
- [x] T010 Verify error handling (Backend down scenario)

## Parallel Execution Examples

- T005 (`ChatButton`) and T006 (`ChatWindow`) are purely presentational and can be built in parallel.

## Implementation Strategy

1. **Skeleton**: Build the UI components with mock data first.
2. **Wiring**: Connect `index.tsx` to the real API.
3. **Integration**: Drop it onto the landing page.
