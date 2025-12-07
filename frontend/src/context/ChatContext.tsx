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

const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://physicalaibookbackend.vercel.app/api/chat'
  : 'http://127.0.0.1:8000/api/chat';

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
    setIsOpen(true);
    setInputQuery(text); // Set for display purposes
    // Automatically send the message
    sendMessage(text);
    // Clear inputQuery after a short delay to prevent re-sends
    setTimeout(() => setInputQuery(''), 100);
  }, [sendMessage]);

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
