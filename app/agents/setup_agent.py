"""
Setup Agent — JD parsing & interviewer persona creation.

Responsibilities:
- Accept a raw Job Description text.
- Use Groq LLM to extract key skills, role, and requirements.
- Generate a tailored system prompt / persona for the Interviewer Agent.
"""

from __future__ import annotations

import json
import logging
import re
from collections import Counter
from typing import Any

from groq import Groq

from app.utils.prompts import (
	SETUP_AGENT_SYSTEM_PROMPT,
	SETUP_AGENT_USER_PROMPT_TEMPLATE,
)

logger = logging.getLogger(__name__)


class SetupAgent:
	"""Generates an interviewer persona from a raw Job Description."""

	def __init__(self, groq_client: Groq | None):
		self._groq = groq_client

	def generate_persona(self, job_description: str) -> dict[str, Any]:
		"""Return a structured interviewer persona dictionary.

		Uses Groq when available. If unavailable or response parsing fails,
		falls back to a deterministic local heuristic persona.
		"""
		if self._groq is None:
			logger.warning("Groq client unavailable. Using fallback setup persona.")
			return self._fallback_persona(job_description)

		try:
			completion = self._groq.chat.completions.create(
				model="llama-3.3-70b-versatile",
				temperature=0.2,
				messages=[
					{"role": "system", "content": SETUP_AGENT_SYSTEM_PROMPT},
					{
						"role": "user",
						"content": SETUP_AGENT_USER_PROMPT_TEMPLATE.format(
							job_description=job_description
						),
					},
				],
				response_format={"type": "json_object"},
			)

			content = completion.choices[0].message.content or "{}"
			parsed = json.loads(content)
			return self._normalize_persona(parsed, job_description)
		except Exception as exc:
			logger.warning("Setup agent LLM parsing failed: %s", exc)
			return self._fallback_persona(job_description)

	def _normalize_persona(
		self,
		persona: dict[str, Any],
		job_description: str,
	) -> dict[str, Any]:
		"""Guarantee required fields and stable shape for downstream services."""
		key_skills = persona.get("key_skills") or self._extract_keywords(job_description)
		focus_areas = persona.get("focus_areas") or key_skills[:5]

		normalized = {
			"role_title": persona.get("role_title") or "Target Role",
			"seniority": persona.get("seniority") or "Mid to Senior",
			"focus_areas": self._as_string_list(focus_areas, max_items=8),
			"key_skills": self._as_string_list(key_skills, max_items=8),
			"interview_style": persona.get("interview_style")
			or "Structured, probing, and practical.",
			"question_strategy": persona.get("question_strategy")
			or "Start broad, then probe on concrete examples and tradeoffs.",
			"do_not_do": self._as_string_list(
				persona.get("do_not_do")
				or [
					"Do not ask unrelated theory-heavy trivia.",
					"Do not ask double-barreled questions.",
					"Do not reward over-explaining without relevance.",
				],
				max_items=6,
			),
			"opening_question": persona.get("opening_question")
			or "Tell me about yourself and why this role is a fit for your experience.",
			"evaluation_rubric": {
				"relevance": (persona.get("evaluation_rubric") or {}).get(
					"relevance",
					"Answers should map clearly to role requirements.",
				),
				"clarity": (persona.get("evaluation_rubric") or {}).get(
					"clarity",
					"Response should be well-structured and easy to follow.",
				),
				"depth": (persona.get("evaluation_rubric") or {}).get(
					"depth",
					"Should include concrete examples, constraints, and tradeoffs.",
				),
				"conciseness": (persona.get("evaluation_rubric") or {}).get(
					"conciseness",
					"Avoid rambling. Stay focused and precise.",
				),
			},
		}
		normalized["system_prompt"] = self._build_interviewer_system_prompt(normalized)
		return normalized

	def _fallback_persona(self, job_description: str) -> dict[str, Any]:
		"""Generate a deterministic persona when LLM is unavailable."""
		key_skills = self._extract_keywords(job_description)
		fallback = {
			"role_title": "Target Role",
			"seniority": "Mid to Senior",
			"focus_areas": key_skills[:5],
			"key_skills": key_skills,
			"interview_style": "Professional, concise, and competency-based.",
			"question_strategy": (
				"Ask behavior + scenario questions aligned to the JD, then "
				"drill into decision-making and measurable outcomes."
			),
			"do_not_do": [
				"Do not ask off-topic questions.",
				"Do not interrupt strong concise answers.",
				"Do not encourage over-explaining.",
			],
			"opening_question": (
				"Walk me through your background and the experiences most relevant "
				"to this role."
			),
			"evaluation_rubric": {
				"relevance": "Answer ties directly to JD needs.",
				"clarity": "Answer is structured and easy to follow.",
				"depth": "Answer includes examples and tradeoffs.",
				"conciseness": "Answer is focused and not verbose.",
			},
		}
		fallback["system_prompt"] = self._build_interviewer_system_prompt(fallback)
		return fallback

	@staticmethod
	def _as_string_list(value: Any, max_items: int) -> list[str]:
		if not isinstance(value, list):
			return []
		cleaned = [str(item).strip() for item in value if str(item).strip()]
		deduped = list(dict.fromkeys(cleaned))
		return deduped[:max_items]

	@staticmethod
	def _extract_keywords(text: str) -> list[str]:
		tokens = re.findall(r"[A-Za-z][A-Za-z+.#-]{2,}", text.lower())
		stop_words = {
			"with",
			"and",
			"the",
			"for",
			"you",
			"your",
			"will",
			"have",
			"from",
			"that",
			"this",
			"years",
			"experience",
			"role",
			"team",
			"work",
			"ability",
			"required",
			"preferred",
			"skills",
			"knowledge",
		}
		filtered = [t for t in tokens if t not in stop_words and len(t) > 2]
		common = [w for w, _ in Counter(filtered).most_common(8)]
		if not common:
			return ["problem-solving", "communication", "execution", "ownership"]
		return common

	@staticmethod
	def _build_interviewer_system_prompt(persona: dict[str, Any]) -> str:
		"""Create the runtime system prompt used later by the interviewer agent."""
		skills = ", ".join(persona.get("key_skills", []))
		focus = ", ".join(persona.get("focus_areas", []))
		return (
			"You are an AI interviewer. "
			f"Role: {persona.get('role_title', 'Target Role')}. "
			f"Seniority: {persona.get('seniority', 'Mid to Senior')}. "
			f"Focus areas: {focus}. "
			f"Key skills to probe: {skills}. "
			f"Interview style: {persona.get('interview_style', '')}. "
			"Ask one clear question at a time. "
			"After each answer, ask a targeted follow-up when needed. "
			"Evaluate relevance, clarity, depth, and conciseness."
		)
