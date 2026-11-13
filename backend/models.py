from pydantic import BaseModel, Field

# The shape of the data that comes IN and goes OUT of the API.
# FastAPI checks the incoming data by itself (types + required fields)


class DocumentCreate(BaseModel):
    """What the client sends to create or change a document.

    The id is made by the server, so here there are only title and content
    """

    model_config = {
        "str_strip_whitespace": True
    }  # Remove the spaces at the start and the end, like " abc " to "abc"
    title: str = Field(min_length=1)  # At least 1 character
    content: str


class DocumentRead(BaseModel):
    """What the API sends back for a document."""

    id: int
    title: str
    content: str

    model_config = {"from_attributes": True}  # Can be built from a database object


class SearchResult(BaseModel):
    """One search result: the piece of text found, and the document it comes from.

    Example: title "README.md", position 2, content "Separate backend and...", distance 0.31
    """

    document_id: int
    title: str
    position: int
    content: str  # The text of the chunk, not the whole document
    distance: float   # 0 = same meaning, 1 = unrelated, 2 = opposite
