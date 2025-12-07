# Data Model: RAG Chat UI

## Frontend Entities

### ChatMessage
**Purpose**: Represents a single message in the chat history.
**Location**: `src/components/RagChat/types.ts`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique UUID. |
| `role` | `'user' \| 'ai'` | Sender. |
| `content` | `string` | The message text. |
| `sources` | `string[]` | List of citations (e.g., "Section 1.2"). |
| `timestamp` | `number` | Unix timestamp. |

### ChatState
**Purpose**: Represents the internal state of the Chat Component.

| Field | Type | Description |
|-------|------|-------------|
| `isOpen` | `boolean` | Visibility of the chat window. |
| `isLoading` | `boolean` | True when waiting for API response. |
| `messages` | `ChatMessage[]` | History of current session. |
| `error` | `string \| null` | Error message if API fails. |
