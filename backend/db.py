import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db_models import Base

# Connection to the database and setup when the app starts

# Read DATABASE_URL from the .env file (the password stays out of the code)
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# The connection to the database, created once for the whole app
engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})

# Turn on pgvector. "IF NOT EXISTS": safe to run at every start
with engine.begin() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

# Create the tables that don't exist yet (it never changes the existing ones)
Base.metadata.create_all(engine)

# Makes a new session (one for each request)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """Give a database session to a route, and close it when the request is done.

    Used in the routes with: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()