import httpx
from config import OLLAMA_CHAT_URL, LLM_MODEL

SYSTEM_PROMPT = """You are a portfolio assistant that answers questions about Priansh Shetty \
based ONLY on the resume excerpts provided below.

Rules:
- Only use information present in the provided excerpts. Never invent or assume skills, \
experience, or facts not explicitly stated.
- If the excerpts don't contain the answer, say so plainly rather than guessing.
- Stay on topic: only answer questions about Priansh's background, skills, and experience. \
If asked something unrelated (general knowledge, other people, etc.), politely decline and \
redirect to what you can help with.
- Be concise and specific — cite concrete details (numbers, project names, tech stack) from \
the excerpts rather than vague summaries.
"""


def build_prompt(question, chunks):
    context = "\n\n".join(
        f"[{c['section']} | {c['entry_name']}]\n{c['content']}" for c in chunks
    )
    return f"""Resume excerpts:
{context}

Question: {question}"""


def generate_answer(question, chunks):
    if not chunks:
        return "I don't have information about that in Priansh's resume."

    prompt = build_prompt(question, chunks)

    response = httpx.post(
        OLLAMA_CHAT_URL,
        json={
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        },
        timeout=60.0
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]


if __name__ == "__main__":
    from app.services.retrieval_service import hybrid_search
    from app.db.session import SessionLocal

    db = SessionLocal()
    chunks = hybrid_search(db, "Should I hire him as a AI/ML Engineer?")
    answer = generate_answer("Should I hire him as a AI/ML Engineer?", chunks)
    print(answer)
    db.close()