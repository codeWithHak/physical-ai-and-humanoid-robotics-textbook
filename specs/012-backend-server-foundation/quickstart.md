# Quickstart: RAG Backend - Phase 1 (Server Foundation)

This guide provides instructions to set up and run the foundational FastAPI backend for the RAG system, locally and deployed on Vercel.

## Prerequisites

1.  **Python 3.12+**: Ensure Python 3.12 or a later version is installed on your system.
2.  **uv**: Ensure `uv` is installed for virtual environment and dependency management.
3.  **Vercel CLI**: For local Vercel deployments and management (`npm i -g vercel`).
4.  **Existing Backend Setup**: The `backend/` directory should exist with its `uv` virtual environment, as set up in the previous RAG Ingestion Engine feature.

## Setup Instructions

1.  **Navigate to the project root**:
    ```bash
    cd /path/to/your/physical-ai-and-humanoid-robotics-textbook
    ```
2.  **Activate the backend virtual environment**:
    ```bash
    cd backend
    source .venv/bin/activate
    ```
3.  **Update backend dependencies**:
    Update `backend/requirements.txt` by adding the new dependencies:
    ```
    fastapi
    uvicorn
    mangum
    pydantic
    ```
    Then install them using `uv`:
    ```bash
    uv pip install -r requirements.txt
    ```
4.  **Create API entry point**:
    Create the directory `backend/api/` and the file `backend/api/index.py` with the FastAPI application code (content for this file will be provided in the implementation phase).
5.  **Configure Vercel**:
    Create or update `vercel.json` at the project root (content for this file will be provided in the implementation phase).

## Running the Backend Locally

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

## Deploying to Vercel

1.  **Ensure Vercel CLI is installed and logged in.**
2.  **From the project root, initiate deployment:**
    ```bash
    vercel
    ```
    Follow the prompts to deploy. This will build both your Docusaurus frontend and FastAPI backend.
3.  **Verify deployed endpoints**:
    Once deployed, access your Vercel project's API URL (e.g., `https://<your-project-name>.vercel.app/api`).
    *   `https://<your-project-name>.vercel.app/api` should return `{"status": "Physical AI API Ready"}`
    *   `https://<your-project-name>.vercel.app/api/health` should return `200 OK`
