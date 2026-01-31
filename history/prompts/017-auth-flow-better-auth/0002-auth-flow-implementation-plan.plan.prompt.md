---
id: "0002"
title: Auth Flow Implementation Plan
stage: plan
date: 2026-01-25
surface: agent
model: claude-opus-4-5-20251101
feature: 017-auth-flow-better-auth
branch: 017-auth-flow-better-auth
user: hak
command: /sp.plan
labels: ["auth", "better-auth", "architecture", "planning"]
links:
  spec: specs/017-auth-flow-better-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/017-auth-flow-better-auth/plan.md
  - specs/017-auth-flow-better-auth/research.md
  - specs/017-auth-flow-better-auth/data-model.md
  - specs/017-auth-flow-better-auth/quickstart.md
  - specs/017-auth-flow-better-auth/contracts/auth-api.yaml
tests:
  - null
---

## Prompt

/sp.plan - Execute implementation planning workflow for 017-auth-flow-better-auth feature

## Response snapshot

Created comprehensive implementation plan for Auth Flow with Better-Auth:

**Architecture Decision**: Hybrid approach with Node.js sidecar service for Better-Auth + FastAPI for JWT validation via JWKS

**Artifacts Generated**:
1. `research.md` - Architecture decisions, Better-Auth compatibility analysis, cross-origin session management
2. `data-model.md` - 5-table PostgreSQL schema (user, session, account, verification, user_profile)
3. `contracts/auth-api.yaml` - OpenAPI 3.1 spec with 8 endpoints for auth and profile management
4. `quickstart.md` - Local development setup guide with OAuth provider configuration
5. `plan.md` - Complete implementation plan with 5 phases

**Key Decisions**:
- Node.js sidecar service (Better-Auth requires Node.js runtime)
- JWT tokens via JWKS (solves cross-origin cookie issues with Vercel public suffix)
- AuthContext in Root.tsx (follows existing ChatContext pattern)
- JSONB for survey responses (flexible schema evolution)

## Outcome

- ✅ Impact: Complete planning artifacts ready for task generation
- 🧪 Tests: N/A (planning phase)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/auth-api.yaml
- 🔁 Next prompts: `/sp.tasks` to generate implementation tasks
- 🧠 Reflection: Hybrid architecture is more complex but necessary for Better-Auth requirement

## Evaluation notes (flywheel)

- Failure modes observed: None - all constitution gates passed
- Graders run and results (PASS/FAIL): Constitution check PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task generation with /sp.tasks
