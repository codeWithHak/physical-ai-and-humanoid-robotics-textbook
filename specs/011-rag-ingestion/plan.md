# Implementation Plan: RAG Ingestion Engine (Backend Initialization)

**Branch**: `011-rag-ingestion` | **Date**: 2025-12-07 | **Spec**: [specs/011-rag-ingestion/spec.md](specs/011-rag-ingestion/spec.md)
**Input**: Feature specification from `specs/011-rag-ingestion/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature initializes the `backend/` directory and implements a local ETL (Extract, Transform, Load) script. This script will parse Docusaurus Markdown content from `frontend/docs/`, strip frontmatter, semantically chunk the content by H2/H3 headers, generate vector embeddings using Google Gemini's `embedding-001` model, and upload these embeddings to Qdrant Cloud into a collection named `physical_ai_textbook`. This forms the foundational data layer for the RAG chatbot.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: `qdrant-client`, `google-generativeai`, `python-dotenv`
**Storage**: Qdrant Cloud (Vector DB)
**Testing**: `pytest`
**Target Platform**: Linux/macOS (local execution)
**Project Type**: Backend Script (local ETL)
**Performance Goals**: Ingestion of approximately 15 Markdown files to complete within a few minutes.
**Constraints**: Local execution only; no deployment to Vercel for this script. Strict separation of Python code to `backend/` with no Python dependencies in `frontend/`.
**Scale/Scope**: Approximately 15 Markdown/MDX files will be processed from `../frontend/docs/`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   **The Triad Architecture**: PASS. This script provides the data preparation for the "AI Planner" component (RAG).
-   **Software-to-Hardware Causality**: PASS. Not directly applicable to this data preparation script.
-   **Tech Stack Isolation**: PASS. Uses specified Python, Qdrant, Gemini.
-   **Compute-Aware Deployment**: PASS. Script is for local execution ("Workstation Logic") and explicitly not deployed to Vercel.
-   **Workflow & Quality Standards (Code Style)**: PASS. Python type-hinting and PEP8 will be ensured during implementation.
-   **Global Constraints (Database)**: PASS. Uses Qdrant Cloud as specified.
-   **Global Constraints (Scope)**: PASS. Enables the RAG agent functionality by preparing the necessary data.

## Project Structure

### Documentation (this feature)

```text
specs/011-rag-ingestion/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
.
├── backend/
│   ├── venv/                 # Python virtual environment (ignored by git)
│   ├── requirements.txt      # Python dependencies
│   └── ingest.py             # Main ingestion script
├── frontend/                 # Existing Docusaurus frontend
│   └── docs/                 # Source of textbook content
└── .env                      # Environment variables for API keys
```

**Structure Decision**: A new `backend/` directory will be created at the repository root to house the Python ingestion script and its dependencies, maintaining strict separation from the existing Docusaurus `frontend/` structure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A