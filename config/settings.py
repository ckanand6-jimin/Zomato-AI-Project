from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "data" / "cache"
RESTAURANTS_PARQUET = CACHE_DIR / "restaurants.parquet"
CACHE_METADATA_JSON = CACHE_DIR / "cache_metadata.json"

BudgetTier = Literal["low", "medium", "high"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Data
    dataset_name: str = "ManikaSaini/zomato-restaurant-recommendation"
    auto_refresh_cache: bool = False
    cache_dir: Path = CACHE_DIR
    restaurants_parquet: Path = RESTAURANTS_PARQUET
    cache_metadata_path: Path = CACHE_METADATA_JSON

    # Budget tiers (INR for two); recalibrated on ingest from percentiles
    budget_low_max: int = 500
    budget_medium_max: int = 1500

    # City normalization
    city_aliases: dict[str, str] = Field(
        default_factory=lambda: {
            "bengaluru": "Bangalore",
            "bangalore": "Bangalore",
            "bombay": "Mumbai",
            "mumbai": "Mumbai",
            "new delhi": "Delhi",
            "delhi ncr": "Delhi",
            "gurgaon": "Gurgaon",
            "gurugram": "Gurgaon",
        }
    )

    # LLM (later phases)
    llm_provider: Literal["groq", "anthropic"] = "groq"
    groq_api_key: str | None = None
    llm_model: str = "llama3-8b-8192"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 600
    llm_timeout_seconds: int = 30
    llm_fallback_on_error: bool = True
    llm_disabled: bool = False
    max_candidates: int = 25
    top_n_recommendations: int = 5
    default_min_rating: float = 3.5


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
