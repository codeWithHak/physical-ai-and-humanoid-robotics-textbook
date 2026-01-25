import React, { type ReactNode } from 'react';
import { useLocation } from '@docusaurus/router';
import { ChatProvider } from '../context/ChatContext';
import { RagChat } from '../components/RagChat';
import { SelectionTooltip } from '../components/SelectionTooltip';

interface RootProps {
  children: ReactNode;
}

// This is a global wrapper for your Docusaurus app.
// It allows you to add context providers or other global elements.
const Root = ({ children }: RootProps): JSX.Element => {
  const location = useLocation();
  const isDocsPage = location.pathname.startsWith('/docs');

  return (
    <ChatProvider>
      {children}
      {isDocsPage && <RagChat />}
      {isDocsPage && <SelectionTooltip />}
    </ChatProvider>
  );
};

export default Root;
