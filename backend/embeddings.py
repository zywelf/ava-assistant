from sentence_transformers import SentenceTransformer

# The model that turns text into numbers. It's slow to load,
# so it's loaded once when the app starts and then reused
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def embed(text: str) -> list[float]:
    """Turn a text into a list of 384 numbers that represent its meaning.

    Texts with a similar meaning get similar numbers, like "car" and "auto"
    """
    vector = model.encode(text)
    return vector.tolist()  # From a numpy array to a normal Python list