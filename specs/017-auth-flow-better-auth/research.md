# Research: Auth Flow with Better-Auth

**Feature**: 017-auth-flow-better-auth
**Date**: 2026-01-25

## Executive Summary

Better-Auth is a TypeScript/JavaScript authentication library designed primarily for Node.js backends. For the PhysAI architecture (Docusaurus frontend on Vercel + FastAPI backend on HuggingFace Spaces), we need an **alternative approach** since Better-Auth cannot run directly on Python/FastAPI.

**Key Decision**: Implement a **hybrid architecture** where:
1. A lightweight Node.js auth service handles Better-Auth
2. FastAPI validates tokens via JWKS
3. Docusaurus frontend uses Better-Auth client library

---

## Research Findings

### 1. Better-Auth Architecture Compatibility

**Finding**: Better-Auth is a Node.js/TypeScript library that cannot run natively on FastAPI.

**Decision**: Deploy a **separate Node.js auth microservice** alongside FastAPI, or use Better-Auth's **JWT plugin** for stateless token validation.

**Rationale**:
- Better-Auth requires Node.js runtime for its auth handler
- FastAPI can validate JWT tokens using JWKS (standard approach)
- This maintains separation of concerns: auth service vs API service

**Alternatives Considered**:
1. **Pure Python auth (rejected)**: Would not fulfill "use Better-Auth" requirement
2. **Auth0/Clerk (rejected)**: Constitution specifies Better-Auth
3. **NextAuth.js (rejected)**: Different library, not Better-Auth

---

### 2. Cross-Origin Session Management

**Finding**: Vercel uses public suffix domains (`.vercel.app`) which **prevent cross-domain cookie sharing**.

**Decision**: Use **custom domain** for production OR implement **JWT-based auth** with Authorization headers.

**Rationale**:
- Cookies with `domain=.vercel.app` are blocked by browsers (public suffix list)
- JWT tokens in Authorization headers work across any domains
- Custom domain (e.g., `physai.dev`) allows subdomain cookie sharing

**Recommended Approach for MVP**:
- Use JWT plugin for Better-Auth
- Frontend stores JWT in memory (not localStorage for security)
- Backend validates JWT via JWKS endpoint
- No cross-domain cookie complexity

---

### 3. Docusaurus Frontend Integration

**Finding**: Docusaurus already has a `Root.tsx` component that wraps the entire app - ideal for auth state.

**Decision**: Extend existing `Root.tsx` with `AuthProvider` context.

**Rationale**:
- Root component is never unmounted during navigation
- Already patterns established (ChatProvider exists)
- BrowserOnly wrapper needed for SSR compatibility

**Existing Pattern** (from `frontend/src/theme/Root.tsx`):
```tsx
const Root = ({ children }: RootProps): JSX.Element => {
  return (
    <ChatProvider>
      {children}
      {/* Add AuthProvider here */}
    </ChatProvider>
  );
};
```

---

### 4. OAuth Provider Configuration

**Finding**: GitHub and Google OAuth have different token behaviors.

**Decision**: Configure both providers with appropriate settings.

**GitHub OAuth**:
- Access tokens don't expire (unless revoked)
- No refresh tokens by default
- Must enable email scope in GitHub app settings

**Google OAuth**:
- Access tokens expire (typically 1 hour)
- Refresh tokens available on first auth
- Must configure consent screen in Google Cloud Console

**Environment Variables Needed**:
```
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
BETTER_AUTH_SECRET=xxx (32+ chars)
```

---

### 5. Database Schema

**Finding**: Better-Auth requires 4 core tables: user, session, account, verification.

**Decision**: Create these tables in Neon PostgreSQL with survey extension.

**Schema Extension for Survey**:
- Add `user_profile` table linked to `user`
- Store survey responses as JSONB for flexibility
- Track survey completion status

---

### 6. Architecture Decision: Deployment Topology

**Finding**: Three viable deployment options exist.

**Decision**: Option B - Sidecar Auth Service

| Option | Pros | Cons |
|--------|------|------|
| A. Auth in FastAPI (Python) | Single service | Can't use Better-Auth |
| **B. Sidecar Node.js service** | Uses Better-Auth, separate concerns | Two services to deploy |
| C. Serverless auth (Vercel) | Uses Better-Auth | Adds Vercel dependency for backend |

**Rationale for Option B**:
- Fulfills requirement to use Better-Auth
- FastAPI remains the primary API service
- Auth service is small and focused
- Can deploy both on HuggingFace Spaces using Docker Compose

---

## Technical Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth library | Better-Auth (Node.js) | Constitution requirement |
| Session mechanism | JWT tokens | Cross-domain compatibility |
| Token validation | JWKS endpoint | Stateless, scalable |
| Frontend state | AuthContext in Root.tsx | Existing pattern |
| Database | Neon PostgreSQL | Constitution requirement |
| OAuth providers | GitHub (primary), Google | Spec requirement |
| Deployment | Node.js sidecar + FastAPI | Best fit for Better-Auth |

---

## Open Questions Resolved

1. **Q: How does Better-Auth work with FastAPI?**
   A: It doesn't directly. Use separate Node.js auth service + JWKS validation.

2. **Q: How to handle cross-domain cookies?**
   A: Use JWT tokens instead of cookies for cross-domain auth.

3. **Q: Where does survey data live?**
   A: New `user_profile` table in Neon PostgreSQL.

4. **Q: How does frontend detect auth state?**
   A: Call `/api/auth/session` endpoint on mount, store in React context.

---

## Implementation Risks

| Risk | Mitigation |
|------|------------|
| Node.js sidecar adds complexity | Keep auth service minimal; use Docker Compose |
| JWT token management in frontend | Store in memory, refresh proactively |
| Survey blocking UX | Show progress indicator, allow partial saves |
| HuggingFace Spaces deployment limits | Monitor container resources; optimize |

---

## Next Steps

1. Create data model with user, session, account, verification, user_profile tables
2. Define API contracts for auth endpoints
3. Create quickstart guide for local development
4. Generate implementation tasks
