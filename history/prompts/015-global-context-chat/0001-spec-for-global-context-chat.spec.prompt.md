---
id: 0001
title: Spec for Global Context Chat
stage: spec
date: 2025-12-07
surface: agent
model: gemini-2.0-flash-exp
feature: 015-global-context-chat
branch: 015-global-context-chat
user: hak
command: /sp.specify
labels: ["rag", "frontend", "context", "global-state", "spec"]
links:
  spec: specs/015-global-context-chat/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/015-global-context-chat/spec.md
 - specs/015-global-context-chat/checklists/requirements.md
tests: []
---

## Prompt

Feature: Global RAG Chat with Contextual Ask Intent: Create a globally persistent RAG Chatbot with a "Contextual Inquiry" feature. The chatbot must appear on every page of the Docusaurus site. Additionally, selecting any text in the book triggers a floating "Ask AI" tooltip that seamlessly feeds the selection into the chat. Feature Scope (Architecture): 1. Global State Management (`src/context/ChatContext.tsx`): - Create a React Context (`ChatProvider`) to manage: - `isOpen`: Boolean (Is the chat window visible?). - `messages`: Array of chat objects. - `inputQuery`: String (The text currently in the input box). - Function `triggerAskAI(text)`: Opens the chat and auto-fills/submits the query. 2. The Global Wrapper (`src/theme/Root.js` or Swizzled Layout): - **Critical Docusaurus Integration:** Create a `src/theme/Root.js` file (if supported by version) or swizzle `Layout`. This component MUST wrap the entire app with `<ChatProvider>`. - Render `<RagChat />` and `<SelectionTooltip />` at this level so they persist across page navigation. 3. Component: `<RagChat />` (The Interface): - Floating Bottom-Right Widget (Fixed position). - "Lufga" Font, Neon Lime (#BFE600) Borders, Black Glassmorphism background. - Connects to the FastAPI backend (`/api/chat`). - Displays Citations as clickable badges. 4. Component: `<SelectionTooltip />` (The Trigger): - Logic: Listens to `document.onselectionchange` or `mouseup`. - Behavior: If text is selected (> 5 chars), calculate X/Y coordinates and show a small "Ask AI" button just above the selection. - Action: Clicking "Ask AI" -> Calls `triggerAskAI(selectedText)` -> Opens Chat -> Sends Query. - Styles: Minimalist, Neon Lime button, high Z-index. Success Criteria (SMART): - Persistence: Navigating from "Chapter 1" to "Chapter 2" does NOT reset the chat history. - Context Flow: Highlighting text in Chapter 1 and clicking "Ask AI" immediately opens the chat window and answers the specific question about that text. - Accessibility: The "Ask AI" popup disappears when selection is cleared or user clicks away. - Mobile: Selection tooltip is disabled or optimized on mobile to prevent conflict with native OS copy menus. Non-Goals: - NOT handling image selection. - NOT storing history in a database yet (Session storage is fine for MVP). User Stories: - "As a student, I can highlight a confusing sentence in Chapter 3, click 'Ask AI', and get an instant explanation without typing."

## Response snapshot

Created feature branch `015-global-context-chat`, detailed specification, and validation checklist. Spec includes requirements for Global State (ChatContext), Docusaurus Root Wrapper, and Contextual Selection Tooltip.

## Outcome

- ✅ Impact: Defined requirements for Global Context Chat.
- 🧪 Tests: N/A (Spec phase)
- 📁 Files: specs/015-global-context-chat/spec.md, specs/015-global-context-chat/checklists/requirements.md
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: This feature requires significant architectural changes (introducing global context and `Root.js` wrapping). The spec captures this complexity explicitly.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A