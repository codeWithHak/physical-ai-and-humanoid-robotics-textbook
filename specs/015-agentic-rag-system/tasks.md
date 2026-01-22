# Tasks: Agentic RAG System Migration

**Input**: Design documents from `/specs/015-agentic-rag-system/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in spec - test tasks omitted. Add tests post-MVP if needed.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Ingestion**: `backend/ingest.py`
- **Config**: `backend/pyproject.toml`, `backend/.env`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add new dependencies and prepare project structure

- [X] T001 Add `rank-bm25>=0.2.2` dependency in backend/pyproject.toml
- [X] T002 [P] Add `tiktoken>=0.7.0` dependency in backend/pyproject.toml
- [X] T003 [P] Add `cachetools>=5.5.0` dependency in backend/pyproject.toml
- [X] T004 Run `uv sync` to install new dependencies
- [X] T005 [P] Create backend/src/services/__init__.py if not exists

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core services that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Hybrid Search Service

- [X] T006 Create HybridSearch class with BM25 initialization in backend/src/services/hybrid_search.py
- [X] T007 Implement BM25 search method in backend/src/services/hybrid_search.py
- [X] T008 Implement Reciprocal Rank Fusion (RRF) method in backend/src/services/hybrid_search.py
- [X] T009 Implement hybrid_search() combining vector + BM25 results in backend/src/services/hybrid_search.py

### Context Manager Service

- [X] T010 [P] Create ContextManager class with tiktoken encoder in backend/src/services/context_manager.py
- [X] T011 [P] Implement fit_to_budget() method for score-based truncation in backend/src/services/context_manager.py
- [X] T012 [P] Implement count_tokens() utility function in backend/src/services/context_manager.py

### Semantic Chunker Service

- [X] T013 [P] Create SemanticChunker class in backend/src/services/semantic_chunker.py
- [X] T014 [P] Implement split_by_headers() for H2/H3 boundaries in backend/src/services/semantic_chunker.py
- [X] T015 [P] Implement split_at_paragraphs() fallback for long sections in backend/src/services/semantic_chunker.py
- [X] T016 Implement semantic_chunk() orchestration method in backend/src/services/semantic_chunker.py

### Embedding Cache

- [X] T017 Implement LRU cached embedding function in backend/src/services/agent_service.py

### Enhanced Data Models

- [X] T018 [P] Add SourceType enum to backend/src/models/rag.py
- [X] T019 [P] Add SearchResult model with hybrid scores to backend/src/models/rag.py
- [X] T020 [P] Add TextbookChunk model with position/parent_heading to backend/src/models/rag.py

**Checkpoint**: Foundation ready - HybridSearch, ContextManager, SemanticChunker services operational

---

## Phase 3: User Story 1 - Student Asks Concept Question (Priority: P1) 🎯 MVP

**Goal**: Students can ask textbook questions and receive accurate, cited responses via hybrid search

**Independent Test**: Ask "What is the Triad Architecture?" and verify response includes relevant content with source citations

### Implementation for User Story 1

- [X] T021 [US1] Integrate HybridSearch into search_textbook() tool in backend/src/services/agent_service.py
- [X] T022 [US1] Load BM25 corpus from Qdrant collection at service startup in backend/src/services/agent_service.py
- [X] T023 [US1] Update search_textbook() to use hybrid search instead of vector-only in backend/src/services/agent_service.py
- [X] T024 [US1] Integrate ContextManager to fit results within 4000 token budget in backend/src/services/agent_service.py
- [X] T025 [US1] Update agent instructions to encourage source citation in backend/src/services/agent_service.py
- [X] T026 [US1] Improve _extract_sources_from_result() to parse source citations in backend/src/services/agent_service.py
- [X] T027 [US1] Add tool invocation logging for debugging in backend/src/services/agent_service.py

**Checkpoint**: User Story 1 complete - core Q&A with hybrid search and citations working

---

## Phase 4: User Story 2 - Agent Handles Ambiguous Questions (Priority: P2)

**Goal**: Agent gracefully handles vague questions with suggestions for specific topics

**Independent Test**: Ask "What is AI?" and verify agent provides overview with topic suggestions

### Implementation for User Story 2

- [X] T028 [US2] Update agent instructions with query analysis guidance in backend/src/services/agent_service.py
- [X] T029 [US2] Add instruction for suggesting specific textbook sections in backend/src/services/agent_service.py
- [X] T030 [US2] Enable multiple search_textbook() calls for query expansion in agent instructions in backend/src/services/agent_service.py

**Checkpoint**: User Story 2 complete - ambiguous questions handled gracefully

---

## Phase 5: User Story 3 - Agent Admits Knowledge Boundaries (Priority: P2)

**Goal**: Agent honestly states when textbook doesn't cover a topic

**Independent Test**: Ask "What is the latest Boston Dynamics robot?" and verify honest "not in textbook" response

### Implementation for User Story 3

- [X] T031 [US3] Update agent instructions with knowledge boundary guidance in backend/src/services/agent_service.py
- [X] T032 [US3] Add low-score threshold handling in search_textbook() to return "no relevant content" in backend/src/services/agent_service.py
- [X] T033 [US3] Update search_textbook() to include confidence indicators in returned context in backend/src/services/agent_service.py

**Checkpoint**: User Story 3 complete - agent honestly admits textbook limitations

---

## Phase 6: User Story 4 - Multi-Section Synthesis (Priority: P3)

**Goal**: Agent synthesizes answers from multiple textbook sections for complex questions

**Independent Test**: Ask "How do sensors and actuators work together?" and verify response draws from multiple sections

### Implementation for User Story 4

- [X] T034 [US4] Update agent instructions to encourage multi-concept search and synthesis in backend/src/services/agent_service.py
- [X] T035 [US4] Ensure search_textbook() returns diverse results (not just top-scoring from one section) in backend/src/services/agent_service.py
- [X] T036 [US4] Update source citation to handle multiple sections from different chapters in backend/src/services/agent_service.py

**Checkpoint**: User Story 4 complete - complex questions synthesized from multiple sources

---

## Phase 7: User Story 5 - Long Context Management (Priority: P3)

**Goal**: System handles queries that retrieve many chunks without token overflow

**Independent Test**: Ask about a fundamental concept and verify coherent response without errors

### Implementation for User Story 5

- [X] T037 [US5] Add defensive token budget check before agent call in backend/src/services/agent_service.py
- [X] T038 [US5] Log context truncation events for monitoring in backend/src/services/agent_service.py
- [X] T039 [US5] Add fallback if context still exceeds budget (emergency truncation) in backend/src/services/agent_service.py

**Checkpoint**: User Story 5 complete - large context handled reliably

---

## Phase 8: Enhanced Ingestion Pipeline

**Purpose**: Upgrade ingestion to use semantic chunking with richer metadata

- [X] T040 Integrate SemanticChunker into ingest.py replacing current chunking logic in backend/ingest.py
- [X] T041 Add token_count field to chunk metadata in backend/ingest.py
- [X] T042 Add position field to chunk metadata for document ordering in backend/ingest.py
- [X] T043 Add parent_heading field for H3 chunks under H2 sections in backend/ingest.py
- [X] T044 Re-run ingestion to update Qdrant collection with enhanced chunks

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, logging, and production readiness

- [X] T045 [P] Add input sanitization to StudentQuery processing in backend/src/services/agent_service.py
- [X] T046 [P] Add rate limiting check before processing in backend/src/api/chat.py
- [X] T047 [P] Add exponential backoff retry for embedding generation in backend/src/services/agent_service.py
- [X] T048 [P] Add Qdrant connection pooling configuration in backend/src/services/agent_service.py
- [X] T049 Update health check to verify HybridSearch and ContextManager status in backend/src/api/chat.py
- [X] T050 Run quickstart.md validation with manual testing

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← BLOCKS all user stories
    ↓
┌───────────────────────────────────────────────────┐
│ Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3)    │ (Sequential by priority)
│       ↓              ↓              ↓              │
│ Phase 6 (US4) → Phase 7 (US5)                    │
└───────────────────────────────────────────────────┘
    ↓
Phase 8 (Enhanced Ingestion) ← Can run after US1 MVP
    ↓
Phase 9 (Polish)
```

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (P1) | Foundational | Phase 2 complete |
| US2 (P2) | US1 (builds on agent instructions) | T027 complete |
| US3 (P2) | US1 (builds on search behavior) | T027 complete |
| US4 (P3) | US1, US3 (multi-source retrieval) | T033 complete |
| US5 (P3) | US1 (context manager already integrated) | T027 complete |

### Within Foundational Phase (Phase 2)

- T006-T009 (HybridSearch): Sequential - class → methods → orchestration
- T010-T012 (ContextManager): Can run in parallel with HybridSearch
- T013-T016 (SemanticChunker): Can run in parallel with HybridSearch
- T017-T020 (Cache & Models): Can run in parallel

### Parallel Opportunities

```bash
# Phase 2 parallelization (3 parallel tracks):
Track A: T006 → T007 → T008 → T009 (HybridSearch)
Track B: T010, T011, T012 (ContextManager - all [P])
Track C: T013, T014, T015 → T016 (SemanticChunker)
Track D: T017, T018, T019, T020 (Cache & Models - all [P])

# Phase 9 parallelization:
T045, T046, T047, T048 (all [P] - different files)
```

---

## Parallel Example: Foundational Phase

```bash
# Launch in parallel after T005:
Task: "Create HybridSearch class in backend/src/services/hybrid_search.py"
Task: "Create ContextManager class in backend/src/services/context_manager.py"
Task: "Create SemanticChunker class in backend/src/services/semantic_chunker.py"
Task: "Implement LRU cached embedding in backend/src/services/agent_service.py"
Task: "Add SourceType enum to backend/src/models/rag.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T020)
3. Complete Phase 3: User Story 1 (T021-T027)
4. **STOP and VALIDATE**: Test with "What is the Triad Architecture?"
5. Deploy if ready - this is the core value

### Incremental Delivery

| Milestone | Stories Complete | Value Delivered |
|-----------|------------------|-----------------|
| MVP | US1 | Core Q&A with hybrid search, citations |
| v1.1 | US1, US2, US3 | Graceful handling of edge cases |
| v1.2 | US1-US5 | Full robustness for complex queries |
| v1.3 | All + Ingestion | Production-ready with enhanced chunking |

### Recommended Sequence

1. **Day 1**: T001-T005 (Setup)
2. **Day 2**: T006-T020 (Foundational - parallel where marked)
3. **Day 3**: T021-T027 (US1 MVP) → **TEST & VALIDATE**
4. **Day 4**: T028-T039 (US2-US5)
5. **Day 5**: T040-T050 (Ingestion + Polish)

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|----------------------|
| Phase 1: Setup | 5 | T002, T003, T005 |
| Phase 2: Foundational | 15 | T010-T012, T013-T015, T017-T020 |
| Phase 3: US1 (MVP) | 7 | - |
| Phase 4: US2 | 3 | - |
| Phase 5: US3 | 3 | - |
| Phase 6: US4 | 3 | - |
| Phase 7: US5 | 3 | - |
| Phase 8: Ingestion | 5 | - |
| Phase 9: Polish | 6 | T045-T048 |
| **Total** | **50** | **~20 parallelizable** |

---

## Notes

- [P] tasks = different files, no dependencies
- [USx] label maps task to specific user story
- Each user story should be independently testable after completion
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
- MVP (US1) delivers core value - other stories add robustness
