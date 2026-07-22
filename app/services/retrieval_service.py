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

def keyword_search(db, query, top_k=5):
    rows = db.execute(
        text("""
            SELECT id, content, section, entry_name,
                   ts_rank(to_tsvector('english', content), plainto_tsquery('english', :q)) AS rank
            FROM documents
            WHERE to_tsvector('english', content) @@ plainto_tsquery('english', :q)
            ORDER BY rank DESC
            LIMIT :top_k
        """),
        {"q": query, "top_k": top_k}
    ).fetchall()

    return [dict(row._mapping) for row in rows]


def hybrid_search(db, query, top_k=5):
    vec_results = vector_search(db, query, top_k=10)
    kw_results = keyword_search(db, query, top_k=10)

    RRF_K = 60
    scores = {}
    chunks_by_id = {}

    for rank, row in enumerate(vec_results, start=1):
        scores[row["id"]] = scores.get(row["id"], 0) + 1 / (RRF_K + rank)
        chunks_by_id[row["id"]] = row

    for rank, row in enumerate(kw_results, start=1):
        scores[row["id"]] = scores.get(row["id"], 0) + 1 / (RRF_K + rank)
        chunks_by_id.setdefault(row["id"], row)

    ranked_ids = sorted(scores.keys(), key=lambda i: scores[i], reverse=True)
    return [chunks_by_id[i] for i in ranked_ids[:top_k]]

if __name__ == "__main__":
    from app.db.session import SessionLocal
    db = SessionLocal()
    results = hybrid_search(db, "does he know Python?")
    for r in results:
        print(r["section"], "|", r["entry_name"])
    db.close()