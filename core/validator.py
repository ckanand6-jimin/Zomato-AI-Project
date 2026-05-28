"""
Validation and normalization of user preference inputs (Phase 2).
"""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from config.settings import get_settings
from core.models import UserPreferences
from data.preprocessor import normalize_city


class PreferenceValidationError(ValueError):
    """Custom exception raised when preference validation fails."""

    def __init__(self, errors: dict[str, str]) -> None:
        self.errors = errors
        super().__init__(str(errors))


def validate_preferences(data: dict[str, Any]) -> UserPreferences:
    """
    Validate and normalize raw user preference input.

    Raises:
        PreferenceValidationError: if validation fails with a dict of field-level errors.
    """
    errors: dict[str, str] = {}
    settings = get_settings()

    # 1. Location validation and normalization
    location_raw = data.get("location")
    if location_raw is None:
        errors["location"] = "Location is required."
    elif not isinstance(location_raw, str) or not location_raw.strip():
        errors["location"] = "Location must be a non-empty string."
    else:
        normalized_loc = normalize_city(location_raw, settings)
        if not normalized_loc:
            errors["location"] = "Location cannot be empty."
        else:
            data = {**data, "location": normalized_loc}

    # 2. Budget validation
    budget = data.get("budget")
    if budget is None:
        errors["budget"] = "Budget is required."
    elif budget not in {"low", "medium", "high"}:
        errors["budget"] = "Budget must be one of: low, medium, high."

    # 3. Min Rating validation and normalization
    min_rating_raw = data.get("min_rating")
    if min_rating_raw is None:
        data = {**data, "min_rating": settings.default_min_rating}
    else:
        try:
            min_rating = float(min_rating_raw)
            if not (0.0 <= min_rating <= 5.0):
                errors["min_rating"] = "Minimum rating must be between 0.0 and 5.0."
            else:
                data = {**data, "min_rating": min_rating}
        except (ValueError, TypeError):
            errors["min_rating"] = "Minimum rating must be a valid number."

    # 4. Cuisine validation and normalization
    cuisine_raw = data.get("cuisine")
    if cuisine_raw is not None:
        cuisine_list: list[str] = []
        if isinstance(cuisine_raw, str):
            # Split comma separated cuisines
            cuisine_list = [c.strip().lower() for c in cuisine_raw.split(",") if c.strip()]
        elif isinstance(cuisine_raw, list):
            cuisine_list = [str(c).strip().lower() for c in cuisine_raw if str(c).strip()]
        else:
            errors["cuisine"] = "Cuisine must be a string or a list of strings."

        if "cuisine" not in errors:
            data = {**data, "cuisine": cuisine_list if cuisine_list else None}

    # 5. Additional preferences normalization
    add_prefs_raw = data.get("additional_preferences")
    if add_prefs_raw is not None:
        data = {**data, "additional_preferences": str(add_prefs_raw).strip()}

    if errors:
        raise PreferenceValidationError(errors)

    try:
        # Final schema check using Pydantic
        return UserPreferences(**data)
    except ValidationError as exc:
        pydantic_errors: dict[str, str] = {}
        for err in exc.errors():
            loc = err["loc"][0]
            pydantic_errors[str(loc)] = err["msg"]
        raise PreferenceValidationError(pydantic_errors) from exc
