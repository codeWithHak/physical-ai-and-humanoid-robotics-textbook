# Data Model: RAG Backend - Phase 1 (Server Foundation)

This document describes the key conceptual entities related to the server foundation setup.

## Entities

### FastAPI Application

-   **Description**: The core Python web service that will handle incoming API requests.
-   **Key Characteristics**:
    -   Initialized as a `FastAPI` instance.
    -   Configured with middleware for Cross-Origin Resource Sharing (CORS).
    -   Exposes basic endpoints for status and health checks.

### CORS Middleware

-   **Description**: A component integrated into the FastAPI application responsible for enforcing Cross-Origin Resource Sharing policies.
-   **Key Characteristics**:
    -   Allows requests from specific origins: `http://localhost:3000` (development) and `https://physical-ai-and-humanoid-robotics-h.vercel.app/` (production).
    -   Permits common HTTP methods (GET, POST, PUT, DELETE, etc.) and headers required for API interaction.

### Vercel Configuration (`vercel.json`)

-   **Description**: A configuration file located at the project root, used by Vercel to define the monorepo's build and routing behavior.
-   **Key Characteristics**:
    -   Defines the Python build for the `backend/` directory.
    -   Routes requests matching `/api/*` to the FastAPI serverless function.
    -   Routes all other requests (e.g., `/`, `/docs`) to the Docusaurus frontend build.
