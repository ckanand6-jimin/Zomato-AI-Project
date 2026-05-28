from __future__ import annotations

import logging
import os
import time
from typing import Sequence

from config.settings import Settings, get_settings
from core.models import Restaurant, UserPreferences
from llm.prompts import build_prompt_messages

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def complete(self, preferences: UserPreferences, candidates: Sequence[Restaurant]) -> str:
        """Send a prompt to the configured LLM provider and return the raw text response."""
        if self.settings.llm_disabled:
            raise RuntimeError("LLM is disabled by configuration.")

        if not candidates:
            raise ValueError("At least one candidate restaurant is required to build an LLM prompt.")

        attempt = 0
        last_exception: Exception | None = None
        messages = build_prompt_messages(
            preferences,
            list(candidates),
            self.settings.top_n_recommendations,
        )

        while attempt < 2:
            try:
                logger.info("Sending prompt to LLM provider=%s (attempt=%d)", self.settings.llm_provider, attempt + 1)
                if self.settings.llm_provider == "groq":
                    return self._complete_groq(messages)
                raise ValueError(
                    f"Unsupported LLM provider: {self.settings.llm_provider}"
                )
            except Exception as exc:
                last_exception = exc
                attempt += 1
                if attempt >= 2:
                    logger.exception("LLM request failed after %d attempts", attempt)
                    # Raise a clearer runtime error to the caller while preserving the original
                    raise RuntimeError("LLM request failed after retries") from exc
                logger.warning(
                    "LLM request failed on attempt %d: %s. Retrying once.",
                    attempt,
                    exc,
                )
                time.sleep(1)

        assert last_exception is not None
        raise last_exception

    def _complete_groq(self, messages: list[dict[str, str]]) -> str:
        try:
            from groq import Groq
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "The groq package is required for Groq LLM calls. "
                "Install it with `pip install groq`."
            ) from exc

        api_key = self.settings.groq_api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "Groq API key is required for LLM requests. "
                "Set GROQ_API_KEY in the environment or groq_api_key in settings."
            )

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=self.settings.llm_model,
            messages=messages,
            temperature=self.settings.llm_temperature,
            max_tokens=self.settings.llm_max_tokens,
            timeout=self.settings.llm_timeout_seconds,
        )

        if not response.choices:
            raise ValueError("Groq returned no choices.")

        message = response.choices[0].message
        if message is None or not getattr(message, "content", None):
            raise ValueError("Groq returned an empty message content.")

        return str(message.content)