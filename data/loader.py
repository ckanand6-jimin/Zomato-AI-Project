"""
Download Zomato dataset from Hugging Face, preprocess, and persist to cache.

Usage:
    python -m data.loader --refresh
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Ensure project root is on path when run as script
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from config.settings import get_settings
from data.preprocessor import preprocess_dataframe

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def download_raw_dataframe(dataset_name: str | None = None):
    from datasets import load_dataset

    settings = get_settings()
    name = dataset_name or settings.dataset_name
    logger.info("Downloading dataset: %s", name)
    dataset = load_dataset(name, split="train")
    logger.info("Loaded %s rows, columns: %s", len(dataset), dataset.column_names)
    return dataset.to_pandas()


def save_cache(
    restaurants: list,
    stats_dict: dict,
    metadata: dict,
) -> Path:
    import pandas as pd

    from core.models import Restaurant

    settings = get_settings()
    settings.cache_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for r in restaurants:
        if isinstance(r, Restaurant):
            records.append(r.model_dump())
        else:
            records.append(r)

    df = pd.DataFrame(records)
    # Serialize raw dict as JSON string for Parquet
    if "raw" in df.columns:
        df["raw"] = df["raw"].apply(json.dumps)

    parquet_path = settings.restaurants_parquet
    df.to_parquet(parquet_path, index=False)
    logger.info("Wrote %s restaurants to %s", len(df), parquet_path)

    meta = {
        "stats": stats_dict,
        "preprocess": metadata,
        "row_count": len(df),
    }
    meta_path = settings.cache_metadata_path
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    logger.info("Wrote metadata to %s", meta_path)
    return parquet_path


def ingest(refresh: bool = True, dataset_name: str | None = None) -> Path:
    settings = get_settings()
    if not refresh and settings.restaurants_parquet.exists():
        logger.info("Cache exists at %s; use --refresh to rebuild", settings.restaurants_parquet)
        return settings.restaurants_parquet

    raw_df = download_raw_dataframe(dataset_name)
    restaurants, stats, metadata = preprocess_dataframe(raw_df)

    if stats.input_rows and stats.output_rows / stats.input_rows < 0.5:
        logger.warning(
            "Low retention rate (%.1f%%). Check preprocessing rules.",
            stats.output_rows / stats.input_rows * 100,
        )

    return save_cache(restaurants, stats.to_dict(), metadata)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest Zomato restaurant dataset")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Download and rebuild cache (required on first run)",
    )
    parser.add_argument(
        "--dataset",
        default=None,
        help="Override Hugging Face dataset name",
    )
    args = parser.parse_args()

    if not args.refresh and not get_settings().restaurants_parquet.exists():
        logger.info("No cache found; running full ingest")
        args.refresh = True

    path = ingest(refresh=args.refresh, dataset_name=args.dataset)
    print(f"Ingest complete: {path}")


if __name__ == "__main__":
    main()
