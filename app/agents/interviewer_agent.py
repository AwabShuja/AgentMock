"""
Interviewer Agent — turn-based voice interview orchestration.

Responsibilities:
- Maintain conversation context (system prompt + history).
- Process each user turn (transcribed text) via Groq LLM.
- Return the next interviewer question / follow-up.
"""
