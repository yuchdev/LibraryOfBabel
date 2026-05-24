"""Tests for vocabulary discovery logic."""

from pathlib import Path

import pytest

from babel.vocabulary.discovery import (
    VocabularyNotFoundError,
    _setup_hint,
    find_default_vocabularies,
    resolve_vocabulary_path,
)

# ---------------------------------------------------------------------------
# find_default_vocabularies
# ---------------------------------------------------------------------------


def test_find_default_vocabularies_empty_dir(tmp_path: Path) -> None:
    assert find_default_vocabularies(tmp_path) == []


def test_find_default_vocabularies_missing_dir(tmp_path: Path) -> None:
    missing = tmp_path / "nonexistent"
    assert find_default_vocabularies(missing) == []


def test_find_default_vocabularies_finds_words_files(tmp_path: Path) -> None:
    source_dir = tmp_path / "scowl"
    source_dir.mkdir()
    words_file = source_dir / "words.txt"
    words_file.write_text("hello\nworld\n", encoding="utf-8")

    found = find_default_vocabularies(tmp_path)
    assert found == [words_file]


def test_find_default_vocabularies_ignores_empty_file(tmp_path: Path) -> None:
    source_dir = tmp_path / "empty_source"
    source_dir.mkdir()
    (source_dir / "words.txt").write_text("", encoding="utf-8")

    assert find_default_vocabularies(tmp_path) == []


def test_find_default_vocabularies_multiple_sources(tmp_path: Path) -> None:
    for name in ("aaa", "bbb", "ccc"):
        d = tmp_path / name
        d.mkdir()
        (d / "words.txt").write_text("word\n", encoding="utf-8")

    found = find_default_vocabularies(tmp_path)
    assert len(found) == 3
    assert all(p.name == "words.txt" for p in found)


def test_find_default_vocabularies_ignores_non_dirs(tmp_path: Path) -> None:
    (tmp_path / "readme.txt").write_text("not a source dir", encoding="utf-8")
    assert find_default_vocabularies(tmp_path) == []


# ---------------------------------------------------------------------------
# resolve_vocabulary_path — explicit path wins
# ---------------------------------------------------------------------------


def test_resolve_explicit_path_wins(tmp_path: Path) -> None:
    vocab = tmp_path / "custom.txt"
    vocab.write_text("word\n", encoding="utf-8")

    result = resolve_vocabulary_path(explicit_path=vocab)
    assert result == vocab


def test_resolve_explicit_path_missing_raises(tmp_path: Path) -> None:
    missing = tmp_path / "no_such.txt"
    with pytest.raises(VocabularyNotFoundError, match="not found"):
        resolve_vocabulary_path(explicit_path=missing)


# ---------------------------------------------------------------------------
# resolve_vocabulary_path — preferred source in default dir
# ---------------------------------------------------------------------------


def test_resolve_preferred_source(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import babel.vocabulary.discovery as disc

    monkeypatch.setattr(disc, "DEFAULT_VOCAB_DIR", tmp_path)
    source_dir = tmp_path / "myscowl"
    source_dir.mkdir()
    words_file = source_dir / "words.txt"
    words_file.write_text("word\n", encoding="utf-8")

    result = resolve_vocabulary_path(
        explicit_path=None,
        preferred_source="myscowl",
        auto_download=False,
    )
    assert result == words_file


def test_resolve_falls_back_to_any_vocab(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import babel.vocabulary.discovery as disc

    monkeypatch.setattr(disc, "DEFAULT_VOCAB_DIR", tmp_path)
    source_dir = tmp_path / "some_source"
    source_dir.mkdir()
    words_file = source_dir / "words.txt"
    words_file.write_text("word\n", encoding="utf-8")

    result = resolve_vocabulary_path(explicit_path=None)
    assert result == words_file


def test_resolve_preferred_source_patched(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import babel.vocabulary.discovery as disc

    monkeypatch.setattr(disc, "DEFAULT_VOCAB_DIR", tmp_path)
    source_dir = tmp_path / "scowl"
    source_dir.mkdir()
    words_file = source_dir / "words.txt"
    words_file.write_text("word\n", encoding="utf-8")

    result = resolve_vocabulary_path(
        explicit_path=None,
        preferred_source="scowl",
    )
    assert result == words_file


# ---------------------------------------------------------------------------
# resolve_vocabulary_path — missing vocabulary produces actionable error
# ---------------------------------------------------------------------------


def test_resolve_no_vocab_raises_actionable_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import babel.vocabulary.discovery as disc

    empty_dir = tmp_path / "empty_vocab"
    empty_dir.mkdir()
    monkeypatch.setattr(disc, "DEFAULT_VOCAB_DIR", empty_dir)

    with pytest.raises(VocabularyNotFoundError) as exc_info:
        resolve_vocabulary_path(explicit_path=None, auto_download=False)

    msg = str(exc_info.value)
    assert "setup-vocab" in msg
    assert "babel-poc" in msg


def test_setup_hint_contains_setup_command() -> None:
    hint = _setup_hint()
    assert "setup-vocab" in hint
    assert "--all" in hint
