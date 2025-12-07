# Tasks: RAG Backend - Phase 1 (Server Foundation)

**Feature Branch**: `012-backend-server-foundation`
**Created**: 2025-12-07
**Status**: Draft
**Spec**: [specs/012-backend-server-foundation/spec.md](specs/012-backend-server-foundation/spec.md)
**Plan**: [specs/012-backend-server-foundation/plan.md](specs/012-backend-server-foundation/plan.md)

## Summary

This document outlines the tasks required to establish the foundational serverless FastAPI application, configured for deployment on Vercel as part of a monorepo.

## Dependencies

This feature depends on the existing `backend/` directory structure and virtual environment setup from the previous RAG Ingestion Engine feature. It also requires `uv` and Vercel CLI to be installed.

## Phase 1: Setup (Project Initialization)

**Goal**: Prepare the backend environment and directory structure for the FastAPI application.

- [x] T001 Update `backend/requirements.txt` to include `fastapi`, `uvicorn`, `mangum`, and `pydantic`.
- [x] T002 Install new dependencies from `backend/requirements.txt` into the virtual environment using `uv pip install`.
- [x] T003 Create the `backend/api/` directory.
- [x] T004 Create the `backend/api/index.py` file.

## Phase 2: Foundational (Core API Logic)

**Goal**: Implement the basic FastAPI application with CORS and foundational endpoints.

- [x] T005 [P] Implement `main` FastAPI application instance in `backend/api/index.py`.
- [x] T006 [P] Implement CORS Middleware in `backend/api/index.py` allowing requests from `http://localhost:3000` and `https://physical-ai-and-humanoid-robotics-h.vercel.app/`.
- [x] T007 [P] Implement `GET /` endpoint in `backend/api/index.py` returning `{"status": "Physical AI API Ready"}`.
- [x] T008 [P] Implement `GET /health` endpoint in `backend/api/index.py` returning `200 OK`.
- [x] T009 Implement basic logging configuration in `backend/api/index.py` for console output.

## Phase 3: User Story 1 - Verify Backend Deployment (Priority: P1)

**Goal**: Configure Vercel for monorepo deployment and verify local and deployed API functionality.
**Independent Test**: Accessing local and deployed API endpoints (`/` and `/health`) yields expected `200 OK` responses and content, and frontend requests are not blocked by CORS.

- [x] T010 [US1] Create or update `vercel.json` at the project root to configure the Python build for the `backend/` directory.
- [x] T011 [US1] Configure `vercel.json` to route requests matching `/api/*` to the Python FastAPI function (`backend/api/index.py`).
- [x] T012 [US1] Configure `vercel.json` to route all other requests to the Docusaurus frontend build.
- [x] T013 [US1] Verify local functionality by running `uvicorn backend.api.index:app --reload` and accessing endpoints via browser/curl.
- [ ] T014 [US1] Deploy the project to Vercel and verify deployed API endpoints.
- [ ] T015 [US1] Verify CORS functionality locally by attempting a request from `localhost:3000` to `localhost:8000/`.

## Final Phase: Polish & Cross-Cutting Concerns

**Goal**: Ensure code quality and comprehensive configuration.

- [ ] T016 Ensure Python code in `backend/api/index.py` adheres to PEP8 and includes type hints.
- [ ] T017 Add structured JSON logging configuration for Vercel deployment to `backend/api/index.py`.
- [ ] T018 Review `vercel.json` for optimal performance and cold start considerations.

---

## Task Mapping and Dependencies

The tasks are ordered to ensure dependencies are met. Phase 1 must be completed before Phase 2, and Phase 2 before Phase 3. Tasks within a Phase can be parallelized where marked `[P]`.

## Parallel Execution Opportunities

- Tasks marked with `[P]` within Phase 2 (`T005`-`T008`) can be implemented in parallel.

## Suggested MVP Scope

The MVP for this feature is the complete implementation of **User Story 1 - Verify Backend Deployment** (Phase 3). This delivers a deployable FastAPI foundation with verified routing and basic endpoints.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
