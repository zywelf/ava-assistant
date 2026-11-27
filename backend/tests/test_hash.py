from services import compute_hash

def test_same_text_gives_same_hash():
    """The same text always gives the same fingerprint."""
    assert compute_hash("ciao") == compute_hash("ciao")


def test_different_text_gives_different_hash():
    """Even one capital letter changes the fingerprint."""
    assert compute_hash("ciao") != compute_hash("Ciao")

def test_hash_has_64_characters():
    """A SHA-256 fingerprint is always 64 characters long, for any text."""
    assert len(compute_hash("a whole book...")) == 64
