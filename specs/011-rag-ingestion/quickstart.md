# Quickstart: RAG Ingestion Engine (Backend Initialization)

This guide provides instructions to set up and run the local ingestion engine that processes Docusaurus content and uploads its vector embeddings to Qdrant Cloud.

## Prerequisites

1.  **Python 3.11+**: Ensure Python 3.11 or a later version is installed on your system.
2.  **API Keys**: You will need the following API keys, stored in a `.env` file at the project root:
    *   `GEMINI_API_KEY`: For Google Gemini Embeddings API.
    *   `QDRANT_URL`: The URL of your Qdrant Cloud instance.
    *   `QDRANT_API_KEY`: The API key for authenticating with Qdrant Cloud.
3.  **Project Structure**: This setup assumes the `frontend/docs/` directory exists and contains your Markdown/MDX content.

## Setup Instructions

1.  **Navigate to the project root**:
    ```bash
    cd /path/to/your/physical-ai-and-humanoid-robotics-textbook
    ```
2.  **Create the backend directory and virtual environment**:
    ```bash
    mkdir backend
    cd backend
    python3.11 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    Create a `requirements.txt` file in the `backend/` directory with the following content:
    ```
    qdrant-client
    google-generativeai
    python-dotenv
    markdown-it-py
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create the ingestion script**:
    Create a file named `ingest.py` in the `backend/` directory. (Content for this file will be provided in the implementation phase).

## Running the Ingestion

1.  **Ensure virtual environment is active**:
    ```bash
    cd /path/to/your/physical-ai-and-humanoid-robotics-textbook/backend
    source venv/bin/activate
    ```
2.  **Execute the ingestion script**:
    ```bash
    python ingest.py
    ```
    The script will process the Markdown files, generate embeddings, and upload them to your Qdrant Cloud instance. You should see progress and error logs in your terminal.

## Verification

*   Check your Qdrant Cloud instance to confirm that the `physical_ai_textbook` collection has been created and populated with data.
*   The script should print a message like "Successfully indexed X chunks." upon completion.
