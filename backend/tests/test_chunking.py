from chunking import split_sentences, split_long, chunk_text


def test_split_sentences_splits_on_punctuation():
    """ "Hi. How are you?" becomes two sentences."""
    result = split_sentences("Hi. How are you?")
    assert result == ["Hi.", "How are you?"]


def test_split_long_cuts_a_long_sentence():
    """With max 4 words, "a b c d e f" becomes two parts."""
    result = split_long("a b c d e f", 4)
    assert result == ["a b c d", "e f"]


def test_short_text_is_one_chunk():
    """A text shorter than max_words stays in one chunk."""
    chunks = chunk_text("Hello. How are you?", max_words=80)
    assert len(chunks) == 1


def test_no_chunk_is_longer_than_max_words():
    """Every chunk has at most max_words words."""
    text = "One two three. Four five six. Seven eight nine. Ten eleven twelve."
    chunks = chunk_text(text, max_words=5)
    for chunk in chunks:
        assert (
            len(chunk.split()) <= 5
        )  # count the words of the chunk, like in chunk_text
