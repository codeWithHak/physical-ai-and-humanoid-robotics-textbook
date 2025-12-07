# Quickstart: RAG Backend

## Prerequisites

- **Python**: 3.12+
- **Environment Variables**: Ensure `.env` in `backend/` contains:
  ```bash
  GEMINI_API_KEY="AIza..."
  QDRANT_URL="https://..."
  QDRANT_API_KEY="th..."
  OPENAI_API_KEY="sk-..."
  ```

## Installation

```bash
cd backend
# Activate virtual environment
source .venv/bin/activate
# Install dependencies (if not already installed)
pip install google-generativeai qdrant-client openai-agents-python tenacity python-dotenv
```

## Running the Server

```bash
# From backend/ directory
uvicorn src.main:app --reload
```

## Testing the API

```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is the hardware nervous system?"}'
```

**Expected Response**:
```json
{
  "answer": "The hardware nervous system refers to...",
  "sources": ["Section 1.3: The Hardware Nervous System"]
}
```
