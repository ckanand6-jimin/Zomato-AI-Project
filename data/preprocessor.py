"""
Normalize raw Hugging Face Zomato rows into canonical Restaurant records.

Raw → canonical field mapping (dataset: ManikaSaini/zomato-restaurant-recommendation):
  name                          → name
  location + address            → location (display)
  listed_in(city)               → city (normalized)
  cuisines                      → cuisine
  rate                          → rating (float)
  approx_cost(for two people)   → cost_for_two (int)
  (derived)                     → budget_tier, id
  (full row)                    → raw
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from typing import Any

import pandas as pd

from config.settings import Settings, get_settings
from core.models import BudgetTier, Restaurant

logger = logging.getLogger(__name__)

# Hugging Face column names
COL_NAME = "name"
COL_ADDRESS = "address"
COL_LOCATION = "location"
COL_CUISINES = "cuisines"
COL_RATE = "rate"
COL_COST = "approx_cost(for two people)"
COL_CITY = "listed_in(city)"


class PreprocessStats:
    def __init__(self) -> None:
        self.input_rows = 0
        self.output_rows = 0
        self.dropped_missing_name = 0
        self.dropped_missing_location = 0
        self.dropped_missing_rating = 0
        self.dropped_invalid_rating = 0
        self.dropped_duplicates = 0

    def to_dict(self) -> dict[str, int | float]:
        total_dropped = (
            self.dropped_missing_name
            + self.dropped_missing_location
            + self.dropped_missing_rating
            + self.dropped_invalid_rating
            + self.dropped_duplicates
        )
        retention = (
            (self.output_rows / self.input_rows * 100) if self.input_rows else 0.0
        )
        return {
            "input_rows": self.input_rows,
            "output_rows": self.output_rows,
            "dropped_missing_name": self.dropped_missing_name,
            "dropped_missing_location": self.dropped_missing_location,
            "dropped_missing_rating": self.dropped_missing_rating,
            "dropped_invalid_rating": self.dropped_invalid_rating,
            "dropped_duplicates": self.dropped_duplicates,
            "total_dropped": total_dropped,
            "retention_percent": round(retention, 2),
        }


def parse_rating(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    if not text or text in {"-", "NEW", "new", "nan"}:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    if not match:
        return None
    rating = float(match.group(1))
    if rating > 5.0:
        rating = rating / 10.0 if rating <= 50 else None
    if rating is None or rating < 0 or rating > 5:
        return None
    return round(rating, 2)


def parse_cost(value: Any) -> int | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    if not text or text in {"-", "nan"}:
        return None
    numbers = re.findall(r"\d+", text.replace(",", ""))
    if not numbers:
        return None
    # Use first number when range like "300, 400"
    cost = int(numbers[0])
    return cost if cost > 0 else None


def normalize_city(city: str, settings: Settings | None = None) -> str:
    settings = settings or get_settings()
    cleaned = " ".join(city.strip().split())
    if not cleaned:
        return ""
    key = cleaned.lower()
    if key in settings.city_aliases:
        return settings.city_aliases[key]
    return cleaned.title()


def assign_budget_tier(
    cost: int | None,
    low_max: int,
    medium_max: int,
) -> BudgetTier | None:
    if cost is None:
        return None
    if cost <= low_max:
        return "low"
    if cost <= medium_max:
        return "medium"
    return "high"


def calibrate_budget_thresholds(costs: pd.Series) -> tuple[int, int]:
    """Set low/medium boundaries at 33rd and 66th percentiles."""
    valid = costs.dropna().astype(int)
    if valid.empty:
        return 500, 1500
    low_max = int(valid.quantile(0.33))
    medium_max = int(valid.quantile(0.66))
    if low_max >= medium_max:
        medium_max = low_max + 1
    return max(low_max, 1), max(medium_max, low_max + 1)


def make_restaurant_id(name: str, city: str, location: str, index: int) -> str:
    payload = f"{name}|{city}|{location}|{index}".lower().encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def _build_location(area: str, address: str, city: str) -> str:
    parts = [p.strip() for p in (area, address) if p and str(p).strip()]
    if not parts and city:
        return city
    display = ", ".join(parts)
    if city and city.lower() not in display.lower():
        return f"{display}, {city}" if display else city
    return display or city


def preprocess_dataframe(
    df: pd.DataFrame,
    settings: Settings | None = None,
) -> tuple[list[Restaurant], PreprocessStats, dict[str, Any]]:
    settings = settings or get_settings()
    stats = PreprocessStats()
    stats.input_rows = len(df)

    costs_for_calibration: list[int] = []
    rows: list[dict[str, Any]] = []

    for idx, record in df.iterrows():
        row = record.to_dict() if hasattr(record, "to_dict") else dict(record)

        name = str(row.get(COL_NAME, "") or "").strip()
        if not name:
            stats.dropped_missing_name += 1
            continue

        city_raw = str(row.get(COL_CITY, "") or "").strip()
        area = str(row.get(COL_LOCATION, "") or "").strip()
        address = str(row.get(COL_ADDRESS, "") or "").strip()
        city = normalize_city(city_raw, settings) if city_raw else ""

        if not city and not area:
            stats.dropped_missing_location += 1
            continue
        if not city:
            city = normalize_city(area.split(",")[-1].strip(), settings) or area

        location = _build_location(area, address, city)
        if not location:
            stats.dropped_missing_location += 1
            continue

        rating = parse_rating(row.get(COL_RATE))
        if rating is None:
            if row.get(COL_RATE) in (None, "", "-", "NEW"):
                stats.dropped_missing_rating += 1
            else:
                stats.dropped_invalid_rating += 1
            continue

        cuisine = str(row.get(COL_CUISINES, "") or "").strip() or "Unknown"
        cost = parse_cost(row.get(COL_COST))
        if cost is not None:
            costs_for_calibration.append(cost)

        rows.append(
            {
                "id": make_restaurant_id(name, city, location, int(idx)),
                "name": name,
                "location": location,
                "city": city,
                "cuisine": cuisine,
                "rating": rating,
                "cost_for_two": cost,
                "raw": {k: (None if pd.isna(v) else v) for k, v in row.items()},
            }
        )

    if not rows:
        stats.output_rows = 0
        return [], stats, {"budget_low_max": settings.budget_low_max, "budget_medium_max": settings.budget_medium_max}

    work = pd.DataFrame(rows)
    before_dedup = len(work)
    work = work.drop_duplicates(subset=["name", "city", "location"], keep="first")
    stats.dropped_duplicates = before_dedup - len(work)

    cost_series = pd.Series(costs_for_calibration)
    low_max, medium_max = calibrate_budget_thresholds(cost_series)

    restaurants: list[Restaurant] = []
    for row in work.to_dict(orient="records"):
        cost_raw = row.get("cost_for_two")
        cost = None if (cost_raw is None or (isinstance(cost_raw, float) and pd.isna(cost_raw))) else int(cost_raw)
        tier = assign_budget_tier(cost, low_max, medium_max)
        restaurants.append(
            Restaurant(
                id=row["id"],
                name=row["name"],
                location=row["location"],
                city=row["city"],
                cuisine=row["cuisine"],
                rating=row["rating"],
                cost_for_two=cost,
                budget_tier=tier,
                raw=row["raw"],
            )
        )

    stats.output_rows = len(restaurants)
    metadata = {
        "budget_low_max": low_max,
        "budget_medium_max": medium_max,
        "budget_calibration": "percentile_33_66",
    }
    logger.info("Preprocess stats: %s", stats.to_dict())
    logger.info("Budget thresholds: low<=%s, medium<=%s", low_max, medium_max)
    return restaurants, stats, metadata


def preprocess_records(
    records: list[dict[str, Any]],
    settings: Settings | None = None,
) -> tuple[list[Restaurant], PreprocessStats, dict[str, Any]]:
    df = pd.DataFrame(records)
    return preprocess_dataframe(df, settings)
