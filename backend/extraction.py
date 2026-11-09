import io
import os
from pypdf import PdfReader

# The file types we can read
ALLOWED = {".txt", ".md", ".pdf", ".csv", ".log"}


class UnsupportedFormatError(Exception):
    """The file type is not in ALLOWED, like a .docx."""

    pass


class EmptyTextError(Exception):
    """The file has no text inside, like a PDF made only of images."""

    pass


def extract_text(file_name: str, content: bytes) -> str:
    """Take the text out of a file.

    Example: "notes.pdf" + its bytes to "the text written in the PDF"
    """
    ext = os.path.splitext(file_name)[1].lower()  # "Notes.PDF" to ".pdf"
    if ext not in ALLOWED:
        raise UnsupportedFormatError(
            f"Format not supported: {ext}. Allowed: {', '.join(sorted(ALLOWED))}"
        )
    if ext == ".pdf":
        reader = PdfReader(io.BytesIO(content))  # BytesIO: the bytes look like a file
        text = "\n".join(page.extract_text() for page in reader.pages)
    else:
        text = content.decode("utf-8-sig")  # Bytes to text ("-sig" removes the BOM)
    if not text.strip():
        raise EmptyTextError("No extractable text found in the file.")
    return text
