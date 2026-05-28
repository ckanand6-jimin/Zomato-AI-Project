from __future__ import annotations

from typing import Any

from core.models import RecommendationResponse
from data.repository import RestaurantRepository


def format_recommendation_cards(
    response: RecommendationResponse,
    repository: RestaurantRepository,
) -> list[dict[str, Any]]:
    """Map recommendation results to UI/display-friendly card dictionaries."""
    restaurant_ids = [recommendation.restaurant_id for recommendation in response.recommendations]
    restaurants = repository.get_by_ids(restaurant_ids)
    restaurant_map = {restaurant.id: restaurant for restaurant in restaurants}

    cards: list[dict[str, Any]] = []
    for recommendation in response.recommendations:
        restaurant = restaurant_map.get(recommendation.restaurant_id)
        if restaurant is None:
            continue

        cards.append(
            {
                "rank": recommendation.rank,
                "name": restaurant.name,
                "cuisine": restaurant.cuisine,
                "rating": restaurant.rating,
                "estimated_cost": (
                    f"₹{restaurant.cost_for_two} for two"
                    if restaurant.cost_for_two is not None
                    else "N/A"
                ),
                "budget_tier": restaurant.budget_tier,
                "location": restaurant.location,
                "explanation": recommendation.explanation,
            }
        )

    return cards
