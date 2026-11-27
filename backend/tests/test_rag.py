from models import SearchResult
from rag import build_messages, SYSTEM_PROMPT


def test_message_have_rules_texts_and_question():
    """The system message has the rules, the user message has numbered texts and the question."""
    results = [
        SearchResult(document_id=1, title="A.md", position=0, content="first text", distance=0.3),
        SearchResult(document_id=2, title="B.md", position=4, content="second text", distance=0.4),
    ]

    messages = build_messages("What is Ava?", results)

    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM_PROMPT
    user = messages[1]["content"]
    assert "[1] (A.md · part 1)" in user
    assert "[2] (B.md · part 5)" in user # the second text: careful with "part"
    assert "Question: What is Ava?" in user
