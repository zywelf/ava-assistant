from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def embed(text: str) -> list[float]:
    vector = model.encode(text)
    return vector.tolist()