from __future__ import annotations

import json
from pathlib import Path

from core.orchestrator import RecommendationOrchestrator
from data.repository import RestaurantRepository


SCENARIOS = [
    {
        "name": "Bangalore Italian family-friendly",
        "prefs": {"location": "Bangalore", "budget": "medium", "cuisine": "Italian", "min_rating": 4.0, "additional_preferences": "family-friendly"},
    },
    {
        "name": "Delhi low-budget Chinese",
        "prefs": {"location": "Delhi", "budget": "low", "cuisine": "Chinese", "min_rating": 3.5},
    },
    {
        "name": "Mumbai high-rated",
        "prefs": {"location": "Mumbai", "budget": "high", "min_rating": 4.5},
    },
]


def run_scenario(repo: RestaurantRepository, scenario: dict) -> None:
    orchestrator = RecommendationOrchestrator(repository=repo)
    print(f"\n=== Scenario: {scenario['name']} ===")
    try:
        resp = orchestrator.recommend(scenario["prefs"])
    except FileNotFoundError as exc:
        print("Data cache missing. Run: python -m data.loader --refresh")
        return
    except Exception as exc:
        print(f"Error generating recommendations: {exc}")
        return

    print(f"Summary: {resp.summary or 'No summary'}")
    print(f"Filters applied: {', '.join(resp.filters_applied)}")
    print(f"Candidates considered: {resp.candidates_considered}")
    print(f"Fallback used: {resp.fallback_used}")
    print("Recommendations:")
    for rec in resp.recommendations:
        print(f"  {rec.rank}. {rec.restaurant_id} — {rec.explanation}")


def main() -> None:
    repo = RestaurantRepository()
    try:
        repo.load()
    except FileNotFoundError as exc:
        print(f"{exc}\nRun: python -m data.loader --refresh")
        return

    for s in SCENARIOS:
        run_scenario(repo, s)


if __name__ == "__main__":
    main()
