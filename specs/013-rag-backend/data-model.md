# Data Model: RAG Service

## Entities

### RAG Request
**Purpose**: Represents the user's natural language query.
**Location**: `backend/src/models/rag.py` (Proposed)

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `message` | `str` | Yes | The user's question. | Min length: 1, Max length: 1000 |

### RAG Response
**Purpose**: The synthesized answer and citations returned to the client.
**Location**: `backend/src/models/rag.py` (Proposed)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `answer` | `str` | Yes | The generated answer from the Agent. |
| `sources` | `List[str]` | Yes | List of unique citations (e.g., "Section 1.2: Hardware"). |

## Internal Service Objects

### SearchResult
**Purpose**: Normalized structure for Qdrant search hits.

| Field | Type | Description |
|-------|------|-------------|
| `text` | `str` | The content chunk. |
| `source_id` | `str` | Section ID (e.g., "section-1.2"). |
| `title` | `str` | Section Title (e.g., "The Nervous System"). |
