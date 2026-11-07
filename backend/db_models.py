from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from pgvector.sqlalchemy import Vector

# The tables of the database, written as Python classes
# One class = one table, one attribute = one column


class Base(DeclarativeBase):
    """The parent of all the tables: create_all() creates every class that uses it."""

    pass


class Document(Base):
    """A document saved by the user.

    Example: title "README.md", content "# Ava A full-stack..."
    """

    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]


class Chunk(Base):
    """A piece of a document, with its own embedding.

    Example: a 10-page PDF becomes many chunks, each one about a paragraph long
    """

    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    # The document this chunk comes from. Delete the document → delete its chunks
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    position: Mapped[int]  # The chunk number in its document: 0, 1, 2...
    content: Mapped[str]
    embedding: Mapped[list[float]] = mapped_column(Vector(384))  # 384 numbers