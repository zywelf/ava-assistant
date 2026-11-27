import re
from sqlalchemy.orm import Session
from models import CitedSource
import services
import rag
import llm

# What Ava says when the search finds nothing (used also by evals.py)
NOT_FOUND_ANSWER = "I couldn't find anything about this in your documents."


def answer_question(db: Session, question: str) -> dict:
    """Answer a question using the user's documents.

    Example: "What is a chunk?" to {"answer": "A piece of a document [1]", "sources": [...]}
    """
    results = services.semantic_search(db, question)
    if not results:
        return {
            "answer": NOT_FOUND_ANSWER,
            "sources": [],
        }
    messages = rag.build_messages(question, results)
    answer = llm.chat(messages)

    cited = re.findall(r"\[(\d+)]", answer)  # "... [1] ... [2]" to ["1", "2"]
    cited_numbers = {int(n) for n in cited}  # ["1", "2"] to {1, 2}

    sources = [
        CitedSource(**chunk.model_dump(), number=number)
        for number, chunk in enumerate(results, start=1)
        if number in cited_numbers
    ]
    return {"answer": answer, "sources": sources}
