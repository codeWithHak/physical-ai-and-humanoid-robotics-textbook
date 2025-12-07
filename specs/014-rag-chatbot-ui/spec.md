# Feature Specification: RAG Frontend UI (The Chatbot)

**Feature Branch**: `014-rag-chatbot-ui`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User description provided via CLI.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask a Question (Priority: P1)

As a reader, I want to open a chat window and ask a question about the book content without navigating away from my current page, so that I can get instant clarification while reading.

**Why this priority**: Core functionality of the feature.

**Independent Test**: Mount the `<RagChat />` component on a test page (or landing page). Click the trigger button to open it. Type a message and send. Verify the request is sent to the backend and the response is displayed.

**Acceptance Scenarios**:

1. **Given** the chat is closed, **When** I click the floating trigger button, **Then** the chat window opens with a glass-morphism effect.
2. **Given** the chat is open, **When** I type "What is a Node?" and press enter/send, **Then** a loading indicator appears, followed by the AI's response text.
3. **Given** the AI responds with citations, **When** the message appears, **Then** clickable "Source: [Section]" badges are displayed below the text.
4. **Given** the backend is down, **When** I send a message, **Then** the UI displays a graceful error message (e.g., "Unable to reach the brain") instead of crashing.

### Edge Cases

- **Mobile View**: Chat window must take up 100% width/height on small screens.
- **Long Responses**: Chat window content must be scrollable if the response exceeds the panel height.
- **Rapid Clicking**: Toggle state should handle rapid clicks robustly (debounced or simple state toggle).
- **Network Latency**: Loading state must persist until response arrives (or timeout).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST render a floating trigger button in the bottom-right corner of the viewport.
  - *Constraint*: Button must have a "Robot/Sparkle" icon and glow `#BFE600` on hover.
- **FR-002**: The system MUST render a chat window panel when the trigger button is clicked.
  - *Constraint*: Panel must use glass-morphism styling (Black background, 90% opacity, Neon Green borders).
  - *Constraint*: On mobile devices, the panel MUST occupy 100% of the viewport width and height.
- **FR-003**: The chat window MUST display a list of messages.
  - *Constraint*: User messages must be right-aligned with gray background.
  - *Constraint*: AI messages must be left-aligned with black background and neon text.
- **FR-004**: The system MUST support sending text messages to the backend API (`POST /api/chat`).
- **FR-005**: The system MUST display a "typing" or "loading" indicator while waiting for the backend response.
- **FR-006**: The system MUST render citations as distinct UI elements (badges) if provided in the API response.
  - *Constraint*: Badges must display the source section (e.g., "Section 2.1").
- **FR-007**: The component MUST be integrated globally into the Docusaurus layout (via `src/theme/Layout.tsx` or fallback `src/pages/index.tsx` for MVP).

### Key Entities

- **Message**: Represents a single chat entry.
  - Attributes: `id`, `text`, `sender` ('user' | 'ai'), `sources` (optional list of strings).
- **ChatState**: Manages the UI state.
  - Attributes: `isOpen` (boolean), `isLoading` (boolean), `messages` (Message[]).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Integration**: The Chat Button is visible and interactive on the landing page immediately after deployment.
- **SC-002**: **Interaction Speed**: The UI transitions from "Sending" to "Loading" state instantly (<100ms) upon user submission.
- **SC-003**: **Data Display**: 100% of AI responses containing `sources` data render the corresponding citation badges in the UI.
- **SC-004**: **Aesthetics**: The component uses the defined color palette (`#BFE600` primary, Black/Glass backgrounds) and "Lufga" font family.