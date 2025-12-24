# Project Structure

```
curelink/
│
├── README.md                     # Main documentation
├── DEPLOYMENT.md                 # Deployment guide
├── PROJECT_STRUCTURE.md          # This file
├── .env                          # Environment variables (not in git)
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Docker orchestration
├── start.sh                      # Linux/Mac startup script
├── start.bat                     # Windows startup script
│
├── backend/                      # Python FastAPI backend
│   ├── Dockerfile                # Backend Docker configuration
│   ├── requirements.txt          # Python dependencies
│   ├── alembic.ini               # Alembic configuration
│   │
│   ├── alembic/                  # Database migrations
│   │   ├── env.py                # Alembic environment
│   │   ├── script.py.mako        # Migration template
│   │   └── versions/             # Migration files
│   │       └── 001_initial_migration.py
│   │
│   └── app/                      # Application code
│       ├── __init__.py
│       ├── main.py               # FastAPI app entry point
│       │
│       ├── core/                 # Core utilities
│       │   ├── __init__.py
│       │   ├── config.py         # Settings & configuration
│       │   ├── database.py       # Database connection
│       │   └── redis_client.py   # Redis client
│       │
│       ├── models/               # SQLAlchemy models
│       │   ├── __init__.py
│       │   ├── user.py           # User model
│       │   ├── message.py        # Message model
│       │   └── memory.py         # Memory model
│       │
│       ├── schemas/              # Pydantic schemas
│       │   ├── __init__.py
│       │   ├── message.py        # Message schemas
│       │   ├── user.py           # User schemas
│       │   └── memory.py         # Memory schemas
│       │
│       ├── routes/               # API endpoints
│       │   ├── __init__.py
│       │   └── chat.py           # Chat routes + WebSocket
│       │
│       ├── services/             # Business logic
│       │   ├── __init__.py
│       │   ├── llm_service.py    # LLM integration
│       │   ├── chat_service.py   # Chat logic
│       │   └── memory_service.py # Memory management
│       │
│       └── utils/                # Utilities
│           ├── __init__.py
│           └── protocols.py      # Medical protocols
│
└── frontend/                     # React frontend
    ├── Dockerfile                # Frontend Docker configuration
    ├── .dockerignore             # Docker ignore rules
    ├── package.json              # NPM dependencies
    │
    ├── public/                   # Static files
    │   └── index.html            # HTML template
    │
    └── src/                      # Source code
        ├── index.js              # Entry point
        ├── index.css             # Global styles
        ├── App.js                # Main App component
        ├── App.css               # App styles
        │
        ├── components/           # React components
        │   ├── ChatHeader.js     # Chat header
        │   ├── ChatHeader.css
        │   ├── MessageList.js    # Message list with infinite scroll
        │   ├── MessageList.css
        │   ├── Message.js        # Individual message
        │   ├── Message.css
        │   ├── MessageInput.js   # Message input
        │   ├── MessageInput.css
        │   ├── TypingIndicator.js # Typing animation
        │   └── TypingIndicator.css
        │
        ├── hooks/                # Custom React hooks
        │   └── useWebSocket.js   # WebSocket hook
        │
        ├── services/             # API services
        │   └── api.js            # API client
        │
        └── utils/                # Utilities
            └── storage.js        # LocalStorage utils
```

## Component Relationships

### Backend Flow

```
Request → FastAPI (main.py)
    ↓
Router (chat.py)
    ↓
Service Layer (chat_service.py, llm_service.py)
    ↓
Models & Database (SQLAlchemy)
```

### Frontend Flow

```
App.js
    ├── ChatHeader (status display)
    ├── MessageList (messages + infinite scroll)
    │   ├── Message (individual message)
    │   └── TypingIndicator (when AI is typing)
    └── MessageInput (user input)

WebSocket Hook (useWebSocket.js)
    → Manages real-time connection
    → Updates message state
```

### Data Flow

```
User Input (MessageInput)
    ↓
WebSocket → Backend
    ↓
chat_service.py
    ├── Save user message
    ├── Get conversation context
    ├── Get user memories
    └── Call LLM service
        ↓
    llm_service.py
        ├── Build system prompt
        ├── Add user context
        ├── Add memories
        ├── Add medical protocols
        ├── Trim conversation history
        └── Call Anthropic/OpenAI API
            ↓
        AI Response
            ↓
    Save assistant message
    Extract new memories
        ↓
WebSocket → Frontend
    ↓
Display in MessageList
```

## Key Files Explained

### Backend

**`app/main.py`**
- FastAPI application initialization
- CORS middleware configuration
- Route registration
- Startup/shutdown events

**`app/core/config.py`**
- Environment variable management
- Application settings
- LLM configuration
- Database URLs

**`app/core/database.py`**
- SQLAlchemy engine creation
- Session management
- Database connection pooling

**`app/models/*.py`**
- Database table definitions
- Relationships between models
- Column definitions

**`app/services/llm_service.py`**
- LLM provider abstraction
- Token counting and trimming
- System prompt construction
- Context management

**`app/services/chat_service.py`**
- Message CRUD operations
- Conversation context retrieval
- User management
- Orchestrates LLM calls

**`app/services/memory_service.py`**
- Memory extraction from conversations
- Importance scoring
- Memory retrieval for context

**`app/utils/protocols.py`**
- Medical knowledge base
- Protocol matching logic
- Refund policies

**`app/routes/chat.py`**
- REST API endpoints
- WebSocket endpoint
- Connection management
- Message routing

### Frontend

**`src/App.js`**
- Main application component
- State management
- Component composition

**`src/hooks/useWebSocket.js`**
- WebSocket connection logic
- Automatic reconnection
- Message state management
- Typing indicator state

**`src/components/MessageList.js`**
- Infinite scroll implementation
- Message rendering
- Loading older messages
- Scroll management

**`src/components/Message.js`**
- Individual message display
- Markdown rendering
- Timestamp formatting

**`src/components/MessageInput.js`**
- Text input handling
- Send message logic
- Enter key handling

**`src/services/api.js`**
- HTTP client (Axios)
- REST API calls
- Error handling

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name VARCHAR,
    phone VARCHAR,
    age VARCHAR,
    gender VARCHAR,
    medical_conditions JSON,
    medications JSON,
    allergies JSON,
    onboarding_completed BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    role VARCHAR,  -- 'user' or 'assistant'
    content TEXT,
    created_at TIMESTAMP,
    is_onboarding BOOLEAN,
    metadata VARCHAR,
    tokens_used INTEGER
);

CREATE INDEX idx_messages_created_at ON messages(created_at);
```

### Memories Table
```sql
CREATE TABLE memories (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    content TEXT,
    memory_type VARCHAR,  -- 'fact', 'preference', 'medical', 'interaction'
    importance FLOAT,
    created_at TIMESTAMP,
    last_accessed TIMESTAMP,
    access_count FLOAT
);
```

## API Endpoints

### REST API

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/chat/user/{user_id}` - Get user info
- `POST /api/chat/user/{user_id}/initialize` - Initialize chat
- `GET /api/chat/user/{user_id}/messages` - Get paginated messages
- `POST /api/chat/user/{user_id}/message` - Send message (REST fallback)

### WebSocket

- `WS /api/chat/ws/{user_id}` - Real-time chat connection

## Environment Variables

Required:
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` - LLM API key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string

Optional:
- `LLM_PROVIDER` - 'anthropic' or 'openai' (default: anthropic)
- `LLM_MODEL` - Model name
- `MAX_CONTEXT_TOKENS` - Max tokens for context (default: 8000)
- `MAX_RESPONSE_TOKENS` - Max tokens for response (default: 1000)
- `MESSAGES_PER_PAGE` - Pagination size (default: 20)
- `ENVIRONMENT` - 'development' or 'production'

## Technologies Used

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **Pydantic** - Data validation
- **Anthropic/OpenAI SDK** - LLM integration
- **Redis** - Caching layer
- **PostgreSQL** - Database

### Frontend
- **React** - UI framework
- **Axios** - HTTP client
- **react-markdown** - Markdown rendering
- **date-fns** - Date formatting
- **WebSocket API** - Real-time communication

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **PostgreSQL** - Database
- **Redis** - Cache/session storage
