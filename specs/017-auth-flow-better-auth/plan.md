# Implementation Plan: Auth Flow with Better-Auth

**Branch**: `017-auth-flow-better-auth` | **Date**: 2026-01-25 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/017-auth-flow-better-auth/spec.md`

---

## Summary

Implement user authentication for PhysAI using Better-Auth with OAuth (GitHub/Google) and a mandatory onboarding survey. The architecture uses a **hybrid approach**: a Node.js sidecar service runs Better-Auth for OAuth handling, while FastAPI validates JWT tokens via JWKS. The Docusaurus frontend uses Better-Auth client library with an AuthContext provider in the existing Root.tsx wrapper.

Key deliverables:
1. Node.js auth service with Better-Auth (OAuth + session management)
2. PostgreSQL schema for users, sessions, accounts, and survey profiles
3. Frontend AuthContext and UI components (SignIn, UserMenu, Survey)
4. FastAPI middleware for JWT validation on protected routes

---

## Technical Context

**Language/Version**: TypeScript 5.x (auth service), Python 3.12 (FastAPI), React 18+ (frontend)
**Primary Dependencies**: Better-Auth, FastAPI, Docusaurus, @better-auth/client
**Storage**: Neon PostgreSQL (user, session, account, verification, user_profile tables)
**Testing**: Jest (auth service), pytest (FastAPI), manual E2E testing
**Target Platform**: Web (Vercel frontend, HuggingFace Spaces backend)
**Project Type**: Web application (frontend + backend + auth sidecar)
**Performance Goals**: <100ms session check, <3s OAuth round-trip
**Constraints**: Cross-origin auth (Vercel → HF Spaces), httpOnly cookies, 7-day sessions
**Scale/Scope**: 100 concurrent users, ~1000 registered users for MVP

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **Auth: Better-Auth** | ✅ PASS | Using Better-Auth as specified |
| **Framework: Docusaurus** | ✅ PASS | Frontend remains Docusaurus |
| **Database: Neon PostgreSQL** | ✅ PASS | User data stored in Neon |
| **Backend: FastAPI** | ✅ PASS | FastAPI validates tokens, auth sidecar handles OAuth |
| **Documentation Strategy** | ✅ PASS | Using `configuring-better-auth` skill for implementation |

**Post-Design Re-Check**: All gates pass. The sidecar auth service pattern complies with constitution by keeping FastAPI as the primary backend while using Better-Auth (Node.js) for its intended purpose.

---

## Project Structure

### Documentation (this feature)

```text
specs/017-auth-flow-better-auth/
├── plan.md              # This file
├── research.md          # Architecture decisions
├── data-model.md        # Database schema
├── quickstart.md        # Local development guide
├── contracts/
│   └── auth-api.yaml    # OpenAPI spec for auth endpoints
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── auth/                      # NEW: Node.js Better-Auth service
│   ├── src/
│   │   ├── index.ts          # Express server entry
│   │   ├── auth.ts           # Better-Auth configuration
│   │   ├── db.ts             # Prisma client
│   │   └── routes/
│   │       └── profile.ts    # Survey endpoints
│   ├── prisma/
│   │   ├── schema.prisma     # Database schema
│   │   └── migrations/       # SQL migrations
│   ├── package.json
│   └── tsconfig.json
│
├── src/                       # Existing FastAPI backend
│   ├── main.py               # Add CORS for auth service
│   ├── api/
│   │   └── chat.py           # Existing (add auth middleware)
│   ├── middleware/
│   │   └── auth.py           # NEW: JWT validation
│   └── services/
│       └── ...               # Existing services
│
└── pyproject.toml

frontend/
├── src/
│   ├── theme/
│   │   └── Root.tsx          # MODIFY: Add AuthProvider
│   ├── context/
│   │   ├── AuthContext.tsx   # NEW: Auth state management
│   │   └── ChatContext.tsx   # Existing
│   ├── components/
│   │   ├── Auth/             # NEW: Auth UI components
│   │   │   ├── SignInButton.tsx
│   │   │   ├── UserMenu.tsx
│   │   │   ├── AuthModal.tsx
│   │   │   └── index.ts
│   │   ├── Survey/           # NEW: Onboarding survey
│   │   │   ├── OnboardingSurvey.tsx
│   │   │   ├── SurveyStep.tsx
│   │   │   └── index.ts
│   │   └── ...               # Existing components
│   └── pages/
│       └── onboarding.tsx    # NEW: Survey page route
│
├── package.json              # Add @better-auth/client
└── docusaurus.config.js
```

**Structure Decision**: Web application with **three services**:
1. `frontend/` - Docusaurus React app (existing)
2. `backend/src/` - FastAPI main API (existing, add auth middleware)
3. `backend/auth/` - Node.js Better-Auth service (new)

---

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Node.js sidecar service | Better-Auth requires Node.js runtime | Python auth libraries don't fulfill "use Better-Auth" requirement |
| Three services (frontend, API, auth) | Separation of concerns, security | Single service would require Node.js for all backend logic |

---

## Key Design Decisions

### 1. Auth Service Architecture

**Decision**: Separate Node.js service for Better-Auth
**Rationale**: Better-Auth is TypeScript-only; can't run in FastAPI
**Alternative rejected**: Python auth libraries (doesn't meet "use Better-Auth" requirement)

### 2. Session Mechanism

**Decision**: JWT tokens validated via JWKS
**Rationale**: Works across origins without cookie domain issues
**Alternative rejected**: Cookie-based sessions (blocked by Vercel public suffix)

### 3. Survey Storage

**Decision**: Separate `user_profile` table with JSONB for flexibility
**Rationale**: Survey questions may evolve; JSONB allows schema flexibility
**Alternative rejected**: Columns per question (rigid, requires migrations for changes)

### 4. Frontend Auth State

**Decision**: AuthContext in Root.tsx with session check on mount
**Rationale**: Follows existing ChatContext pattern; Root never unmounts
**Alternative rejected**: Local storage (security concerns, SSR issues)

---

## API Endpoints Summary

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/auth/signin/:provider` | GET | No | Initiate OAuth flow |
| `/api/auth/callback/:provider` | GET | No | OAuth callback handler |
| `/api/auth/session` | GET | Cookie | Get current session |
| `/api/auth/signout` | POST | Cookie | End session |
| `/api/auth/token` | GET | Cookie | Get JWT for API calls |
| `/api/auth/jwks` | GET | No | Public keys for JWT verification |
| `/api/user/profile` | GET | Cookie | Get user profile + survey |
| `/api/user/profile` | POST | Cookie | Submit survey responses |

See [contracts/auth-api.yaml](contracts/auth-api.yaml) for full OpenAPI spec.

---

## Database Schema Summary

| Table | Purpose |
|-------|---------|
| `user` | OAuth identity (email, name, avatar) |
| `session` | Active sessions (token, expiry) |
| `account` | OAuth provider links (GitHub/Google) |
| `verification` | Email verification tokens |
| `user_profile` | Survey responses (role, skills, hardware, goals) |

See [data-model.md](data-model.md) for full schema.

---

## Implementation Phases

### Phase 1: Database & Auth Service Setup
- Create Prisma schema and migrations
- Set up Node.js project with Better-Auth
- Configure GitHub OAuth provider
- Deploy to HuggingFace Spaces

### Phase 2: Frontend Auth Integration
- Create AuthContext provider
- Add SignInButton and UserMenu components
- Modify Root.tsx to include AuthProvider
- Add session check on mount

### Phase 3: Survey Implementation
- Create OnboardingSurvey component
- Add /onboarding page route
- Implement survey submission API
- Add survey completion redirect logic

### Phase 4: FastAPI Integration
- Add JWT validation middleware
- Protect chat endpoints (optional for MVP)
- Add CORS for auth service origin

### Phase 5: Testing & Polish
- E2E testing of OAuth flows
- Mobile browser testing
- Error handling improvements
- Documentation updates

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| HuggingFace Spaces doesn't support multiple services | Use Docker Compose or single container with process manager |
| OAuth callback URL misconfiguration | Document exact URLs in quickstart; test in staging |
| Cross-origin cookie issues | Use JWT tokens instead of cookies for API calls |
| Survey abandonment | Allow anonymous browsing; gentle prompts for personalization |

---

## Dependencies

```
# backend/auth/package.json
better-auth: ^1.0.0
@prisma/client: ^5.0.0
express: ^4.18.0
cors: ^2.8.0

# frontend/package.json (additions)
@better-auth/client: ^1.0.0
```

---

## Next Steps

Run `/sp.tasks` to generate implementation tasks from this plan.
