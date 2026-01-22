# Feature Specification: Agentic RAG System Migration

**Feature Branch**: `015-agentic-rag-system`
**Created**: 2026-01-21
**Status**: Draft
**Input**: User description: "Migrate Physical AI textbook chatbot from simple API-based RAG to OpenAI Agents SDK-powered agentic system with semantic chunking, hybrid search, query expansion, and context window management"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Asks Concept Question (Priority: P1)

A student using the Physical AI textbook chatbot asks a question about a robotics concept (e.g., "What is the Triad Architecture?"). The tutor agent analyzes the question, searches the textbook corpus using hybrid retrieval, and returns an educational explanation that cites specific textbook sections.

**Why this priority**: This is the core value proposition - students need accurate, well-sourced answers to learn from the textbook effectively. Without this working, the chatbot has no purpose.

**Independent Test**: Can be fully tested by asking any textbook-related question and verifying the response includes relevant content with source citations.

**Acceptance Scenarios**:

1. **Given** a student on the chat interface, **When** they ask "What is embodied cognition?", **Then** the agent searches the textbook, retrieves relevant sections, and responds with an explanation citing the source sections (e.g., "According to the Embodiment Thesis section...")
2. **Given** a student asks a question with technical terminology, **When** the hybrid search runs, **Then** both semantic similarity and keyword matching contribute to finding the exact terminology in the textbook
3. **Given** the agent retrieves multiple relevant chunks, **When** generating the response, **Then** it synthesizes information across sources rather than just quoting one chunk

---

### User Story 2 - Agent Handles Ambiguous Questions (Priority: P2)

A student asks an unclear or overly broad question (e.g., "Tell me about robots"). The agent recognizes the ambiguity and either asks a clarifying question or provides a high-level overview with suggestions for more specific topics to explore.

**Why this priority**: Real students often ask vague questions. The agent must handle these gracefully rather than returning irrelevant or overwhelming information.

**Independent Test**: Can be tested by asking intentionally vague questions and verifying the agent responds helpfully without hallucinating.

**Acceptance Scenarios**:

1. **Given** a student asks "What is AI?", **When** the query is too broad, **Then** the agent provides a brief overview and suggests specific textbook sections to explore (e.g., "The textbook covers several aspects of AI. Are you interested in embodied AI, physical intelligence, or humanoid control systems?")
2. **Given** a student asks a question with multiple interpretations, **When** the agent processes it, **Then** it uses query expansion to search for multiple phrasings and returns the most relevant combined results

---

### User Story 3 - Agent Admits Knowledge Boundaries (Priority: P2)

A student asks about a topic not covered in the textbook (e.g., "What is the latest Boston Dynamics robot?"). The agent honestly states that the textbook doesn't cover this topic rather than hallucinating an answer.

**Why this priority**: Trust is essential for educational tools. Students must know when information comes from the textbook versus when the agent is guessing.

**Independent Test**: Can be tested by asking questions about topics explicitly outside the textbook's scope and verifying honest "not covered" responses.

**Acceptance Scenarios**:

1. **Given** a student asks about current events or topics not in the textbook, **When** the search returns no relevant results, **Then** the agent responds honestly: "I couldn't find information about that in the textbook. The textbook focuses on [relevant scope]."
2. **Given** search results have very low relevance scores (below threshold), **When** generating a response, **Then** the agent acknowledges uncertainty rather than presenting low-confidence information as fact

---

### User Story 4 - Multi-Section Synthesis (Priority: P3)

A student asks a complex question that spans multiple chapters or concepts (e.g., "How do sensors and actuators work together in humanoid robots?"). The agent performs multiple searches, retrieves content from different sections, and synthesizes a coherent answer.

**Why this priority**: Advanced understanding requires connecting concepts across the textbook. This represents the full power of an agentic system over simple RAG.

**Independent Test**: Can be tested with cross-cutting questions and verifying the response draws from multiple textbook sections.

**Acceptance Scenarios**:

1. **Given** a student asks a question spanning sensors and actuators, **When** the agent reasons about the query, **Then** it performs searches for both concepts and synthesizes the results
2. **Given** retrieved chunks come from different chapters, **When** generating the response, **Then** the agent explains how the concepts relate and cites all relevant source sections

---

### User Story 5 - Long Context Management (Priority: P3)

A student asks a question that retrieves many relevant chunks (e.g., a fundamental concept mentioned throughout the textbook). The agent intelligently manages context to stay within token limits while preserving the most relevant information.

**Why this priority**: Without context management, the system either truncates important information or fails with token errors. This ensures reliability under all conditions.

**Independent Test**: Can be tested with questions known to retrieve many chunks and verifying responses remain coherent without errors.

**Acceptance Scenarios**:

1. **Given** a query retrieves 15 relevant chunks totaling 8000 tokens, **When** the context budget is 4000 tokens, **Then** the agent prioritizes chunks by relevance score and truncates lower-scoring chunks
2. **Given** context truncation occurs, **When** generating the response, **Then** the answer still addresses the question accurately using the retained high-relevance chunks

---

### Edge Cases

- What happens when the Qdrant vector database is temporarily unavailable? The agent returns a graceful error message asking the student to try again later
- How does the system handle extremely long student questions (>1000 characters)? The system truncates at 1000 characters and processes the truncated query
- What happens when a student sends rapid consecutive questions? Rate limiting (10 requests/minute) prevents abuse while maintaining responsiveness for normal use
- How does the agent handle questions in languages other than English? The agent responds in English, explaining the textbook content is in English
- What happens when embedding generation fails? The system retries with exponential backoff (3 attempts), then returns a friendly error message

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use the OpenAI Agents SDK to create a tutor agent with tool-use capabilities
- **FR-002**: Agent MUST have a `search_textbook` tool that queries the vector database for relevant content
- **FR-003**: System MUST implement hybrid search combining dense vector similarity (OpenAI embeddings) with sparse keyword matching (BM25)
- **FR-004**: Agent MUST perform query expansion by generating 2-3 reformulated search queries for ambiguous or complex questions
- **FR-005**: System MUST implement context window management that prioritizes chunks by relevance when total content exceeds 4000 tokens
- **FR-006**: Ingestion pipeline MUST produce semantic chunks (200-500 tokens) split at natural boundaries (headers, paragraphs, topic shifts)
- **FR-007**: Each chunk MUST include metadata: source filepath, section heading, hierarchical position in document
- **FR-008**: Agent MUST cite source sections in every response based on retrieved chunk metadata
- **FR-009**: System MUST maintain the existing `/api/chat` endpoint interface for frontend compatibility
- **FR-010**: System MUST log all agent tool invocations for debugging and monitoring
- **FR-011**: System MUST sanitize user inputs before passing to embedding APIs
- **FR-012**: System MUST implement connection pooling for the Qdrant client on the dedicated server
- **FR-013**: System MUST cache embeddings for repeated identical queries

### Key Entities

- **TextbookChunk**: A semantic unit of textbook content with associated metadata (content text, source filepath, section heading, hierarchical position, embedding vector)
- **StudentQuery**: A question submitted by a student (raw text, sanitized text, generated embedding, expanded query variants)
- **SearchResult**: A ranked retrieval result (chunk reference, relevance score, source type - vector/keyword/hybrid)
- **AgentResponse**: The tutor's answer (response text, cited sources, tool invocations log, processing metadata)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Students receive responses to textbook questions within 3 seconds (p95 latency)
- **SC-002**: Hybrid search returns measurably better results than pure vector search on a test set of 20 queries (measured by Mean Reciprocal Rank improvement of at least 15%)
- **SC-003**: Query expansion improves retrieval quality for at least 50% of ambiguous test queries (measured by human relevance judgment)
- **SC-004**: Agent successfully invokes search tool on 100% of factual textbook questions (verified by tool invocation logs)
- **SC-005**: Zero token overflow errors occur during normal operation (context management handles all cases)
- **SC-006**: 90% of student queries receive responses with at least one relevant source citation
- **SC-007**: System handles 50 concurrent users without degradation in response quality or latency
- **SC-008**: All existing frontend chat functionality continues working without modification

## Scope Boundaries

### In Scope

- Single tutor agent with multiple tools (search, future: quiz, concept map)
- Hybrid retrieval (vector + BM25)
- Query expansion via agent reasoning
- Context window management
- Semantic chunking in ingestion pipeline
- Dedicated server deployment with connection pooling and caching
- Comprehensive logging for debugging and monitoring

### Out of Scope (Future Features)

- Multi-agent orchestration with specialized sub-agents
- Persistent conversation memory across sessions
- User authentication and personalization
- Quiz generation functionality
- Real-time streaming responses
- Fine-tuned embedding models
- Multi-language support beyond English

## Assumptions

- Students have basic familiarity with the textbook's subject matter
- Questions are primarily in English
- The textbook content is static (no real-time updates during operation)
- OpenAI API rate limits are sufficient for expected traffic (50 concurrent users)
- Qdrant Cloud provides adequate availability for production use
- The dedicated server has sufficient memory for embedding caching
