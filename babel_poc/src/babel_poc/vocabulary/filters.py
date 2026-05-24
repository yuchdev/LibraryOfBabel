def filter_words(
    words: list[str],
    min_length: int = 1,
    max_length: int | None = None,
    allow_digits: bool = True,
) -> list[str]:
    """Filter vocabulary by length and character constraints."""
    result = []
    for w in words:
        if len(w) < min_length:
            continue
        if max_length is not None and len(w) > max_length:
            continue
        if not allow_digits and any(c.isdigit() for c in w):
            continue
        result.append(w)
    return result
