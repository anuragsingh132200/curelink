import React from 'react';
import './ChatHeader.css';

const ChatHeader = ({ isConnected }) => {
  return (
    <div className="chat-header">
      <div className="header-content">
        <div className="header-avatar">
          <span className="avatar-icon">🏥</span>
        </div>
        <div className="header-info">
          <h1 className="header-title">Disha</h1>
          <p className="header-status">
            {isConnected ? (
              <>
                <span className="status-dot online"></span>
                Online
              </>
            ) : (
              <>
                <span className="status-dot offline"></span>
                Connecting...
              </>
            )}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatHeader;
