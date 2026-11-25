from sqlalchemy import select
from db import SessionLocal
from db_models import Document
from services import compute_hash

# Fill the fingerprint of the documents saved before content_hash existed.
# Run it once with: python backfill_hashes.py

with SessionLocal() as db:
    documents = db.scalars(select(Document)).all()
    for document in documents:
        document.content_hash = compute_hash(document.content)
        print(f"Hashed: {document.title}")
    db.commit()
