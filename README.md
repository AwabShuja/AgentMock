# AgentMock

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
├── main.py                # FastAPI app factory & lifespan
├── config.py              # pydantic-settings (all env vars)
├── dependencies.py        # Shared FastAPI dependencies (get_supabase, get_groq)
├── exceptions.py          # Custom exception hierarchy
├── middleware.py           # CORS + global exception handlers
├── api/
│   ├── router.py          # Central router — aggregates all endpoint routers
│   └── endpoints/
│       ├── health.py      # GET /health
│       ├── auth.py        # POST /auth/login, GET /auth/callback, GET /auth/me
│       ├── sessions.py    # CRUD for interview sessions
│       ├── setup.py       # POST /setup/jd, GET /setup/persona/{id}
│       ├── interview.py   # WS /interview/{session_id}
│       └── coach.py       # POST /coach/analyse/{id}, GET /coach/feedback/{id}
├── core/
│   ├── supabase_client.py # Supabase client init
│   ├── groq_client.py     # Groq client init
│   ├── tts.py             # gTTS wrapper
│   └── security.py        # JWT validation, get_current_user dependency
├── models/                # Pydantic request/response schemas
├── agents/                # AI logic (setup, interviewer, coach) — no HTTP/DB
├── services/              # Business logic layer — orchestrates agents + DB
└── utils/                 # Helpers (audio, prompts, validators)
tests/
├── conftest.py            # Async test client fixture
└── ...
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
