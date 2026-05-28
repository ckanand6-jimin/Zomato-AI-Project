"""
Candidate filtering pipeline (Phase 2).
"""

from __future__ import annotations

import logging

from pydantic import BaseModel

from config.settings import Settings, get_settings
from core.models import Restaurant, UserPreferences
from data.repository import RestaurantRepository

logger = logging.getLogger(__name__)


class FilterResult(BaseModel):
    """Container for filtering results and metadata (architecture §5.1)."""

    candidates: list[Restaurant]
    filters_applied: list[str]
    suggestions: list[str]


class CandidateFilterService:
    """Service to deterministically filter restaurants based on preferences (architecture §4.2.4)."""

    def __init__(
        self,
        repository: RestaurantRepository,
        settings: Settings | None = None,
    ) -> None:
        self.repository = repository
        self.settings = settings or get_settings()

    def apply(self, prefs: UserPreferences) -> FilterResult:
        """
        Apply preference filters to the repository database.

        Returns:
            FilterResult: contains filtered candidates, list of filters applied,
                         and suggestions if the result is empty.
        """
        all_restaurants = self.repository.get_all()
        filters_applied: list[str] = []

        # 1. Location match
        # Try exact city match first (case-insensitive)
        location_matches = [
            r for r in all_restaurants
            if r.city.lower() == prefs.location.lower()
        ]
        filters_applied.append("location")

        # If no exact city match, fallback to substring matching on location or city
        if not location_matches:
            search_term = prefs.location.lower()
            location_matches = [
                r for r in all_restaurants
                if search_term in r.city.lower() or search_term in r.location.lower()
            ]
            logger.info(
                "No exact city match for '%s'. Fallback substring search returned %d matches.",
                prefs.location,
                len(location_matches),
            )

        # 2. Filter pipeline (using location_matches as the base candidate list)
        candidates = list(location_matches)

        # Rating Filter
        candidates = [r for r in candidates if r.rating >= prefs.min_rating]
        filters_applied.append("min_rating")

        # Cuisine Filter
        if prefs.cuisine:
            def matches_cuisine(restaurant: Restaurant, user_cuisines: list[str]) -> bool:
                rc_lower = restaurant.cuisine.lower()
                return any(uc.strip().lower() in rc_lower for uc in user_cuisines)

            candidates = [r for r in candidates if matches_cuisine(r, prefs.cuisine)]
            filters_applied.append("cuisine")

        # Budget Filter
        candidates = [r for r in candidates if r.budget_tier == prefs.budget]
        filters_applied.append("budget")

        # Sort by rating descending (highest rated first)
        candidates.sort(key=lambda r: r.rating, reverse=True)

        suggestions: list[str] = []
        if not candidates:
            suggestions = self._generate_suggestions(prefs, location_matches)

        capped_candidates = candidates[: self.settings.max_candidates]

        logger.info(
            "Filter applied: %d candidates returned after capping (max=%d).",
            len(capped_candidates),
            self.settings.max_candidates,
        )

        return FilterResult(
            candidates=capped_candidates,
            filters_applied=filters_applied,
            suggestions=suggestions,
        )

    def _generate_suggestions(
        self,
        prefs: UserPreferences,
        location_matches: list[Restaurant],
    ) -> list[str]:
        suggestions: list[str] = []
        if not location_matches:
            # We don't have restaurants matching this location.
            cities = self.repository.distinct_cities()
            if cities:
                suggestions.append(
                    f"We couldn't find any restaurants in or near '{prefs.location}'. "
                    f"Try searching in one of our supported cities: {', '.join(cities[:5])}."
                )
            else:
                suggestions.append(
                    "We couldn't find any restaurants in our database. "
                    "Please make sure the cache is populated."
                )
            return suggestions

        # Location matches exist. Let's see why they were filtered out.
        # Check rating filter
        rating_matches = [r for r in location_matches if r.rating >= prefs.min_rating]
        if not rating_matches:
            max_rating = max(r.rating for r in location_matches)
            suggestions.append(
                f"No restaurants in '{prefs.location}' have a rating of {prefs.min_rating} or higher. "
                f"Try lowering your minimum rating filter (highest available is {max_rating})."
            )

        # Check budget filter
        budget_matches = [r for r in location_matches if r.budget_tier == prefs.budget]
        if not budget_matches:
            available_tiers = sorted({r.budget_tier for r in location_matches if r.budget_tier})
            if available_tiers:
                suggestions.append(
                    f"No restaurants in '{prefs.location}' match the '{prefs.budget}' budget tier. "
                    f"Try selecting another budget tier: {', '.join(available_tiers)}."
                )
            else:
                suggestions.append(
                    f"No budget information is available for restaurants in '{prefs.location}'."
                )

        # Check cuisine filter
        if prefs.cuisine:
            def matches_cuisine(restaurant: Restaurant, user_cuisines: list[str]) -> bool:
                rc_lower = restaurant.cuisine.lower()
                return any(uc.strip().lower() in rc_lower for uc in user_cuisines)

            cuisine_matches = [r for r in location_matches if matches_cuisine(r, prefs.cuisine)]
            if not cuisine_matches:
                suggestions.append(
                    f"No restaurants in '{prefs.location}' serve the requested cuisine(s): {', '.join(prefs.cuisine)}. "
                    f"Try removing or changing the cuisine filter."
                )

        # General suggestion if individual filters have matches but the intersection doesn't
        if not suggestions:
            suggestions.append(
                "No restaurants match all your selected criteria simultaneously. "
                "Try relaxing your filters (e.g., lower min rating or remove cuisine preference)."
            )

        return suggestions
