import httpx
from config import OLLAMA_URL, EMBEDDING_MODEL

EMBEDDING_DIM = 768

def _embed(text):
    response = httpx.post(
        OLLAMA_URL,
        json={"model": EMBEDDING_MODEL, "prompt": text},
        timeout=30.0
    )
    response.raise_for_status()
    data = response.json()
    embedding = data["embedding"]

    if len(embedding) != EMBEDDING_DIM:
        raise ValueError(f"Expected {EMBEDDING_DIM}-dim embedding, got {len(embedding)}")

    return embedding


def embed_document(text):
    return _embed(f"search_document: {text}")


def embed_query(text):
    return _embed(f"search_query: {text}")