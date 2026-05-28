from __future__ import annotations

import logging
from typing import Any

from config.settings import Settings, get_settings
from core.filter import CandidateFilterService
from core.models import RecommendationResponse, UserPreferences
from core.validator import validate_preferences
from data.repository import RestaurantRepository
from llm.client import LLMClient
from llm.parser import fallback_recommendation_response, parse_llm_response

logger = logging.getLogger(__name__)


class RecommendationOrchestrator:
    def __init__(
        self,
        repository: RestaurantRepository | None = None,
        filter_service: CandidateFilterService | None = None,
        llm_client: LLMClient | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.repository = repository or RestaurantRepository(self.settings)
        self.filter_service = filter_service or CandidateFilterService(self.repository, self.settings)
        self.llm_client = llm_client or LLMClient(self.settings)

    def recommend(self, raw_preferences: dict[str, Any] | UserPreferences) -> RecommendationResponse:
        if isinstance(raw_preferences, UserPreferences):
            preferences = raw_preferences
        else:
            preferences = validate_preferences(raw_preferences)

        self.repository.ensure_loaded()
        filter_result = self.filter_service.apply(preferences)

        if not filter_result.candidates:
            return RecommendationResponse(
                recommendations=[],
                summary=(
                    "No restaurants match all selected criteria. "
                    "Try relaxing filters or changing location/budget."
                ),
                model_version=None,
                filters_applied=filter_result.filters_applied,
                candidates_considered=0,
                suggestions=filter_result.suggestions,
                fallback_used=False,
            )

        try:
            raw_response = self.llm_client.complete(
                preferences,
                filter_result.candidates,
            )
            response = parse_llm_response(
                raw_response,
                filter_result.candidates,
                self.settings.top_n_recommendations,
            )
            fallback_used = False
        except Exception as exc:
            # Provide more context in logs for debugging
            logger.warning(
                "LLM request or parsing failed; falling back to deterministic recommendations. error=%s",
                exc,
            )
            if self.settings.llm_fallback_on_error:
                response = fallback_recommendation_response(
                    filter_result.candidates,
                    self.settings.top_n_recommendations,
                )
                fallback_used = True
            else:
                # Reraise with context to aid callers
                raise RuntimeError("LLM processing failed and fallback is disabled") from exc

        return response.model_copy(
            update={
                "filters_applied": filter_result.filters_applied,
                "candidates_considered": len(filter_result.candidates),
                "suggestions": filter_result.suggestions,
                "fallback_used": fallback_used,
            }
        )
