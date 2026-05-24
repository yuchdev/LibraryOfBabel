"""Vocabulary installer — download, normalize, and register vocabulary sources."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from babel.config import DEFAULT_CACHE_DIR, DEFAULT_MANIFEST, DEFAULT_VOCAB_DIR
from babel.vocabulary.manifest import InstalledVocabulary, load_manifest, register_vocabulary
from babel.vocabulary.sources import KNOWN_VOCABULARY_SOURCES, VocabularySource


def install_source(
    source_id: str,
    force: bool = False,
    vocab_dir: Path = DEFAULT_VOCAB_DIR,
    cache_dir: Path = DEFAULT_CACHE_DIR,
    manifest_path: Path = DEFAULT_MANIFEST,
) -> InstalledVocabulary:
    """
    Download, normalize, and register a single vocabulary source.

    Skips the download if the source is already installed and *force* is False.
    Returns the :class:`~babel.vocabulary.manifest.InstalledVocabulary`
    entry for the installed vocabulary.
    """
    if source_id not in KNOWN_VOCABULARY_SOURCES:
        known = ", ".join(KNOWN_VOCABULARY_SOURCES)
        raise ValueError(f"Unknown source {source_id!r}. Known sources: {known}")

    source = KNOWN_VOCABULARY_SOURCES[source_id]

    # Skip if already installed
    if not force:
        manifest = load_manifest(manifest_path)
        existing = next((v for v in manifest.installed if v.vocabulary_id == source_id), None)
        if existing and Path(existing.path).exists():
            return existing

    if source.download_url is None:
        raise NotImplementedError(
            f"Source {source_id!r} ({source.display_name}) does not have an automatic "
            f"download URL. Please install it manually. See: {source.homepage_url}"
        )

    return _install_from_url(source, vocab_dir, cache_dir, manifest_path)


def install_all_sources(
    force: bool = False,
    vocab_dir: Path = DEFAULT_VOCAB_DIR,
    cache_dir: Path = DEFAULT_CACHE_DIR,
    manifest_path: Path = DEFAULT_MANIFEST,
) -> list[InstalledVocabulary]:
    """Install all known vocabulary sources that have a download URL."""
    results: list[InstalledVocabulary] = []
    for source_id in KNOWN_VOCABULARY_SOURCES:
        source = KNOWN_VOCABULARY_SOURCES[source_id]
        if source.download_url is None:
            continue
        entry = install_source(
            source_id,
            force=force,
            vocab_dir=vocab_dir,
            cache_dir=cache_dir,
            manifest_path=manifest_path,
        )
        results.append(entry)
    return results


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _install_from_url(
    source: VocabularySource,
    vocab_dir: Path,
    cache_dir: Path,
    manifest_path: Path,
) -> InstalledVocabulary:
    from babel.vocabulary.downloader import download_file

    assert source.download_url is not None  # guarded by caller

    # Prepare directories
    source_vocab_dir = vocab_dir / source.local_subdir
    source_vocab_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Download to cache
    url = source.download_url
    filename = url.split("/")[-1] or f"{source.source_id}_raw"
    cached_raw = cache_dir / filename
    download_file(url, cached_raw, show_progress=True)

    # Parse and normalize based on file format
    words = _extract_words(cached_raw, source)

    # Write normalized words.txt
    words_file = source_vocab_dir / "words.txt"
    words_file.write_text("\n".join(sorted(set(words))) + "\n", encoding="utf-8")

    # Write metadata.json
    sha256 = _sha256(words_file)
    metadata = {
        "source_id": source.source_id,
        "display_name": source.display_name,
        "homepage_url": source.homepage_url,
        "download_url": source.download_url,
        "license_name": source.license_name,
        "word_count": len(words),
        "installed_at": datetime.now(UTC).isoformat(),
        "sha256": sha256,
    }
    (source_vocab_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    installed_at_str = str(metadata["installed_at"])
    entry = InstalledVocabulary(
        source_id=source.source_id,
        vocabulary_id=source.source_id,
        path=words_file,
        word_count=len(words),
        installed_at=installed_at_str,
        source_url=source.download_url,
        license_name=source.license_name,
        sha256=sha256,
    )
    register_vocabulary(entry, manifest_path)
    return entry


def _extract_words(raw_file: Path, source: VocabularySource) -> list[str]:
    """Parse the raw downloaded file and return a list of words."""
    suffix = raw_file.suffix.lower()

    if suffix == ".json":
        return _extract_words_from_json(raw_file)
    if suffix in {".txt", ".text", ""}:
        return _extract_words_from_txt(raw_file)
    if suffix == ".csv":
        return _extract_words_from_csv(raw_file)

    # Fallback: try JSON then plain text
    try:
        return _extract_words_from_json(raw_file)
    except (json.JSONDecodeError, KeyError, TypeError):
        return _extract_words_from_txt(raw_file)


def _extract_words_from_json(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    # Support dict {word: frequency, ...} or list of [word, freq] pairs or list of words
    if isinstance(data, dict):
        return [str(k) for k in data.keys() if k and not str(k).startswith("#")]
    if isinstance(data, list):
        words: list[str] = []
        for item in data:
            if isinstance(item, str):
                words.append(item)
            elif isinstance(item, (list, tuple)) and item:
                words.append(str(item[0]))
        return words
    return []


def _extract_words_from_txt(path: Path) -> list[str]:
    words: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        token = line.strip()
        if token and not token.startswith("#"):
            # Take only the first whitespace-delimited token
            parts = token.split()
            if parts:
                words.append(parts[0])
    return words


def _extract_words_from_csv(path: Path) -> list[str]:
    import csv

    words: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    reader = csv.reader(text.splitlines())
    header: list[str] | None = None
    word_col = 0
    for row in reader:
        if not row:
            continue
        if header is None:
            header = row
            # Try to find "Word" column
            for i, col in enumerate(header):
                if col.strip().lower() in {"word", "words"}:
                    word_col = i
                    break
            continue
        if len(row) > word_col:
            token = row[word_col].strip()
            if token:
                words.append(token)
    return words


_SHA256_CHUNK = 65_536


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(_SHA256_CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()
