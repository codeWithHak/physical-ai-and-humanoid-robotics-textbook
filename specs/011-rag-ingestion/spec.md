# Feature Specification: RAG Ingestion Engine (Backend Initialization)

**Feature Branch**: `011-rag-ingestion`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User description: "Feature: RAG Ingestion Engine (Backend Init) Intent: Initialize the `backend/` directory and create the \"Ingestion Engine\" script. This script acts as a local ETL tool to parse the Docusaurus content and upload vector embeddings to Qdrant Cloud. Feature Scope (Structure & Logic): 1. Directory Architecture: - Create a root-level folder `backend/`. - Create `backend/venv/` (instruction to ignore in git). - Create `backend/requirements.txt` (Dependencies: `qdrant-client`, `google-generativeai`, `python-dotenv`). 2. The Ingestion Script (`backend/ingest.py`): - **Input:** Reads Markdown files from `../frontend/docs/`. - **Processing:** - Strip Frontmatter. - \"Semantic Chunking\": Split by H2/H3 headers. - **Output:** - Generate embeddings via Google Gemini (`models/embedding-001`). - Upload to Qdrant Cloud (Collection: `physical_ai_textbook`). 3. Configuration: - Use `python-dotenv` to load keys from a `.env` file in the root. Success Criteria (SMART): - Separation: All Python code lives strictly in `backend/`. No Python files in `frontend/`. - Execution: Running `cd backend && python ingest.py` populates Qdrant. - Verification: The script prints \"Successfully indexed X chunks.\" Non-Goals: - NOT deploying this script to Vercel (it runs locally). - NOT building the FastAPI server yet (that is the next feature). User Stories: - \"As a developer, I want a clean `backend` folder so my frontend deployment doesn't break due to Python errors.\""

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Local Content Ingestion (Priority: P1)

As a developer, I want to initialize a `backend/` directory and run an ingestion script locally to process Docusaurus content and upload its vector embeddings to Qdrant Cloud.

**Why this priority**: This is the foundational step for the entire RAG system. Without content ingestion, the chatbot cannot function.

**Independent Test**: The script can be run locally, and its output (success message, populated Qdrant collection) can be verified independently of any frontend or chatbot UI.

**Acceptance Scenarios**:

1.  **Given** the `backend/` directory is set up with `ingest.py` and `requirements.txt`, **When** I run `cd backend && python ingest.py`, **Then** the script executes without errors and prints "Successfully indexed X chunks."
2.  **Given** the `ingest.py` script runs successfully, **When** I check the Qdrant Cloud instance, **Then** a collection named `physical_ai_textbook` exists and contains vector embeddings of the Docusaurus content.
3.  **Given** the project structure, **When** I inspect the `frontend/` directory, **Then** no Python-related files or dependencies are present.

### Edge Cases

-   What happens if there are no Markdown files in `../frontend/docs/`? (Script should handle gracefully, e.g., print "No documents found").
-   How does the system handle malformed Markdown files or files without frontmatter? (Script should ideally skip or log errors without crashing).
-   What happens if Qdrant is unreachable or API keys are invalid? (Script should report connection/authentication errors).

## Clarifications

### Session 2025-12-07

- Q: How should individual document chunks be uniquely identified in Qdrant, especially to handle re-ingestion and updates effectively? → A: Use a deterministic UUID generated from a SHA-256 hash of the file path and content.
- Q: What are the approximate expected number of Markdown files and the total volume (in MB or GB) of content for the textbook that will be ingested? → A: Approx 15 MDX files in /docs.
- Q: What level of detail and format is expected for logging errors and progress from the ingestion script? (e.g., just critical errors, detailed debug info, structured logs?) → A: Log critical errors and a summary of progress (e.g., number of files processed, chunks indexed).
- Q: How should the ingestion script handle potential rate limits or transient errors from the Google Gemini Embeddings API? → A: Stop and report an error immediately upon encountering a rate limit or API error.
- Q: Beyond splitting by H2/H3 headers, are there any additional rules for chunking (e.g., max chunk size in tokens/words, overlap between chunks) to optimize for RAG quality? → A: No additional rules; rely solely on H2/H3 splitting.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST create a root-level directory named `backend/`.
-   **FR-002**: The `backend/` directory MUST contain a `venv/` directory, which MUST be ignored by Git.
-   **FR-003**: The `backend/` directory MUST contain a `requirements.txt` file listing `qdrant-client`, `google-generativeai`, and `python-dotenv` as dependencies.
-   **FR-004**: The `backend/` directory MUST contain an ingestion script named `ingest.py`.
-   **FR-005**: The `ingest.py` script MUST read Markdown files from `../frontend/docs/`.
-   **FR-006**: The `ingest.py` script MUST strip frontmatter from the Markdown files during processing.
-   **FR-007**: The `ingest.py` script MUST perform "Semantic Chunking" by splitting content by H2/H3 headers, with no additional rules for max chunk size, overlap, or further splitting.
-   **FR-008**: The `ingest.py` script MUST generate embeddings for the chunks using the Google Gemini model (`models/embedding-001`).
-   **FR-009**: The `ingest.py` script MUST upload the generated embeddings to Qdrant Cloud into a collection named `physical_ai_textbook`.
-   **FR-010**: The `ingest.py` script MUST load API keys and other configurations from a `.env` file located in the project root, using `python-dotenv`.
-   **FR-011**: All Python code related to this feature MUST reside strictly within the `backend/` directory.
-   **FR-012**: The `ingest.py` script MUST log critical errors and provide a summary of progress (e.g., number of files processed, chunks indexed) to stdout.
-   **FR-013**: The `ingest.py` script MUST stop execution and report an error immediately upon encountering a rate limit or any other API error from the Google Gemini Embeddings API.

-   **Document Chunk**: A segment of the textbook content, semantically coherent, typically delimited by H2/H3 headers. Its unique identifier in Qdrant MUST be a deterministic UUID generated from a SHA-256 hash of its source file path and content, ensuring idempotency.
-   **Vector Embedding**: A numerical representation of a Document Chunk, generated by the Google Gemini model, used for similarity search in Qdrant.
-   **Qdrant Collection**: A named store within Qdrant Cloud (`physical_ai_textbook`) to hold the vector embeddings and associated payload data.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: The `backend/` directory and its contents (`venv/`, `requirements.txt`, `ingest.py`) are created correctly and follow the specified architecture.
-   **SC-002**: Running `cd backend && python ingest.py` successfully executes the script without errors.
-   **SC-003**: Upon successful execution, the `ingest.py` script prints a confirmation message, including the number of indexed chunks (e.g., "Successfully indexed X chunks.").
-   **SC-004**: The `physical_ai_textbook` collection in Qdrant Cloud is successfully created and populated with vector embeddings derived from the Docusaurus content.
-   **SC-005**: The `frontend/` directory remains free of any Python-related code or dependencies after this feature's implementation.