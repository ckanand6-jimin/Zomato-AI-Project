from __future__ import annotations

import json
from typing import List

from core.models import Restaurant, RecommendationResponse, UserPreferences
from core.orchestrator import RecommendationOrchestrator
from config.settings import get_settings, Settings


class FakeRepo:
    def __init__(self, restaurants: List[Restaurant]):
        self._restaurants = restaurants

    def ensure_loaded(self):
        return None

    def get_all(self):
        return list(self._restaurants)

    def distinct_cities(self):
        return sorted({r.city for r in self._restaurants})


class FakeLLMClientSuccess:
    def __init__(self, payload: dict):
        self.payload = payload

    def complete(self, preferences, candidates):
        return json.dumps(self.payload)


class FakeLLMClientFail:
    def complete(self, preferences, candidates):
        raise RuntimeError("simulated LLM failure")


def make_restaurant(rid: str, city: str, budget: str, rating: float) -> Restaurant:
    return Restaurant(
        id=rid,
        name=f"Name {rid}",
        location="Somewhere",
        city=city,
        cuisine="Indian",
        rating=rating,
        cost_for_two=500,
        budget_tier=budget,
        raw={},
    )


def test_orchestrator_parses_llm_and_returns_recommendations():
    settings = get_settings()
    settings.top_n_recommendations = 2

    restaurants = [
        make_restaurant("r1", "Bangalore", "low", 4.2),
        make_restaurant("r2", "Bangalore", "low", 4.5),
        make_restaurant("r3", "Bangalore", "low", 3.9),
    ]

    payload = {
        "recommendations": [
            {"restaurant_id": "r2", "rank": 1, "explanation": "Great pick"},
            {"restaurant_id": "r1", "rank": 2, "explanation": "Also solid"},
        ],
        "summary": "Top picks",
        "model_version": "test-v1",
    }

    repo = FakeRepo(restaurants)
    llm = FakeLLMClientSuccess(payload)
    orch = RecommendationOrchestrator(repository=repo, llm_client=llm, settings=settings)

    prefs = UserPreferences(location="Bangalore", budget="low")
    response: RecommendationResponse = orch.recommend(prefs)

    assert len(response.recommendations) == 2
    assert response.recommendations[0].restaurant_id == "r2"
    assert response.fallback_used is False
    assert response.candidates_considered == 3


def test_orchestrator_falls_back_on_llm_error():
    settings = get_settings()
    settings.top_n_recommendations = 2
    settings.llm_fallback_on_error = True

    restaurants = [
        make_restaurant("r1", "Bangalore", "low", 4.2),
        make_restaurant("r2", "Bangalore", "low", 4.5),
        make_restaurant("r3", "Bangalore", "low", 3.9),
    ]

    repo = FakeRepo(restaurants)
    llm = FakeLLMClientFail()
    orch = RecommendationOrchestrator(repository=repo, llm_client=llm, settings=settings)

    prefs = UserPreferences(location="Bangalore", budget="low")
    response = orch.recommend(prefs)

    assert response.fallback_used is True
    assert len(response.recommendations) <= settings.top_n_recommendations
    assert response.candidates_considered == 3
