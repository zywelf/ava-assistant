import ask
from models import SearchResult


def test_no_result_does_not_call_the_llm(monkeypatch):
    """When the search finds nothing, Ava answers by itself and never calls the LLM."""

    # The fake search: always finds nothing
    def fake_search(db, question):
        return []

    # The fake LLM: writes down that it was called
    llm_calls = []

    def fake_chat(messages):
        llm_calls.append(messages)
        return "fake answer"

    monkeypatch.setattr(ask.services, "semantic_search", fake_search)
    monkeypatch.setattr(ask.llm, "chat", fake_chat)

    result = ask.answer_question(db=None, question="carbonara recipe")

    assert result["sources"] == []
    assert llm_calls == []  # the LLM must NEVER be called


def make_result(title: str) -> SearchResult:
    """A fake result, only the title changes.

    Example: make_result("A.md") → a SearchResult with title "A.md"
    """
    return SearchResult(
        document_id=1, title=title, position=0, content="some text", distance=0.3
    )


def test_only_cited_sources_are_kept_with_their_number(monkeypatch):
    """If the answer cites only [2], only the second source is shown, with number 2."""

    def fake_search(db, question):
        return [make_result("A.md"), make_result("B.md")]

    def fake_chat(messages):
        return "Ava is a document assistant [2]." # an answer that cites only the second text

    monkeypatch.setattr(ask.services, "semantic_search", fake_search)
    monkeypatch.setattr(ask.llm, "chat", fake_chat)

    result = ask.answer_question(db=None, question="What is Ava?")

    sources = result["sources"]
    assert len(sources) == 1
    assert sources[0].title == "B.md"
    assert sources[0].number == 2
