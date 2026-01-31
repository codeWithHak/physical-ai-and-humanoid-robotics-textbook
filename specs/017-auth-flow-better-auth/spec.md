# Feature Specification: Auth Flow with Better-Auth and User Survey

**Feature Branch**: `017-auth-flow-better-auth`
**Created**: 2026-01-25
**Status**: Draft
**Input**: User description: "Implement user authentication for PhysAI using Better-Auth with OAuth/OIDC, including a mandatory onboarding survey capturing user's software/hardware background"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - New User Sign-Up with Survey (Priority: P1)

A new visitor to PhysAI clicks "Sign In" in the header, selects GitHub as their OAuth provider, completes the GitHub authorization flow, and is redirected back to PhysAI. Since this is their first visit, the system detects no existing profile and presents the mandatory onboarding survey. The user completes the survey by selecting their role, software background, hardware access, and learning goals. Upon submission, their profile is created and they are redirected to the chapter content they were trying to access (or the homepage).

**Why this priority**: This is the foundational flow that enables all personalization features. Without sign-up and survey completion, the platform cannot deliver personalized content - which is a core constitution requirement.

**Independent Test**: Can be fully tested by creating a new GitHub account, signing up on PhysAI, and verifying the survey appears, data is captured, and profile is stored retrievably.

**Acceptance Scenarios**:

1. **Given** a new user on the homepage, **When** they click "Sign In" and select GitHub, **Then** they are redirected to GitHub's OAuth consent page
2. **Given** a user completes GitHub OAuth for the first time, **When** they are redirected back to PhysAI, **Then** they see the mandatory onboarding survey before accessing any personalized features
3. **Given** a user is on the survey page, **When** they complete all four sections (role, software background, hardware access, learning goal), **Then** they can submit and their profile is saved
4. **Given** a user submits the survey, **When** the submission succeeds, **Then** they are redirected to their original destination or the homepage

---

### User Story 2 - Returning User Sign-In (Priority: P1)

A returning user clicks "Sign In", selects their OAuth provider (GitHub or Google), completes authentication, and is immediately redirected to their destination without seeing the survey again. Their session persists across browser tabs and for 7 days without requiring re-authentication.

**Why this priority**: Returning users are the primary engaged audience. A frictionless sign-in experience is critical for retention and engagement with personalized features.

**Independent Test**: Can be fully tested by signing in with an existing account and verifying immediate access without survey, plus verifying session persistence across tabs and over multiple days.

**Acceptance Scenarios**:

1. **Given** a returning user with a completed profile, **When** they sign in via GitHub OAuth, **Then** they are redirected directly to their destination without seeing the survey
2. **Given** an authenticated user in one browser tab, **When** they open a new tab to PhysAI, **Then** they remain authenticated (shared session)
3. **Given** a user signed in 6 days ago, **When** they return to PhysAI, **Then** they remain authenticated without re-authentication required

---

### User Story 3 - Session State on Page Load (Priority: P2)

On every page load, the system checks authentication state via a lightweight session endpoint. For authenticated users, the UI shows their avatar and profile access. For anonymous users, the UI shows a "Sign In" button. Protected features (future: progress tracking, bookmarks) redirect unauthenticated users to sign-in.

**Why this priority**: Session management is necessary infrastructure for all authenticated features but is not user-facing value on its own. It supports the primary sign-up/sign-in flows.

**Independent Test**: Can be tested by loading pages as both authenticated and anonymous users and verifying correct UI state and protected route behavior.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they load any page, **Then** the header shows their avatar and a profile menu instead of "Sign In"
2. **Given** an anonymous user, **When** they load any page, **Then** the header shows a "Sign In" button
3. **Given** an anonymous user, **When** they attempt to access a protected route, **Then** they are redirected to the sign-in flow with return URL preserved

---

### User Story 4 - OAuth Provider Unavailable (Priority: P3)

A user attempts to sign in but the OAuth provider (GitHub/Google) is temporarily unavailable or returns an error. The system displays a user-friendly error message with a retry option rather than crashing or showing technical errors.

**Why this priority**: Error handling is important for user experience but represents an edge case that doesn't block core functionality.

**Independent Test**: Can be tested by simulating OAuth errors (invalid state, provider timeout) and verifying friendly error display with retry option.

**Acceptance Scenarios**:

1. **Given** a user attempting OAuth sign-in, **When** the provider returns an error, **Then** a friendly error message is displayed: "Sign-in failed. Please try again."
2. **Given** a user on the error page, **When** they click "Try Again", **Then** they are returned to the sign-in provider selection

---

### Edge Cases

- **Survey abandonment**: User completes OAuth but closes browser before finishing survey. On next visit, they remain in "incomplete profile" state and must complete survey to access personalized features. Anonymous browsing of public content is still allowed.
- **Multiple OAuth providers**: User signs up with GitHub, later tries to sign in with Google using the same email. System treats as separate accounts (no account linking for MVP). User must use original provider.
- **Session expiry during activity**: User's 7-day session expires while they are actively using the site. Next API call returns 401, frontend shows gentle "Session expired, please sign in again" message.
- **Survey question changes**: If survey questions are updated, existing users retain their old answers. New questions appear as unanswered in their profile but don't force re-survey.
- **Rate limiting triggered**: User exceeds 10 auth attempts per minute. System returns "Too many attempts. Please wait a moment." message.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use Better-Auth as the authentication library, configured following the `configuring-better-auth` skill patterns
- **FR-002**: System MUST support GitHub OAuth as the primary authentication provider
- **FR-003**: System MUST support Google OAuth as a secondary authentication provider
- **FR-004**: System MUST present a mandatory onboarding survey to first-time users before allowing access to personalized features
- **FR-005**: Survey MUST capture user's primary role (student, researcher, hobbyist, professional)
- **FR-006**: Survey MUST capture user's software background via multi-select (Python proficiency, ROS experience, ML/AI familiarity, Linux comfort level)
- **FR-007**: Survey MUST capture user's hardware access via multi-select (NVIDIA Jetson, GPU workstation, cloud GPU, simulation-only)
- **FR-008**: Survey MUST capture user's learning goal (build humanoid robot, understand embodied AI, career transition, academic research)
- **FR-009**: System MUST store user profiles in the database with: user ID, OAuth provider, email, display name, avatar URL, survey responses, timestamps
- **FR-010**: System MUST expose a session endpoint that returns user profile data for authenticated users and 401 for anonymous users
- **FR-011**: System MUST expose a profile endpoint for survey submission and retrieval
- **FR-012**: System MUST use httpOnly secure cookies with SameSite=Lax for all authentication tokens
- **FR-013**: System MUST implement PKCE flow for all OAuth authentication (Better-Auth default)
- **FR-014**: System MUST implement rate limiting: 10 auth attempts per minute per IP
- **FR-015**: System MUST display a visible "Sign In" button in the header on all pages
- **FR-016**: System MUST preserve the original destination URL and redirect after successful authentication
- **FR-017**: System MUST allow anonymous users to browse public chapter content without authentication
- **FR-018**: System MUST use JWKS for token verification between frontend and backend

### Key Entities

- **User**: Represents an authenticated user with OAuth identity (user ID, provider, provider ID, email, display name, avatar URL, created timestamp, last login timestamp)
- **UserProfile**: Represents the user's survey responses and preferences (user ID reference, role, software background array, hardware access array, learning goal, survey completed flag, survey completed timestamp)
- **Session**: Represents an active authentication session (session token, user ID reference, expiry timestamp, created timestamp)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: New users can complete sign-up and survey in under 90 seconds (excluding OAuth provider time)
- **SC-002**: Returning users can sign in and reach their destination in under 5 seconds (excluding OAuth provider time)
- **SC-003**: Session check endpoint responds in under 100ms for 95% of requests
- **SC-004**: 100% of first-time users see the survey before accessing personalized features
- **SC-005**: Survey data is retrievable for 100% of users who completed it
- **SC-006**: Session persists for 7 days without requiring re-authentication
- **SC-007**: Authentication works correctly on mobile browsers (Safari iOS, Chrome Android)
- **SC-008**: OAuth errors display user-friendly messages 100% of the time (no raw error codes shown)
- **SC-009**: System handles 100 concurrent authentication requests without degradation

## Scope Boundaries

### In Scope

- GitHub OAuth integration
- Google OAuth integration
- Mandatory onboarding survey (4 categories)
- User profile storage and retrieval
- Session management with 7-day persistence
- Sign-in/sign-out UI in header
- Mobile-responsive authentication UI
- Rate limiting for authentication endpoints
- CORS configuration for frontend domains

### Out of Scope (Future Features)

- Email/password authentication
- Password reset flows
- Admin user management dashboard
- Role-based access control (beyond authenticated/anonymous)
- Social profile data import (beyond avatar/name)
- Account deletion self-service (manual process for MVP)
- Account linking (multiple OAuth providers for same account)
- Multi-factor authentication
- Remember me / persistent sessions beyond 7 days

## Assumptions

- Users have existing GitHub or Google accounts
- OAuth provider uptime is sufficient (99.9%+)
- Neon PostgreSQL database is available and configured
- Frontend is deployed on Vercel with environment variable support
- Backend is deployed on HuggingFace Spaces with secrets support
- Better-Auth is compatible with FastAPI backend and Docusaurus frontend
- Survey questions will remain stable for MVP (no dynamic survey builder needed)

## Implementation Notes

- **CRITICAL**: Use the `configuring-better-auth` skill during implementation for all Better-Auth configuration, including SSO client setup, PKCE flows, and JWKS token verification patterns
- Frontend authentication UI should use React components wrapped with `@docusaurus/BrowserOnly` to avoid SSR hydration issues
- Survey should be implemented as a dedicated route (`/onboarding`) rather than a modal for simpler state management
- Database schema should be created via migration scripts compatible with Neon PostgreSQL
- Better-Auth session must be validated on the FastAPI backend using JWKS public key verification
- Environment variables required: OAuth client IDs/secrets for both providers, database connection string, JWKS endpoints
