from __future__ import annotations
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st

from config.settings import get_settings
from core.formatter import format_recommendation_cards
from core.orchestrator import RecommendationOrchestrator
from data.repository import RestaurantRepository
from app.logging_config import configure_logging


def load_repository() -> RestaurantRepository:
    repo = RestaurantRepository()
    repo.load()
    return repo


@st.cache_resource
def get_cached_repository() -> RestaurantRepository:
    return load_repository()


def load_streamlit_secrets() -> None:
    if "GROQ_API_KEY" not in os.environ:
        secret_key = st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else None
        if secret_key:
            os.environ["GROQ_API_KEY"] = secret_key


def main() -> None:
    load_streamlit_secrets()
    configure_logging()
    settings = get_settings()
    st.set_page_config(
        page_title="Zomato AI Restaurant Recommender",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.title("Zomato AI Restaurant Recommender")
    st.write(
        "Use structured preferences to get grounded restaurant recommendations with AI explanations. "
        "The AI ranks from a filtered candidate set so output stays grounded in real data."
    )

    repository = get_cached_repository()
    city_options = repository.distinct_cities()

    if not city_options:
        st.error("Restaurant data is unavailable. Run data ingestion and refresh the app.")
        return

    default_city_index = city_options.index("Delhi") if "Delhi" in city_options else 0

    with st.form("preference_form"):
        selected_location = st.selectbox(
            "Location",
            options=city_options,
            index=default_city_index,
            help="Select the city where you want restaurant recommendations.",
        )
        selected_budget = st.radio(
            "Budget tier",
            options=["low", "medium", "high"],
            index=1,
            horizontal=True,
        )
        selected_cuisine = st.text_input(
            "Cuisine preference",
            value="",
            help="Enter one or more cuisines separated by commas (e.g. Indian, Chinese).",
        )
        min_rating = st.slider(
            "Minimum rating",
            min_value=0.0,
            max_value=5.0,
            value=settings.default_min_rating,
            step=0.1,
        )
        additional_preferences = st.text_area(
            "Additional preferences",
            help="Optional details like family-friendly, quick service, fine dining, or vegetarian options.",
        )
        submitted = st.form_submit_button("Find restaurants")

    if not submitted:
        st.info("Fill the form above and click Find restaurants to get started.")
        return

    raw_preferences: dict[str, object] = {
        "location": selected_location,
        "budget": selected_budget,
        "min_rating": min_rating,
    }
    if selected_cuisine.strip():
        raw_preferences["cuisine"] = selected_cuisine
    if additional_preferences.strip():
        raw_preferences["additional_preferences"] = additional_preferences.strip()

    orchestrator = RecommendationOrchestrator(repository=repository)
    with st.spinner("Generating grounded recommendations..."):
        response = orchestrator.recommend(raw_preferences)

    if response.fallback_used:
        st.warning(
            "The AI recommendation step could not be completed reliably, so grounded fallback rankings are shown instead."
        )

    if not response.recommendations:
        st.error("No recommendations matched your preferences.")
        if response.suggestions:
            st.markdown("**Suggestions:**")
            for suggestion in response.suggestions:
                st.write(f"- {suggestion}")
        return

    if response.summary:
        st.markdown("### Summary")
        st.write(response.summary)

    cards = format_recommendation_cards(response, repository)
    for card in cards:
        st.markdown(f"### #{card['rank']} — {card['name']}")
        st.write(
            f"**Cuisine:** {card['cuisine']}  \n"
            f"**Rating:** ★ {card['rating']}  \n"
            f"**Cost:** {card['estimated_cost']}  \n"
            f"**Budget tier:** {card['budget_tier']}  \n"
            f"**Location:** {card['location']}"
        )
        st.write(f"**Why we picked this:** {card['explanation']}")
        st.markdown("---")

    with st.expander("Recommendation details"):
        st.write(f"Filters applied: {', '.join(response.filters_applied)}")
        st.write(f"Candidates considered: {response.candidates_considered}")
        st.write(f"Fallback used: {response.fallback_used}")
        if response.suggestions:
            st.markdown("**Suggestions:**")
            for suggestion in response.suggestions:
                st.write(f"- {suggestion}")


if __name__ == "__main__":
    main()
