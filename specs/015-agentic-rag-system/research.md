# Research: Agentic RAG System Migration

**Feature**: 015-agentic-rag-system
**Date**: 2026-01-21

## Research Tasks Completed

### 1. OpenAI Agents SDK Patterns

**Decision**: Use `@function_tool` decorator with `Agent` class and `Runner.run()` for async execution

**Rationale**:
- The OpenAI Agents SDK provides a clean abstraction for tool-calling agents
- `@function_tool` automatically generates JSON schemas for tool parameters
- `Runner.run()` handles the agent loop including tool execution
- Supports async/await natively for FastAPI integration

**Alternatives Considered**:
- LangChain Agents: More complex, heavier dependency, unnecessary abstraction for this use case
- Raw OpenAI function calling: Lower-level, would require manual loop management
- Haystack Agents: Good but less native OpenAI integration

**Best Practices**:
```python
from agents import Agent, Runner, function_tool

@function_tool
def search_textbook(query: str) -> str:
    """Search the textbook for relevant content."""
    # Tool implementation
    return formatted_context

agent = Agent(
    name="Tutor",
    instructions="You are a helpful tutor...",
    model="gpt-4o-mini",
    tools=[search_textbook],
)

# Async execution
result = await Runner.run(agent, user_message)
```

---

### 2. Hybrid Search Implementation

**Decision**: Use `rank-bm25` for sparse retrieval combined with Qdrant vector search via Reciprocal Rank Fusion (RRF)

**Rationale**:
- BM25 excels at exact keyword matching (technical terms like "Triad Architecture")
- Vector search captures semantic similarity (conceptual questions)
- RRF is parameter-free and well-studied for combining ranked lists
- Corpus size (64 chunks) is small enough for in-memory BM25

**Alternatives Considered**:
- Qdrant Sparse Vectors: Would require re-indexing, more complex setup
- Elasticsearch: Overkill for 64 documents, adds operational complexity
- Dense-only retrieval: Misses exact terminology matches

**Implementation Pattern**:
```python
from rank_bm25 import BM25Okapi

class HybridSearch:
    def __init__(self, documents: list[str]):
        tokenized = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query: str, vector_results: list, k: int = 10) -> list:
        # BM25 search
        bm25_scores = self.bm25.get_scores(query.lower().split())

        # Reciprocal Rank Fusion
        # RRF(d) = Σ 1/(k + rank(d)) for each ranking
        return self._rrf_fusion(vector_results, bm25_scores, k=60)
```

**RRF Formula**: `score(d) = Σ 1/(k + rank_i(d))` where k=60 (standard constant)

---

### 3. Semantic Chunking Strategy

**Decision**: Header-based chunking with token-count fallback (200-500 tokens per chunk)

**Rationale**:
- Markdown documents have natural structure (H2/H3 headers)
- Header boundaries align with conceptual boundaries in educational content
- Token-count fallback handles sections that are too long
- Preserves hierarchical context in metadata

**Alternatives Considered**:
- Fixed-size chunking: Breaks mid-sentence, loses context
- Sentence-based chunking: Too granular for educational content
- LLM-based chunking: Expensive, unnecessary given clear document structure

**Implementation Pattern**:
```python
def semantic_chunk(markdown: str, max_tokens: int = 500) -> list[Chunk]:
    sections = split_by_headers(markdown)  # H2/H3 boundaries
    chunks = []
    for section in sections:
        if count_tokens(section.content) > max_tokens:
            # Split long sections at paragraph boundaries
            sub_chunks = split_at_paragraphs(section.content, max_tokens)
            chunks.extend(sub_chunks)
        else:
            chunks.append(section)
    return chunks
```

---

### 4. Context Window Management

**Decision**: Score-based truncation with 4000 token budget for retrieved content

**Rationale**:
- gpt-4o-mini has 128K context but keeping retrieved content focused improves quality
- 4000 tokens leaves room for system prompt (~500) + agent reasoning (~1000) + response (~2500)
- Higher-relevance chunks preserved, lower-relevance truncated
- Simple token counting via `tiktoken`

**Alternatives Considered**:
- Summarization: Adds latency, may lose important details
- Map-reduce: Overkill for this scale
- No management: Risk of overwhelming context or truncation errors

**Implementation Pattern**:
```python
import tiktoken

class ContextManager:
    def __init__(self, budget: int = 4000):
        self.budget = budget
        self.encoder = tiktoken.encoding_for_model("gpt-4o-mini")

    def fit_to_budget(self, chunks: list[tuple[str, float]]) -> list[str]:
        """chunks is list of (content, relevance_score)"""
        # Sort by relevance descending
        sorted_chunks = sorted(chunks, key=lambda x: x[1], reverse=True)

        result = []
        used_tokens = 0
        for content, _ in sorted_chunks:
            chunk_tokens = len(self.encoder.encode(content))
            if used_tokens + chunk_tokens <= self.budget:
                result.append(content)
                used_tokens += chunk_tokens
        return result
```

---

### 5. Query Expansion Strategy

**Decision**: Agent-native reasoning (no separate tool)

**Rationale**:
- The agent can naturally consider query variations during its reasoning
- Adding explicit "expand_query" tool adds complexity without clear benefit
- Agent instructions can guide query reformulation behavior
- Multiple search calls possible if agent determines it's needed

**Implementation**: Update agent instructions to encourage query analysis:
```
When searching, consider:
- The exact terminology the user used
- Related concepts that might be relevant
- Alternative phrasings of the question
You may call search_textbook multiple times with different queries if needed.
```

---

### 6. Embedding Cache Strategy

**Decision**: LRU in-memory cache with `functools.lru_cache` or `cachetools`

**Rationale**:
- Dedicated server deployment allows persistent in-memory state
- Common queries (textbook concepts) will be repeated
- Embedding API calls are the primary latency source
- Simple implementation, no external cache service needed

**Alternatives Considered**:
- Redis cache: Adds operational complexity, unnecessary for this scale
- Disk cache: Slower than memory, unnecessary given server memory
- No cache: Higher latency, more API costs

**Implementation Pattern**:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_embedding(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        dimensions=768
    )
    return response.data[0].embedding
```

---

## Dependencies to Add

```toml
# pyproject.toml additions
dependencies = [
    # Existing...
    "rank-bm25>=0.2.2",      # BM25 sparse retrieval
    "tiktoken>=0.7.0",       # Token counting
    "cachetools>=5.5.0",     # LRU cache with TTL support
]

[project.optional-dependencies]
test = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
]
```

---

## Resolved Clarifications

| Original Unknown | Resolution | Source |
|-----------------|------------|--------|
| BM25 library choice | `rank-bm25` (simple, widely used) | PyPI research, RAG best practices |
| Hybrid fusion method | Reciprocal Rank Fusion (RRF) | Academic literature, industry standard |
| Token counting | `tiktoken` (OpenAI's library) | OpenAI documentation |
| Cache implementation | `lru_cache` or `cachetools` | Python stdlib + production patterns |
