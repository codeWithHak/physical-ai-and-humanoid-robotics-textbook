# Feature Specification: Global RAG Chat with Contextual Ask

**Feature Branch**: `015-global-context-chat`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User description provided via CLI.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Persistent Chat (Priority: P1)

As a student, I want the chat window to stay open and retain my conversation history when I navigate between chapters, so that I can continue my learning session seamlessly without losing context.

**Why this priority**: Core architectural requirement for a smooth user experience in a multi-page book.

**Independent Test**:
1. Open Chat on "Chapter 1".
2. Type "Hello".
3. Navigate to "Chapter 2".
4. Verify Chat is still open (or closed state persisted) and "Hello" message is still there.

**Acceptance Scenarios**:

1. **Given** I have an open chat session on the Home page, **When** I click a link to Chapter 1, **Then** the chat window remains visible and the message history is preserved.
2. **Given** I have closed the chat window, **When** I navigate to another page, **Then** the chat window remains closed.

### User Story 2 - Contextual Ask (Priority: P2)

As a student, I want to highlight a confusing sentence in the text and click a button to instantly ask the AI about it, so that I don't have to copy-paste or retype the context.

**Why this priority**: The "Killer Feature" that integrates the book content with the AI intelligence.

**Independent Test**:
1. Highlight text > 5 chars.
2. Verify "Ask AI" tooltip appears.
3. Click "Ask AI".
4. Verify Chat opens and sends query automatically.

**Acceptance Scenarios**:

1. **Given** I select text > 5 characters, **When** I release the mouse button, **Then** a floating "Ask AI" tooltip appears above the selection.
2. **Given** the tooltip is visible, **When** I click "Ask AI", **Then** the chat window opens (if closed) AND the selected text is sent as a query context (e.g., "Explain this: [selection]").
3. **Given** the tooltip is visible, **When** I click anywhere else or clear selection, **Then** the tooltip disappears.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a global state provider (`ChatProvider`) that wraps the entire application.
  - *Constraint*: Must manage `isOpen`, `messages`, and `inputQuery` state globally.
- **FR-002**: The system MUST render the `<RagChat />` component at the root level (via `src/theme/Root.js` or Swizzled Layout) to ensure persistence across navigation.
- **FR-003**: The system MUST render a `<SelectionTooltip />` component at the root level.
- **FR-004**: The `<SelectionTooltip />` MUST detect text selection events (`mouseup` / `selectionchange`).
  - *Constraint*: Trigger only if selection length > 5 characters.
  - *Constraint*: Calculate X/Y coordinates to position tooltip above selection.
- **FR-005**: Clicking the "Ask AI" tooltip button MUST trigger the `triggerAskAI(text)` function in the global context.
  - *Constraint*: This function must open the chat window and submit the selected text as a user message.
- **FR-006**: The UI MUST adhere to the "Neon Lime" (#BFE600) and "Black Glassmorphism" visual identity.

### Key Entities

- **ChatContext**: Global React Context.
  - `isOpen`: boolean
  - `messages`: Message[]
  - `triggerAskAI`: (text: string) => void

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Persistence**: 100% of chat history is retained when navigating between any two Docusaurus routes.
- **SC-002**: **Context Flow**: Clicking "Ask AI" results in a visible AI response in the chat window within 5 seconds.
- **SC-003**: **Accessibility**: Tooltip must NOT block reading when not requested (disappears on un-focus).
- **SC-004**: **Mobile Optimization**: Tooltip logic handles or disables touch events to avoid conflict with OS native selection menus (optional disable for MVP).