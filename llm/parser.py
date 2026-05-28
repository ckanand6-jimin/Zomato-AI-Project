from __future__ import annotations

import json
import logging
import re
from typing import Sequence

from core.models import Recommendation, RecommendationResponse, Restaurant

logger = logging.getLogger(__name__)


def parse_llm_response(
    raw_response: str,
    candidates: Sequence[Restaurant],
    max_recommendations: int,
) -> RecommendationResponse:
    """Parse and validate LLM JSON output against a candidate restaurant list."""
    try:
        raw_response = raw_response.strip()
        raw_response = re.sub(r'^```(?:json)?\s*', '', raw_response)
        raw_response = re.sub(r'\s*```$', '', raw_response)

        parsed = json.loads(raw_response)

        print(parsed)

    except json.JSONDecodeError as exc:
        raise ValueError("LLM response is not valid JSON") from exc

    if not isinstance(parsed, dict):
        raise ValueError("LLM response must be a JSON object.")

    recommendations = parsed.get("recommendations")
    if not isinstance(recommendations, list):
        raise ValueError("LLM response must contain a `recommendations` list.")

    candidate_ids = {restaurant.id for restaurant in candidates}
    seen_ranks: set[int] = set()
    validated_recommendations: list[Recommendation] = []

    for item in recommendations:
        if not isinstance(item, dict):
            raise ValueError("Each recommendation item must be a JSON object.")

        restaurant_id = item.get("restaurant_id")
        if not restaurant_id or not isinstance(restaurant_id, str):
            raise ValueError("Each recommendation must include a string `restaurant_id`.")
        if restaurant_id not in candidate_ids:
            raise ValueError(
                f"Unknown restaurant_id in LLM response: {restaurant_id}. "
                "Recommendations must come from the provided candidate list."
            )

        rank_raw = item.get("rank")
        if rank_raw is None:
            raise ValueError("Each recommendation must include a `rank` field.")
        try:
            rank = int(rank_raw)
        except (TypeError, ValueError) as exc:
            raise ValueError("Recommendation `rank` must be an integer.") from exc
        if rank < 1 or rank > max_recommendations:
            raise ValueError(
                f"Recommendation rank must be between 1 and {max_recommendations}."
            )
        if rank in seen_ranks:
            raise ValueError(f"Duplicate recommendation rank found: {rank}.")
        seen_ranks.add(rank)

        explanation = item.get("explanation")
        if not explanation or not isinstance(explanation, str):
            raise ValueError("Each recommendation must include a non-empty `explanation`.")

        validated_recommendations.append(
            Recommendation(
                restaurant_id=restaurant_id,
                rank=rank,
                explanation=explanation.strip(),
            )
        )

    if not validated_recommendations:
        raise ValueError("LLM response contains no valid recommendations.")

    validated_recommendations.sort(key=lambda recommendation: recommendation.rank)
    if len(validated_recommendations) > max_recommendations:
        validated_recommendations = validated_recommendations[:max_recommendations]

    summary = parsed.get("summary")
    if summary is not None and not isinstance(summary, str):
        raise ValueError("Optional `summary` must be a string.")

    model_version = parsed.get("model_version")
    if model_version is not None and not isinstance(model_version, str):
        raise ValueError("Optional `model_version` must be a string.")

    return RecommendationResponse(
        recommendations=validated_recommendations,
        summary=summary,
        model_version=model_version,
    )


def fallback_recommendation_response(
    candidates: Sequence[Restaurant],
    max_recommendations: int,
) -> RecommendationResponse:
    """Create a safe fallback response when the LLM output cannot be trusted."""
    sorted_candidates = sorted(
        candidates,
        key=lambda restaurant: (-restaurant.rating, restaurant.name),
    )[:max_recommendations]

    recommendations = [
        Recommendation(
            restaurant_id=restaurant.id,
            rank=index + 1,
            explanation=(
                f"Fallback ranking based on grounded candidate data: {restaurant.name} "
                f"has a rating of {restaurant.rating} and matches the selected budget and cuisine filters."
            ),
        )
        for index, restaurant in enumerate(sorted_candidates)
    ]

    return RecommendationResponse(
        recommendations=recommendations,
        summary=(
            "The AI recommendation could not be parsed reliably, so top grounded candidates are returned instead."
        ),
        model_version=None,
    )
