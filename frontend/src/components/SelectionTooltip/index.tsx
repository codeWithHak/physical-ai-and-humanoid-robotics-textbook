import React, { useState, useEffect, useRef, useCallback } from 'react';
import { MessageCircle } from 'lucide-react';
import { useChat } from '../../context/ChatContext';
import styles from './styles.module.css';

export const SelectionTooltip: React.FC = () => {
  const { triggerAskAI } = useChat();
  const [visible, setVisible] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [selectedText, setSelectedText] = useState('');
  const tooltipRef = useRef<HTMLDivElement>(null);

  // Helper to check if the current device is likely a touch device
  const isTouchDevice = useCallback(() => {
    if (typeof window === 'undefined') return false;
    return ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0);
  }, []);

  const handleSelectionChange = useCallback(() => {
    if (isTouchDevice() || window.innerWidth < 768) { // Disable on mobile/small screens
      setVisible(false);
      return;
    }

    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) {
      setVisible(false);
      return;
    }

    const range = selection.getRangeAt(0);
    const text = selection.toString().trim();

    // Check if selection is within a text node and not a form input
    const isTextNode = range.commonAncestorContainer.nodeType === Node.TEXT_NODE || range.commonAncestorContainer.parentNode?.nodeName !== 'INPUT';
    const isMeaningfulSelection = text.length > 5;
    
    // Ensure the tooltip doesn't appear when selecting within itself
    const isInsideTooltip = tooltipRef.current && tooltipRef.current.contains(range.commonAncestorContainer);

    if (isMeaningfulSelection && isTextNode && !isInsideTooltip) {
      const rect = range.getBoundingClientRect();
      setPosition({
        x: rect.left + window.scrollX + rect.width / 2,
        y: rect.top + window.scrollY - 10, // Position above the selection
      });
      setSelectedText(text);
      setVisible(true);
    } else {
      setVisible(false);
    }
  }, [isTouchDevice]);

  const handleClickAway = useCallback((event: MouseEvent) => {
    if (tooltipRef.current && !tooltipRef.current.contains(event.target as Node)) {
      setVisible(false);
    }
  }, []);

  useEffect(() => {
    document.addEventListener('mouseup', handleSelectionChange);
    document.addEventListener('selectionchange', handleSelectionChange);
    document.addEventListener('mousedown', handleClickAway);

    return () => {
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('selectionchange', handleSelectionChange);
      document.removeEventListener('mousedown', handleClickAway);
    };
  }, [handleSelectionChange, handleClickAway]);

  const handleAskAI = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    console.log('[SelectionTooltip] Ask clicked with text:', selectedText);
    if (selectedText) {
      console.log('[SelectionTooltip] Calling triggerAskAI...');
      triggerAskAI(selectedText);
      setVisible(false);
      console.log('[SelectionTooltip] triggerAskAI called successfully');
    }
  };

  return (
    <div
      ref={tooltipRef}
      className={`${styles.selectionTooltip} ${visible ? styles.visible : ''}`}
      style={{ top: position.y, left: position.x }}
      onClick={handleAskAI}
      onMouseDown={handleAskAI}
    >
      <MessageCircle size={14} style={{ marginRight: '4px' }} />
      Ask
    </div>
  );
};
