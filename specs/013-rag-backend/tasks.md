# Tasks: RAG Backend - Phase 2 (The Intelligence)

**Feature**: RAG Backend - Phase 2 (The Intelligence)
**Status**: Pending

## Dependencies

1. **Phase 1 (Setup)**: Complete environment configuration.
2. **Phase 2 (Foundational)**: Implement core `RagService` logic.
3. **Phase 3 (User Story 1)**: Expose API endpoint and integrate components.

## Phase 1: Setup

*Goal: Prepare the environment and install necessary dependencies.*

- [x] T001 Install dependencies (`google-generativeai`, `qdrant-client`, `openai`, `tenacity`, `python-dotenv`) in `backend/`
- [x] T007 [P] [US1] Implement `RagService.generate_answer` using `openai` (Chat Completions)
- [x] T008 [US1] Implement `RagService.process_query` orchestration method (Embed -> Retrieve -> Generate) with `tenacity` retries

## Phase 3: User Story 1 - Student Query

*Goal: Enable students to ask questions and receive textbook-cited answers.*
*Priority: P1*

**Independent Test**:
- Send POST to `/api/chat` with `{"message": "What is ROS?"}`.
- Verify 200 OK response with `answer` and `sources`.
- Verify 503 Service Unavailable if dependencies are mocked to fail.

- [x] T009 [US1] Create API endpoint `POST /api/chat` in `backend/src/api/chat.py`
- [x] T010 [US1] Integrate `RagService` into `backend/src/api/chat.py`
- [x] T011 [US1] Register `chat_router` in `backend/src/main.py`
- [x] T012 [US1] Add error handling for 503 (Upstream Failure) in `backend/src/api/chat.py`

## Final Phase: Polish

*Goal: Ensure code quality and robust error handling.*

- [x] T013 Verify type hints and Pydantic validation across all new files
- [x] T014 Review error logs for clear diagnostics on upstream failures

## Parallel Execution Examples

- **RagService Components**: T005 (Embedding), T006 (Retrieval), and T007 (Generation) can be implemented in parallel by different developers.

## Implementation Strategy

1. **MVP**: Focus on a "Happy Path" where all services are up.
2. **Robustness**: Add `tenacity` retries and error handling in T008 and T012.
