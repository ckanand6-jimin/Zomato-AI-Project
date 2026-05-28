from __future__ import annotations

import json
from typing import Any

from core.models import Restaurant, UserPreferences

PROMPT_VERSION = "1.0"

SYSTEM_PROMPT = (
    "You are a restaurant recommendation assistant."
    " Your goal is to recommend up to the requested number of restaurants from a provided candidate list."
    " Do not invent, add, rename, or modify any restaurant outside the provided candidate list."
    " Only return valid JSON that can be parsed by a downstream system."
    ""
)

USER_INSTRUCTIONS = (
    "Return an object with a top-level `recommendations` array."
    " Each recommendation must include `restaurant_id`, `rank`, and `explanation`."
    " Optionally include a `summary` field with a short rationale for the overall selection."
    " Do not include any additional top-level keys beyond `recommendations` and optional `summary`."
    " Sort recommendations by ascending `rank` (1 is best)."
    " Use only the restaurants listed in candidate_restaurants."
)


def _serialize_candidate(candidate: Restaurant) -> dict[str, Any]:
    return {
        "restaurant_id": candidate.id,
        "name": candidate.name,
        "cuisine": candidate.cuisine,
        "rating": candidate.rating,
        "cost_for_two": candidate.cost_for_two,
        "location": candidate.location,
    }


def build_prompt_messages(
    preferences: UserPreferences,
    candidates: list[Restaurant],
    max_recommendations: int,
) -> list[dict[str, str]]:
    user_payload = {
        "prompt_version": PROMPT_VERSION,
        "preferences": {
            "location": preferences.location,
            "budget": preferences.budget,
            "cuisine": preferences.cuisine,
            "min_rating": preferences.min_rating,
            "additional_preferences": preferences.additional_preferences,
        },
        "max_recommendations": max_recommendations,
        "candidate_restaurants": [_serialize_candidate(r) for r in candidates],
    }

    user_message = (
        "Here are the user preferences and candidate restaurants."
        " Recommend the best options that satisfy the user's budget, cuisine and rating filters."
        " Only choose from the candidate list."
        ""
        f"\n\n{json.dumps(user_payload, indent=2, ensure_ascii=False)}"
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_INSTRUCTIONS + "\n\n" + user_message},
    ]
