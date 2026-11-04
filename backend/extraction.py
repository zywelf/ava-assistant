import io
import os
from pypdf import PdfReader

ALLOWED = {".txt", ".md", ".pdf", ".csv", ".log"}


class UnsupportedFormatError(Exception):
    pass


class EmptyTextError(Exception):
    pass


def extract_text(file_name: str, content: bytes) -> str:
    ext = os.path.splitext(file_name)[1].lower()
    if ext not in ALLOWED:
        raise UnsupportedFormatError(
            f"Format not supported: {ext}. Allowed: {', '.join(sorted(ALLOWED))}"
        )
    if ext == ".pdf":
        reader = PdfReader(io.BytesIO(content))
        text = "\n".join(page.extract_text() for page in reader.pages)
    else:
        text = content.decode("utf-8-sig")
    if not text.strip():
        raise EmptyTextError("Not extractable text found in the file.")
    return text
