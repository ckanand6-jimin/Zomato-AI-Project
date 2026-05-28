from typing import Any, Literal

from pydantic import BaseModel, Field

BudgetTier = Literal["low", "medium", "high"]


class Restaurant(BaseModel):
    """Normalized restaurant record (architecture §5.1)."""

    id: str
    name: str
    location: str
    city: str
    cuisine: str
    rating: float = Field(ge=0.0, le=5.0)
    cost_for_two: int | None = None
    budget_tier: BudgetTier | None = None
    raw: dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class UserPreferences(BaseModel):
    """User preferences schema for recommendations."""

    location: str
    budget: BudgetTier
    cuisine: list[str] | None = None
    min_rating: float = Field(default=3.5, ge=0.0, le=5.0)
    additional_preferences: str | None = None

    model_config = {"frozen": True}


class Recommendation(BaseModel):
    """A single recommendation returned by the LLM or fallback path."""

    restaurant_id: str
    rank: int = Field(gt=0)
    explanation: str

    model_config = {"frozen": True}


class RecommendationResponse(BaseModel):
    """Structured LLM recommendation payload."""

    recommendations: list[Recommendation]
    summary: str | None = None
    model_version: str | None = None
    filters_applied: list[str] = Field(default_factory=list)
    candidates_considered: int = 0
    suggestions: list[str] = Field(default_factory=list)
    fallback_used: bool = False

    model_config = {"frozen": True}

