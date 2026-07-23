# Portfolio RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about my background using my resume as the knowledge base — built as a learning project to understand RAG systems end-to-end, not just as a wrapper around an LLM API.

## Status: In Progress

Ingestion and retrieval pipelines are complete and tested. LLM response generation is being finalized next, followed by the FastAPI backend and integration into my portfolio site (currently also in progress).

## What's Built So Far

### 1. Ingestion Pipeline (`ingestion/`)
- **PDF extraction** — extracts clean text from a resume PDF using `pdfplumber`, with fixes for word-gluing (`x_tolerance` tuning), unmapped bullet glyphs, and line-wrap hyphenation artifacts.
- **Section-aware chunking** — splits resume text into semantically complete chunks (one per job, one per project, one per skills category, etc.) instead of naive fixed-size text splitting. Produces 11 chunks: Experience, Projects (x3), Education, Skills (x5 categories), Extracurriculars.
- **Embedding + storage** — embeds each chunk locally via Ollama (`nomic-embed-text-v2-moe`, 768-dim) and stores them in PostgreSQL with the pgvector extension.

### 2. Retrieval (`app/services/retrieval_service.py`)
- **Vector search** — cosine similarity search using pgvector's `<=>` operator.
- **Keyword search** — PostgreSQL full-text search (`tsvector` / `tsquery`).
- **Hybrid search** — merges both result sets using Reciprocal Rank Fusion (RRF), so retrieval benefits from both semantic similarity and exact keyword matches, not just one or the other.

### 3. LLM Response Generation (`app/services/llm_service.py`) — in progress
- Builds a grounded prompt from retrieved chunks, with a system prompt that restricts answers to resume-related questions only and enforces citation-only responses (no invented experience).
- Currently wired to a local Ollama model (`llama3.2`), keeping the project fully local and free to run during development.

## Not Yet Built
- FastAPI backend (`/chat` endpoint)
- Frontend chat interface (portfolio site is still in progress)
- Evaluation set to measure retrieval quality

## Tech Stack
- **Backend (planned)**: FastAPI
- **Database**: PostgreSQL + pgvector (via Docker)
- **Embeddings**: `nomic-embed-text-v2-moe` via Ollama (local)
- **LLM**: `llama3.2` via Ollama (local)
- **PDF processing**: pdfplumber
- **ORM**: SQLAlchemy

## Project Structure
```
Resume_chatbot/
├── .env                          # local secrets/config (not committed)
├── config.py                     # loads env vars
├── app/
│   ├── db/
│   │   ├── models.py              # Document table (pgvector column)
│   │   ├── session.py             # DB session setup
│   │   └── create_tables.py       # one-time table creation script
│   └── services/
│       ├── embedding_service.py   # Ollama embedding calls
│       ├── retrieval_service.py   # vector + keyword + hybrid search
│       └── llm_service.py         # prompt building + LLM call
├── ingestion/
│   ├── ingest.py                  # PDF extraction
│   ├── chunking.py                # section-aware chunking
│   └── store_embeddings.py        # embed + insert into Postgres
└── requirements.txt
```

## Setup (local dev)
1. Run PostgreSQL via Docker with the pgvector extension enabled
2. Run Ollama locally with `nomic-embed-text-v2-moe` and `llama3.2` pulled
3. Configure `.env` with `DATABASE_URL`, `OLLAMA_URL`, `OLLAMA_CHAT_URL`, `EMBEDDING_MODEL`, `LLM_MODEL`
4. `python -m app.db.create_tables` — create the documents table
5. `python -m ingestion.store_embeddings` — extract, chunk, embed, and store resume content
6. `python -m app.services.retrieval_service` — test hybrid retrieval standalone