import React, { useState, useRef, useEffect } from 'react';
import { X, Send } from 'lucide-react';
import styles from './styles.module.css';
import { ChatMessage } from './types';

interface ChatWindowProps {
  isOpen: boolean;
  onClose: () => void;
  messages: ChatMessage[];
  isLoading: boolean;
  onSendMessage: (text: string) => void;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  isOpen,
  onClose,
  messages,
  isLoading,
  onSendMessage,
}) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  if (!isOpen) return null;

  return (
    <div className={styles.chatWindow}>
      <div className={styles.header}>
        <span className={styles.headerTitle}>RoboLearn AI</span>
        <button className={styles.closeButton} onClick={onClose} aria-label="Close">
          <X size={20} />
        </button>
      </div>

      <div className={styles.messageList}>
        {messages.length === 0 && (
          <div className={styles.message} style={{ textAlign: 'center', color: '#888' }}>
            Ask me anything about the book!
          </div>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`${styles.message} ${
              msg.role === 'user' ? styles.userMessage : styles.aiMessage
            }`}
          >
            {msg.content}
            {msg.sources && msg.sources.length > 0 && (
              <div className={styles.citationContainer}>
                {msg.sources.map((source, idx) => (
                  <span key={idx} className={styles.citation}>
                    {source}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className={styles.typingIndicator}>
            AI is thinking...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className={styles.inputArea} onSubmit={handleSubmit}>
        <input
          type="text"
          className={styles.input}
          placeholder="Type a question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isLoading}
        />
        <button type="submit" className={styles.sendButton} disabled={isLoading || !input.trim()}>
          <Send size={18} />
        </button>
      </form>
    </div>
  );
};
