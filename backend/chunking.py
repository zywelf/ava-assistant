import re

# Max words per chunk: ~80 words fit inside the model's 128-token window
MAX_WORDS = 80


def split_sentences(text: str) -> list[str]:
    """Split a text into sentences (or paragraphs, when there is a blank line)."""
    # Cut on spaces after . ! ? OR on blank lines (end of a paragraph)
    sentences = re.split(r"(?<=[.!?])\s+|\n\s*\n", text.strip())
    # Drop empty strings
    return [s for s in sentences if s]


def split_long(sentence: str, max_words: int) -> list[str]:
    """Emergency knife: cut a sentence longer than max_words into smaller pieces."""
    words = sentence.split()
    # i = start of each piece (0, max_words, 2*max_words, ...)
    # each piece = the words from i to i + max_words
    # a short sentence comes back unchanged, as a one-item list
    return [
        " ".join(words[i:i + max_words])
        for i in range(0, len(words), max_words)
    ]


def chunk_text(text: str, max_words: int = MAX_WORDS) -> list[str]:
    """Split a text into chunks of up to max_words, cut on sentence boundaries,
    with a one-sentence overlap between consecutive chunks."""

    # 1. Text → sentences → pieces (long sentences are cut, short ones stay whole)
    pieces = []
    for sentence in split_sentences(text):
        pieces.extend(split_long(sentence, max_words))   # extend: add each piece, not the list

    # 2. Fill the "boxes" with pieces
    chunks = []          # closed boxes: the final chunks (strings)
    current = []         # the open box: pieces not yet joined
    current_words = 0    # how many words are in the open box

    for piece in pieces:
        words = len(piece.split())

        # The piece doesn't fit: close the box and open a new one
        if current and current_words + words > max_words:
            chunks.append(" ".join(current))     # close: join the pieces into one string
            last = current[-1]                   # overlap: keep the last piece...
            current = [last]                     # ...as the first one of the new box
            current_words = len(last.split())

        # Put the piece in the open box
        current.append(piece)
        current_words += words

    # Close the last box, if it isn't empty
    if current:
        chunks.append(" ".join(current))

    return chunks