# CareerFit AI

Voice-based AI interviewer & career coach — FastAPI backend.

## Quick Start

```bash
# 1. Create & activate a virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Fill in SUPABASE_URL, SUPABASE_KEY, GROQ_API_KEY, etc.

# 4. Run the development server
uvicorn app.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

## Project Structure

```
app/
├── main.py            # FastAPI app factory & lifespan
├── config.py          # pydantic-settings configuration
├── dependencies.py    # Shared FastAPI dependencies
├── exceptions.py      # Custom exception classes
├── middleware.py       # CORS, error handlers
├── core/              # Infrastructure clients (Supabase, Groq, TTS, Auth)
├── models/            # Pydantic request/response schemas
├── agents/            # AI agent logic (Setup, Interviewer, Coach)
├── routers/           # HTTP & WebSocket endpoint definitions
├── services/          # Business logic layer
└── utils/             # Helpers (audio, prompts, validators)
tests/                 # Pytest test suite
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database & Auth | Supabase (PostgreSQL + Google OAuth) |
| LLM | Groq |
| STT | Groq Whisper |
| TTS | gTTS |
| Config | pydantic-settings |
