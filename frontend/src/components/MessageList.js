import React, { useEffect, useRef, useState } from 'react';
import Message from './Message';
import TypingIndicator from './TypingIndicator';
import { chatAPI } from '../services/api';
import './MessageList.css';

const MessageList = ({ messages, isTyping, userId }) => {
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [oldMessages, setOldMessages] = useState([]);
  const [isInitialLoad, setIsInitialLoad] = useState(true);
  const prevMessagesLengthRef = useRef(0);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    // Scroll to bottom when new messages arrive
    if (messages.length > prevMessagesLengthRef.current) {
      scrollToBottom();
      prevMessagesLengthRef.current = messages.length;
    }

    // Mark initial load as complete once we have messages
    if (isInitialLoad && messages.length > 0) {
      setIsInitialLoad(false);
    }
  }, [messages, isInitialLoad]);

  useEffect(() => {
    // Scroll to bottom when typing indicator appears
    if (isTyping) {
      scrollToBottom();
    }
  }, [isTyping]);

  const loadOlderMessages = async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    try {
      const result = await chatAPI.getMessages(userId, page + 1, 20);

      if (result.messages && result.messages.length > 0) {
        setOldMessages((prev) => [...result.messages, ...prev]);
        setPage((prev) => prev + 1);
        setHasMore(result.has_more);
      } else {
        setHasMore(false);
      }
    } catch (error) {
      console.error('Error loading messages:', error);
      setHasMore(false);
    } finally {
      setLoading(false);
    }
  };

  const handleScroll = (e) => {
    const { scrollTop } = e.target;

    // Load more messages when scrolled to top
    if (scrollTop === 0 && hasMore && !loading) {
      loadOlderMessages();
    }
  };

  const allMessages = [...oldMessages, ...messages];

  return (
    <div
      className="message-list"
      ref={messagesContainerRef}
      onScroll={handleScroll}
    >
      {loading && (
        <div className="loading-indicator">
          <div className="spinner"></div>
        </div>
      )}

      {!hasMore && allMessages.length > 0 && (
        <div className="start-of-conversation">
          <p>Start of conversation</p>
        </div>
      )}

      {allMessages.length === 0 && !isInitialLoad && (
        <div className="empty-state">
          <p>No messages yet. Start a conversation!</p>
        </div>
      )}

      {allMessages.map((message) => (
        <Message key={message.id} message={message} />
      ))}

      {isTyping && <TypingIndicator />}

      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
