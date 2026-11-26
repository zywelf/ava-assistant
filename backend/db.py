import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config

# Read DATABASE_URL from the .env file (the password stays out of the code)
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# The connection to the database, created once for the whole app
engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})


# Makes a new session (one for each request)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Bring the database to the latest migration (like "alembic upgrade head").

    Example: on a new PC it creates all the tables, on mine it does nothing new
    """
    alembic_config = Config("alembic.ini")
    command.upgrade(alembic_config, "head")


def get_db():
    """Give a database session to a route, and close it when the request is done.

    Used in the routes with: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
