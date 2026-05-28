import pandas as pd

from data.preprocessor import (
    assign_budget_tier,
    normalize_city,
    parse_cost,
    parse_rating,
    preprocess_dataframe,
)


def test_parse_rating_formats():
    assert parse_rating("4.5/5") == 4.5
    assert parse_rating("4.1") == 4.1
    assert parse_rating("-") is None
    assert parse_rating("NEW") is None


def test_parse_cost_formats():
    assert parse_cost("800") == 800
    assert parse_cost("300, 400") == 300
    assert parse_cost("₹1,200") == 1200
    assert parse_cost("-") is None


def test_normalize_city_aliases():
    assert normalize_city("Bengaluru") == "Bangalore"
    assert normalize_city("new delhi") == "Delhi"


def test_assign_budget_tier():
    assert assign_budget_tier(400, 500, 1500) == "low"
    assert assign_budget_tier(800, 500, 1500) == "medium"
    assert assign_budget_tier(2000, 500, 1500) == "high"
    assert assign_budget_tier(None, 500, 1500) is None


def test_preprocess_drops_invalid_rows():
    df = pd.DataFrame(
        [
            {
                "name": "Valid Place",
                "location": "Koramangala",
                "address": "Street 1",
                "listed_in(city)": "Bangalore",
                "cuisines": "Italian",
                "rate": "4.5/5",
                "approx_cost(for two people)": "800",
            },
            {
                "name": "",
                "location": "X",
                "address": "",
                "listed_in(city)": "Delhi",
                "cuisines": "Chinese",
                "rate": "4.0/5",
                "approx_cost(for two people)": "500",
            },
            {
                "name": "No Rating",
                "location": "CP",
                "address": "",
                "listed_in(city)": "Delhi",
                "cuisines": "North Indian",
                "rate": "-",
                "approx_cost(for two people)": "600",
            },
        ]
    )
    restaurants, stats, _ = preprocess_dataframe(df)
    assert len(restaurants) == 1
    assert restaurants[0].name == "Valid Place"
    assert restaurants[0].city == "Bangalore"
    assert stats.dropped_missing_name == 1
    assert stats.dropped_missing_rating == 1
