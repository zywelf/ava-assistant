from sqlalchemy import select
from sqlalchemy.orm import Session
from db_models import Document
from models import DocumentCreate
from embeddings import embed


def get_documents(db: Session):
    return db.scalars(select(Document)).all()


def search_documents(db: Session, keyword: str):
    return db.scalars(
        select(Document).where(Document.content.ilike(f"%{keyword}%"))
    ).all()


def create_document(db: Session, doc: DocumentCreate):
    new_doc = Document(
        title=doc.title, content=doc.content, embedding=embed(doc.content)
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


def delete_document(db: Session, doc_id):
    doc = db.get(Document, doc_id)
    if doc:
        db.delete(doc)
        db.commit()


def update_document(db: Session, doc_id, doc: DocumentCreate):
    existing = db.get(Document, doc_id)
    existing.title = doc.title
    existing.content = doc.content
    existing.embedding = embed(doc.content)
    db.commit()
    return existing
