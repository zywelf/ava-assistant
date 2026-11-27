from db import SessionLocal
import ask

# The questions to ask Ava, and what we expect from each answer.
# Run with Docker and Ollama on: python evals.py
CASES = [
    {
        "question": "What is the backend of Ava built with?",
        "expect": "answer",  # it answers, citing at least one source
        "source": "README.md",  # ...and one of the sources is this document
    },
    {
        "question": "What's GTA 6?",
        "expect": "not_found",   # the code answers "I couldn't find..."
    },
    {
        "question": "Who is the CEO of Ava?",
        "expect": "dont_know",  # the model doesn't know: no sources
    },
    {
        "question": "Where's the best pizza place in Naples",  # finds a chunk about restaurants on a map, but no answer
        "expect": "dont_know",   # the model doesn't know: no sources
    },
    {
        "question": "What is the frontend of Ava built with?",
        "expect": "answer",  # it answers, citing at least one source
        "source": "README.md",  # ...and one of the sources is this document
    },
]


def check(case: dict, result: dict) -> bool:
    """Tell if Ava's answer is what the case expects.

    Example: expect "dont_know" and no sources -> True
    """
    titles = [source.title for source in result["sources"]]

    if case["expect"] == "answer":
        return len(titles) > 0 and case["source"] in titles
    if case["expect"] == "dont_know":
        return titles == []
    if case["expect"] == "not_found":
        return result["answer"] == ask.NOT_FOUND_ANSWER
    return False


with SessionLocal() as db:
    passed = 0
    for case in CASES:
        result = ask.answer_question(db, case["question"])
        ok = check(case, result)
        passed += ok
        print("✅" if ok else "❌", case["question"])
        if not ok:
            print("   answer: ", result["answer"])
            print("   sources:", [source.title for source in result["sources"]])
    print(f"\n{passed}/{len(CASES)} passed")
