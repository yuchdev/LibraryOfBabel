"""Tests for vocabulary manifest read/write/register."""

from pathlib import Path

from babel.vocabulary.manifest import (
    InstalledVocabulary,
    VocabularyManifest,
    load_manifest,
    register_vocabulary,
    save_manifest,
)

DUMMY_ENTRY = InstalledVocabulary(
    source_id="test_source",
    vocabulary_id="test_source",
    path=Path("/tmp/test/words.txt"),
    word_count=100,
    installed_at="2024-01-01T00:00:00+00:00",
    source_url="https://example.com/words.json",
    license_name="MIT",
    sha256="abc123",
)


def test_load_manifest_missing_returns_empty(tmp_path: Path) -> None:
    manifest_path = tmp_path / "vocabulary_manifest.json"
    manifest = load_manifest(manifest_path)
    assert manifest.version == 1
    assert manifest.installed == []


def test_save_and_load_manifest_roundtrip(tmp_path: Path) -> None:
    manifest_path = tmp_path / "vocabulary_manifest.json"
    manifest = VocabularyManifest(base_dir=tmp_path / "vocabulary")
    manifest.installed.append(DUMMY_ENTRY)

    save_manifest(manifest, manifest_path)
    assert manifest_path.exists()

    loaded = load_manifest(manifest_path)
    assert loaded.version == 1
    assert len(loaded.installed) == 1
    assert loaded.installed[0].vocabulary_id == "test_source"
    assert loaded.installed[0].sha256 == "abc123"


def test_save_manifest_creates_parent_dirs(tmp_path: Path) -> None:
    manifest_path = tmp_path / "nested" / "deep" / "manifest.json"
    manifest = VocabularyManifest(base_dir=tmp_path)
    save_manifest(manifest, manifest_path)
    assert manifest_path.exists()


def test_register_vocabulary_adds_entry(tmp_path: Path) -> None:
    manifest_path = tmp_path / "vocabulary_manifest.json"
    register_vocabulary(DUMMY_ENTRY, manifest_path)

    loaded = load_manifest(manifest_path)
    assert len(loaded.installed) == 1
    assert loaded.installed[0].vocabulary_id == "test_source"


def test_register_vocabulary_no_duplicates(tmp_path: Path) -> None:
    manifest_path = tmp_path / "vocabulary_manifest.json"

    register_vocabulary(DUMMY_ENTRY, manifest_path)
    # Register again with updated word count
    updated = DUMMY_ENTRY.model_copy(update={"word_count": 200, "sha256": "def456"})
    register_vocabulary(updated, manifest_path)

    loaded = load_manifest(manifest_path)
    assert len(loaded.installed) == 1
    assert loaded.installed[0].word_count == 200
    assert loaded.installed[0].sha256 == "def456"


def test_register_multiple_distinct_vocabularies(tmp_path: Path) -> None:
    manifest_path = tmp_path / "vocabulary_manifest.json"

    entry_a = DUMMY_ENTRY.model_copy(update={"vocabulary_id": "source_a", "source_id": "source_a"})
    entry_b = DUMMY_ENTRY.model_copy(update={"vocabulary_id": "source_b", "source_id": "source_b"})

    register_vocabulary(entry_a, manifest_path)
    register_vocabulary(entry_b, manifest_path)

    loaded = load_manifest(manifest_path)
    assert len(loaded.installed) == 2
    ids = {v.vocabulary_id for v in loaded.installed}
    assert ids == {"source_a", "source_b"}


def test_manifest_stores_sha256(tmp_path: Path) -> None:
    manifest_path = tmp_path / "vocabulary_manifest.json"
    register_vocabulary(DUMMY_ENTRY, manifest_path)
    loaded = load_manifest(manifest_path)
    assert loaded.installed[0].sha256 == "abc123"
