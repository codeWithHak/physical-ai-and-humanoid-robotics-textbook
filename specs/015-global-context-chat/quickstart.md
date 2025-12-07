# Quickstart: Global Context Chat

## Prerequisites

- **Frontend**: `npm start` in `frontend/`.
- **Backend**: `uvicorn src.main:app` in `backend/`.

## Testing Persistence

1. **Open Chat**: Click the floating button on the Home page.
2. **Type**: "Test Persistence".
3. **Navigate**: Click a link to "Chapter 1".
4. **Verify**: Chat window remains open and "Test Persistence" message is visible.

## Testing Contextual Ask

1. **Select Text**: Highlight any sentence (> 5 chars) on the page.
2. **Verify Tooltip**: "Ask AI" button appears above selection.
3. **Click Tooltip**: Click the button.
4. **Verify Action**:
   - Chat opens.
   - Query "Explain this: [selection]" is sent.
   - AI responds.

## Testing Mobile (Simulated)

1. **Toggle Device Toolbar**: In Chrome DevTools.
2. **Select Text**: Highlight text.
3. **Verify**: "Ask AI" tooltip does NOT appear (if touch simulation is active).