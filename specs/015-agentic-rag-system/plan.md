# Implementation Plan: Agentic RAG System Migration

**Branch**: `015-agentic-rag-system` | **Date**: 2026-01-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/015-agentic-rag-system/spec.md`

## Summary

Migrate the Physical AI textbook chatbot from a simple request-response RAG pipeline to an agentic architecture using the OpenAI Agents SDK. The agent will have tool-use capabilities for textbook search, implementing hybrid retrieval (vector + BM25), query expansion, semantic chunking, and context window management. Deployment targets a dedicated FastAPI server with connection pooling and embedding caching.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: FastAPI 0.124+, OpenAI Agents SDK (openai-agents 0.6+), Qdrant Client 1.16+, rank-bm25 (for sparse retrieval)
**Storage**: Qdrant Cloud (vector DB with `physical_ai_textbook_v2` collection)
**Testing**: pytest with pytest-asyncio for async agent tests
**Target Platform**: Dedicated Linux server (long-running process)
**Project Type**: Web application (backend API serving frontend)
**Performance Goals**: p95 latency <3 seconds, 50 concurrent users
**Constraints**: 4000 token context budget for retrieved content, gpt-4o-mini model limits
**Scale/Scope**: 64 textbook chunks indexed, ~50 concurrent users expected

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **Chatbot Backend**: FastAPI with OpenAI Agents/ChatKit SDKs | ✅ PASS | Using FastAPI + OpenAI Agents SDK as specified |
| **Database**: Qdrant Cloud (Vector DB) | ✅ PASS | Continuing to use Qdrant Cloud |
| **Code Style**: Python must be type-hinted and follow PEP8 | ✅ PASS | All new code will be type-hinted |
| **Documentation Strategy**: Use MCP Server for library docs | ✅ PASS | Will fetch OpenAI Agents SDK docs via context7 |
| **RAG Agent**: Chatbot answers questions, highlight+ask support | ✅ PASS | Core feature being enhanced |

**Gate Result**: PASS - No violations detected

## Project Structure

### Documentation (this feature)

```text
specs/015-agentic-rag-system/
├── plan.md              # This file
├── research.md          # Phase 0 output - technology decisions
├── data-model.md        # Phase 1 output - entity definitions
├── quickstart.md        # Phase 1 output - getting started guide
├── contracts/           # Phase 1 output - API contracts
│   └── chat-api.yaml    # OpenAPI spec for chat endpoint
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py                    # FastAPI app entry point
│   ├── api/
│   │   └── chat.py                # /api/chat endpoint (existing, updated)
│   ├── models/
│   │   └── rag.py                 # Request/Response models (existing)
│   └── services/
│       ├── agent_service.py       # OpenAI Agents SDK tutor (existing, enhanced)
│       ├── hybrid_search.py       # NEW: BM25 + vector fusion
│       ├── semantic_chunker.py    # NEW: Semantic chunking logic
│       └── context_manager.py     # NEW: Token budget management
├── ingest.py                      # Ingestion pipeline (existing, enhanced)
├── tests/
│   ├── test_agent.py              # Agent behavior tests
│   ├── test_hybrid_search.py      # Hybrid search tests
│   └── test_context_manager.py    # Context management tests
└── pyproject.toml                 # Dependencies (existing, updated)
```

**Structure Decision**: Existing web application structure retained. New services added under `backend/src/services/` following existing patterns.

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────────────────────────────────────┐
│   Frontend      │     │                    Backend                        │
│   (Docusaurus)  │────▶│  ┌─────────────────────────────────────────────┐  │
│                 │     │  │              AgentService                    │  │
└─────────────────┘     │  │  ┌─────────────────────────────────────────┐│  │
                        │  │  │         Tutor Agent (gpt-4o-mini)       ││  │
                        │  │  │  - Analyzes student questions           ││  │
                        │  │  │  - Decides when to search               ││  │
                        │  │  │  - Synthesizes educational responses    ││  │
                        │  │  └──────────────┬──────────────────────────┘│  │
                        │  │                 │ @function_tool             │  │
                        │  │  ┌──────────────▼──────────────────────────┐│  │
                        │  │  │         search_textbook()               ││  │
                        │  │  │  1. Query expansion (agent reasoning)   ││  │
                        │  │  │  2. Generate embedding                  ││  │
                        │  │  │  3. Hybrid search (vector + BM25)       ││  │
                        │  │  │  4. Context window management           ││  │
                        │  │  │  5. Return formatted context            ││  │
                        │  │  └──────────────┬──────────────────────────┘│  │
                        │  └─────────────────┼───────────────────────────┘  │
                        │                    │                              │
                        │  ┌─────────────────▼───────────────────────────┐  │
                        │  │              HybridSearch                    │  │
                        │  │  ┌───────────────┐  ┌───────────────────┐   │  │
                        │  │  │ Vector Search │  │   BM25 Search     │   │  │
                        │  │  │  (Qdrant)     │  │ (In-memory index) │   │  │
                        │  │  └───────┬───────┘  └─────────┬─────────┘   │  │
                        │  │          │    Reciprocal Rank │             │  │
                        │  │          └────────Fusion──────┘             │  │
                        │  └─────────────────────────────────────────────┘  │
                        └──────────────────────────────────────────────────┘
                                              │
                        ┌─────────────────────▼───────────────────────────┐
                        │              Qdrant Cloud                        │
                        │  Collection: physical_ai_textbook_v2            │
                        │  - 768-dim OpenAI embeddings                    │
                        │  - Metadata: filepath, heading, position        │
                        └─────────────────────────────────────────────────┘
```

## Key Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| BM25 Implementation | `rank-bm25` in-memory | Simple, no external service needed; corpus is small (64 chunks) |
| Hybrid Fusion | Reciprocal Rank Fusion (RRF) | Standard approach, parameter-free, works well in practice |
| Query Expansion | Agent reasoning (not separate tool) | Agent can naturally consider query variations during planning |
| Context Management | Score-based truncation | Preserves highest-relevance chunks within token budget |
| Semantic Chunking | Header-based with fallback | Markdown structure provides natural boundaries |
| Embedding Cache | LRU in-memory cache | Simple, effective for dedicated server deployment |

## Complexity Tracking

> No constitution violations requiring justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
