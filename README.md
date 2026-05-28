# Zomato AI Restaurant Recommendation System

AI-powered restaurant recommendations using the Hugging Face Zomato dataset and an LLM (later phases).

## Documentation

- [Problem statement](docs/Problem%20statement.txt)
- [Context](docs/context.md)
- [Architecture](docs/architecture.md)
- [Implementation plan](docs/implementation-plan.md)
- [Edge cases](docs/edge-cases.md)

## Phase 1: Data ingestion (current)

### Setup

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Download and build cache

```bash
python -m data.loader --refresh
```

Writes:

- `data/cache/restaurants.parquet` — normalized restaurants
- `data/cache/cache_metadata.json` — stats and budget thresholds

### Verify

```bash
python -m app.main
python -m app.main --ingest   # force re-download
pytest tests/ -q
```

### Run the Streamlit demo

```bash
streamlit run app/streamlit_app.py
```

### Run demo scenarios (CLI)

```bash
python scripts/demo_scenarios.py
```

### Pinned requirements (optional)

If you need a reproducible environment, use the pinned requirements:

```bash
pip install -r requirements-pinned.txt
```

## Phase 6: QA, Demo, and Reproducibility

Follow these steps to run demos and verify the system end-to-end.

1. Ensure the data cache exists (ingest if needed):

```bash
python -m data.loader --refresh
```

2. Run unit tests:

```bash
pytest -q
```

3. Run demo scenarios (CLI):

```bash
python scripts/demo_scenarios.py
```

4. Run the Streamlit UI:

```bash
streamlit run app/streamlit_app.py
```

5. Create a reproducible environment (optional):

```bash
pip install -r requirements.txt
```

## Raw → canonical field mapping

| Hugging Face column | Canonical field | Notes |
|---------------------|-----------------|-------|
| `name` | `name` | Required |
| `location`, `address` | `location` | Display string |
| `listed_in(city)` | `city` | Normalized via alias map |
| `cuisines` | `cuisine` | Defaults to `"Unknown"` |
| `rate` | `rating` | Parsed from `4.1/5`; drops `-`, `NEW` |
| `approx_cost(for two people)` | `cost_for_two` | First integer extracted |
| (derived) | `budget_tier` | `low` / `medium` / `high` from percentiles |
| (derived) | `id` | SHA-256 hash of name + city + location + index |
| (full row) | `raw` | Original record for debugging |

Dataset: [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) (~51k rows).

## Project layout

```
app/           # Entry point
config/        # Settings and paths
core/          # Domain models
data/          # Loader, preprocessor, repository, cache/
tests/         # Unit tests
docs/          # Planning documents
```
