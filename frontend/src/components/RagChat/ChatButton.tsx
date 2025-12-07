import React from 'react';
import { Bot, Sparkles } from 'lucide-react';
import styles from './styles.module.css';

interface ChatButtonProps {
  onClick: () => void;
  isOpen: boolean;
}

export const ChatButton: React.FC<ChatButtonProps> = ({ onClick, isOpen }) => {
  if (isOpen) return null;

  return (
    <button className={styles.triggerButton} onClick={onClick} aria-label="Open Chat">
      <Bot size={24} />
    </button>
  );
};
