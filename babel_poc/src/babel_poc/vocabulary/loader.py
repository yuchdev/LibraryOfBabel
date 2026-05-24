from pathlib import Path

from babel_poc.progress.progress import progress_context


def load_words(path: Path) -> list[str]:
    """
    Load a local wordlist.
    - one token per line
    - ignore empty lines
    - ignore comment lines starting with '#'
    - strip whitespace
    - deduplicate
    - preserve deterministic sorted order
    """
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    seen: set[str] = set()
    words: list[str] = []
    total = len(raw_lines)
    with progress_context("Loading vocabulary", total) as progress:
        for line in raw_lines:
            token = line.strip()
            if not token or token.startswith("#"):
                progress.advance(1)
                continue
            if token not in seen:
                seen.add(token)
                words.append(token)
            progress.advance(1)
    return sorted(words)
