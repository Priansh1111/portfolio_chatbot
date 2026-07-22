import httpx
from ingestion.ingest import extraction
from ingestion.chunking import chunk_resume

text = extraction()
chunks = chunk_resume(text)

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text-v2-moe"
EMBEDDING_DIM = 768

def _embed(text):
    response = httpx.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": text},
        timeout=30.0
    )
    response.raise_for_status()
    data = response.json()
    embedding = data["embedding"]

    if len(embedding) != EMBEDDING_DIM:
        raise ValueError(f"Expected {EMBEDDING_DIM}-dim embedding, got {len(embedding)}")

    return embedding


def embed_document(text):
    """Use this when embedding chunks going INTO storage (ingestion)."""
    return _embed(f"search_document: {text}")


def embed_query(text):
    """Use this when embedding a user's QUESTION at retrieval time."""
    return _embed(f"search_query: {text}")



if __name__ == "__main__":
    # vec = embed_document("AI/ML Intern at SynergyConnect Data Innovations")
    # print(len(vec))
    # print(vec[:5])
    for chunk in chunks:
        vec = embed_document(chunk["content"])
        print(chunk["entry_name"], "->", len(vec))