# Quickstart: Auth Flow with Better-Auth

**Feature**: 017-auth-flow-better-auth
**Date**: 2026-01-25

This guide explains how to set up and run the authentication system locally.

---

## Prerequisites

- Node.js 20+ (for Better-Auth service)
- Python 3.12+ (for FastAPI)
- PostgreSQL (or Neon account)
- GitHub OAuth App credentials
- Google OAuth App credentials (optional for MVP)

---

## 1. Environment Setup

### Create `.env` files

**Backend Auth Service** (`backend/auth/.env`):
```env
# Better-Auth configuration
BETTER_AUTH_SECRET=your-secret-key-min-32-chars-random
BETTER_AUTH_URL=http://localhost:3001

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/physai

# OAuth Providers
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Frontend URL (for CORS and redirects)
FRONTEND_URL=http://localhost:3000
```

**Frontend** (`frontend/.env.local`):
```env
# Auth service URL
NEXT_PUBLIC_AUTH_URL=http://localhost:3001
```

---

## 2. Database Setup

### Option A: Local PostgreSQL

```bash
# Create database
createdb physai

# Run migrations
cd backend/auth
npx prisma migrate dev
```

### Option B: Neon PostgreSQL

1. Create a Neon project at https://neon.tech
2. Copy connection string to `DATABASE_URL`
3. Run migrations:
   ```bash
   cd backend/auth
   npx prisma migrate deploy
   ```

---

## 3. OAuth Provider Setup

### GitHub OAuth App

1. Go to https://github.com/settings/developers
2. Click "New OAuth App"
3. Fill in:
   - **Application name**: PhysAI Local
   - **Homepage URL**: `http://localhost:3000`
   - **Authorization callback URL**: `http://localhost:3001/api/auth/callback/github`
4. Copy Client ID and Client Secret to `.env`

### Google OAuth App (Optional)

1. Go to https://console.cloud.google.com/apis/credentials
2. Create OAuth 2.0 Client ID
3. Add authorized redirect URI: `http://localhost:3001/api/auth/callback/google`
4. Copy Client ID and Client Secret to `.env`

---

## 4. Install Dependencies

```bash
# Auth service (Node.js)
cd backend/auth
npm install

# FastAPI backend
cd backend
uv sync

# Frontend
cd frontend
npm install
```

---

## 5. Start Services

### Terminal 1: Auth Service
```bash
cd backend/auth
npm run dev
# Runs on http://localhost:3001
```

### Terminal 2: FastAPI Backend
```bash
cd backend
source .venv/bin/activate
uvicorn src.main:app --reload --port 8000
# Runs on http://localhost:8000
```

### Terminal 3: Frontend
```bash
cd frontend
npm run start
# Runs on http://localhost:3000
```

---

## 6. Test Authentication Flow

### Sign Up (New User)

1. Open http://localhost:3000
2. Click "Sign In" in header
3. Select "Continue with GitHub"
4. Authorize on GitHub
5. Complete onboarding survey
6. Verify redirect to homepage with avatar visible

### Sign In (Returning User)

1. Open http://localhost:3000 in incognito
2. Click "Sign In"
3. Select "Continue with GitHub"
4. Verify immediate redirect without survey

### Session Persistence

1. Sign in on one tab
2. Open new tab to http://localhost:3000
3. Verify still signed in (avatar visible)

---

## 7. API Testing

### Check Session
```bash
curl http://localhost:3001/api/auth/session \
  -H "Cookie: better-auth.session_token=YOUR_TOKEN"
```

### Get JWKS
```bash
curl http://localhost:3001/api/auth/jwks
```

### Submit Survey
```bash
curl -X POST http://localhost:3001/api/user/profile \
  -H "Content-Type: application/json" \
  -H "Cookie: better-auth.session_token=YOUR_TOKEN" \
  -d '{
    "role": "student",
    "softwareBackground": ["python_intermediate", "linux_comfortable"],
    "hardwareAccess": ["simulation_only"],
    "learningGoal": "understand_embodied_ai"
  }'
```

---

## 8. Troubleshooting

### OAuth Redirect Error

**Problem**: "redirect_uri_mismatch" error from provider

**Solution**: Ensure callback URL in provider settings exactly matches:
- GitHub: `http://localhost:3001/api/auth/callback/github`
- Google: `http://localhost:3001/api/auth/callback/google`

### Session Not Persisting

**Problem**: User logged out after page refresh

**Solution**:
1. Check browser allows cookies from localhost
2. Verify CORS allows credentials
3. Check cookie domain settings

### Database Connection Failed

**Problem**: "Connection refused" error

**Solution**:
1. Verify PostgreSQL is running
2. Check DATABASE_URL format
3. For Neon: ensure SSL mode is set

---

## 9. Project Structure

```
backend/
├── auth/                    # Node.js Better-Auth service
│   ├── src/
│   │   ├── index.ts        # Auth server entry
│   │   ├── auth.ts         # Better-Auth config
│   │   └── routes/
│   │       └── profile.ts  # Survey endpoints
│   ├── prisma/
│   │   └── schema.prisma   # Database schema
│   └── package.json
│
├── src/                     # FastAPI main backend
│   ├── main.py
│   ├── api/
│   │   └── chat.py         # Existing chat API
│   └── middleware/
│       └── auth.py         # JWT validation middleware
│
└── pyproject.toml

frontend/
├── src/
│   ├── theme/
│   │   └── Root.tsx        # Auth provider wrapper
│   ├── context/
│   │   ├── AuthContext.tsx # New auth context
│   │   └── ChatContext.tsx # Existing
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── SignInButton.tsx
│   │   │   ├── UserMenu.tsx
│   │   │   └── OnboardingSurvey.tsx
│   │   └── ...
│   └── pages/
│       └── onboarding.tsx  # Survey page
│
└── package.json
```

---

## 10. Deployment Notes

### HuggingFace Spaces

Deploy auth service as Docker container alongside FastAPI:

```dockerfile
# Dockerfile.auth
FROM node:20-alpine
WORKDIR /app
COPY backend/auth/package*.json ./
RUN npm ci --only=production
COPY backend/auth/ ./
RUN npm run build
EXPOSE 3001
CMD ["npm", "start"]
```

### Vercel

Frontend deploys automatically. Ensure environment variables are set:
- `NEXT_PUBLIC_AUTH_URL` → HuggingFace auth service URL

### Secrets Required

| Secret | Location | Description |
|--------|----------|-------------|
| BETTER_AUTH_SECRET | HF Spaces | Auth signing key |
| DATABASE_URL | HF Spaces | Neon connection string |
| GITHUB_CLIENT_ID | HF Spaces | GitHub OAuth |
| GITHUB_CLIENT_SECRET | HF Spaces | GitHub OAuth |
| GOOGLE_CLIENT_ID | HF Spaces | Google OAuth |
| GOOGLE_CLIENT_SECRET | HF Spaces | Google OAuth |
