# Disha - AI Health Coach

**India's first AI health coach** - A WhatsApp-like chat interface where users can get personalized health guidance and support from an AI health coach powered by Claude/GPT.

## Features

- **WhatsApp-like Chat Interface**: Clean, intuitive chat UI with real-time messaging
- **WebSocket Support**: Real-time communication with typing indicators
- **Infinite Scroll**: Load older messages automatically when scrolling up
- **LLM Integration**: Powered by Anthropic Claude or OpenAI GPT
- **Context Management**: Intelligent token management to handle context overflow
- **Long-term Memory**: Extracts and stores important user information across conversations
- **Medical Protocols**: Built-in knowledge base for common health conditions (fever, stomach ache, headache, etc.)
- **Personalized Responses**: Uses user profile and memories for tailored advice
- **Onboarding Flow**: Friendly initial conversation to gather user information
- **Fully Dockerized**: Easy deployment with Docker Compose

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Cache**: Redis
- **LLM**: Anthropic Claude / OpenAI GPT
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **WebSocket**: Native FastAPI WebSocket support

### Frontend
- **Framework**: React
- **Styling**: CSS (WhatsApp-inspired design)
- **HTTP Client**: Axios
- **Markdown**: react-markdown
- **Date Handling**: date-fns

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15
- **Cache**: Redis 7

## Architecture Overview

### Backend Architecture

```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py           # Configuration management
│   │   ├── database.py         # Database session management
│   │   └── redis_client.py     # Redis client wrapper
│   ├── models/
│   │   ├── user.py             # User model (profile, medical info)
│   │   ├── message.py          # Message model (chat history)
│   │   └── memory.py           # Memory model (long-term facts)
│   ├── schemas/
│   │   ├── message.py          # Pydantic schemas for messages
│   │   ├── user.py             # Pydantic schemas for users
│   │   └── memory.py           # Pydantic schemas for memories
│   ├── routes/
│   │   └── chat.py             # Chat endpoints & WebSocket
│   ├── services/
│   │   ├── llm_service.py      # LLM integration & context management
│   │   ├── chat_service.py     # Chat business logic
│   │   └── memory_service.py   # Memory extraction & retrieval
│   └── utils/
│       └── protocols.py        # Medical protocols knowledge base
└── alembic/                    # Database migrations
```

### Frontend Architecture

```
frontend/
├── src/
│   ├── App.js                  # Main application component
│   ├── components/
│   │   ├── ChatHeader.js       # Header with status indicator
│   │   ├── MessageList.js      # Message list with infinite scroll
│   │   ├── Message.js          # Individual message component
│   │   ├── MessageInput.js     # Message input with send button
│   │   └── TypingIndicator.js  # Animated typing indicator
│   ├── hooks/
│   │   └── useWebSocket.js     # WebSocket connection hook
│   ├── services/
│   │   └── api.js              # API client
│   └── utils/
│       └── storage.js          # Local storage utilities
└── public/
```

## Design Decisions

### 1. LLM Context Management

**Problem**: LLMs have token limits, and long conversations can overflow the context window.

**Solution**: Implemented a multi-layered context strategy:
- **Token Counting**: Estimates tokens before sending to LLM
- **Conversation Trimming**: Keeps system prompt + most recent N messages that fit within token limit
- **Long-term Memory**: Important facts extracted and stored separately, then injected into system prompt
- **Protocol Matching**: Relevant medical protocols dynamically added to context based on user query

### 2. Memory System

**Approach**: Automatic extraction of important information:
- **Medical Information**: Diagnoses, medications, allergies (importance: 0.85-0.9)
- **Personal Facts**: Age, name, occupation (importance: 0.7)
- **Preferences**: Likes, dislikes, habits (importance: 0.6)
- **Access-based Ranking**: Frequently accessed memories prioritized

**Implementation**:
- Pattern matching and keyword detection
- Importance scoring
- Recency and access count tracking

### 3. Medical Protocols

**Knowledge Base**: Pre-defined protocols for common conditions:
- Fever management
- Stomach ache care
- Headache treatment
- Cold & flu guidelines
- General wellness advice
- Refund policies

**Retrieval**: Keyword matching on user messages to inject relevant protocols into LLM context.

### 4. WebSocket vs REST API

**Both Supported**:
- **WebSocket**: Primary interface for real-time chat experience with typing indicators
- **REST API**: Available for fetching historical messages with pagination

**Benefits**:
- Typing indicators
- Immediate message delivery
- Automatic reconnection with exponential backoff
- Better user experience (feels like WhatsApp)

### 5. Frontend State Management

**No Redux/MobX**: Used React hooks for simplicity:
- `useWebSocket`: Manages WebSocket connection and messages
- `useState`: Local component state
- `useEffect`: Side effects and lifecycle

**Rationale**: For this scope, hooks provide sufficient state management without added complexity.

### 6. Database Schema

**User Table**: Stores profile and medical information
**Message Table**: Complete chat history with role-based storage
**Memory Table**: Long-term facts with importance scoring

**Relationships**:
- User → Messages (1:N)
- User → Memories (1:N)

### 7. Infinite Scroll Implementation

**Approach**:
- Messages loaded in reverse chronological order (newest first)
- Pagination from API
- Scroll detection at top of container
- Automatic loading when scrolled to top
- Prevents duplicate loading with flags

## Setup Instructions

### Prerequisites

- Docker & Docker Compose installed
- API key for Anthropic Claude OR OpenAI GPT

### Local Setup (Step by Step)

#### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd curelink
```

#### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Choose your LLM provider
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
# OR
OPENAI_API_KEY=sk-xxxxxxxxxxxxx

# Set the provider (anthropic or openai)
LLM_PROVIDER=anthropic

# For Anthropic Claude
LLM_MODEL=claude-3-5-sonnet-20241022

# For OpenAI
# LLM_MODEL=gpt-4-turbo-preview

# Database (default is fine for Docker)
DATABASE_URL=postgresql://curelink:curelink_password@postgres:5432/curelink_db

# Redis (default is fine for Docker)
REDIS_URL=redis://redis:6379
```

#### 3. Start the Application

Using Docker Compose:

```bash
docker-compose up --build
```

This will start:
- PostgreSQL database on port 5432
- Redis on port 6379
- Backend API on port 8000
- Frontend React app on port 3000

#### 4. Access the Application

Open your browser and navigate to:

```
http://localhost:3000
```

The backend API is available at:

```
http://localhost:8000
```

API documentation (Swagger):

```
http://localhost:8000/docs
```

### Running Without Docker (Manual Setup)

#### Backend Setup

1. **Create Virtual Environment**:

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

2. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

3. **Set Up PostgreSQL**:

Install PostgreSQL and create a database:

```sql
CREATE DATABASE curelink_db;
CREATE USER curelink WITH PASSWORD 'curelink_password';
GRANT ALL PRIVILEGES ON DATABASE curelink_db TO curelink;
```

4. **Set Up Redis**:

Install and start Redis server.

5. **Configure Environment**:

Create a `.env` file in the backend directory with your settings.

6. **Run Migrations**:

```bash
alembic upgrade head
```

7. **Start Backend**:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup

1. **Install Dependencies**:

```bash
cd frontend
npm install
```

2. **Configure Environment**:

Create `.env.local`:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

3. **Start Frontend**:

```bash
npm start
```

The app will open at `http://localhost:3000`.

## API Documentation

### REST Endpoints

#### Get User
```
GET /api/chat/user/{user_id}
```

#### Initialize Chat
```
POST /api/chat/user/{user_id}/initialize
```

#### Get Messages (Paginated)
```
GET /api/chat/user/{user_id}/messages?page=1&per_page=20
```

#### Send Message
```
POST /api/chat/user/{user_id}/message
Body: { "content": "message text" }
```

### WebSocket Endpoint

```
WS /api/chat/ws/{user_id}
```

**Message Format (Send)**:
```json
{
  "type": "message",
  "content": "Hello, I have a fever"
}
```

**Message Format (Receive)**:
```json
{
  "type": "message",
  "role": "assistant",
  "content": "I'm sorry to hear you have a fever...",
  "id": "uuid",
  "created_at": "2025-12-24T12:00:00"
}
```

**Typing Indicator**:
```json
{
  "type": "typing_indicator",
  "is_typing": true
}
```

## LLM Implementation Details

### Provider: Anthropic Claude

**Model**: `claude-3-5-sonnet-20241022`

**Prompting Strategy**:

1. **System Prompt**: Defines Disha's personality, role, and guidelines
2. **User Context**: Injects user profile (age, gender, conditions, medications)
3. **Memories**: Adds relevant long-term memories
4. **Protocols**: Includes matching medical protocols
5. **Conversation History**: Recent messages (trimmed to fit token limit)

**Example System Prompt Structure**:

```
You are Disha, India's first AI health coach...

[Role & Communication Style]

User Information:
- Name: John
- Age: 35
- Medical Conditions: Type 2 Diabetes

What You Remember:
- User prefers morning workouts
- Takes Metformin 500mg twice daily

Relevant Medical Protocols:
[Fever Management Protocol if user mentions fever]

[Recent Conversation]
```

### Context Overflow Handling

**Token Budget**:
- Max Context Tokens: 8000
- Max Response Tokens: 1000

**Trimming Strategy**:
1. Calculate system prompt tokens
2. Calculate available tokens for conversation
3. Add messages from most recent, working backwards
4. Stop when token limit reached

### Alternative: OpenAI GPT

Set `LLM_PROVIDER=openai` and `LLM_MODEL=gpt-4-turbo-preview` in `.env`.

The system adapts the prompting format for OpenAI's API.

## Testing

### Manual Testing Checklist

1. **Initial Load**:
   - Onboarding message appears
   - User can respond

2. **Chat Functionality**:
   - Messages send successfully
   - AI responds appropriately
   - Typing indicator shows during AI response
   - Messages appear in correct order

3. **Infinite Scroll**:
   - Scroll to top loads older messages
   - Loading indicator appears
   - No duplicate messages
   - "Start of conversation" appears when no more messages

4. **Context Awareness**:
   - AI remembers information from earlier in conversation
   - Profile updates (name, age) reflected in responses

5. **Medical Protocols**:
   - Mention "fever" gets fever protocol in response
   - Mention "stomach ache" gets stomach protocol
   - General health question gets relevant advice

6. **Edge Cases**:
   - Empty message prevented
   - Very long messages handled
   - Reconnection after network interruption
   - Multiple rapid messages

## Trade-offs & Future Improvements

### Current Trade-offs

1. **Simple Memory System**:
   - Current: Keyword-based extraction
   - Better: Embedding-based semantic search with vector DB (Pinecone, Weaviate)

2. **Protocol Matching**:
   - Current: Keyword matching
   - Better: Semantic similarity with embeddings

3. **No User Authentication**:
   - Current: Client-side generated user ID
   - Better: Proper auth with JWT/OAuth

4. **Single Session**:
   - Current: One continuous conversation
   - Better: Multiple sessions/conversations

5. **No Message Editing/Deletion**:
   - Current: Messages immutable
   - Better: Allow edit/delete with history

### If I Had More Time...

#### High Priority

1. **Vector Database for RAG**:
   - Use Pinecone/Qdrant for semantic search
   - Embed medical knowledge base
   - Better protocol matching
   - More relevant context retrieval

2. **User Authentication**:
   - JWT-based auth
   - Secure user sessions
   - Multi-device support

3. **Enhanced Memory System**:
   - Automatic summarization of long conversations
   - Memory consolidation
   - Importance re-ranking over time

4. **Testing**:
   - Unit tests (pytest for backend, Jest for frontend)
   - Integration tests
   - E2E tests (Playwright/Cypress)

5. **Monitoring & Logging**:
   - Structured logging
   - Error tracking (Sentry)
   - Analytics dashboard
   - Token usage tracking

#### Medium Priority

6. **Multi-session Support**:
   - Start new conversations
   - Archive old conversations
   - Search across conversations

7. **Rich Media Support**:
   - Image upload for symptoms
   - Voice messages
   - PDF reports

8. **Improved UI/UX**:
   - Dark mode
   - Message reactions
   - Message search
   - Export conversation

9. **Advanced Features**:
   - Appointment scheduling
   - Medication reminders
   - Health tracking integration
   - Symptom checker

10. **Performance Optimizations**:
    - Message caching with Redis
    - Lazy loading components
    - Service workers for offline support
    - CDN for static assets

#### Low Priority

11. **Admin Dashboard**:
    - User management
    - Conversation monitoring
    - Analytics & insights

12. **Internationalization**:
    - Multi-language support
    - Regional medical guidelines

13. **Compliance**:
    - HIPAA compliance enhancements
    - Data encryption at rest
    - Audit logs

## Deployment

### Deployment Options

#### 1. Render.com (Recommended for Demo)

**Backend**:
- Create new Web Service
- Connect GitHub repo
- Set build command: `cd backend && pip install -r requirements.txt`
- Set start command: `cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add environment variables

**Frontend**:
- Create new Static Site
- Connect GitHub repo
- Set build command: `cd frontend && npm install && npm run build`
- Set publish directory: `frontend/build`

**Database**:
- Create PostgreSQL database
- Create Redis instance
- Connect to backend

#### 2. Vercel (Frontend) + Railway (Backend)

**Frontend** on Vercel:
```bash
cd frontend
vercel --prod
```

**Backend** on Railway:
- Connect GitHub repo
- Auto-detects Python
- Add PostgreSQL & Redis plugins

#### 3. AWS/GCP/Azure

- Use ECS/Cloud Run/Container Apps for containers
- RDS/Cloud SQL for PostgreSQL
- ElastiCache/Memorystore for Redis
- Load balancer for production traffic

### Environment Variables for Production

```env
# Production settings
ENVIRONMENT=production
SECRET_KEY=<strong-random-secret>

# LLM
ANTHROPIC_API_KEY=<your-key>
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022

# Database (from hosting provider)
DATABASE_URL=<production-database-url>

# Redis (from hosting provider)
REDIS_URL=<production-redis-url>

# Frontend URLs
REACT_APP_API_URL=<backend-url>
REACT_APP_WS_URL=<websocket-url>
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - feel free to use this for your own projects!

## Contact

For questions or feedback, reach out at: anurag132200@gmail.com

---

Built with ❤️ for Curelink
