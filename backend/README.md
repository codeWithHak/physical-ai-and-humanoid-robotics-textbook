---
title: Physical AI Textbook Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# Physical AI Textbook Backend

Agentic RAG backend for the Physical AI & Humanoid Robotics Textbook.

## Features

- **Hybrid Search**: Combines vector similarity (OpenAI embeddings) with BM25 sparse retrieval
- **OpenAI Agents SDK**: Intelligent query processing with function tools
- **Context Management**: Token budget optimization for responses

## API Endpoints

- `POST /api/chat` - Process a query against the textbook
- `GET /api/health` - Health check with service status
- `GET /health` - Simple health check

## Environment Variables

Required secrets (set in HF Spaces settings):
- `OPENAI_API_KEY` - OpenAI API key
- `QDRANT_URL` - Qdrant Cloud cluster URL
- `QDRANT_API_KEY` - Qdrant API key
