"""
Read-only access to normalized restaurant data from Parquet cache.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import pandas as pd

from config.settings import Settings, get_settings
from core.models import Restaurant
from data.loader import ingest

logger = logging.getLogger(__name__)


class RestaurantRepository:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._restaurants: list[Restaurant] = []
        self._by_id: dict[str, Restaurant] = {}
        self._loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def load(self, force_refresh: bool = False) -> None:
        path = self._settings.restaurants_parquet
        if force_refresh or not path.exists():
            if self._settings.auto_refresh_cache or force_refresh:
                ingest(refresh=True)
            elif not path.exists():
                raise FileNotFoundError(
                    f"Restaurant cache not found at {path}. "
                    "Run: python -m data.loader --refresh"
                )

        start = time.perf_counter()
        logger.info("Loading restaurants from parquet: %s", path)
        try:
            df = pd.read_parquet(path)
            logger.info("Successfully read parquet - shape: %s, columns: %s", df.shape, list(df.columns))
        except Exception as e:
            logger.exception("CRITICAL: Failed to read parquet file at %s: %s", path, type(e).__name__)
            raise

        logger.info("Converting dataframe to records (size: %s rows)", len(df))
        try:
            records = df.to_dict(orient="records")
            logger.info("Successfully converted %s records to dict", len(records))
        except Exception as e:
            logger.exception("CRITICAL: Failed to convert dataframe to dict: %s", type(e).__name__)
            raise

        restaurants: list[Restaurant] = []
        creation_errors = 0
        for idx, row in enumerate(records):
            try:
                raw = row.get("raw")
                if isinstance(raw, str):
                    try:
                        raw = json.loads(raw)
                    except json.JSONDecodeError:
                        raw = {}
                elif raw is None or (isinstance(raw, float) and pd.isna(raw)):
                    raw = {}

                tier_raw = row.get("budget_tier")
                if tier_raw is None or (isinstance(tier_raw, float) and pd.isna(tier_raw)):
                    budget_tier = None
                else:
                    budget_tier = str(tier_raw)

                restaurants.append(
                    Restaurant(
                        id=str(row["id"]),
                        name=str(row["name"]),
                        location=str(row["location"]),
                        city=str(row["city"]),
                        cuisine=str(row["cuisine"]),
                        rating=float(row["rating"]),
                        cost_for_two=(
                            int(row["cost_for_two"])
                            if row.get("cost_for_two") is not None
                            and not pd.isna(row["cost_for_two"])
                            else None
                        ),
                        budget_tier=budget_tier,
                        raw=raw if isinstance(raw, dict) else {},
                    )
                )
            except Exception as e:
                creation_errors += 1
                if creation_errors <= 3:  # Log first 3 errors only
                    logger.error(
                        "CRITICAL: Failed to create Restaurant at index %s: %s | Row keys: %s | Error: %s",
                        idx, type(e).__name__, list(row.keys()) if isinstance(row, dict) else "N/A", str(e)
                    )
                if creation_errors > 10:  # Give up after 10 consecutive errors
                    logger.critical("Too many Restaurant creation errors (%d), aborting load", creation_errors)
                    raise

        if creation_errors > 0:
            logger.warning("Restaurant creation encountered %d errors (processed %d/%d rows)", 
                          creation_errors, len(restaurants), len(records))

        self._restaurants = restaurants
        self._by_id = {r.id: r for r in restaurants}
        self._loaded = True
        elapsed = time.perf_counter() - start
        logger.info("Loaded %s restaurants in %.2fs", len(restaurants), elapsed)

    def ensure_loaded(self) -> None:
        if not self._loaded:
            self.load()

    def get_all(self) -> list[Restaurant]:
        self.ensure_loaded()
        return list(self._restaurants)

    def get_by_ids(self, ids: list[str]) -> list[Restaurant]:
        self.ensure_loaded()
        result: list[Restaurant] = []
        for rid in ids:
            restaurant = self._by_id.get(rid)
            if restaurant:
                result.append(restaurant)
            else:
                logger.warning("Unknown restaurant id skipped: %s", rid)
        return result

    def get_by_id(self, restaurant_id: str) -> Restaurant | None:
        self.ensure_loaded()
        return self._by_id.get(restaurant_id)

    def distinct_cities(self) -> list[str]:
        self.ensure_loaded()
        logger.info("Extracting distinct cities from %s restaurants", len(self._restaurants))
        try:
            cities = sorted({r.city for r in self._restaurants if r.city})
            logger.info("Found %d distinct cities: %s", len(cities), cities[:5] if len(cities) > 5 else cities)
            return cities
        except Exception as e:
            logger.exception("CRITICAL: Failed to extract distinct cities: %s", type(e).__name__)
            raise

    def filter_by_city(self, city: str, *, case_insensitive: bool = True) -> list[Restaurant]:
        self.ensure_loaded()
        needle = city.strip()
        if not needle:
            return []
        if case_insensitive:
            needle_lower = needle.lower()
            return [r for r in self._restaurants if r.city.lower() == needle_lower]
        return [r for r in self._restaurants if r.city == needle]

    def count(self) -> int:
        self.ensure_loaded()
        return len(self._restaurants)

    @staticmethod
    def cache_metadata(settings: Settings | None = None) -> dict | None:
        settings = settings or get_settings()
        path = settings.cache_metadata_path
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))


_default_repo: RestaurantRepository | None = None


def get_repository() -> RestaurantRepository:
    global _default_repo
    if _default_repo is None:
        _default_repo = RestaurantRepository()
        _default_repo.load()
    return _default_repo
