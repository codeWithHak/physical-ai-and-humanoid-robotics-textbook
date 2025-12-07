# Research: RAG Frontend UI (The Chatbot)

**Status**: Complete
**Date**: 2025-12-07

## Technical Context

**Language/Version**: TypeScript 5.x, React 18+
**Framework**: Docusaurus v3+
**Styling**: CSS Modules (`styles.module.css`) + Docusaurus "Infima" vars override.
**Icons**: `lucide-react` (or standard Docusaurus icons).

## Decisions & Rationale

### 1. Component Architecture
- **Decision**: Create a self-contained feature directory `src/components/RagChat/`.
- **Rationale**: Keeps logic, styles, and types co-located. Easy to mount anywhere.
- **Structure**:
  - `index.tsx`: Main logic (state machine).
  - `ChatWindow.tsx`: Presentational component for the panel.
  - `ChatButton.tsx`: Presentational component for the trigger.
  - `styles.module.css`: Scoped styles.

### 2. State Management
- **Decision**: Local React `useState` / `useReducer`.
- **Rationale**: Complexity is low (open/close, message list). No need for Redux/Context yet.

### 3. Global Integration
- **Decision**: Mount in `src/pages/index.tsx` (Landing Page) for MVP.
- **Rationale**: Swizzling `Layout` or creating a Layout Wrapper can be fragile in Docusaurus updates. The Spec allows this fallback.
- **Plan**:
  1. Build component.
  2. Import and render in `src/pages/index.tsx`.
  3. (Optional Polish) Move to `src/theme/Root.js` (Docusaurus "Root" component) for truly global presence if time permits.

### 4. Styling Strategy
- **Decision**: Glass-morphism via CSS `backdrop-filter: blur()`.
- **Rationale**: User mandated aesthetic.
- **Vars**:
  - Primary: `#BFE600`
  - Background: `rgba(0, 0, 0, 0.9)`
  - Border: `1px solid #BFE600`

## Open Questions Resolved

- **Icons**: Will use `lucide-react` if available, or SVG assets if not. `lucide-react` is not a default Docusaurus dependency but commonly used. Will check `package.json` or use generic SVG placeholders.
- **Backend URL**: Hardcoded `http://127.0.0.1:8000/api/chat` for Dev, relative `/api/chat` or Env var for Prod.
