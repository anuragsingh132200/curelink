import React from 'react';
import ReactMarkdown from 'react-markdown';
import { format } from 'date-fns';
import './Message.css';

const Message = ({ message }) => {
  const isUser = message.role === 'user';
  const timestamp = message.created_at
    ? format(new Date(message.created_at), 'HH:mm')
    : '';

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-assistant'}`}>
      <div className="message-bubble">
        <div className="message-content">
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown>{message.content}</ReactMarkdown>
          )}
        </div>
        <div className="message-time">{timestamp}</div>
      </div>
    </div>
  );
};

export default Message;
