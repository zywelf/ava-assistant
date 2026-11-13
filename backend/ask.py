from sqlalchemy.orm import Session
import services
import rag
import llm


def answer_question(db: Session, question: str) -> dict:
    """Answer a question using the user's documents.

    Example: "What is a chunk?" to {"answer": "A piece of a document [1]", "sources": [...]}
    """
    results = services.semantic_search(db, question)
    messages = rag.build_messages(question, results)
    answer = llm.chat(messages)
    if not results:
        return {
            "answer": "I couldn't find anything about this in your documents.",
            "sources": [],
        }
    return {"answer": answer, "sources": results}
