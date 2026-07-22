from sqlalchemy import text
from app.services.embedding_service import embed_query

def vector_search(db, query, top_k=5):
    query_vector = embed_query(query)

    rows = db.execute(
        text("""
            SELECT id, content, section, entry_name,
                   embedding <=> CAST(:qvec AS vector) AS distance
            FROM documents
            ORDER BY distance ASC
            LIMIT :top_k
        """),
        {"qvec": str(query_vector), "top_k": top_k}
    ).fetchall()

    return [dict(row._mapping) for row in rows]

if __name__ == "__main__":
    from app.db.session import SessionLocal
    db = SessionLocal()
    results = vector_search(db, "what has he worked on in his internship?")
    for r in results:
        print(r["section"], "|", r["entry_name"], "| distance:", r["distance"])
    db.close()