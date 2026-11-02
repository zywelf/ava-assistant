# Baby Ultron Assistant

A full-stack document assistant: a REST API backend with a React frontend to
upload, store, search and manage documents. Built as a learning and portfolio
project, with an AI layer (semantic search / RAG) planned.

## Tech Stack

**Backend**

- Python + FastAPI
- SQLAlchemy ORM + PostgreSQL
- Pydantic (request/response validation)
- pypdf (PDF text extraction)
- Layered architecture (routes / services / data / models)

**Frontend**

- React + TypeScript
- Vite
- Tailwind CSS

## Features

- Full CRUD on documents (list, create, update, delete)
- Keyword search (case-insensitive)
- File upload with text extraction (`.txt`, `.md`, `.pdf`, `.csv`, `.log`)
- Upload validation: unsupported type (`415`) and no extractable text (`422`)
- Persistent storage in PostgreSQL
- Typed end-to-end (Pydantic on the backend, TypeScript on the frontend)

## Architecture

Separate backend and frontend communicating over HTTP (REST + JSON):

```
frontend (React SPA) → HTTP → backend (FastAPI) → PostgreSQL
```

The backend follows a layered structure:

```
main.py        → routes (HTTP layer, dependency injection of the DB session)
services.py    → business logic + data access (SQLAlchemy)
db.py          → engine, session factory, get_db dependency
db_models.py   → ORM models (database tables)
models.py      → Pydantic schemas (API input/output)
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL running locally, with a database created:
  ```sql
  CREATE DATABASE baby_ultron;
  ```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/` with your database URL:

```
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/baby_ultron
```

Then run the server:

```bash
uvicorn main:app --reload       # runs on http://localhost:8000
```

Interactive API docs are available at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev                     # runs on http://localhost:5173
```

Make sure the backend is running before starting the frontend.

## API Endpoints

| Method | Path                      | Description                          |
| ------ | ------------------------- | ------------------------------------ |
| GET    | `/documents`              | List all documents                   |
| GET    | `/documents/titles`       | List document titles                 |
| GET    | `/documents/search`       | Search documents by `keyword`        |
| POST   | `/documents`              | Create a document (JSON)             |
| POST   | `/documents/upload`       | Upload a file and extract its text   |
| PUT    | `/documents/{id}`         | Update a document                    |
| DELETE | `/documents/{id}`         | Delete a document                    |

## Roadmap

- [x] Edit and delete documents (PUT / DELETE)
- [x] Persistent database (PostgreSQL) instead of in-memory storage
- [x] File upload with text extraction
- [ ] AI layer: embeddings + semantic search (pgvector)
- [ ] RAG / LangGraph for document Q&A
- [ ] Dockerize the stack
- [ ] Deployment