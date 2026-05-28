from __future__ import annotations

from core.filter import CandidateFilterService
from core.models import Restaurant, UserPreferences


class TinyRepo:
    def __init__(self, restaurants):
        self._restaurants = restaurants

    def ensure_loaded(self):
        return None

    def get_all(self):
        return list(self._restaurants)

    def distinct_cities(self):
        return sorted({r.city for r in self._restaurants})


from core.models import Restaurant


def make_restaurant(rid: str, city: str, budget: str, rating: float, cuisine: str = "Indian") -> Restaurant:
    return Restaurant(
        id=rid,
        name=f"Name {rid}",
        location="Loc",
        city=city,
        cuisine=cuisine,
        rating=rating,
        cost_for_two=1000,
        budget_tier=budget,
        raw={},
    )


def test_filter_suggestions_when_no_candidates():
    restaurants = [
        make_restaurant("r1", "Mumbai", "medium", 4.0),
        make_restaurant("r2", "Mumbai", "high", 4.5),
    ]
    repo = TinyRepo(restaurants)
    service = CandidateFilterService(repo)

    prefs = UserPreferences(location="Bangalore", budget="low", min_rating=4.5)
    result = service.apply(prefs)

    assert result.candidates == []
    assert len(result.suggestions) >= 1
    assert any("supported cities" in s or "couldn't find" in s.lower() for s in result.suggestions)


def test_budget_and_rating_edge_case():
    restaurants = [
        make_restaurant("r1", "Delhi", "low", 3.0),
        make_restaurant("r2", "Delhi", "low", 3.4),
    ]
    repo = TinyRepo(restaurants)
    service = CandidateFilterService(repo)

    prefs = UserPreferences(location="Delhi", budget="low", min_rating=3.5)
    result = service.apply(prefs)

    assert result.candidates == []
    # Suggest lowering min_rating
    assert any("lowering your minimum rating" in s or "lower your minimum" in s.lower() for s in result.suggestions)
