# Feature Specification: RAG Backend - Phase 1 (Server Foundation)

**Feature Branch**: `012-backend-server-foundation`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User description: "Feature: RAG Backend - Phase 1 (Server Foundation) Intent: Initialize a production-ready FastAPI application in the `backend/` directory, configured specifically for Serverless deployment on Vercel. Feature Scope (Infrastructure): 1. Dependency Management: - Update `backend/requirements.txt`: Add `fastapi`, `uvicorn`, `mangum` (Vercel adapter), `pydantic`. 2. Server Architecture (`backend/api/index.py`): - Create a FastAPI instance. - Implement CORS Middleware: Allow requests from `localhost:3000` (Dev) and `https://physical-ai-and-humanoid-robotics-h.vercel.app/` (Production). *This is critical for the React frontend to talk to the Python backend.* - Endpoints: - `GET /`: Returns `{"status": "Physical AI API Ready"}`. - `GET /health`: Returns `200 OK`. 3. Vercel Configuration (`vercel.json`): - Define the build (Python). - Route `/api/*` requests to the Python function. - Route all other requests (UI) to the Docusaurus build. Success Criteria (SMART): - Local Test: Running `uvicorn backend.api.index:app --reload` works locally. - Deployment Config: The `vercel.json` is correctly structured to handle the "Monorepo" setup (Frontend = Docusaurus, Backend = Python). Non-Goals: - NOT implementing the OpenAI/Qdrant logic yet (Phase 2). - NOT building the React UI yet (Phase 3). User Stories: - "As a developer, I want a working API URL so I can verify my backend deployment strategy works before I write complex code."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Verify Backend Deployment (Priority: P1)

As a developer, I want a working API URL so I can verify my backend deployment strategy works before I write complex code.

**Why this priority**: This is a critical foundational step to ensure the FastAPI application can be deployed and accessed correctly from the Vercel platform, validating the monorepo setup.

**Independent Test**: The deployed `GET /` and `GET /health` endpoints can be accessed via a web browser or `curl`, confirming a `200 OK` response and the expected status message.

**Acceptance Scenarios**:

1.  **Given** the FastAPI application is deployed on Vercel, **When** I access the base URL (e.g., `https://my-vercel-app.vercel.app/api`), **Then** I receive a `200 OK` response with the body `{"status": "Physical AI API Ready"}`.
2.  **Given** the FastAPI application is deployed on Vercel, **When** I access the health endpoint (e.g., `https://my-vercel-app.vercel.app/api/health`), **Then** I receive a `200 OK` response.
3.  **Given** the FastAPI application is running locally (e.g., via `uvicorn`), **When** I access `http://localhost:8000/` or `http://localhost:8000/health`, **Then** I receive the expected `200 OK` responses.
4.  **Given** the Docusaurus frontend is running locally on `localhost:3000`, **When** it makes a request to the local FastAPI backend (e.g., `http://localhost:8000/`), **Then** the request is not blocked by CORS.

### Edge Cases

-   What happens if the `vercel.json` routing is misconfigured? (Deployment will fail or routes won't be accessible, requiring correction).
-   What happens if CORS origins are not correctly set? (Frontend requests will be blocked, requiring adjustment).
-   What happens if required environment variables (e.g., from `.env`) are missing on Vercel? (API will fail to start).

## Clarifications

### Session 2025-12-07

- Q: What logging strategy is desired for the FastAPI application (e.g., basic console output, structured JSON logs, integration with a specific logging service)? → A: Basic console output for local development; structured JSON logs (stdout/stderr) for Vercel deployment.
- Q: Is there an explicit performance goal (e.g., maximum acceptable duration in milliseconds) for the serverless function's cold start time? → A: Under 2 seconds.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The project MUST update `backend/requirements.txt` to include `fastapi`, `uvicorn`, `mangum`, and `pydantic`.
-   **FR-002**: The project MUST create a FastAPI application instance in `backend/api/index.py`.
-   **FR-003**: The FastAPI application MUST implement CORS Middleware allowing requests from `http://localhost:3000` (development) and `https://physical-ai-and-humanoid-robotics-h.vercel.app/` (production).
-   **FR-004**: The FastAPI application MUST expose a `GET /` endpoint returning `{"status": "Physical AI API Ready"}`.
-   **FR-005**: The FastAPI application MUST expose a `GET /health` endpoint returning `200 OK`.
-   **FR-006**: The project MUST create or update `vercel.json` at the root to define the Python build for the backend.
-   **FR-007**: The `vercel.json` configuration MUST route all requests matching `/api/*` to the Python FastAPI function.
-   **FR-008**: The `vercel.json` configuration MUST route all other requests (not matching `/api/*`) to the Docusaurus frontend build.
-   **FR-009**: The FastAPI application MUST provide basic console logging for local development and output structured JSON logs to stdout/stderr when deployed on Vercel.

### Key Entities

-   **FastAPI Application**: The core Python web service responsible for handling API requests.
-   **CORS Middleware**: A component that handles Cross-Origin Resource Sharing policies for the API.
-   **Vercel Configuration (`vercel.json`)**: A configuration file defining how the monorepo (Docusaurus frontend, Python backend) is built and routed on the Vercel platform.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: Running `uvicorn backend.api.index:app --reload` successfully starts the FastAPI application locally.
-   **SC-002**: Local requests to `http://localhost:8000/` and `http://localhost:8000/health` yield the expected responses.
-   **SC-003**: The project successfully deploys to Vercel with the new `vercel.json` configuration.
-   **SC-004**: Deployed requests to `https://my-vercel-app.vercel.app/api` and `https://my-vercel-app.vercel.app/api/health` return the expected `200 OK` responses.
-   **SC-005**: The `vercel.json` file accurately configures the monorepo to route API requests to the Python backend and other requests to the Docusaurus frontend.
-   **SC-006**: Frontend requests from the specified `localhost:3000` and Vercel domain are successfully handled by the backend without CORS issues.
-   **SC-007**: The FastAPI serverless function's cold start time MUST be under 2 seconds.