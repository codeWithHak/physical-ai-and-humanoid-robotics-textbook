# Feature Specification: RAG Backend - Phase 1 (Server Foundation)

**Feature Branch**: `012-backend-server-foundation`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User description: "Feature: RAG Backend - Phase 1 (Server Foundation) Intent: Initialize a production-ready FastAPI application in the `backend/` directory, configured specifically for Serverless deployment on Vercel. Feature Scope (Infrastructure): 1. Dependency Management: - Update `backend/requirements.txt`: Add `fastapi`, `uvicorn`, `mangum` (Vercel adapter), `pydantic`. 2. Server Architecture (`backend/api/index.py`): - Create a FastAPI instance. - Implement CORS Middleware: Allow requests from `localhost:3000` (Dev) and `https://physical-ai-and-humanoid-robotics-h.vercel.app/` (Production). *This is critical for the React frontend to talk to the Python backend.* - Endpoints: - `GET /`: Returns `{"status": "Physical AI API Ready"}`. - `GET /health`: Returns `200 OK`. 3. Vercel Configuration (`vercel.json`): - Define the build (Python). - Route `/api/*` requests to the Python function. - Route all other requests (UI) to the Docusaurus build. Success Criteria (SMART): - Local Test: Running `uvicorn backend.api.index:app --reload` works locally. - Deployment Config: The `vercel.json` is correctly structured to handle the "Monorepo" setup (Frontend = Docusaurus, Backend = Python). Non-Goals: - NOT implementing the OpenAI/Qdrant logic yet (Phase 2). - NOT building the React UI yet (Phase 3). User Stories: - "As a developer, I want a working API URL so I can verify my backend deployment strategy works before I write complex code."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Verify Backend API Deployment (Priority: P1)

As a developer, I want a working FastAPI application deployed to Vercel (targeting the `backend/` subdirectory of this repository) so I can verify its accessibility and functionality.

**Why this priority**: This is a critical foundational step to ensure the backend API can be deployed and accessed correctly before integration with the frontend.

**Independent Test**: The deployed `GET /` and `GET /health` endpoints of the separately deployed FastAPI API can be accessed via a web browser or `curl`, confirming a `200 OK` response and the expected status message.

**Acceptance Scenarios**:

1.  **Given** the FastAPI application is deployed as a Vercel project targeting the `backend/` subdirectory, **When** I access its base URL (e.g., `https://my-backend-api.vercel.app/`), **Then** I receive a `200 OK` response with the body `{"status": "Physical AI API Ready"}`.
2.  **Given** the FastAPI application is deployed as a Vercel project targeting the `backend/` subdirectory, **When** I access its health endpoint (e.g., `https://my-backend-api.vercel.app/health`), **Then** I receive a `200 OK` response.
3.  **Given** the FastAPI application is running locally (e.g., via `uvicorn`), **When** I access `http://localhost:8000/` or `http://localhost:8000/health`, **Then** I receive the expected `200 OK` responses.

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
-   **FR-003**: The FastAPI application MUST implement CORS Middleware allowing requests from `http://localhost:3000` (development) and the deployed URL of the Docusaurus frontend (`https://physical-ai-and-humanoid-robotics-h.vercel.app/`).
-   **FR-006**: The `backend/` subdirectory MUST contain a `vercel.json` file to define the Python build for the FastAPI application.
-   **FR-007**: The `vercel.json` configuration in the `backend/` subdirectory MUST route all requests to the Python FastAPI function (e.g., `/`).
-   **FR-008**: The `vercel.json` file at the root of the repository MUST be removed or simplified to avoid conflicts, allowing the `frontend/` and `backend/` Vercel projects to be deployed from their respective subdirectories.
-   **FR-009**: The FastAPI application MUST provide basic console logging for local development and output structured JSON logs to stdout/stderr when deployed on Vercel.

### Key Entities

-   **FastAPI Application**: The core Python web service responsible for handling API requests, deployed as an independent Vercel project targeting the `backend/` subdirectory.
-   **CORS Middleware**: A component that handles Cross-Origin Resource Sharing policies for the API, allowing requests from specified frontend origins.
-   **Vercel Configuration (Backend `vercel.json`)**: A configuration file within the `backend/` subdirectory defining how the FastAPI application is built and deployed as an independent Vercel project.
-   **Vercel Configuration (Frontend Deployment)**: The Docusaurus frontend deployed as an independent Vercel project targeting the `frontend/` subdirectory, relying on Vercel's auto-detection or a `vercel.json` within `frontend/`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: Running `uvicorn backend.api.index:app --reload` successfully starts the FastAPI application locally.
-   **SC-002**: Local requests to `http://localhost:8000/` and `http://localhost:8000/health` yield the expected responses.
-   **SC-003**: The backend Vercel project (targeting the `backend/` subdirectory) successfully deploys to Vercel with its `vercel.json` configuration.
-   **SC-004**: Deployed requests to the backend Vercel project's URL (e.g., `https://<backend-project-name>.vercel.app/`) and its health endpoint (e.g., `/health`) return the expected `200 OK` responses.
-   **SC-005**: The `vercel.json` file at the root of the repository is removed or simplified to avoid conflicts, and the frontend Vercel project (targeting the `frontend/` subdirectory) is accurately configured to deploy only the Docusaurus frontend.
-   **SC-006**: Frontend requests from the specified `localhost:3000` and the deployed Docusaurus frontend domain are successfully handled by the *local* FastAPI backend without CORS issues.
-   **SC-007**: The FastAPI serverless function's cold start time MUST be under 2 seconds.