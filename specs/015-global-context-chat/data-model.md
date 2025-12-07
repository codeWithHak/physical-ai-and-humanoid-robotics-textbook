# Data Model: Global Chat Context

## Entities

### ChatContextProps
**Location**: `frontend/src/context/ChatContext.tsx`

| Field | Type | Description |
|-------|------|-------------|
| `isOpen` | `boolean` | Visibility of the chat window. |
| `setIsOpen` | `(open: boolean) => void` | Toggle visibility. |
| `messages` | `ChatMessage[]` | Chat history. |
| `isLoading` | `boolean` | Backend loading state. |
| `inputQuery` | `string` | Text to auto-fill in input. |
| `triggerAskAI` | `(text: string) => void` | Open chat and set query. |
| `sendMessage` | `(text: string) => Promise<void>` | Send a message to backend. |

### TooltipState
**Location**: `frontend/src/components/SelectionTooltip/index.tsx`

| Field | Type | Description |
|-------|------|-------------|
| `visible` | `boolean` | Tooltip visibility. |
| `top` | `number` | CSS top position. |
| `left` | `number` | CSS left position. |
| `text` | `string` | Selected text content. |