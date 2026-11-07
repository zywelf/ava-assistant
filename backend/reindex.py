from sqlalchemy import select
from db import SessionLocal
from db_models import Document
import services

# Redo the chunks of every document. Run it with: python reindex.py
# Use it after changing MAX_WORDS or the embedding model, or for old documents

with SessionLocal() as db:  # Outside FastAPI we make the session ourselves
    documents = db.scalars(select(Document)).all()
    for document in documents:
        services.rebuild_chunks(db, document)
        print(f"Reindexed: {document.title}")
    db.commit()  # Save everything at the end, all together