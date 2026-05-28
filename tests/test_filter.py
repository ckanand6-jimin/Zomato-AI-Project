"""
Tests for preference parser, validation layer, and candidate filter service (Phase 2).
"""

from __future__ import annotations

import pytest

from config.settings import get_settings
from core.filter import CandidateFilterService
from core.models import Restaurant, UserPreferences
from core.validator import PreferenceValidationError, validate_preferences
from data.repository import RestaurantRepository


# =====================================================================
# Validator Tests
# =====================================================================

def test_validate_preferences_valid():
    raw = {
        "location": "bengaluru",
        "budget": "medium",
        "cuisine": "Italian, Chinese",
        "min_rating": "4.2",
        "additional_preferences": "  outdoor seating  ",
    }
    prefs = validate_preferences(raw)
    assert prefs.location == "Bangalore"  # Normalized via alias
    assert prefs.budget == "medium"
    assert prefs.cuisine == ["italian", "chinese"]
    assert prefs.min_rating == 4.2
    assert prefs.additional_preferences == "outdoor seating"


def test_validate_preferences_defaults():
    raw = {
        "location": "Delhi",
        "budget": "low",
    }
    prefs = validate_preferences(raw)
    assert prefs.location == "Delhi"
    assert prefs.budget == "low"
    assert prefs.cuisine is None
    assert prefs.min_rating == get_settings().default_min_rating
    assert prefs.additional_preferences is None


def test_validate_preferences_invalid_location():
    with pytest.raises(PreferenceValidationError) as exc_info:
        validate_preferences({"budget": "low"})
    assert "location" in exc_info.value.errors

    with pytest.raises(PreferenceValidationError) as exc_info:
        validate_preferences({"location": "   ", "budget": "low"})
    assert "location" in exc_info.value.errors


def test_validate_preferences_invalid_budget():
    with pytest.raises(PreferenceValidationError) as exc_info:
        validate_preferences({"location": "Delhi", "budget": "super-expensive"})
    assert "budget" in exc_info.value.errors


def test_validate_preferences_invalid_min_rating():
    with pytest.raises(PreferenceValidationError) as exc_info:
        validate_preferences({"location": "Delhi", "budget": "medium", "min_rating": "invalid"})
    assert "min_rating" in exc_info.value.errors

    with pytest.raises(PreferenceValidationError) as exc_info:
        validate_preferences({"location": "Delhi", "budget": "medium", "min_rating": 6.0})
    assert "min_rating" in exc_info.value.errors


def test_validate_preferences_invalid_cuisine():
    with pytest.raises(PreferenceValidationError) as exc_info:
        validate_preferences({"location": "Delhi", "budget": "medium", "cuisine": 1234})
    assert "cuisine" in exc_info.value.errors


# =====================================================================
# Filtering & Suggestions Tests
# =====================================================================

class DummyRepository(RestaurantRepository):
    """InMemory repository containing test fixtures."""

    def __init__(self, restaurants: list[Restaurant]) -> None:
        super().__init__()
        self._restaurants = restaurants
        self._by_id = {r.id: r for r in restaurants}
        self._loaded = True


@pytest.fixture
def mock_repo() -> DummyRepository:
    restaurants = [
        Restaurant(
            id="1",
            name="Delhi Diner",
            location="Connaught Place, Delhi",
            city="Delhi",
            cuisine="North Indian, Chinese",
            rating=4.5,
            cost_for_two=400,
            budget_tier="low",
        ),
        Restaurant(
            id="2",
            name="Bistro Bangalore",
            location="Koramangala, Bangalore",
            city="Bangalore",
            cuisine="Italian, Continental",
            rating=4.2,
            cost_for_two=1200,
            budget_tier="medium",
        ),
        Restaurant(
            id="3",
            name="Mumbai Masala",
            location="Colaba, Mumbai",
            city="Mumbai",
            cuisine="South Indian, Street Food",
            rating=3.8,
            cost_for_two=300,
            budget_tier="low",
        ),
        Restaurant(
            id="4",
            name="Delhi Cafe",
            location="South Ext, Delhi",
            city="Delhi",
            cuisine="Chinese, Fast Food",
            rating=4.0,
            cost_for_two=800,
            budget_tier="medium",
        ),
    ]
    return DummyRepository(restaurants)


def test_filter_exact_location(mock_repo):
    service = CandidateFilterService(mock_repo)
    prefs = UserPreferences(location="Delhi", budget="low")
    result = service.apply(prefs)

    assert len(result.candidates) == 1
    assert result.candidates[0].id == "1"
    assert "location" in result.filters_applied
    assert "budget" in result.filters_applied


def test_filter_fuzzy_location_fallback(mock_repo):
    service = CandidateFilterService(mock_repo)
    # Searching for 'Koramangala' (a neighborhood) instead of 'Bangalore'
    prefs = UserPreferences(location="Koramangala", budget="medium")
    result = service.apply(prefs)

    assert len(result.candidates) == 1
    assert result.candidates[0].city == "Bangalore"
    assert result.candidates[0].id == "2"


def test_filter_cuisine_matching(mock_repo):
    service = CandidateFilterService(mock_repo)
    prefs = UserPreferences(location="Delhi", budget="medium", cuisine=["chinese"])
    result = service.apply(prefs)

    assert len(result.candidates) == 1
    assert result.candidates[0].id == "4"


def test_filter_rating_matching(mock_repo):
    service = CandidateFilterService(mock_repo)
    prefs = UserPreferences(location="Delhi", budget="low", min_rating=4.8)
    result = service.apply(prefs)

    assert len(result.candidates) == 0
    assert len(result.suggestions) > 0
    assert "rating" in result.suggestions[0]


def test_filter_capping_and_sorting(mock_repo, monkeypatch):
    service = CandidateFilterService(mock_repo)
    # Force max_candidates to 1
    monkeypatch.setattr(service.settings, "max_candidates", 1)

    # Both Delhi Diner (4.5) and Delhi Cafe (4.0) match budget 'low'/'medium' in Delhi
    # Let's search Delhi without budget filter (wait, budget is required.
    # Let's add another Delhi restaurant with low budget and different ratings)
    test_restaurants = [
        Restaurant(
            id="1",
            name="Delhi Low 1",
            location="Loc 1",
            city="Delhi",
            cuisine="Chinese",
            rating=4.0,
            cost_for_two=200,
            budget_tier="low",
        ),
        Restaurant(
            id="2",
            name="Delhi Low 2",
            location="Loc 2",
            city="Delhi",
            cuisine="Chinese",
            rating=4.8,
            cost_for_two=200,
            budget_tier="low",
        ),
    ]
    repo = DummyRepository(test_restaurants)
    service = CandidateFilterService(repo)
    monkeypatch.setattr(service.settings, "max_candidates", 1)

    prefs = UserPreferences(location="Delhi", budget="low")
    result = service.apply(prefs)

    # Should only return Delhi Low 2 (rating 4.8) because of rating desc sort and cap at 1
    assert len(result.candidates) == 1
    assert result.candidates[0].id == "2"


def test_empty_state_suggestions_no_location(mock_repo):
    service = CandidateFilterService(mock_repo)
    prefs = UserPreferences(location="Chennai", budget="low")
    result = service.apply(prefs)

    assert len(result.candidates) == 0
    assert len(result.suggestions) == 1
    assert "Chennai" in result.suggestions[0]
    # Should suggest existing cities
    assert "Delhi" in result.suggestions[0] or "Bangalore" in result.suggestions[0]


def test_empty_state_suggestions_no_cuisine(mock_repo):
    service = CandidateFilterService(mock_repo)
    prefs = UserPreferences(location="Delhi", budget="low", cuisine=["french"])
    result = service.apply(prefs)

    assert len(result.candidates) == 0
    assert len(result.suggestions) == 1
    assert "cuisine" in result.suggestions[0]
