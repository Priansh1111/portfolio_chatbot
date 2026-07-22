import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.db.session import SessionLocal
from app.db.models import Document
from app.services.embedding_service import embed_document
from ingestion.ingest import extraction
from ingestion.chunking import chunk_resume

text = extraction()
chunks = chunk_resume(text)

db = SessionLocal()

try:
    for chunk in chunks:
        vector = embed_document(chunk["content"])

        doc = Document(
            content=chunk["content"],
            section=chunk["section"],
            entry_name=chunk["entry_name"],
            embedding=vector,
        )
        db.add(doc)
        print(f"Prepared: {chunk['section']} | {chunk['entry_name']}")

    db.commit()
    print(f"\nDone. {len(chunks)} chunks stored in the documents table.")

except Exception as e:
    db.rollback()
    print(f"Something went wrong, rolled back: {e}")

finally:
    db.close()