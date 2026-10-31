from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): pass

class Document(Base):
  __tablename__ = "documents"
  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] 
  content: Mapped[str]
