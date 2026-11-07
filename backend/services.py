from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from db_models import Document
from models import DocumentCreate
from embeddings import embed
from db_models import Chunk
from chunking import chunk_text


def get_documents(db: Session):
    return db.scalars(select(Document)).all()


def search_documents(db: Session, keyword: str):
    return db.scalars(
        select(Document).where(Document.content.ilike(f"%{keyword}%"))
    ).all()


def save_chunks(db: Session, document: Document):
    """Split the document content in chunks and save them, each with its embedding.

    Example: a long text becomes chunks 0, 1, 2... all linked to this document
    """
    for position, text in enumerate(chunk_text(document.content)):
        db.add(
            Chunk(
                document_id=document.id,
                position=position,
                content=text,
                embedding=embed(text),
            )
        )


def create_document(db: Session, doc: DocumentCreate):
    new_doc = Document(
        title=doc.title, content=doc.content, embedding=embed(doc.content)
    )
    db.add(new_doc)
    db.flush()
    save_chunks(db, new_doc)
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

    rebuild_chunks(db, existing)
    db.commit()
    return existing


def semantic_search(db: Session, query: str, limit: int = 3):
    query_vector = embed(query)
    return db.scalars(
        select(Document)
        .order_by(Document.embedding.cosine_distance(query_vector))
        .limit(limit)
    ).all()


def rebuild_chunks(db: Session, document: Document):
    """Delete the chunks of a document and make them again from its content.

    Use it when the content changes, or to redo all the chunks(reindex)
    """

    # Delete the old chunks
    db.execute(delete(Chunk).where(Chunk.document_id == document.id))
    # Make the new chunks from the content
    save_chunks(db, document)
