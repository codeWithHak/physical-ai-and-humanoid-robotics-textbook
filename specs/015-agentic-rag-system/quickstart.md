# Quickstart: Agentic RAG System

**Feature**: 015-agentic-rag-system
**Date**: 2026-01-21

## Prerequisites

- Python 3.12+
- UV package manager
- OpenAI API key
- Qdrant Cloud account with API key

## Environment Setup

1. **Clone and navigate to backend**:
```bash
cd backend
```

2. **Create `.env` file** (if not exists):
```bash
OPENAI_API_KEY=sk-your-openai-key
QDRANT_URL=https://your-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key
```

3. **Install dependencies**:
```bash
uv sync
```

## Running the System

### Option 1: Development Server
```bash
uv run uvicorn src.main:app --reload --port 8000
```

### Option 2: Production Server
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing the API

### Health Check
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Agent Service (OpenAI)",
  "checks": {
    "openai": "configured",
    "qdrant_url": "configured",
    "qdrant_api_key": "configured"
  }
}
```

### Chat Query
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the Triad Architecture?"}'
```

Expected response:
```json
{
  "answer": "The Triad Architecture is a framework that...",
  "sources": ["The Triad Architecture", "Human Intent Layer"]
}
```

## Re-indexing Content

If textbook content changes, re-run the ingestion pipeline:

```bash
uv run python ingest.py
```

This will:
1. Parse all markdown files in `frontend/docs/`
2. Create semantic chunks (200-500 tokens each)
3. Generate embeddings with OpenAI
4. Upsert to Qdrant collection `physical_ai_textbook_v2`

## Troubleshooting

### "No relevant content found"
- Check similarity threshold in `agent_service.py` (should be ~0.25 for OpenAI embeddings)
- Verify collection has data: Check Qdrant dashboard

### 403 Forbidden from Qdrant
- API key may have expired
- Generate new key from Qdrant Cloud dashboard
- Update `.env` file

### Slow responses (>3s)
- Check OpenAI API status
- Consider enabling embedding cache
- Verify network connectivity to Qdrant

### Agent not using search tool
- Check agent instructions in `agent_service.py`
- Ensure tool is properly registered with `@function_tool`

## Architecture Overview

```
Student Question
       │
       ▼
┌──────────────┐
│ AgentService │
│   (tutor)    │
└──────┬───────┘
       │ @function_tool
       ▼
┌──────────────┐
│search_textbook│
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│Vector Search │────▶│  Hybrid RRF  │
│  (Qdrant)    │     │   Fusion     │
└──────────────┘     └──────┬───────┘
                            │
┌──────────────┐            │
│ BM25 Search  │────────────┘
│ (in-memory)  │
└──────────────┘
       │
       ▼
┌──────────────┐
│   Context    │
│   Manager    │
└──────┬───────┘
       │
       ▼
  Agent Response
```

## Key Files

| File | Purpose |
|------|---------|
| `backend/src/services/agent_service.py` | OpenAI Agents SDK tutor agent |
| `backend/src/services/hybrid_search.py` | BM25 + vector fusion |
| `backend/src/services/context_manager.py` | Token budget management |
| `backend/src/api/chat.py` | FastAPI endpoint |
| `backend/ingest.py` | Document ingestion pipeline |

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement hybrid search service
3. Add semantic chunking to ingestion
4. Implement context management
5. Write tests for each component
