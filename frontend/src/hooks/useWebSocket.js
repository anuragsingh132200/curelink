import { useEffect, useRef, useState, useCallback } from 'react';
import { chatAPI } from '../services/api';

const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

const useWebSocket = (userId) => {
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [initialLoadComplete, setInitialLoadComplete] = useState(false);
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const reconnectAttempts = useRef(0);

  const connect = useCallback(() => {
    if (!userId) return;

    try {
      const ws = new WebSocket(`${WS_URL}/api/chat/ws/${userId}`);

      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        reconnectAttempts.current = 0;
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          if (data.type === 'message') {
            const newMessage = {
              id: data.id,
              role: data.role,
              content: data.content,
              created_at: data.created_at,
            };

            setMessages((prev) => {
              // For user messages, replace temp message with real one
              if (data.role === 'user') {
                const withoutTemp = prev.filter(msg => !msg.id.toString().startsWith('temp-'));
                return [...withoutTemp, newMessage];
              }

              // For assistant messages, check if it already exists to avoid duplicates
              const exists = prev.some(msg => msg.id === data.id);
              if (exists) {
                return prev;
              }

              return [...prev, newMessage];
            });
          } else if (data.type === 'typing_indicator') {
            setIsTyping(data.is_typing);
          } else if (data.type === 'error') {
            console.error('WebSocket error:', data.message);
          }
        } catch (error) {
          console.error('Error parsing message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);

        // Attempt to reconnect with exponential backoff
        if (reconnectAttempts.current < 5) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 30000);
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttempts.current += 1;
            connect();
          }, delay);
        }
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Error creating WebSocket:', error);
    }
  }, [userId]);

  const sendMessage = useCallback((content) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      // Immediately add user message to UI for instant feedback
      const userMessage = {
        id: `temp-${Date.now()}`,
        role: 'user',
        content,
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMessage]);

      // Send message through WebSocket
      wsRef.current.send(JSON.stringify({
        type: 'message',
        content,
      }));
    } else {
      console.error('WebSocket is not connected');
    }
  }, []);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  // Load initial messages when userId is available
  useEffect(() => {
    const loadInitialMessages = async () => {
      if (!userId || initialLoadComplete) return;

      try {
        const result = await chatAPI.getMessages(userId, 1, 50);
        if (result.messages && result.messages.length > 0) {
          setMessages(result.messages);
        }
        setInitialLoadComplete(true);
      } catch (error) {
        console.error('Error loading initial messages:', error);
        setInitialLoadComplete(true);
      }
    };

    loadInitialMessages();
  }, [userId, initialLoadComplete]);

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    messages,
    setMessages,
    sendMessage,
    isConnected,
    isTyping,
  };
};

export default useWebSocket;
