# Ava

A full-stack AI document assistant: upload, store and manage documents, then
find them **by meaning, not by exact words**, and **ask questions** answered only
from your documents, with sources. Built as a learning and portfolio project, step
by step, from a REST API to semantic search and RAG with a local LLM, with agents
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
- Ollama + `gemma3:4b` (local LLM, no external API) via httpx

**Frontend**

- React + TypeScript
- Vite
- Tailwind CSS

**Infrastructure**

- Docker Compose (PostgreSQL + pgvector)
- Ollama (runs the LLM locally, on the GPU when available)

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
- Search results show the matching passage, the document it comes from and its
  distance; passages too far from the query are discarded (distance threshold)
- **Ask your documents (RAG)**: questions in natural language, answered by a local
  LLM using **only** the passages found, with numbered citations (`[1]`)
- **Only the cited sources** are shown below the answer, with the same number
  used in the text; citations are clickable and open the full passage
- When nothing relevant is found, Ava says so without calling the LLM (no
  made-up answers); the LLM runs at temperature 0, so the same question gives
  the same answer
- **Duplicate detection**: every document has a SHA-256 fingerprint of its
  content, so the same file is rejected (`409`) even if it has another name
- Clear errors instead of crashes: `404` for a missing document, `409` for a
  duplicate, `503` when the database or the LLM is not reachable
- The server stays responsive during long uploads (heavy work runs outside the
  event loop) and shows the upload progress in the UI
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
   vectors are closest by **cosine distance** (at most 3), together with the
   title of the document they come from. Chunks with a distance above
   `MAX_DISTANCE` (0.65, measured on real queries) are discarded, so an
   unrelated query returns nothing instead of the "least bad" chunks.

Equivalent SQL:

```sql
SELECT chunks.*, documents.title
FROM chunks
JOIN documents ON chunks.document_id = documents.id
WHERE chunks.embedding <=> '[0.18, 0.19, ...]' < 0.65   -- cosine distance
ORDER BY chunks.embedding <=> '[0.18, 0.19, ...]'
LIMIT 3;
```

Data model: one document has many chunks (`chunks.document_id` is a foreign key
with `ON DELETE CASCADE`, indexed).

## How RAG works (Ask your documents)

**RAG** = Retrieval-Augmented Generation: first find the right passages, then give
them to the LLM together with the question.

```
POST /ask {"question": "..."}
  → semantic search   → passages under the distance threshold   (Retrieval)
  → prompt builder    → numbered passages + the question         (Augmented)
  → local LLM         → answer with citations like [1]           (Generation)
  ← {"answer": "...", "sources": [...]}
```

The system prompt tells the model to answer **only** from the numbered passages,
to say it doesn't know when the answer is not there, to cite the passage number
after each piece of information, and to answer in the language of the question.

Two different models, two different jobs:

| Model                                                | Job                       | If you change it                                  |
| ---------------------------------------------------- | ------------------------- | ------------------------------------------------- |
| `paraphrase-multilingual-MiniLM-L12-v2` (embeddings) | text → vectors, distances | re-run `reindex.py` and re-measure `MAX_DISTANCE` |
| `gemma3:4b` (LLM, via Ollama)                        | writes the answer         | nothing else to change                            |

## Architecture

Separate backend and frontend communicating over HTTP (REST + JSON):

```
frontend (React SPA) → HTTP → backend (FastAPI) → PostgreSQL + pgvector (Docker)
                                               → Ollama (local LLM)
```

The backend follows a layered structure — each module has one responsibility:

```
main.py        → routes (HTTP only: request in, response out, errors → status codes)
services.py    → business logic + data access (SQLAlchemy)
embeddings.py  → text → vector (model loaded once, lazily, and warmed up at startup)
chunking.py    → text → chunks (sentence split, overlap, cut of too-long sentences)
extraction.py  → file → text (format checks, PDF/text extraction, domain errors)
db.py          → engine, init_db() (pgvector extension + tables, run in the app lifespan), get_db
db_models.py   → ORM models (documents, chunks)
reindex.py     → script: rebuild the chunks of every document
models.py      → Pydantic schemas (API input/output)
ask.py         → RAG pipeline: search → prompt → LLM (the only module that knows all three)
rag.py         → system prompt + numbered passages (no database, no HTTP)
llm.py         → talks to Ollama (the only file to change to use another LLM)
```

The frontend mirrors the same separation of concerns:

```
api.ts                 → HTTP calls to the backend
hooks/useDocuments.ts  → state + CRUD logic
components/            → presentation (ask, form, upload, search, list, section layout)
App.tsx                → composition
```

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.com/)
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

### 2. LLM (Ollama)

```bash
ollama pull gemma3:4b      # download the model once (a few GB)
ollama ps                  # after the first question: shows the model and GPU/CPU use
```

The Ollama server runs in the background on `http://localhost:11434` (no need to
keep `ollama run` open).

### 3. Backend

From the project root:

```bash
python -m venv venv
source venv/Scripts/activate    # Windows (Git Bash) — macOS/Linux: source venv/bin/activate
pip install -r backend/requirements.txt
```

Create a `.env` file in `backend/`:

```
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5434/ava_assistant
# Optional, these are the defaults:
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:4b
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

### 4. Frontend

```bash
cd frontend
npm install
npm run dev                     # runs on http://localhost:5173
```

### Startup order

1. Docker Desktop running
2. `docker compose up -d`
3. Ollama running (for the "Ask your documents" section)
4. Backend (`uvicorn`, with the venv active)
5. Frontend (`npm run dev`)

## API Endpoints

| Method | Path                         | Description                                                                                                 |
| ------ | ---------------------------- | ----------------------------------------------------------------------------------------------------------- |
| GET    | `/documents`                 | List all documents                                                                                          |
| GET    | `/documents/titles`          | List document titles                                                                                        |
| GET    | `/documents/search`          | Keyword search by `keyword` (case-insensitive)                                                              |
| GET    | `/documents/semantic-search` | Semantic search by `query`: up to 3 passages under the distance threshold, with their document and distance |
| POST   | `/documents`                 | Create a document (JSON)                                                                                    |
| POST   | `/documents/upload`          | Upload a file and extract its text                                                                          |
| GET    | `/documents/{id}`            | Read one document                                                                                           |
| PUT    | `/documents/{id}`            | Update a document (chunks are rebuilt)                                                                      |
| DELETE | `/documents/{id}`            | Delete a document (its chunks too)                                                                          |
| POST   | `/ask`                       | Ask a question (`{"question": "..."}`): answer from the documents + the cited sources                       |

**Errors**

| Status        | When                                                                     |
| ------------- | ------------------------------------------------------------------------ |
| `404`         | No document with this id (`GET`, `PUT`, `DELETE /documents/{id}`)        |
| `409`         | A document with the same content already exists (create, upload, update) |
| `415` / `422` | Unsupported file type / file with no extractable text (upload)           |
| `503`         | The database or the LLM (Ollama) is not reachable                        |

## Roadmap

- [x] Full CRUD on documents
- [x] Persistent database (PostgreSQL)
- [x] File upload with text extraction
- [x] PostgreSQL + pgvector in Docker
- [x] Embeddings + semantic search (backend and UI)
- [x] Chunking: split long documents into searchable pieces
- [x] RAG: ask questions in natural language, answers citing the documents (local LLM)
- [ ] Chat with conversation memory
- [ ] Agents: a generator and a verifier working together (LangGraph)
- [ ] Dockerize the full stack
- [ ] Deployment
