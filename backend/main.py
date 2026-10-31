from fastapi import FastAPI, Depends
from models import DocumentCreate, DocumentRead
from sqlalchemy.orm import Session
from db import get_db
import services
from fastapi.middleware.cors import CORSMiddleware

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


@app.delete("/documents/{doc_id}", status_code=204)
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    return services.delete_document(db, doc_id)


@app.put("/documents/{doc_id}", response_model=DocumentRead)
def update_document(doc_id: int, doc: DocumentCreate, db: Session = Depends(get_db)):
    return services.update_document(db, doc_id, doc)
