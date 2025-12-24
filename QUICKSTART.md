# Quick Start Guide - Disha AI Health Coach

Get up and running in 5 minutes!

## Prerequisites

- Docker Desktop installed
- API key from Google Gemini or OpenAI (GPT)

## Steps

### 1. Get Your API Key

**Option A: Google Gemini (Recommended)**
- Go to https://aistudio.google.com/app/apikey
- Sign in with your Google account
- Click "Create API Key"
- Copy it

**Option B: OpenAI GPT**
- Go to https://platform.openai.com/
- Sign up or log in
- Create an API key
- Copy it

### 2. Configure Environment

Open the `.env` file and add your API key:

```env
# For Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# OR for OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
```

### 3. Start the Application

**On Windows:**
```bash
start.bat
```

**On Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Or manually:**
```bash
docker-compose up --build
```

### 4. Open Your Browser

Navigate to:
```
http://localhost:3000
```

That's it! You should see the chat interface.

## What to Try

1. **Initial Greeting**: The AI will greet you and ask for your information
2. **Share Details**: Tell it your name, age, any health conditions
3. **Ask Health Questions**: Try asking about:
   - "I have a fever, what should I do?"
   - "I have a stomach ache"
   - "How can I improve my sleep?"
   - "What foods are good for diabetes?"

4. **Test Memory**: In a new message, ask "What do you remember about me?"
5. **Scroll Up**: Try scrolling to the top to load older messages

## Troubleshooting

### Docker not running?
- Start Docker Desktop
- Wait for it to fully start
- Try again

### API key not working?
- Check you copied the full key
- Make sure there are no extra spaces
- Verify the key is active in your dashboard

### Port already in use?
Edit `docker-compose.yml` and change ports:
```yaml
ports:
  - "3001:3000"  # Frontend
  - "8001:8000"  # Backend
```

### Can't connect to backend?
- Check all containers are running: `docker ps`
- View logs: `docker-compose logs backend`
- Restart: `docker-compose restart`

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Review [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) to understand the code

## Important Notes

- User ID is stored in browser's localStorage
- Clear localStorage to start a fresh conversation
- The AI is for informational purposes only, not medical diagnosis
- For emergencies, always call emergency services

## Stopping the Application

Press `Ctrl+C` in the terminal, then run:
```bash
docker-compose down
```

To remove all data:
```bash
docker-compose down -v
```

## Need Help?

- Check the logs: `docker-compose logs`
- View API documentation: http://localhost:8000/docs
- Open an issue on GitHub

---

Enjoy chatting with Disha! 💬🏥
