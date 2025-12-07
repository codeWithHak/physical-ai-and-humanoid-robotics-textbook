---
id: 0001
title: Spec for RAG Frontend UI
stage: spec
date: 2025-12-07
surface: agent
model: gemini-2.0-flash-exp
feature: 014-rag-chatbot-ui
branch: 014-rag-chatbot-ui
user: hak
command: /sp.specify
labels: ["rag", "frontend", "react", "docusaurus", "spec"]
links:
  spec: specs/014-rag-chatbot-ui/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/014-rag-chatbot-ui/spec.md
 - specs/014-rag-chatbot-ui/checklists/requirements.md
tests: []
---

## Prompt

Feature: RAG Frontend UI (The Chatbot) Intent: Create a custom, fully integrated React Chat Component (`<RagChat />`) that floats in the bottom-right corner of the Docusaurus site. It connects to the FastAPI backend to send user queries and render AI responses with citations. Feature Scope (Component Architecture): 1. The Component (`src/components/RagChat/index.tsx`): - **State:** `isOpen` (toggle window), `messages` (list of chats), `isLoading` (typing indicator). - **UI Layout:** - **Trigger Button:** A circular floating button with a "Robot/Sparkle" icon. Glows #BFE600 on hover. - **Chat Window:** A glass-morphism panel (Black background, 90% opacity, Neon Green borders). - **Message Bubble:** - User: Gray background, right align. - AI: Black background, left align, Neon text. - **Citations:** If the API returns `sources`, render them as small clickable badges (e.g., "Section 2.1") below the AI response. - **Network Logic:** - `POST` to `http://127.0.0.1:8000/api/chat` (Dev) or your Vercel URL (Prod). - Handle loading states and error states gracefully. 2. Global Integration (`src/theme/Layout.tsx`): - Wrap the default Docusaurus Layout to include `<RagChat />` so it appears on *every* page. - *Note:* If Swizzling is too complex for the MVP, instruct the Plan to simply mount it in `src/pages/index.tsx` first for testing. 3. Styling (`src/components/RagChat/styles.module.css`): - Strict adherence to the "Lufga" font family. - Use CSS Variables for colors (`var(--ifm-color-primary)` which we set to #BFE600). - Mobile Responsive: On mobile, the chat window takes up 100% width/height when open. Success Criteria (SMART): - Integration: The Chat Button appears on the landing page. - Interaction: User types "What is a Node?", waits ~3s, and sees the response. - Citations: The response includes a "Source: Section 2.2" badge. - Aesthetics: The component looks native to the "RoboLearn" dark theme, not like a generic Intercom widget. Non-Goals: - NOT implementing "Login/Auth" yet (Chat is public for now). - NOT implementing "Markdown Rendering" inside the chat bubbles (keep it simple text for MVP, or basic formatting). User Stories: - "As a reader, I can ask the book a question without losing my place in the chapter."

## Response snapshot

Created feature branch `014-rag-chatbot-ui`, detailed specification, and validation checklist. Spec includes requirements for the React Chat component, including UI/UX specifics (Glass-morphism, Neon Green) and backend integration requirements.

## Outcome

- ✅ Impact: Defined requirements for RAG Frontend UI.
- 🧪 Tests: N/A (Spec phase)
- 📁 Files: specs/014-rag-chatbot-ui/spec.md, specs/014-rag-chatbot-ui/checklists/requirements.md
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: User provided very detailed UI constraints, which were incorporated directly into the spec to ensure the visual identity is preserved.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A