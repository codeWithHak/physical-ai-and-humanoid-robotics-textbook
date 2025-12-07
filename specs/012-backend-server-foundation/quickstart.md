# Quickstart: RAG Backend - Phase 1 (Server Foundation) - Subdirectory Deployment

This guide provides instructions to set up and run the foundational FastAPI backend for the RAG system, locally and deployed to Vercel targeting the `backend/` subdirectory of this repository.

## Prerequisites

1.  **Python 3.12+**: Ensure Python 3.12 or a later version is installed on your system.
2.  **uv**: Ensure `uv` is installed for virtual environment and dependency management.
3.  **Vercel CLI**: For local Vercel deployments and management (`npm i -g vercel`).
4.  **Existing Backend Setup**: The `backend/` directory should exist with its `uv` virtual environment, as set up in the previous RAG Ingestion Engine feature.

## Setup Instructions (for the `backend/` subdirectory within this repository)

1.  **Navigate to the `backend/` directory**:
    ```bash
    cd /path/to/your/physical-ai-and-humanoid-robotics-textbook/backend
    ```
2.  **Activate the backend virtual environment**:
    ```bash
    source .venv/bin/activate
    ```
3.  **Update backend dependencies**:
    *   Ensure `backend/requirements.txt` includes:
        ```
        fastapi
        uvicorn
        mangum
        pydantic
        ```
    *   Install them using `uv`:
        ```bash
        uv pip install -r requirements.txt
        ```
4.  **Create API entry point**:
    *   Create the directory `backend/api/` (if not already created) and the file `backend/api/index.py` with the FastAPI application code (content for this file will be provided in the implementation phase).
5.  **Configure Vercel for the `backend/` project**:
    *   Create a `vercel.json` file *inside the `backend/` subdirectory* with the following content:
        ```json
        {
          "builds": [
            {
              "src": "api/index.py",
              "use": "@vercel/python",
              "config": { "maxLambdaSize": "15mb", "runtime": "python3.12" }
            }
          ],
          "routes": [
            {
              "src": "/(.*)",
              "dest": "api/index.py"
            }
          ]
        }
        ```
    *   **Note**: This `vercel.json` specifically configures the deployment when `backend/` is chosen as the "Root Directory" on Vercel.

## Running the Backend Locally (within the `backend/` subdirectory)

1.  **Ensure virtual environment is active**:
    ```bash
    cd /path/to/your/physical-ai-and-humanoid-robotics-textbook/backend
    source .venv/bin/activate
    ```
2.  **Start the FastAPI application**:
    ```bash
    uvicorn api.index:app --reload
    ```
3.  **Verify local endpoints**:
    Open your browser or use `curl`:
    *   `http://localhost:8000/` should return `{"status": "Physical AI API Ready"}`
    *   `http://localhost:8000/health` should return `200 OK`

## Deploying the Backend to Vercel (targeting the `backend/` subdirectory)

1.  **Ensure Vercel CLI is installed and logged in.**
2.  **Navigate to the `backend/` subdirectory**:
    ```bash
    cd /path/to/your/physical-ai-and-humanoid-robotics-textbook/backend
    ```
3.  **Initiate deployment**:
    ```bash
    vercel
    ```
    *   When prompted "Which directory should contain your project's source code?", select `.`.
    *   Follow the prompts to link to your *backend Vercel project* (e.g., `physical-ai-book-backend`).
4.  **Verify deployed endpoints**:
    Once deployed, get the URL for your backend project (e.g., `https://<backend-project-name>.vercel.app`).
    *   `https://<backend-project-name>.vercel.app/` should return `{"status": "Physical AI API Ready"}`
    *   `https://<backend-project-name>.vercel.app/health` should return `200 OK`

## Updating the Root of the Repository

1.  **Remove root `vercel.json`**: Delete the `vercel.json` file from the root of the repository (`/physical-ai-and-humanoid-robotics-textbook/vercel.json`) to avoid conflicts.
2.  **Frontend API Calls**: Update the Docusaurus frontend to call the deployed URL of your backend API.
