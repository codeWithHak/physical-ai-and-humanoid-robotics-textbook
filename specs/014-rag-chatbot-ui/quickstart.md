# Quickstart: RAG Chat UI

## Prerequisites

- **Frontend**: Docusaurus running (`npm start` in `frontend/`).
- **Backend**: FastAPI running (`uvicorn src.main:app` in `backend/`).

## Installation

No new dependencies required (standard React).
*Optional*: `npm install lucide-react` for icons if not present.

## Testing the Chatbot

1. **Start Backend**:
   ```bash
   cd backend
   source .venv/bin/activate
   uvicorn src.main:app --reload --port 8000
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm start
   ```

3. **Interact**:
   - Open `http://localhost:3000`.
   - Click the **Sparkle/Robot Icon** in the bottom right.
   - Type "Hello".
   - Verify response appears.

4. **Verify Citations**:
   - Ask "What is ROS?".
   - Verify citations (e.g., "Section 2.1") appear below the answer.
