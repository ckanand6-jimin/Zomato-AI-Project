import json

import pytest

from core.models import Restaurant
from llm.parser import fallback_recommendation_response, parse_llm_response


def make_restaurant(restaurant_id: str, name: str, rating: float, cuisine: str = "Indian") -> Restaurant:
    return Restaurant(
        id=restaurant_id,
        name=name,
        location="Sample Location",
        city="Delhi",
        cuisine=cuisine,
        rating=rating,
        cost_for_two=400,
        budget_tier="low",
        raw={},
    )


def test_parse_llm_response_valid_json_matches_candidates():
    candidates = [make_restaurant("a1", "Alpha", 4.5), make_restaurant("b2", "Bravo", 4.2)]
    payload = {
        "recommendations": [
            {
                "restaurant_id": "a1",
                "rank": 1,
                "explanation": "Alpha is the best match for location, rating, and budget.",
            }
        ],
        "summary": "Top recommendation from the grounded candidate list.",
    }
    response = parse_llm_response(json.dumps(payload), candidates, max_recommendations=5)

    assert len(response.recommendations) == 1
    assert response.recommendations[0].restaurant_id == "a1"
    assert response.summary == payload["summary"]


def test_parse_llm_response_rejects_unknown_ids():
    candidates = [make_restaurant("a1", "Alpha", 4.5)]
    payload = {
        "recommendations": [
            {
                "restaurant_id": "unknown",
                "rank": 1,
                "explanation": "This restaurant is not in the candidate list.",
            }
        ]
    }

    with pytest.raises(ValueError, match="Unknown restaurant_id"):
        parse_llm_response(json.dumps(payload), candidates, max_recommendations=5)


def test_parse_llm_response_rejects_malformed_json():
    candidates = [make_restaurant("a1", "Alpha", 4.5)]
    raw_response = "{ invalid json }"

    with pytest.raises(ValueError, match="not valid JSON"):
        parse_llm_response(raw_response, candidates, max_recommendations=5)


def test_fallback_recommendation_response_returns_top_candidates():
    candidates = [
        make_restaurant("a1", "Alpha", 4.5),
        make_restaurant("b2", "Bravo", 4.9),
        make_restaurant("c3", "Charlie", 4.1),
    ]

    fallback = fallback_recommendation_response(candidates, max_recommendations=2)

    assert len(fallback.recommendations) == 2
    assert fallback.recommendations[0].restaurant_id == "b2"
    assert fallback.summary is not None
