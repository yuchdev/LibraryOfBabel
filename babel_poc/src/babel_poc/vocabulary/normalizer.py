import string

from babel_poc.progress.progress import progress_context


def normalize_word(word: str, lowercase: bool = True) -> str:
    """Normalize one vocabulary token."""
    w = word.strip()
    if lowercase:
        w = w.lower()
    return w


def normalize_words(
    words: list[str],
    lowercase: bool = True,
    reject_spaces: bool = True,
    reject_digits: bool = False,
    reject_punctuation: bool = False,
) -> list[str]:
    """Normalize, deduplicate, and sort vocabulary."""
    seen: set[str] = set()
    result: list[str] = []
    total = len(words)
    with progress_context("Normalizing vocabulary", total) as progress:
        for word in words:
            w = normalize_word(word, lowercase=lowercase)
            if not w:
                progress.advance(1)
                continue
            if reject_spaces and " " in w:
                progress.advance(1)
                continue
            if reject_digits and any(c.isdigit() for c in w):
                progress.advance(1)
                continue
            if reject_punctuation and any(c in string.punctuation for c in w):
                progress.advance(1)
                continue
            if w not in seen:
                seen.add(w)
                result.append(w)
            progress.advance(1)
    return sorted(result)
