from __future__ import annotations

import logging
import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from config.settings import get_settings
from core.models import RecommendationResponse, UserPreferences
from core.orchestrator import RecommendationOrchestrator
from data.repository import RestaurantRepository

logger = logging.getLogger(__name__)
settings = get_settings()


def parse_cors_origins(raw: str | None) -> list[str]:
    if not raw or raw.strip() == "*":
        return ["*"]

    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins or ["*"]


def get_cors_origins() -> list[str]:
    return parse_cors_origins(os.environ.get("CORS_ORIGINS", "*"))


app = FastAPI(
    title="Zomato AI Recommender API",
    description="Backend API for the Zomato AI recommender frontend.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_repository: RestaurantRepository | None = None


def load_repository() -> RestaurantRepository:
    logger.info("Initializing RestaurantRepository from settings: %s", settings.restaurants_parquet)
    repository = RestaurantRepository(settings)
    try:
        logger.info("Calling repository.load()...")
        repository.load()
        logger.info("Repository loaded successfully")
    except FileNotFoundError as e:
        logger.warning("Cache file not found: %s", e)
        if os.environ.get("AUTO_REFRESH_CACHE", "").lower() in ("1", "true", "yes") or settings.auto_refresh_cache:
            logger.info("AUTO_REFRESH_CACHE enabled, attempting refresh...")
            repository.load(force_refresh=True)
        else:
            raise
    except Exception as e:
        logger.exception("CRITICAL: Failed to load repository - %s: %s", type(e).__name__, str(e))
        raise

    return repository


def get_repository() -> RestaurantRepository:
    global _repository
    if _repository is None:
        _repository = load_repository()
    return _repository


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/cities")
def list_cities() -> list[str]:
    try:
        logger.info("GET /api/cities - fetching distinct cities")
        cities = get_repository().distinct_cities()
        logger.info("GET /api/cities - returning %d cities", len(cities))
        return cities
    except Exception as e:
        logger.exception("CRITICAL: /api/cities failed - %s: %s", type(e).__name__, str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch cities: {type(e).__name__}"
        )


@app.post("/api/recommend", response_model=RecommendationResponse)
def request_recommendation(payload: dict[str, Any]) -> RecommendationResponse:
    try:
        preferences = UserPreferences(**payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors())

    orchestrator = RecommendationOrchestrator(repository=get_repository())
    return orchestrator.recommend(preferences)


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("app.api:app", host="0.0.0.0", port=port, log_level="info")
