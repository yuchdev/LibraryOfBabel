from pathlib import Path

from babel.progress.progress import progress_context


def load_words(path: Path) -> list[str]:
    """
    Load a deterministic local word list from a text file.

    Purpose:
      - provide normalized lexical vocabulary for Stage 1–3 and fallback data in later stages
    Expected input:
      - UTF-8 text file, one token per line (`words.txt` style)
    Behavior:
      - ignores empty lines and `#` comment lines
      - strips whitespace, de-duplicates, returns sorted tokens
    Example:
      - `words = load_words(Path(".../words.txt"))`
    Failure modes:
      - `FileNotFoundError` / read errors from the underlying filesystem
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
    Load optional POS vocabulary files from a vocabulary source directory.

    Expected files:
    - nouns.txt
    - verbs.txt
    - adjectives.txt
    - adverbs.txt

    Purpose:
      - provide Stage 4 grammar categories from WordNet-style source packs
    Example:
      - `pos_vocab = load_pos_vocab(Path("~/.local/.../wordnet"))`
    Failure modes:
      - missing files are skipped (returns partial/empty POS mapping)
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
