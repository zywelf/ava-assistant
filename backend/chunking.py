import re

# Max words in one chunk. The model reads max 128 tokens, about 80 words
MAX_WORDS = 80


def split_sentences(text: str) -> list[str]:
    """Split a text into sentences.

    Example: "Hi. How are you?" to ["Hi.", "How are you?"]
    """
    # Cut after . ! ? or where there is an empty line
    sentences = re.split(r"(?<=[.!?])\s+|\n\s*\n", text.strip())
    # Remove the empty ones
    return [s for s in sentences if s]


def split_long(sentence: str, max_words: int) -> list[str]:
    """If a sentence is too long, cut it in smaller parts of max_words.

    Example with max_words = 4: "a b c d e f" to ["a b c d", "e f"]
    A short sentence stays the same: "a b" to ["a b"]
    """
    words = sentence.split()
    # i is where each part starts: 0, 4, 8...
    return [
        " ".join(words[i:i + max_words])
        for i in range(0, len(words), max_words)
    ]


def chunk_text(text: str, max_words: int = MAX_WORDS) -> list[str]:
    """Split a text in chunks of max max_words.

    Each new chunk starts with the last sentence of the chunk before,
    so we don't lose the meaning between two chunks.
    """
    # First: text to sentences, and cut the sentences that are too long
    pieces = []
    for sentence in split_sentences(text):
        pieces.extend(split_long(sentence, max_words))

    chunks = []          # The finished chunks
    current = []         # The chunk we are filling now
    current_words = 0    # How many words are in the chunk we are filling

    for piece in pieces:
        words = len(piece.split())

        # The new sentence doesn't fit: save the chunk and start a new one
        if current and current_words + words > max_words:
            chunks.append(" ".join(current))
            last = current[-1]               # The last sentence of the saved chunk
            last_words = len(last.split())

            # Start the new chunk with the last sentence, only if it fits
            if last_words + words <= max_words:
                current = [last]
                current_words = last_words
            # Too big: start the new chunk empty
            else:
                current = []
                current_words = 0

        # Add the sentence to the chunk we are filling
        current.append(piece)
        current_words += words

    # Save the last chunk
    if current:
        chunks.append(" ".join(current))

    return chunks