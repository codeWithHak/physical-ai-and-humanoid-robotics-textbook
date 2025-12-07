# Feature Specification: RAG Backend - Phase 2 (The Intelligence)

**Feature Branch**: `013-rag-backend`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User description provided via CLI.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Query (Priority: P1)

As a student reading the textbook, I want to ask natural language questions about the content (e.g., "What GPU do I need?") so that I receive an immediate, accurate answer based specifically on the textbook material, complete with citations to the relevant sections.

**Why this priority**: Core value proposition of the "Intelligence" phase; enables the interactive learning experience.

**Independent Test**: Can be tested by sending a POST request to `/api/chat` with a known question from Chapter 1 and verifying the response contains the correct text and citations.

**Acceptance Scenarios**:

1. **Given** the RAG service is operational, **When** a student asks "How do I install ROS?", **Then** the system returns a JSON response containing a natural language answer derived from the textbook and a list of source citations (e.g., "Section 2.1").
2. **Given** a question about a topic *not* in the textbook (e.g., "Who won the 1994 World Cup?"), **When** the query is processed, **Then** the system responds with "I cannot find that in the textbook" as per the system prompt instructions.
3. **Given** the Qdrant vector database is unreachable, **When** a query is submitted, **Then** the API returns a graceful error message (e.g., 503 Service Unavailable or specific JSON error) instead of a raw 500 server crash.

### Edge Cases

- **Empty/Malicious Input**: What happens when the user sends an empty string or a very long nonsense string? (System should validate input and return 400 Bad Request).
- **No Context Found**: Qdrant returns 0 results (System should return the "I cannot find that..." fallback response).
- **API Rate Limits**: Google Embedding or OpenAI API limits reached (System should handle upstream 429 errors gracefully).

## Requirements *(mandatory)*

### Functional Requirements

#### Service Module (`backend/services/rag_service.py`)

- **FR-001**: The system MUST use `google.generativeai` (model: `embedding-001`) to generate vector embeddings for incoming user queries.
- **FR-002**: The system MUST use `qdrant_client` to search the `physical_ai_textbook` collection using the generated query embedding.
  - *Constraint*: Search must limit results to the top 5 chunks (`limit=5`).
  - *Constraint*: Search must extract `payload.source` and `payload.header` fields for citation purposes.
- **FR-003**: The system MUST use the `openai-agents` library (specifically `Agent` and `Runner` classes) to synthesize the final answer.
  - *Constraint*: Must use the `gpt-4o-mini` model.
  - *Constraint*: Must NOT use the experimental OpenAI Assistants API.
- **FR-004**: The Agent MUST use the following System Prompt: *"You are an expert AI Robotics Professor. Answer based ONLY on the provided context. If the answer is not in the context, say 'I cannot find that in the textbook'. Always cite the section title."*

#### API Endpoint (`backend/api/chat.py`)

- **FR-005**: The system MUST expose a `POST /api/chat` endpoint.
- **FR-006**: The endpoint MUST accept a JSON payload: `{ "message": "string" }`.
- **FR-007**: The endpoint MUST return a JSON payload: `{ "answer": "string", "sources": ["string"] }`.
- **FR-008**: The endpoint MUST handle downstream service failures (Qdrant, OpenAI, Google) by returning a structured error response, ensuring the application does not crash.

### Key Entities

- **Query**: The natural language question from the user.
- **Context Chunk**: A piece of text retrieved from Qdrant, containing `text`, `source` (Section ID), and `header` (Section Title).
- **RAG Response**: The synthesized answer and list of citations returned to the client.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Latency**: The full RAG pipeline (Embedding generation -> Vector Search -> LLM Synthesis) completes in under 5 seconds for standard queries (defined as < 100 words).
- **SC-002**: **Accuracy**: Queries specific to "Chapter 1" content return answers derived *exclusively* from the textbook data, verified by the presence of correct "Section X.Y" citations.
- **SC-003**: **Robustness**: In the event of a Qdrant connection failure, 100% of requests return a controlled error code (e.g., 503) rather than an unhandled 500 Internal Server Error.