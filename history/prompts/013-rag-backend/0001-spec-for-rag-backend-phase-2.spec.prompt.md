---
id: 0001
title: Spec for RAG Backend Phase 2
stage: spec
date: 2025-12-07
surface: agent
model: gemini-2.0-flash-exp
feature: 013-rag-backend
branch: 013-rag-backend
user: hak
command: /sp.specify
labels: ["rag", "backend", "spec", "fastapi"]
links:
  spec: specs/013-rag-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/013-rag-backend/spec.md
 - specs/013-rag-backend/checklists/requirements.md
tests: []
---

## Prompt

Feature: RAG Backend - Phase 2 (The Intelligence) Intent: Implement the RAG (Retrieval-Augmented Generation) logic within the FastAPI application. This feature bridges the "Ingestion Engine" (Qdrant) and the "User Interface" (React) by processing natural language queries. Feature Scope (The RAG Service): 1. Service Module (`backend/services/rag_service.py`): - **Step 1: Embedding.** Use `google.generativeai` to embed the incoming user query (Model: `embedding-001`) (Check @/backend/ingest.py for more details about model and injestion logic). - **Step 2: Retrieval.** Use `qdrant_client` to search the `physical_ai_textbook` collection. - *Constraint:* Retrieve `limit=5` chunks. - *Constraint:* Extract `payload.source` and `payload.header` for citations. - **Step 3: Synthesis.** Use `openai-agents-python` (Model: `gpt-4o-mini`). - *System Prompt:* "You are an expert AI Robotics Professor. Answer based ONLY on the provided context. If the answer is not in the context, say 'I cannot find that in the textbook'. Always cite the section title." 2. API Endpoint (`backend/api/chat.py`): - `POST /api/chat`: - Input: `{ "message": "How do I install ROS?" }` - Logic: Calls `rag_service.generate_answer(message)`. - Output: `{ "answer": "...", "sources": ["Section 2.1", "Section 2.3"] }` 3. Context 7 Usage: - Must use the latest `OpenAI Agents SDK syntax (v1.0+). - Must use the latest `qdrant-client` search syntax. Success Criteria (SMART): - Latency: The full pipeline (Embed -> Search -> Generate) completes in under 5 seconds for standard queries. - Accuracy: Questions about "Chapter 1" content return answers *specifically* from the textbook, not general internet knowledge. - Robustness: If Qdrant is empty or down, the API returns a graceful error, not a 500 crash. Hello World Example (Open AI Agnts SDK): ```from agents import Agent, Runner agent = Agent(name="Assistant", instructions="You are a helpful assistant") result = Runner.run_sync(agent, "Write a haiku about recursion in programming.") print(result.final_output)``` Non-Goals: - Not Using COpenAI's Chat Completion API Directly wthout OpenAI Agents SDK. - NOT implementing "Chat History" memory yet (that is Phase 3 with Neon). - NOT using the experimental "OpenAI Assistants API" (too slow for serverless); use standard Chat Completions. User Stories: - "As a student, I want to ask 'What GPU do I need?' and get an answer citing 'Chapter 1.3: The Hardware Nervous System'."

## Response snapshot

Created feature branch `013-rag-backend`, detailed specification, and validation checklist. Spec includes requirements for RAG service (Google Embedding, Qdrant, OpenAI Agents) and Chat API.

## Outcome

- ✅ Impact: Defined requirements for Phase 2 RAG backend.
- 🧪 Tests: N/A (Spec phase)
- 📁 Files: Created spec and checklist.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: Specification faithfully translates user's technical constraints into functional requirements.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A