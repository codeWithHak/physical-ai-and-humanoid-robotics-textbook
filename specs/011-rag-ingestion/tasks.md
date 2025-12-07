# Tasks: RAG Ingestion Engine (Backend Initialization)

**Feature Branch**: `011-rag-ingestion`
**Created**: 2025-12-07
**Status**: Draft
**Spec**: [specs/011-rag-ingestion/spec.md](specs/011-rag-ingestion/spec.md)
**Plan**: [specs/011-rag-ingestion/plan.md](specs/011-rag-ingestion/plan.md)

## Summary

This document outlines the tasks required to implement the RAG Ingestion Engine, organized by phases and user stories. The primary goal is to create a local Python script capable of processing Docusaurus Markdown content, generating vector embeddings via Google Gemini, and uploading them to Qdrant Cloud.

## Dependencies

This feature has no external dependencies beyond the specified Python libraries and API keys.

## Phase 1: Setup (Project Initialization)

**Goal**: Establish the basic directory structure, virtual environment, and dependency management for the backend.

- [x] T001 Create the `backend/` directory at the project root.
- [x] T002 Create a `.gitignore` entry for `backend/venv/` in the project's root `.gitignore` file.
- [x] T003 Initialize a Python virtual environment in `backend/.venv/` using uv.
- [x] T004 Create `backend/requirements.txt` with `qdrant-client`, `google-generativeai`, `python-dotenv`, and `markdown-it-py` (for markdown parsing).
- [x] T005 Install dependencies from `backend/requirements.txt` into the virtual environment.

## Phase 2: Foundational (Core Ingestion Logic)

**Goal**: Implement the core components of the ingestion script, excluding specific data processing.

- [x] T006 Create the `backend/ingest.py` script.
- [x] T007 [P] Implement `load_environment_variables()` function in `backend/ingest.py` to load API keys from `.env`.
- [x] T008 [P] Implement `initialize_qdrant_client()` function in `backend/ingest.py` to connect to Qdrant Cloud.
- [x] T009 [P] Implement `initialize_gemini_model()` function in `backend/ingest.py` to get the Gemini embedding model.
- [x] T010 Implement `create_qdrant_collection()` function in `backend/ingest.py` to create the `physical_ai_textbook` collection if it doesn't exist, defining the vector size and distance metric.

## Phase 3: User Story 1 - Local Content Ingestion (Priority: P1)

**Goal**: Process Docusaurus content, generate embeddings, and upload to Qdrant.
**Independent Test**: Running `cd backend && python ingest.py` executes successfully, populates Qdrant, and prints a success message.

- [x] T011 [US1] Implement `get_markdown_files()` function in `backend/ingest.py` to find all `.md` and `.mdx` files in `../frontend/docs/`.
- [x] T012 [P] [US1] Implement `parse_markdown_file(filepath)` function in `backend/ingest.py` to read content and strip frontmatter.
- [x] T013 [P] [US1] Implement `chunk_content(text)` function in `backend/ingest.py` to split content by H2/H3 headers.
- [x] T014 [P] [US1] Implement `generate_embedding(text_chunk)` function in `backend/ingest.py` using the Gemini embedding model, handling immediate error reporting on API issues.
- [x] T015 [P] [US1] Implement `generate_chunk_id(filepath, content_hash)` function in `backend/ingest.py` to create unique IDs for Qdrant points.
- [x] T016 [US1] Implement `upload_chunks_to_qdrant(chunks)` function in `backend/ingest.py` to upsert points to the `physical_ai_textbook` collection, including payload metadata.
- [x] T017 [US1] Orchestrate the main ingestion workflow in `backend/ingest.py`: call prerequisite functions, iterate through files, parse, chunk, embed, and upload.
- [x] T018 [US1] Add logging for critical errors and progress summary (e.g., number of files processed, chunks indexed) to `backend/ingest.py`.
- [x] T019 [US1] Add a `main` execution block to `backend/ingest.py` to run the ingestion process.

## Final Phase: Polish & Cross-Cutting Concerns

**Goal**: Ensure the script is robust, adheres to code quality standards, and provides a good user experience.

- [x] T020 [P] Ensure Python code in `backend/ingest.py` adheres to PEP8 and includes type hints.
- [x] T021 [P] Review `backend/ingest.py` to ensure graceful handling of edge cases (no markdown files, malformed markdown, Qdrant/API unreachable).
- [x] T022 Update the project's root `.gitignore` to include the `backend/` directory itself (excluding `backend/venv` which is already covered).

---

## Task Mapping and Dependencies

The tasks are ordered to ensure dependencies are met. Phase 1 must be completed before Phase 2, and Phase 2 before Phase 3. Tasks within a Phase can be parallelized where marked `[P]`.

## Parallel Execution Opportunities

- Tasks marked with `[P]` can be worked on concurrently if assigned to different developers or executed in parallel. For example, `T007`, `T008`, `T009` are independent initialization steps. Similarly, within `US1`, tasks like `T012`, `T013`, `T014`, `T015`, `T016` can be thought of as functions developed in parallel, then integrated.

## Suggested MVP Scope

The MVP for this feature is the complete implementation of **User Story 1 - Local Content Ingestion** (Phase 3). This delivers a fully functional, local ingestion script capable of populating Qdrant.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
