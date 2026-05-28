"""
Application entry point (Phase 0+).

    python -m app.main
    python -m app.main --ingest
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config.settings import get_settings
from data.repository import RestaurantRepository
from app.logging_config import configure_logging


def main() -> None:
    configure_logging()
    parser = argparse.ArgumentParser(description="Zomato AI Restaurant Recommender")
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Run data ingest (python -m data.loader --refresh)",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["recommend"],
        help="Run a named command, such as recommend.",
    )
    parser.add_argument(
        "--location",
        type=str,
        help="Location name for recommendation queries.",
    )
    parser.add_argument(
        "--budget",
        type=str,
        choices=["low", "medium", "high"],
        help="Budget tier: low, medium, or high.",
    )
    parser.add_argument(
        "--cuisine",
        type=str,
        help="Cuisine preference as comma-separated text.",
    )
    parser.add_argument(
        "--min-rating",
        type=float,
        help="Minimum acceptable rating.",
    )
    parser.add_argument(
        "--additional-preferences",
        type=str,
        help="Additional preference text for the recommendation prompt.",
    )
    parser.add_argument(
        "--filter-file",
        type=str,
        help="Path to JSON file containing user preferences to test filtering.",
    )
    parser.add_argument(
        "--filter-prefs",
        type=str,
        help="JSON string of user preferences to test filtering.",
    )
    args = parser.parse_args()

    settings = get_settings()

    if args.ingest:
        from data.loader import ingest

        path = ingest(refresh=True)
        print(f"  Ingested → {path}")
        return

    repository = RestaurantRepository()
    try:
        repository.load()
    except FileNotFoundError as exc:
        print(f"\n  {exc}")
        print("  Run: python -m data.loader --refresh")
        sys.exit(1)

    if args.command == "recommend":
        raw_prefs: dict[str, object] = {}
        if args.filter_prefs:
            try:
                raw_prefs = json.loads(args.filter_prefs)
            except json.JSONDecodeError as exc:
                print(f"Error: Invalid JSON format in --filter-prefs: {exc}")
                sys.exit(1)
        elif args.filter_file:
            path = Path(args.filter_file)
            if not path.exists():
                print(f"Error: Preferences file not found at {path}")
                sys.exit(1)
            try:
                raw_prefs = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                print(f"Error: Failed to read/parse preferences file: {exc}")
                sys.exit(1)
        else:
            if args.location:
                raw_prefs["location"] = args.location
            if args.budget:
                raw_prefs["budget"] = args.budget
            if args.cuisine:
                raw_prefs["cuisine"] = args.cuisine
            if args.min_rating is not None:
                raw_prefs["min_rating"] = args.min_rating
            if args.additional_preferences:
                raw_prefs["additional_preferences"] = args.additional_preferences

        orchestrator = RecommendationOrchestrator(repository=repository)
        try:
            response = orchestrator.recommend(raw_prefs)
        except Exception as exc:
            print(f"Recommendation failed: {exc}")
            sys.exit(1)

        print("\nRecommendation Results")
        print("-" * 80)
        if response.recommendations:
            for rec in response.recommendations:
                restaurant = repository.get_by_id(rec.restaurant_id)
                if restaurant is None:
                    continue
                print(
                    f"#{rec.rank}: {restaurant.name} — {restaurant.cuisine} | ★ {restaurant.rating}"
                )
                print(
                    f"    Cost: {restaurant.cost_for_two or 'N/A'} | Budget: {restaurant.budget_tier}"
                )
                print(f"    Location: {restaurant.location}")
                print(f"    Explanation: {rec.explanation}")
                print("-" * 80)
        else:
            print("No recommendations could be generated.")

        if response.summary:
            print("Summary:")
            print(response.summary)
            print("-" * 80)

        print("Metadata:")
        print(f"  Filters applied: {', '.join(response.filters_applied)}")
        print(f"  Candidates considered: {response.candidates_considered}")
        print(f"  Fallback used: {response.fallback_used}")
        if response.suggestions:
            print("Suggestions:")
            for suggestion in response.suggestions:
                print(f"  - {suggestion}")
        return

    print("Zomato AI Restaurant Recommender")
    print(f"  Dataset: {settings.dataset_name}")
    print(f"  Cache:   {settings.restaurants_parquet}")
    print(f"  Loaded:  {repository.count()} restaurants")
    meta = RestaurantRepository.cache_metadata()
    if meta:
        stats = meta.get("stats", {})
        print(f"  Retention: {stats.get('retention_percent', '?')}% of raw rows")

    cities = repository.distinct_cities()
    print(
        f"  Cities:  {len(cities)} ({', '.join(cities[:5])}{'...' if len(cities) > 5 else ''})"
    )

    delhi = repository.filter_by_city("Delhi")
    print(f"  Delhi:   {len(delhi)} restaurants")
    if delhi:
        top = sorted(delhi, key=lambda r: r.rating, reverse=True)[0]
        print(f"  Sample:  {top.name} (★ {top.rating}) — {top.location}")


if __name__ == "__main__":
    main()
