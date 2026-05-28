import sys
from types import SimpleNamespace

from core.models import Restaurant, UserPreferences
from llm.client import LLMClient


def make_restaurant(restaurant_id: str, name: str, rating: float) -> Restaurant:
    return Restaurant(
        id=restaurant_id,
        name=name,
        location="Sample Location",
        city="Delhi",
        cuisine="Indian",
        rating=rating,
        cost_for_two=300,
        budget_tier="low",
        raw={},
    )


def test_llm_client_retries_once_on_groq_error(monkeypatch):

    class DummyMessage:
        def __init__(self, content: str) -> None:
            self.content = content

    class DummyChoice:
        def __init__(self, content: str) -> None:
            self.message = DummyMessage(content)

    class DummyResponse:
        def __init__(self, content: str) -> None:
            self.choices = [DummyChoice(content)]

    class DummyCompletions:
        calls = 0

        def create(self, **kwargs):
            DummyCompletions.calls += 1
            if DummyCompletions.calls == 1:
                raise RuntimeError("transient failure")
            return DummyResponse('{"recommendations": []}')

    class DummyChat:
        def __init__(self):
            self.completions = DummyCompletions()

    class DummyGroqClient:
        def __init__(self, api_key=None, **kwargs):
            self.chat = DummyChat()

    # Reset call counter before test
    DummyCompletions.calls = 0

    # Patch groq module
    dummy_groq_module = SimpleNamespace(Groq=DummyGroqClient)
    sys.modules["groq"] = dummy_groq_module

    monkeypatch.setattr("llm.client.time.sleep", lambda _: None)
    monkeypatch.setenv("GROQ_API_KEY", "test-key")

    client = LLMClient()
    prefs = UserPreferences(location="Delhi", budget="low")
    restaurants = [make_restaurant("a1", "Alpha", 4.5)]

    try:
        result = client.complete(prefs, restaurants)
        assert "{" in result or "recommend" in result.lower()
        assert DummyCompletions.calls == 2
    finally:
        sys.modules.pop("groq", None)