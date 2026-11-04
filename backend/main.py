import io
import os
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pypdf import PdfReader
from models import DocumentCreate, DocumentRead
from db import get_db
import services

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],  # Allow the frontend to access to the backend
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, etc.
    allow_headers=["*"],
)

ALLOWED = {".txt", ".md", ".pdf", ".csv", ".log"}


# When a GET request hits the root path "/", FastAPI runs this function,
# which returns a dictionary {"status": "ok"} (auto-converted to JSON).
@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/documents", response_model=list[DocumentRead])
def list_documents(db: Session = Depends(get_db)):
    return services.get_documents(db)


@app.get("/documents/titles")
def list_title(db: Session = Depends(get_db)):
    return {"titles": [d.title for d in services.get_documents(db)]}


@app.get("/documents/search", response_model=list[DocumentRead])
def search_documents(keyword: str, db: Session = Depends(get_db)):
    return services.search_documents(db, keyword)


@app.post("/documents", status_code=201, response_model=DocumentRead)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    return services.create_document(db, doc)


@app.post("/documents/upload", response_model=DocumentRead)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()  # Read the BYTE of the file
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED:
        raise HTTPException(
            status_code=415,
            detail=f"Format not supported: {ext}. Allowed: {', '.join(sorted(ALLOWED))}",
        )
    if ext == ".pdf":
        reader = PdfReader(io.BytesIO(content))
        text = "\n".join(page.extract_text() for page in reader.pages)
    else:
        text = content.decode("utf-8-sig")
    if not text.strip():
        raise HTTPException(
            status_code=422, detail="Text not extractable from the pdf file"
        )
    doc = DocumentCreate(title=file.filename, content=text)
    return services.create_document(db, doc)


@app.delete("/documents/{doc_id}", status_code=204)
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    return services.delete_document(db, doc_id)


@app.put("/documents/{doc_id}", response_model=DocumentRead)
def update_document(doc_id: int, doc: DocumentCreate, db: Session = Depends(get_db)):
    return services.update_document(db, doc_id, doc)


@app.get("/documents/semantic-search", response_model=list[DocumentRead])
def semantic_search(query: str, db: Session = Depends(get_db)):
    return services.semantic_search(db, query)