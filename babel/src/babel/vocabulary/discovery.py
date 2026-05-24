"""Vocabulary discovery — locate usable vocabulary files locally."""

from __future__ import annotations

from pathlib import Path

from babel.config import DEFAULT_VOCAB_DIR


def find_default_vocabularies(base_dir: Path = DEFAULT_VOCAB_DIR) -> list[Path]:
    """
    Return all usable vocabulary ``words.txt`` files found under *base_dir*.

    Searches one level of sub-directories (one per source) for a ``words.txt``
    file and returns each one that is non-empty.
    """
    if not base_dir.exists():
        return []
    results: list[Path] = []
    for candidate in sorted(base_dir.iterdir()):
        if not candidate.is_dir():
            continue
        words_file = candidate / "words.txt"
        if words_file.exists() and words_file.stat().st_size > 0:
            results.append(words_file)
    return results


def resolve_vocabulary_path(
    explicit_path: Path | None,
    preferred_source: str | None = None,
    auto_download: bool = False,
) -> Path:
    """
    Resolve the vocabulary path to use, following this priority:

    1. *explicit_path* — if provided and exists, use it directly.
    2. *preferred_source* sub-directory inside the default vocab dir.
    3. Any usable vocabulary file found in the default vocab dir.
    4. If *auto_download* is True, trigger installation of the preferred (or
       first known) source and return its path.
    5. Raise a :class:`VocabularyNotFoundError` with actionable instructions.
    """
    # 1. Explicit path wins
    if explicit_path is not None:
        if not explicit_path.exists():
            raise VocabularyNotFoundError(
                f"Vocabulary file not found: {explicit_path}\n\n"
                + _setup_hint()
            )
        return explicit_path

    # 2. Preferred source in default dir
    if preferred_source is not None:
        preferred_path = DEFAULT_VOCAB_DIR / preferred_source / "words.txt"
        if preferred_path.exists() and preferred_path.stat().st_size > 0:
            return preferred_path

    # 3. Any usable vocabulary in default dir
    found = find_default_vocabularies(DEFAULT_VOCAB_DIR)
    if found:
        return found[0]

    # 4. Auto-download if requested
    if auto_download:
        from babel.vocabulary.installer import install_source
        from babel.vocabulary.sources import KNOWN_VOCABULARY_SOURCES

        source_id = preferred_source or next(iter(KNOWN_VOCABULARY_SOURCES))
        entry = install_source(source_id)
        return entry.path

    # 5. Actionable error
    raise VocabularyNotFoundError(_setup_hint())


def _setup_hint() -> str:
    return (
        "No vocabulary file found.\n\n"
        "Pass one explicitly:\n"
        "  babel-poc page --vocab /path/to/words.txt\n\n"
        "Or install default vocabularies:\n"
        "  babel-poc setup-vocab --source wordfreq_25k\n"
        "  babel-poc setup-vocab --all"
    )


class VocabularyNotFoundError(FileNotFoundError):
    """Raised when no vocabulary can be located."""
