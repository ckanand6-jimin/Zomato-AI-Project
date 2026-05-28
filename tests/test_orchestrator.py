import pytest

from core.models import Restaurant
from core.orchestrator import RecommendationOrchestrator
from core.models import UserPreferences


class DummyRestaurantRepository:
    def __init__(self, restaurants):
        self._restaurants = restaurants

    def ensure_loaded(self):
        return None

    def get_all(self):
        return self._restaurants

    def get_by_ids(self, ids):
        return [restaurant for restaurant in self._restaurants if restaurant.id in ids]

    def distinct_cities(self):
        return sorted({restaurant.city for restaurant in self._restaurants})


class DummyLLMClient:
    def __init__(self, response: str | Exception):
        self.response = response

    def complete(self, preferences, candidates):
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


def make_restaurant(restaurant_id: str, name: str, city: str = "Delhi") -> Restaurant:
    return Restaurant(
        id=restaurant_id,
        name=name,
        location="Connaught Place",
        city=city,
        cuisine="Chinese",
        rating=4.5,
        cost_for_two=600,
        budget_tier="low",
        raw={},
    )


def test_recommendation_orchestrator_returns_llm_recommendations():
    restaurants = [make_restaurant("r1", "Red Dragon")]
    repository = DummyRestaurantRepository(restaurants)
    llm_response = '{"recommendations": [{"restaurant_id": "r1", "rank": 1, "explanation": "Best fit for low budget Chinese in Delhi."}], "summary": "Top grounded recommendation."}'
    orchestrator = RecommendationOrchestrator(
        repository=repository,
        llm_client=DummyLLMClient(llm_response),
    )

    result = orchestrator.recommend({"location": "Delhi", "budget": "low", "cuisine": "Chinese"})

    assert len(result.recommendations) == 1
    assert result.recommendations[0].restaurant_id == "r1"
    assert result.summary == "Top grounded recommendation."
    assert result.filters_applied == ["location", "min_rating", "cuisine", "budget"]
    assert result.candidates_considered == 1
    assert result.fallback_used is False


def test_recommendation_orchestrator_uses_fallback_on_llm_error():
    restaurants = [make_restaurant("r1", "Red Dragon"), make_restaurant("r2", "Blue Lotus")]
    repository = DummyRestaurantRepository(restaurants)
    orchestrator = RecommendationOrchestrator(
        repository=repository,
        llm_client=DummyLLMClient(RuntimeError("LLM unavailable")),
    )

    result = orchestrator.recommend({"location": "Delhi", "budget": "low", "cuisine": "Chinese"})

    assert result.fallback_used is True
    assert len(result.recommendations) == 2
    assert result.summary is not None
    assert result.candidates_considered == 2
    assert result.filters_applied == ["location", "min_rating", "cuisine", "budget"]
