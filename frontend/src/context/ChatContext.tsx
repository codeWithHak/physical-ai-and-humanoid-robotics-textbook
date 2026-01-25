import React, { createContext, useContext, useState, ReactNode, useCallback } from 'react';
import { ChatMessage } from '../components/RagChat/types'; // Re-use message type from RagChat

interface ChatContextProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  messages: ChatMessage[];
  isLoading: boolean;
  inputQuery: string; // For auto-filling input
  triggerAskAI: (text: string) => void; // For contextual ask
  sendMessage: (text: string) => Promise<void>; // Actual send logic
  clearMessages: () => void;
  clearInputQuery: () => void; // Clear input query after use
}

const ChatContext = createContext<ChatContextProps | undefined>(undefined);

// Hugging Face Spaces backend
const API_URL = 'https://hak-16-physical-ai-backend.hf.space/api/chat';
// const API_URL = 'http://localhost:8000/api/chat';

export const ChatProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputQuery, setInputQuery] = useState('');

  const sendMessage = useCallback(async (text: string) => {
    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      
      const aiMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'ai',
        content: data.answer,
        sources: data.sources,
        timestamp: Date.now(),
      };
      
      setMessages((prev) => [...prev, aiMsg]);
    } catch (error) {
      console.error('Chat API error:', error);
      const errorMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'ai',
        content: "I'm having trouble connecting to my brain right now. Please try again later.",
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const triggerAskAI = useCallback((text: string) => {
    console.log('[ChatContext] triggerAskAI called with text:', text);
    setIsOpen(true);
    console.log('[ChatContext] Chat opened');
    
    // Create a hidden prompt that wraps the selected text
    const hiddenPrompt = `Can you explain this: "${text}"`;
    
    // Show only the selected text to the user in the chat
    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text, // User sees only the selected text
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    
    // Send the hidden prompt to the API
    console.log('[ChatContext] Sending message with hidden prompt...');
    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: hiddenPrompt }), // Send the wrapped prompt
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        
        const aiMsg: ChatMessage = {
          id: crypto.randomUUID(),
          role: 'ai',
          content: data.answer,
          sources: data.sources,
          timestamp: Date.now(),
        };
        
        setMessages((prev) => [...prev, aiMsg]);
      })
      .catch((error) => {
        console.error('Chat API error:', error);
        const errorMsg: ChatMessage = {
          id: crypto.randomUUID(),
          role: 'ai',
          content: "I'm having trouble connecting to my brain right now. Please try again later.",
          timestamp: Date.now(),
        };
        setMessages((prev) => [...prev, errorMsg]);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  const clearInputQuery = useCallback(() => {
    setInputQuery('');
  }, []);

  const value = {
    isOpen,
    setIsOpen,
    messages,
    isLoading,
    inputQuery,
    triggerAskAI,
    sendMessage,
    clearMessages,
    clearInputQuery,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};
