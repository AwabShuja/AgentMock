"""
Setup service — orchestrates JD parsing and persona generation.
"""

from __future__ import annotations

from typing import Any

from groq import Groq
from supabase import Client

from app.agents.setup_agent import SetupAgent
from app.exceptions import CareerFitException, SessionNotFoundError


class SetupService:
	"""Application service for setup-domain workflows."""

	def __init__(self, supabase: Client | None, groq: Groq | None):
		self._sb = supabase
		self._setup_agent = SetupAgent(groq)

	def create_session_from_jd(
		self,
		user_id: str,
		job_description: str,
		title: str | None = None,
	) -> dict[str, Any]:
		"""Generate persona from JD and persist a new interview session."""
		if self._sb is None:
			raise CareerFitException("Supabase client is not configured.")

		persona = self._setup_agent.generate_persona(job_description)

		payload = {
			"user_id": user_id,
			"title": title,
			"job_description": job_description,
			"persona": persona,
			"status": "created",
		}

		response = (
			self._sb.table("interview_sessions")
			.insert(payload)
			.execute()
		)

		row = self._extract_single_row(response.data)
		if row is None:
			raise CareerFitException("Failed to create interview session.")

		return row

	def get_persona_for_session(self, user_id: str, session_id: str) -> dict[str, Any]:
		"""Fetch persona data for a user-owned session."""
		if self._sb is None:
			raise CareerFitException("Supabase client is not configured.")

		response = (
			self._sb.table("interview_sessions")
			.select("id, user_id, status, persona")
			.eq("id", session_id)
			.eq("user_id", user_id)
			.maybe_single()
			.execute()
		)

		row = response.data
		if row is None:
			raise SessionNotFoundError("Session not found for this user.")

		return row

	@staticmethod
	def _extract_single_row(data: Any) -> dict[str, Any] | None:
		"""Handle supabase-py response shapes (dict or single-item list)."""
		if isinstance(data, dict):
			return data
		if isinstance(data, list) and data:
			first = data[0]
			if isinstance(first, dict):
				return first
		return None
