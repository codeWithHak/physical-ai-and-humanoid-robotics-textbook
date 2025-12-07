# Research Summary: RAG Backend - Phase 1 (Server Foundation)

This document summarizes technical decisions and clarifications made during the specification and planning phases for the RAG Backend - Phase 1 (Server Foundation) feature.

## Decision: Logging Strategy

-   **What was chosen**: Basic console output for local development; structured JSON logs (stdout/stderr) for Vercel deployment.
-   **Rationale**: This approach balances simplicity for local debugging with enhanced observability in the Vercel serverless environment, leveraging Vercel's native log collection capabilities without introducing complex external logging integrations at this foundational stage.
-   **Alternatives considered**:
    -   Basic console output only: Rejected as insufficient for production observability.
    -   External logging service integration: Rejected as overkill for this initial phase, adding unnecessary complexity.

## Decision: Serverless Cold Start Performance Goal

-   **What was chosen**: The FastAPI serverless function's cold start time MUST be under 2 seconds.
-   **Rationale**: This target aligns with industry best practices for responsive serverless applications, ensuring a good user experience. While Vercel optimizes for this, setting an explicit goal allows for future monitoring and optimization if needed.
-   **Alternatives considered**: None explicitly, as this was a clarification of a non-functional requirement.

## Decision: Core Backend Technologies

-   **What was chosen**: FastAPI for the web framework, Uvicorn as the ASGI server, Mangum as the adapter for Vercel Serverless, and Pydantic for data validation.
-   **Rationale**: FastAPI is explicitly mentioned in the project's constitution for the Chatbot Backend, ensuring alignment with overall project architecture. These tools form a standard, performant, and Vercel-compatible Python backend stack.
-   **Alternatives considered**: None explicitly, as FastAPI was a constitutional choice.

## Decision: CORS Configuration

-   **What was chosen**: CORS Middleware will allow requests from `http://localhost:3000` (development) and `https://physical-ai-and-humanoid-robotics-h.vercel.app/` (production).
-   **Rationale**: These origins directly correspond to the Docusaurus frontend's development and expected production URLs, enabling seamless communication between the frontend and backend without security blocks.
-   **Alternatives considered**:
    -   Wildcard (`*`) origin: Rejected due to security implications in a production environment.
    -   No CORS: Rejected as it would prevent frontend-backend communication across origins.

## Decision: Vercel Deployment Strategy

-   **What was chosen**: The FastAPI backend will be deployed as an independent Vercel project targeting the `backend/` subdirectory of this repository. The `vercel.json` within the `backend/` subdirectory will configure its Python build and routing. The Docusaurus frontend will also be deployed as an independent Vercel project targeting the `frontend/` subdirectory, relying on Vercel's auto-detection or a `vercel.json` within `frontend/`. The root `vercel.json` will be removed.
-   **Rationale**: This decision was made to resolve persistent `vercel.json` parsing and routing issues encountered with a root-level monorepo `vercel.json` and to align with the user's current deployment approach. This strategy simplifies configuration for both frontend and backend deployments and enables independent deployment cycles for each subdirectory, while keeping all code in a single Git repository. This aligns with the amended ADR-0005: Decouple Backend Deployment.
-   **Alternatives considered**:
    -   Continue troubleshooting Vercel root-level monorepo configuration: Rejected due to excessive time consumption and complexity.
    -   Completely separate GitHub repositories: Rejected as the user's current deployment approach already involves Vercel projects targeting subdirectories, making a full repository separation unnecessary and adding overhead.
    -   Original monorepo approach with root `vercel.json`: Superseded by this decision and failed to deploy effectively.
