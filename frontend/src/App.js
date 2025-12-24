import React, { useEffect, useState } from 'react';
import ChatHeader from './components/ChatHeader';
import MessageList from './components/MessageList';
import MessageInput from './components/MessageInput';
import useWebSocket from './hooks/useWebSocket';
import { getUserId } from './utils/storage';
import './App.css';

function App() {
  const [userId] = useState(() => getUserId());
  const { messages, sendMessage, isConnected, isTyping } = useWebSocket(userId);

  const handleSendMessage = (content) => {
    sendMessage(content);
  };

  return (
    <div className="app">
      <ChatHeader isConnected={isConnected} />
      <MessageList
        messages={messages}
        isTyping={isTyping}
        userId={userId}
      />
      <MessageInput
        onSendMessage={handleSendMessage}
        disabled={!isConnected}
      />
    </div>
  );
}

export default App;
