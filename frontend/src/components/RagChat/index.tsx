import React, { useState } from 'react';
import { ChatButton } from './ChatButton';
import { ChatWindow } from './ChatWindow';
import { ChatMessage } from './types';

const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://physicalaibookbackend.vercel.app/api/chat'
  : 'http://127.0.0.1:8000/api/chat';

export const RagChat: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const handleSendMessage = async (text: string) => {
    // Add user message
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
      console.error('Chat error:', error);
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
  };

  return (
    <>
      <ChatButton onClick={() => setIsOpen(true)} isOpen={isOpen} />
      <ChatWindow
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        messages={messages}
        isLoading={isLoading}
        onSendMessage={handleSendMessage}
      />
    </>
  );
};
