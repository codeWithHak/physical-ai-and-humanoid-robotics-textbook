# Complete Backend Deployment Guide for Beginners

A simple, reliable guide to deploy full-stack apps (Frontend + Backend) when you're coding with AI assistants like Claude.

---

## Table of Contents

1. [The Big Picture](#the-big-picture)
2. [Project Structure Decision](#project-structure-decision)
3. [Setting Up Your Project](#setting-up-your-project)
4. [Building Your Backend](#building-your-backend)
5. [Deploying Frontend to Vercel](#deploying-frontend-to-vercel)
6. [Deploying Backend to Hugging Face Spaces](#deploying-backend-to-hugging-face-spaces)
7. [Connecting Frontend and Backend](#connecting-frontend-and-backend)
8. [The Complete Workflow](#the-complete-workflow)
9. [Troubleshooting](#troubleshooting)

---

## The Big Picture

When you build a web app, you typically have two parts:

```
┌─────────────────┐         ┌─────────────────┐
│    FRONTEND     │  ────►  │    BACKEND      │
│  (What users    │  HTTP   │  (Your server   │
│   see/click)    │  calls  │   & database)   │
└─────────────────┘         └─────────────────┘
     Vercel                  Hugging Face
```

**Frontend:** React, Next.js, HTML — the visual part users interact with
**Backend:** FastAPI, Node.js, Flask — handles data, AI, databases

**Why separate deployments?**
- Vercel is optimized for frontends (fast, global CDN)
- Hugging Face is optimized for backends (more memory, good for AI/ML)

---

## Project Structure Decision

### The Question: One Repo or Two?

**Recommendation: ONE REPO (Monorepo)**

Why? When coding with Claude or other AI assistants:
- AI can see your entire project context
- No switching between repos
- Easier to keep frontend/backend in sync
- Simpler git history

### Recommended Structure

```
my-project/
├── frontend/          # Your React/Next.js app
│   ├── src/
│   ├── package.json
│   └── ...
├── backend/           # Your FastAPI/Python app
│   ├── src/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── ...
├── .gitignore
└── README.md
```

### Create This Structure

```bash
# Create project folder
mkdir my-project
cd my-project
git init

# Create frontend (example with Next.js)
npx create-next-app@latest frontend

# Create backend folder
mkdir -p backend/src
```

---

## Setting Up Your Project

### Step 1: Create the Backend Structure

```bash
cd my-project/backend
mkdir -p src/api src/services src/models
```

Your backend folder should look like:

```
backend/
├── src/
│   ├── __init__.py       # Empty file (makes it a Python package)
│   ├── main.py           # FastAPI app entry point
│   ├── api/
│   │   └── chat.py       # Your API endpoints
│   ├── services/
│   │   └── my_service.py # Business logic
│   └── models/
│       └── schemas.py    # Data models
├── requirements.txt      # Python dependencies
├── Dockerfile           # For deployment
├── README.md            # HF Spaces metadata
└── .env                 # Local secrets (NEVER commit this)
```

### Step 2: Create Essential Files

**backend/requirements.txt**
```
fastapi>=0.100.0
uvicorn>=0.23.0
python-dotenv>=1.0.0
pydantic>=2.0.0
```

**backend/src/main.py**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS: Allow your frontend to call your backend
origins = [
    "http://localhost:3000",              # Local development
    "https://your-app.vercel.app",        # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "API Ready"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Import and include your API routes
# from src.api.chat import router
# app.include_router(router, prefix="/api")
```

**backend/.env** (for local development)
```
OPENAI_API_KEY=your-key-here
DATABASE_URL=your-db-url
```

**backend/.gitignore**
```
__pycache__/
*.pyc
.env
.env.*
.venv/
```

### Step 3: Test Locally

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn src.main:app --reload --port 8000
```

Visit http://localhost:8000 — you should see `{"status": "API Ready"}`

---

## Building Your Backend

### Adding an API Endpoint

**backend/src/api/chat.py**
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Your logic here
    return ChatResponse(answer=f"You said: {request.message}")
```

**Update backend/src/main.py** to include the router:
```python
from src.api.chat import router as chat_router
app.include_router(chat_router, prefix="/api")
```

Now `POST /api/chat` is available.

---

## Deploying Frontend to Vercel

This is the easy part.

### Step 1: Push to GitHub

```bash
cd my-project
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Connect to Vercel

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import your GitHub repo
4. **Important:** Set the Root Directory to `frontend`
5. Click Deploy

That's it. Vercel auto-deploys on every push.

**Your frontend URL:** `https://your-project.vercel.app`

---

## Deploying Backend to Hugging Face Spaces

### Why Hugging Face?

| Feature | Vercel | Hugging Face |
|---------|--------|--------------|
| Memory | 256MB-1GB | 16GB free |
| Cold starts | Frequent | Minimal |
| Python/ML | Limited | Optimized |
| Cost | Limited free | Generous free |

### Step 1: Create Dockerfile

**backend/Dockerfile**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Create non-root user (required by HF)
RUN useradd -m -u 1000 user
USER user

# HF Spaces uses port 7860
EXPOSE 7860

# Start the server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Step 2: Create HF Spaces README

**backend/README.md**
```markdown
---
title: My Backend
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# My Backend API

Backend service for my application.
```

The `---` section is YAML frontmatter that tells HF how to run your app.

### Step 3: Create HF Space

1. Go to https://huggingface.co/new-space
2. Fill in:
   - **Space name:** `my-backend`
   - **SDK:** Docker
   - **Hardware:** CPU basic (free)
3. Click "Create Space"

### Step 4: Clone and Deploy

```bash
# Clone the empty HF Space
cd ~/projects
git clone https://huggingface.co/spaces/YOUR_USERNAME/my-backend hf-backend

# Copy your backend files
cp -r my-project/backend/* hf-backend/
cp my-project/backend/.gitignore hf-backend/

# Clean up dev files
cd hf-backend
rm -rf __pycache__ .venv .env .env.*

# Commit and push
git add .
git commit -m "Deploy backend"
git push origin main
```

**If git push asks for credentials:**
1. Go to https://huggingface.co/settings/tokens
2. Create a token with "write" permission
3. Use it as your password

### Step 5: Add Secrets

Your `.env` variables need to be added as HF Secrets:

1. Go to your Space: `https://huggingface.co/spaces/YOUR_USERNAME/my-backend`
2. Click **Settings**
3. Scroll to **Variables and secrets**
4. Add each secret:
   - `OPENAI_API_KEY` = your key
   - `DATABASE_URL` = your url
   - etc.

The Space will automatically restart.

### Step 6: Verify

Your backend URL: `https://YOUR_USERNAME-my-backend.hf.space`

Test it:
```bash
curl https://YOUR_USERNAME-my-backend.hf.space/health
# Should return: {"status": "healthy"}
```

---

## Connecting Frontend and Backend

### Update Frontend to Call Backend

In your frontend code, create an API utility:

**frontend/src/lib/api.ts**
```typescript
const API_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:8000'
  : 'https://YOUR_USERNAME-my-backend.hf.space';

export async function chat(message: string) {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  return response.json();
}
```

### Update Backend CORS

Make sure your backend allows requests from your Vercel frontend:

**backend/src/main.py**
```python
origins = [
    "http://localhost:3000",
    "https://your-project.vercel.app",  # Add your actual Vercel URL
]
```

Then redeploy the backend.

---

## The Complete Workflow

### Daily Development Flow

```
1. Code locally (both frontend and backend)
2. Test locally (frontend on :3000, backend on :8000)
3. Commit and push to GitHub
4. Frontend auto-deploys to Vercel
5. Run deploy script for backend → HF Spaces
```

### Backend Deploy Script

Save this as **backend/deploy.sh**:

```bash
#!/bin/bash
# Usage: ./deploy.sh "commit message"

set -e

HF_DIR="$HOME/projects/hf-backend"  # Where you cloned HF Space
BACKEND_DIR="$(dirname "$0")"
MSG="${1:-Update backend}"

echo "Deploying to HF Spaces..."

# Clean HF directory (keep .git)
find "$HF_DIR" -mindepth 1 -maxdepth 1 ! -name '.git' ! -name '.gitattributes' -exec rm -rf {} +

# Copy files
cp -r "$BACKEND_DIR/src" "$HF_DIR/"
cp "$BACKEND_DIR/Dockerfile" "$HF_DIR/"
cp "$BACKEND_DIR/requirements.txt" "$HF_DIR/"
cp "$BACKEND_DIR/README.md" "$HF_DIR/"

# Clean pycache
find "$HF_DIR" -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Push
cd "$HF_DIR"
git add -A
git commit -m "$MSG" || echo "No changes"
git push origin main

echo "Done! https://YOUR_USERNAME-my-backend.hf.space"
```

Make it executable:
```bash
chmod +x backend/deploy.sh
```

Deploy with:
```bash
./backend/deploy.sh "Added new feature"
```

---

## Troubleshooting

### "CORS error" in browser console

Your backend isn't allowing requests from your frontend domain.

**Fix:** Add your Vercel URL to the `origins` list in `main.py`, then redeploy backend.

### "403 Forbidden" from external APIs

Your secrets aren't configured in HF Spaces.

**Fix:** Go to Space Settings → Variables and secrets → Add your API keys.

### HF Space stuck on "Building"

Check the build logs for errors.

**Common issues:**
- Invalid Dockerfile syntax
- Missing requirements.txt
- Wrong Python version

### "Connection refused" locally

Backend isn't running.

**Fix:** Make sure uvicorn is running on port 8000:
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend can't find backend locally

Check you're using the right URL for development.

**Fix:** Use environment-based URLs:
```typescript
const API_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:8000'
  : 'https://your-backend.hf.space';
```

---

## Summary

| What | Where | How |
|------|-------|-----|
| Code | One GitHub repo | `my-project/frontend` + `my-project/backend` |
| Frontend | Vercel | Auto-deploys from GitHub |
| Backend | HF Spaces | Run `deploy.sh` script |
| Secrets | HF Settings | Add manually in UI |
| CORS | Backend code | List allowed frontend URLs |

**The simple mental model:**
1. Write code in one repo (AI can see everything)
2. Push to GitHub (frontend auto-deploys)
3. Run deploy script (backend deploys)
4. Done

---

## Quick Reference

```bash
# Local development
cd frontend && npm run dev          # Frontend on :3000
cd backend && uvicorn src.main:app --reload  # Backend on :8000

# Deploy frontend
git push origin main                # Vercel auto-deploys

# Deploy backend
./backend/deploy.sh "message"       # Pushes to HF Spaces

# Check backend health
curl https://YOUR_USER-my-backend.hf.space/health
```

---

*Last updated: January 2026*
