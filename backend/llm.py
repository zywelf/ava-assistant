import os
import httpx

# Where Ollama runs and which model to use (can be changed in .env)
OLLAMA_URL= os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL= os.getenv("OLLAMA_MODEL", "gemma3:4b")


def chat(messages: list[dict]) -> str:
    """Send messages to the LLM and return its answer.

    Example: chat([{"role": "user", "content": "Hi!"}]) to "Hello! How can I help?"
    """
    res = httpx.post(
      f"{OLLAMA_URL}/api/chat",
      json={
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
      },
      timeout=60
    )
    res.raise_for_status()
    return res.json()["message"]["content"]
