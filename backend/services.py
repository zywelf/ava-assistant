from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from db_models import Document, Chunk
from models import DocumentCreate
from embeddings import embed
from chunking import chunk_text

# The real work of the app. These functions don't know anything about HTTP:
# they get data, use the database and give data back


def get_documents(db: Session):
    """Return all the documents."""
    return db.scalars(select(Document)).all()


def search_documents(db: Session, keyword: str):
    """Find the documents that contain a word (upper or lower case doesn't matter).

    Example: "auto" finds "Auto" and "AUTO", but not "macchina"
    """
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
                embedding=embed(text),  # The embedding of this chunk only
            )
        )


def create_document(db: Session, doc: DocumentCreate):
    """Save a new document and its chunks."""
    new_doc = Document(title=doc.title, content=doc.content)
    db.add(new_doc)
    db.flush()  # Send the document to the DB to get its id, without saving yet
    save_chunks(db, new_doc)
    db.commit()  # Save the document and its chunks together
    db.refresh(new_doc)
    return new_doc


def delete_document(db: Session, doc_id):
    """Delete a document. Its chunks are deleted by the database (cascade)."""
    doc = db.get(Document, doc_id)
    if doc:
        db.delete(doc)
        db.commit()


def update_document(db: Session, doc_id, doc: DocumentCreate):
    """Change the title and the content of a document, and redo its chunks."""
    existing = db.get(Document, doc_id)
    existing.title = doc.title
    existing.content = doc.content

    rebuild_chunks(db, existing)  # The old chunks belong to the old content
    db.commit()
    return existing


def semantic_search(db: Session, query: str, limit: int = 3):
    """Find the chunks closest in meaning to the query.

    Example: "backend tech" finds the README part about FastAPI and PostgreSQL
    """
    query_vector = embed(query)
    rows = db.execute(
        select(Chunk, Document.title)
        .join(Document, Chunk.document_id == Document.id)
        .order_by(  # Compare with the CHUNK, not the document
            Chunk.embedding.cosine_distance(query_vector)
        )
        .limit(limit)
    ).all()

    # Turn each row (chunk, title) into a result
    return [
        {
            "document_id": chunk.document_id,
            "title": title,
            "position": chunk.position,
            "content": chunk.content,
        }
        for chunk, title in rows
    ]


def rebuild_chunks(db: Session, document: Document):
    """Delete the chunks of a document and make them again from its content.

    Use it when the content changes, or to redo all the chunks (reindex)
    """
    # Delete the old chunks
    db.execute(delete(Chunk).where(Chunk.document_id == document.id))
    # Make the new chunks from the content
    save_chunks(db, document)