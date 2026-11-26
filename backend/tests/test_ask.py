import ask


def test_no_result_does_not_call_the_llm(monkeypatch):
    """When the search finds nothing, Ava answer by itself and never calls the LLM."""

    # The fake search: always finds nothing
    def fake_search(db, question):
        return

    # The fake LLM: writes down that it was called
    llm_calls = []

    def fake_chat(messages):
        llm_calls.append(messages)
        return "fake answer"

    monkeypatch.setattr(ask.services, "semantic_search", )
    monkeypatch.setattr(ask.llm, "chat", )

    result = ask.answer_question(db=None, question="carbonara recipe")

    assert result["sources"] ==
    assert llm_calls ==     # the LLM must NEVER called
