from functools import lru_cache
from sentence_transformers import SentenceTransformer


@lru_cache  # Remember the result: the model is loaded only once
def get_model():
    """Give the model that turns text into numbers, loading it the first time.

    Example: 1st call loads it (a few seconds), the next calls give the same one instantly
    """
    return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def embed(text: str) -> list[float]:
    """Turn a text into a list of 384 numbers that represent its meaning.

    Texts with a similar meaning get similar numbers, like "car" and "auto"
    """
    vector = get_model().encode(text)
    return vector.tolist()  # From a numpy array to a normal Python list
