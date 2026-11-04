from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector
class Base(DeclarativeBase): pass

class Document(Base):
  __tablename__ = "documents"
  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] 
  content: Mapped[str]
  embedding: Mapped[list[float]] = mapped_column(Vector(384))
