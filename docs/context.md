# Project Context: AI-Powered Restaurant Recommendation System (Zomato Use Case)

## Overview

Build an **AI-powered restaurant recommendation service** inspired by Zomato. The system intelligently suggests restaurants based on user preferences by combining **structured restaurant data** with a **Large Language Model (LLM)** to produce personalized, human-like recommendations.

---

## Objective

Design and implement an application that:

- Takes user preferences (location, budget, cuisine, ratings, and more)
- Uses a real-world dataset of restaurants
- Leverages an LLM to generate personalized, human-like recommendations
- Displays clear and useful results to the user

---

## System Workflow

### 1. Data Ingestion

- Load and preprocess the Zomato dataset from Hugging Face:
  - **Dataset URL:** https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation
- Extract relevant fields, including:
  - Restaurant name
  - Location
  - Cuisine
  - Cost
  - Rating
  - (and other applicable fields from the dataset)

### 2. User Input

Collect user preferences:

| Preference | Examples / Notes |
|------------|------------------|
| **Location** | Delhi, Bangalore |
| **Budget** | low, medium, high |
| **Cuisine** | Italian, Chinese |
| **Minimum rating** | Numeric threshold |
| **Additional preferences** | family-friendly, quick service, etc. |

### 3. Integration Layer

- Filter and prepare relevant restaurant data based on user input
- Pass structured results into an LLM prompt
- Design a prompt that helps the LLM **reason** and **rank** options

### 4. Recommendation Engine

Use the LLM to:

- **Rank** restaurants
- **Explain** why each recommendation fits the user’s preferences
- **Optionally summarize** the overall set of choices

### 5. Output Display

Present top recommendations in a user-friendly format. Each recommendation should include:

- Restaurant name
- Cuisine
- Rating
- Estimated cost
- AI-generated explanation (why it was recommended)

---

## Architecture Summary

```
User Preferences → Filter Dataset → Structured Candidates → LLM (rank + explain) → Formatted Results
```

| Layer | Responsibility |
|-------|----------------|
| **Data** | Hugging Face Zomato dataset; ingest, clean, extract fields |
| **Input** | Location, budget, cuisine, min rating, optional extras |
| **Integration** | Filter data; build LLM prompt for reasoning and ranking |
| **Engine** | LLM ranks, explains, and optionally summarizes |
| **Output** | Top picks with name, cuisine, rating, cost, and explanation |

---

## Key Constraints & Expectations

- Recommendations must be grounded in **real dataset** entries (not purely hallucinated restaurants).
- The LLM’s role is **personalization, ranking, and explanation** on top of filtered structured data.
- Results should be **actionable and readable** for end users.
- The experience should feel similar in spirit to **Zomato-style** discovery: preference-driven, explainable suggestions.

---

## Source

Full problem statement: `docs/Problem statement.txt`
