from sqlalchemy import select
from db import SessionLocal
from db_models import Document
import services

# Redo the chunks of every document 
# Use it after changing MAX_WORDS or the emebdding model, or for old documents
with SessionLocal() as db:
    documents = db.scalars(select(Document)).all()
    for document in documents:
        services.rebuild_chunks(db, document)
        print(f"Reindexed: {document.title}")
    db.commit()