export interface ChatMessage {
  id: string;
  role: 'user' | 'ai';
  content: string;
  sources?: string[];
  timestamp: number;
}

export interface ChatState {
  isOpen: boolean;
  isLoading: boolean;
  messages: ChatMessage[];
  error: string | null;
}
