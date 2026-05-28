import json
from pathlib import Path

import pandas as pd
import pytest

from core.models import Restaurant
from data.repository import RestaurantRepository


@pytest.fixture
def sample_parquet(tmp_path, monkeypatch):
    import sys
    import config
    settings_module = sys.modules["config.settings"]

    cache = tmp_path / "cache"
    cache.mkdir()
    parquet = cache / "restaurants.parquet"
    meta = cache / "cache_metadata.json"

    rows = [
        Restaurant(
            id="id1",
            name="Delhi Diner",
            location="Connaught Place, Delhi",
            city="Delhi",
            cuisine="Chinese",
            rating=4.5,
            cost_for_two=600,
            budget_tier="medium",
            raw={"source": "test"},
        ).model_dump()
    ]
    df = pd.DataFrame(rows)
    df["raw"] = df["raw"].apply(json.dumps)
    df.to_parquet(parquet, index=False)
    meta.write_text('{"stats": {"retention_percent": 100}}', encoding="utf-8")

    test_settings = settings_module.get_settings().__class__(
        restaurants_parquet=parquet,
        cache_metadata_path=meta,
        cache_dir=cache,
    )
    monkeypatch.setattr(settings_module, "get_settings", lambda: test_settings)
    monkeypatch.setattr(settings_module, "settings", test_settings)
    import data.repository
    monkeypatch.setattr(data.repository, "get_settings", lambda: test_settings)
    return parquet


def test_repository_load_and_query(sample_parquet):
    repo = RestaurantRepository()
    repo.load()
    assert repo.count() == 1
    assert repo.get_by_id("id1") is not None
    assert repo.get_by_ids(["id1", "missing"]) == [repo.get_by_id("id1")]
    delhi = repo.filter_by_city("Delhi")
    assert len(delhi) == 1
    assert "Delhi" in repo.distinct_cities()
