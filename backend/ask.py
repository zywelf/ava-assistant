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
    return {"answer": answer, "sources": results}
