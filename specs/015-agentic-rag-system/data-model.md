# Data Model: Agentic RAG System

**Feature**: 015-agentic-rag-system
**Date**: 2026-01-21

## Entity Relationship Diagram

```
┌─────────────────────┐
│   TextbookChunk     │
├─────────────────────┤
│ id: UUID            │
│ content: str        │
│ filepath: str       │
│ heading: str        │
│ position: int       │
│ parent_heading: str?│
│ token_count: int    │
│ embedding: [float]  │
└─────────────────────┘
         │
         │ retrieved by
         ▼
┌─────────────────────┐       ┌─────────────────────┐
│   SearchResult      │       │   StudentQuery      │
├─────────────────────┤       ├─────────────────────┤
│ chunk_id: UUID      │◀──────│ raw_text: str       │
│ content: str        │       │ sanitized_text: str │
│ heading: str        │       │ embedding: [float]  │
│ vector_score: float │       │ expanded_queries:   │
│ bm25_score: float   │       │   list[str]         │
│ hybrid_score: float │       │ timestamp: datetime │
│ source_type: enum   │       └─────────────────────┘
└─────────────────────┘
         │
         │ used to generate
         ▼
┌─────────────────────┐
│   AgentResponse     │
├─────────────────────┤
│ answer: str         │
│ sources: list[str]  │
│ tool_calls: list    │
│ latency_ms: int     │
│ tokens_used: int    │
└─────────────────────┘
```

## Entity Definitions

### TextbookChunk

A semantic unit of textbook content stored in Qdrant.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | UUID | Unique identifier (hash of filepath + content) | Primary key, deterministic |
| `content` | string | The chunk text content | 200-500 tokens target |
| `filepath` | string | Source markdown file path | Required |
| `heading` | string | Section heading (H2/H3) | Required |
| `position` | integer | Order within document | >= 0 |
| `parent_heading` | string? | Parent section (H2 for H3 chunks) | Optional |
| `token_count` | integer | Pre-computed token count | Required |
| `embedding` | float[768] | OpenAI text-embedding-3-small vector | Required |

**Storage**: Qdrant Cloud collection `physical_ai_textbook_v2`

---

### StudentQuery

A question submitted by a student through the chat interface.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `raw_text` | string | Original user input | Max 1000 chars |
| `sanitized_text` | string | Input after sanitization | Required |
| `embedding` | float[768] | Query embedding for vector search | Generated on-demand |
| `expanded_queries` | string[] | Agent-generated query variations | 0-3 items |
| `timestamp` | datetime | When query was received | UTC |

**Storage**: Not persisted (processed in-memory)

---

### SearchResult

A ranked retrieval result from hybrid search.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `chunk_id` | UUID | Reference to TextbookChunk | Foreign key |
| `content` | string | Chunk content (denormalized) | From chunk |
| `heading` | string | Section title for citation | From chunk |
| `vector_score` | float | Cosine similarity score | 0.0-1.0 |
| `bm25_score` | float | BM25 relevance score | >= 0 |
| `hybrid_score` | float | Combined RRF score | >= 0 |
| `source_type` | enum | Which search found it | VECTOR, BM25, BOTH |

**Storage**: Not persisted (computed per query)

---

### AgentResponse

The tutor agent's response to a student query.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `answer` | string | Generated educational response | Required |
| `sources` | string[] | Cited section titles | 0+ items |
| `tool_calls` | object[] | Log of tool invocations | For debugging |
| `latency_ms` | integer | End-to-end response time | >= 0 |
| `tokens_used` | integer | Total tokens consumed | >= 0 |

**Storage**: Logged for monitoring (not persisted to DB)

---

## Pydantic Models (Python)

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class SourceType(str, Enum):
    VECTOR = "vector"
    BM25 = "bm25"
    BOTH = "both"

class TextbookChunk(BaseModel):
    id: str
    content: str
    filepath: str
    heading: str
    position: int
    parent_heading: Optional[str] = None
    token_count: int

class StudentQuery(BaseModel):
    raw_text: str = Field(..., max_length=1000)
    sanitized_text: str
    embedding: Optional[list[float]] = None
    expanded_queries: list[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SearchResult(BaseModel):
    chunk_id: str
    content: str
    heading: str
    vector_score: float = 0.0
    bm25_score: float = 0.0
    hybrid_score: float = 0.0
    source_type: SourceType = SourceType.VECTOR

class AgentResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
    tool_calls: list[dict] = Field(default_factory=list)
    latency_ms: int = 0
    tokens_used: int = 0
```

---

## State Transitions

### Query Processing Flow

```
[Raw Input] ──sanitize──▶ [Sanitized] ──embed──▶ [With Embedding]
                                                       │
                               ┌───────────────────────┘
                               ▼
                    [Hybrid Search] ──RRF──▶ [Ranked Results]
                                                       │
                               ┌───────────────────────┘
                               ▼
                    [Context Manager] ──fit──▶ [Budgeted Context]
                                                       │
                               ┌───────────────────────┘
                               ▼
                    [Agent Reasoning] ──generate──▶ [Response]
```

### Chunk Lifecycle

```
[Markdown File] ──parse──▶ [Raw Sections] ──chunk──▶ [Semantic Chunks]
                                                           │
                                    ┌──────────────────────┘
                                    ▼
                          [Embed Batch] ──upsert──▶ [Qdrant Collection]
```

---

## Validation Rules

| Entity | Rule | Error Message |
|--------|------|---------------|
| StudentQuery | `len(raw_text) <= 1000` | "Query exceeds maximum length of 1000 characters" |
| StudentQuery | `len(sanitized_text) > 0` | "Query cannot be empty after sanitization" |
| TextbookChunk | `token_count >= 50` | "Chunk too small, likely incomplete" |
| TextbookChunk | `token_count <= 600` | "Chunk exceeds target size, should be split" |
| SearchResult | `0 <= vector_score <= 1` | "Invalid cosine similarity score" |
| AgentResponse | `len(answer) > 0` | "Agent must provide a response" |
