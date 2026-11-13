from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import DocumentCreate, DocumentRead, SearchResult
from db import get_db
from extraction import UnsupportedFormatError, EmptyTextError, extract_text
import services
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

# The routes of the API: they only handle HTTP (request in, response out).
# The real work is done in services.py

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow the frontend to call the backend
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, etc.
    allow_headers=["*"],
)


@app.exception_handler(OperationalError)
def database_unavailable(request, exc):
    """Answer with a clear error when the database can't be reached.

    Example: the database container is stopped -> 503 "Database not available"
    """
    return JSONResponse(
        status_code=503,
        content={"detail": "Database not available, try again in a moment"},
    )


@app.get("/")
def read_root():
    """Check that the server is running.

    Example: GET / returns {"status": "ok"}
    """
    return {"status": "ok"}


@app.get("/documents", response_model=list[DocumentRead])
def list_documents(db: Session = Depends(get_db)):
    """Return all the documents."""
    return services.get_documents(db)


@app.get("/documents/titles")
def list_title(db: Session = Depends(get_db)):
    """Return only the titles of the documents.

    Example: {"titles": ["README.md", "Notes.pdf"]}
    """
    return {"titles": [d.title for d in services.get_documents(db)]}


@app.get("/documents/search", response_model=list[DocumentRead])
def search_documents(keyword: str, db: Session = Depends(get_db)):
    """Find the documents that contain a word (upper or lower case doesn't matter).

    Example: /documents/search?keyword=auto
    """
    return services.search_documents(db, keyword)


@app.post("/documents", status_code=201, response_model=DocumentRead)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    """Create a document from a title and a content written by hand."""
    return services.create_document(db, doc)


@app.post("/documents/upload", response_model=DocumentRead)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a file, take its text and save it as a document.

    Wrong format gives 415, a file with no text (like a scanned PDF) gives 422
    """
    content = await file.read()  # Read the bytes of the file
    try:
        text = extract_text(file.filename, content)
    except UnsupportedFormatError as e:
        raise HTTPException(status_code=415, detail=str(e))
    except EmptyTextError as e:
        raise HTTPException(status_code=422, detail=str(e))
    doc = DocumentCreate(title=file.filename, content=text)
    return services.create_document(db, doc)


@app.delete("/documents/{doc_id}", status_code=204)
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """Delete a document (its chunks are deleted too)."""
    return services.delete_document(db, doc_id)


@app.put("/documents/{doc_id}", response_model=DocumentRead)
def update_document(doc_id: int, doc: DocumentCreate, db: Session = Depends(get_db)):
    """Change the title and the content of a document."""
    return services.update_document(db, doc_id, doc)


@app.get("/documents/semantic-search", response_model=list[SearchResult])
def semantic_search(query: str, db: Session = Depends(get_db)):
    """Find the 3 pieces of text closest in meaning to the query.

    Example: /documents/semantic-search?query=car also finds "automobili"
    """
    return services.semantic_search(db, query)
