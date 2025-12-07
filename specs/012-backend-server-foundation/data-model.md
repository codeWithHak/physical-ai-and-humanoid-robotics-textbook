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

### Vercel Configuration (Backend `vercel.json`)

-   **Description**: A configuration file within the `backend/` subdirectory (of this repository) that defines how the FastAPI application is built and deployed as an independent Vercel project targeting that subdirectory.
-   **Key Characteristics**:
    -   Defines the Python build for the FastAPI application.
    -   Routes requests to the FastAPI serverless function.

