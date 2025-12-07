# Research: RAG Backend - Phase 2 (The Intelligence)

**Status**: Complete
**Date**: 2025-12-07

## Technical Context

**Language/Version**: Python 3.12
**Framework**: FastAPI
**Key Libraries**:
- `google-generativeai` (Embeddings)
- `qdrant-client` (Vector Search)
- `openai-agents-python` (Synthesis / Agent Logic)

## Decisions & Rationale

### 1. Agent Framework
- **Decision**: Use `openai-agents-python` SDK (v1.0+).
- **Rationale**: Explicitly requested by user. Provides a structured way to define agent persona ("Expert AI Robotics Professor") and instructions.
- **Alternatives Considered**: Direct OpenAI Chat Completions API (rejected per "Non-Goals"), LangChain (rejected per project stack constraints).

### 2. Embedding Model
- **Decision**: `embedding-001` via `google.generativeai`.
- **Rationale**: Consistent with the ingestion pipeline (`backend/ingest.py`). Using a different model would break retrieval compatibility.
- **Implementation**: Will adapt the existing `initialize_gemini_api` and embedding logic from `ingest.py` into a reusable pattern or service method.

### 3. Vector Database Interaction
- **Decision**: `qdrant-client` with payload extraction.
- **Rationale**: Matches the ingestion schema.
- **Pattern**:
  ```python
  results = client.search(
      collection_name="physical_ai_textbook",
      query_vector=embedding,
      limit=5
  )
  # Extract payload.source and payload.header
  ```

### 4. Error Handling Strategy
- **Decision**: "Fail Gracefully" with Service Degradation.
- **Rationale**: If Qdrant is down, the user should know "I can't search the book right now" rather than seeing a 500 server error.
- **Mechanism**:
  - `try/except` blocks around external API calls.
  - Return HTTP 503 for upstream failures.
  - Return HTTP 200 with fallback text if search returns empty (as per "Context not found" logic).

## Open Questions Resolved

- **Authentication**: Usage of `.env` variables (`GEMINI_API_KEY`, `QDRANT_API_KEY`, `OPENAI_API_KEY`) is standard and confirmed by `ingest.py` presence.
- **Request/Response Format**: JSON structure defined in Spec is compatible with Pydantic models.
