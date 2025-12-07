# Tasks: RAG Backend - Phase 1 (Server Foundation) - Subdirectory Deployment

**Feature Branch**: `012-backend-server-foundation`
**Created**: 2025-12-07
**Status**: Draft
**Spec**: [specs/012-backend-server-foundation/spec.md](specs/012-backend-server-foundation/spec.md)
**Plan**: [specs/012-backend-server-foundation/plan.md](specs/012-backend-server-foundation/plan.md)

## Summary

This document outlines the tasks required to establish the foundational serverless FastAPI application within the `backend/` subdirectory of this repository and configure it for deployment on Vercel as a separate project. It also includes updating the repository's root and frontend Vercel configurations.

## Dependencies

*   This feature depends on the existing `backend/` directory structure and virtual environment setup from the previous RAG Ingestion Engine feature.
*   `uv` and Vercel CLI are required.

## Phase 1: Backend Subdirectory Setup & Initial Implementation

**Goal**: Prepare the `backend/` subdirectory environment and implement the basic FastAPI application.

- [ ] T001 Navigate to the `backend/` directory.
- [ ] T002 Activate the backend virtual environment (`source .venv/bin/activate`).
- [ ] T003 Update `backend/requirements.txt` to include `fastapi`, `uvicorn`, `mangum`, and `pydantic`.
- [ ] T004 Install new dependencies from `backend/requirements.txt` into the virtual environment using `uv pip install`.
- [x] T005 Create the `backend/api/` directory.
- [x] T006 Create the `backend/api/index.py` file.
- [x] T007 Implement `main` FastAPI application instance in `backend/api/index.py`.
- [x] T008 Implement CORS Middleware in `backend/api/index.py` allowing requests from `http://localhost:3000` and `https://physical-ai-and-humanoid-robotics-h.vercel.app/`.
- [x] T009 Implement `GET /` endpoint in `backend/api/index.py` returning `{"status": "Physical AI API Ready"}`.
- [x] T010 Implement `GET /health` endpoint in `backend/api/index.py` returning `200 OK`.
- [x] T011 Implement basic logging configuration in `backend/api/index.py` for console output.
- [ ] T012 Create `backend/vercel.json` to configure the Python build and routing for the backend project.
- [x] T013 Ensure Python code in `backend/api/index.py` adheres to PEP8 and includes type hints.

## Phase 2: Backend Deployment & Verification (User Story 1 - Verify Backend API Deployment)

**Goal**: Deploy the FastAPI backend from the `backend/` subdirectory to Vercel and verify its functionality.
**Independent Test**: Accessing the deployed backend API endpoints (`/` and `/health`) yields expected `200 OK` responses and content, and frontend requests are not blocked by CORS.

- [x] T014 [US1] Verify local functionality by running `uvicorn api.index:app --reload` (from `backend/`) and accessing endpoints via browser/curl.
- [x] T015 [US1] Deploy the `backend/` subdirectory to Vercel as a new project, setting `backend/` as the Root Directory when prompted by the Vercel CLI.
- [x] T016 [US1] Verify deployed functionality by accessing the backend's Vercel URL and its endpoints.

## Phase 3: Root and Frontend Vercel Configuration Updates

**Goal**: Clean up repository root configuration and ensure frontend deploys correctly.

- [x] T017 Remove `vercel.json` from the root of the repository.
- [x] T018 (Optional) Create `frontend/vercel.json` if custom frontend build/routing is required; otherwise, rely on Vercel's auto-detection for the Docusaurus frontend.

## Final Phase: Polish & Cross-Cutting Concerns

**Goal**: Ensure comprehensive configuration for the backend project.

- [x] T019 Add structured JSON logging configuration for Vercel deployment to `backend/api/index.py`.
- [x] T020 Review `backend/vercel.json` for optimal performance and cold start considerations.

---

## Task Mapping and Dependencies

Tasks are ordered sequentially within phases. Phase 1 must be completed before Phase 2, and Phase 2 before Phase 3.

## Parallel Execution Opportunities

- Tasks T007-T011 (FastAPI implementation details) can be implemented in parallel once the basic file is created (T006).

## Suggested MVP Scope

The MVP for this feature is the complete implementation of **Phase 1: Backend Subdirectory Setup & Initial Implementation** and **Phase 2: Backend Deployment & Verification**. This delivers a deployable FastAPI API ready for frontend integration.

---

## Implementation Strategy

### MVP First (Phases 1 & 2)

1.  Complete Phase 1: Backend Subdirectory Setup & Initial Implementation.
2.  Complete Phase 2: Backend Deployment & Verification.
3.  **STOP and VALIDATE**: Test the deployed backend API.
4.  Proceed to Phase 3 and beyond.

### Incremental Delivery

*   This feature is foundational; phases should be completed sequentially.

### Parallel Team Strategy

*   If working with multiple developers, tasks within Phase 1 (T007-T011) can be parallelized.

---

## Notes

-   Ensure all environment variables for the backend are properly configured for local development and Vercel deployment (e.g., `GEMINI_API_KEY`, `QDRANT_URL`, etc.).
-   The `.gitignore` in the repository root will continue to ignore `backend/venv/` (now `.venv/`) and other Python-specific files.
