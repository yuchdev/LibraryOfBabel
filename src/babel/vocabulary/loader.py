from pathlib import Path

from babel.progress.progress import progress_context


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


def load_pos_vocab(base_dir: Path) -> dict[str, list[str]]:
    """
    Load optional POS vocab files from a vocabulary directory.

    Expected files:
    - nouns.txt
    - verbs.txt
    - adjectives.txt
    - adverbs.txt
    """
    mapping = {
        "NOUN": "nouns.txt",
        "VERB": "verbs.txt",
        "ADJ": "adjectives.txt",
        "ADV": "adverbs.txt",
    }
    pos_vocab: dict[str, list[str]] = {}
    for tag, filename in mapping.items():
        file_path = base_dir / filename
        if file_path.exists() and file_path.stat().st_size > 0:
            pos_vocab[tag] = load_words(file_path)
    return pos_vocab
