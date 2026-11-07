# Ava

A full-stack AI document assistant: upload, store and manage documents, then
find them **by meaning, not by exact words**. Built as a learning and portfolio
project, step by step, from a REST API to semantic search, with RAG and agents
on the roadmap.

> **Why "Ava"?** It's a palindrome: two mirrored halves around a single core —
> the same idea as the planned architecture, where two AI "minds" (a generator
> and a verifier) work around the same knowledge base.

## Tech Stack

**Backend**

- Python + FastAPI
- SQLAlchemy ORM + PostgreSQL
- pgvector (vector storage and similarity search inside PostgreSQL)
- sentence-transformers (local embedding model, no external API)
- Pydantic (request/response validation)
- pypdf (PDF text extraction)

**Frontend**

- React + TypeScript
- Vite
- Tailwind CSS

**Infrastructure**

- Docker Compose (PostgreSQL + pgvector)

## Features

- Full CRUD on documents (list, create, update, delete)
- File upload with text extraction (`.txt`, `.md`, `.pdf`, `.csv`, `.log`)
- Upload validation: unsupported type (`415`) and no extractable text (`422`)
- **Semantic search**: results ranked by meaning using vector embeddings and
  cosine distance (e.g. searching "car" finds a document about "automobili")
- **Cross-lingual search**: a multilingual embedding model places different
  languages on the same "map of meaning", so English queries find Italian
  documents and vice versa
- Keyword search (case-insensitive) kept alongside semantic search
- **Chunking**: long documents are split into ~80-word pieces (on sentence
  boundaries, with overlap), each with its own embedding, so search finds the
  exact passage instead of only the start of a document
- Search results show the matching passage and the document it comes from
- Chunks are rebuilt when a document is updated, and deleted with it (cascade)
- Typed end-to-end (Pydantic on the backend, TypeScript on the frontend)

## How semantic search works

```
INDEXING TIME (document saved)                QUERY TIME (user searches)
  content → chunks (~80 words each)             query → embedding
  each chunk → embedding (384 numbers)          ORDER BY cosine distance → top 3 chunks
  stored in PostgreSQL (pgvector)               + title of the source document
```

1. When a document is created or updated, its content is split into **chunks**:
   pieces of about 80 words, cut on sentence boundaries, where each chunk starts
   with the last sentence of the previous one (overlap). The embedding model reads
   at most 128 tokens, so a whole long document would be cut after its first lines.
2. Each chunk is turned into an **embedding**: a list of 384 numbers representing
   its meaning (`paraphrase-multilingual-MiniLM-L12-v2`, running locally), stored
   in a `vector(384)` column thanks to pgvector.
3. A search turns the query into an embedding and returns the chunks whose
   vectors are closest by **cosine distance** (top-K, K = 3), together with the
   title of the document they come from.

Equivalent SQL:

```sql
SELECT chunks.*, documents.title
FROM chunks
JOIN documents ON chunks.document_id = documents.id
ORDER BY chunks.embedding <=> '[0.18, 0.19, ...]'   -- cosine distance
LIMIT 3;
```

Data model: one document has many chunks (`chunks.document_id` is a foreign key
with `ON DELETE CASCADE`, indexed).

## Architecture

Separate backend and frontend communicating over HTTP (REST + JSON):

```
frontend (React SPA) → HTTP → backend (FastAPI) → PostgreSQL + pgvector (Docker)
```

The backend follows a layered structure — each module has one responsibility:

```
main.py        → routes (HTTP only: request in, response out, errors → status codes)
services.py    → business logic + data access (SQLAlchemy)
embeddings.py  → text → vector (embedding model loaded once at startup)
chunking.py    → text → chunks (sentence split, overlap, cut of too-long sentences)
extraction.py  → file → text (format checks, PDF/text extraction, domain errors)
db.py          → engine, idempotent setup (pgvector extension + tables), get_db
db_models.py   → ORM models (documents, chunks)
reindex.py     → script: rebuild the chunks of every document
models.py      → Pydantic schemas (API input/output)
```

The frontend mirrors the same separation of concerns:

```
api.ts                 → HTTP calls to the backend
hooks/useDocuments.ts  → state + CRUD logic
components/            → presentation (form, upload, search, list, section layout)
App.tsx                → composition
```

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Python 3.11+
- Node.js 18+

### 1. Database (Docker)

From the project root:

```bash
docker compose up -d       # PostgreSQL 18 + pgvector on localhost:5434
docker compose ps          # should show the db service as "Up"
```

The database, the `vector` extension and the tables are created automatically:
no manual SQL needed. Data persists in a Docker volume across restarts.

### 2. Backend

From the project root:

```bash
python -m venv venv
source venv/Scripts/activate    # Windows (Git Bash) — macOS/Linux: source venv/bin/activate
pip install -r backend/requirements.txt
```

Create a `.env` file in `backend/`:

```
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5434/ava_assistant
```

Then run the server:

```bash
cd backend
uvicorn main:app --reload       # runs on http://localhost:8000
```

> The first start downloads the embedding model (~470 MB). Later starts use the
> local copy.

Interactive API docs are available at `http://localhost:8000/docs`.

To rebuild the chunks of all documents (e.g. after changing the chunk size or the
embedding model, or for documents created before chunking existed):

```bash
cd backend
python reindex.py
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev                     # runs on http://localhost:5173
```

### Startup order

1. Docker Desktop running
2. `docker compose up -d`
3. Backend (`uvicorn`, with the venv active)
4. Frontend (`npm run dev`)

## API Endpoints

| Method | Path                         | Description                                      |
| ------ | ---------------------------- | ------------------------------------------------ |
| GET    | `/documents`                 | List all documents                               |
| GET    | `/documents/titles`          | List document titles                             |
| GET    | `/documents/search`          | Keyword search by `keyword` (case-insensitive)   |
| GET    | `/documents/semantic-search` | Semantic search by `query`: top 3 matching passages with their document |
| POST   | `/documents`                 | Create a document (JSON)                         |
| POST   | `/documents/upload`          | Upload a file and extract its text               |
| PUT    | `/documents/{id}`            | Update a document (embedding is recomputed)      |
| DELETE | `/documents/{id}`            | Delete a document                                |

## Roadmap

- [x] Full CRUD on documents
- [x] Persistent database (PostgreSQL)
- [x] File upload with text extraction
- [x] PostgreSQL + pgvector in Docker
- [x] Embeddings + semantic search (backend and UI)
- [x] Chunking: split long documents into searchable pieces
- [ ] RAG: ask questions in natural language, answers citing the documents (local LLM)
- [ ] Chat with conversation memory
- [ ] Agents: a generator and a verifier working together (LangGraph)
- [ ] Dockerize the full stack
- [ ] Deployment