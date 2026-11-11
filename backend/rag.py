# The rules the LLM must follow in every answer (the "system" message)
SYSTEM_PROMPT = """You are Ava, an assistant that answers questions about the user's documents.

Rules:
1. Answer using ONLY the numbered texts you receive.
2. If the answer is not in the texts, say that you don't know. Do NOT invent.
3. After each piece of information, write the number of its text, like [1].
4. Answer in the same language as the question. Keep it short and clear.
"""


def build_messages(question: str, results: list[dict]) -> list[dict]:
    """Build the messages for the LLM: the rules, the found texts and the question.

    Example: 3 search results + "Which backend?" to [system message, user message]
    """
    # Each found text becomes a numbered block, like "[1] (README.md · part 1)\n..."
    blocks = []
    for number, result in enumerate(results, start=1):
        blocks.append(
            f"[{number}] ({result['title']} · part {result['position'] + 1})\n{result['content']}"
        )

    # The texts, then the question
    user_content = "\n\n".join(blocks) + f"\n\nQuestion: {question}"

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]
