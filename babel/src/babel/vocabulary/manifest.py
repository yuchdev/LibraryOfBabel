"""Vocabulary manifest — tracks installed vocabulary datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from babel.config import DEFAULT_MANIFEST


class InstalledVocabulary(BaseModel):
    source_id: str
    vocabulary_id: str
    path: Path
    word_count: int
    installed_at: str
    source_url: str
    license_name: Optional[str]
    sha256: str


class VocabularyManifest(BaseModel):
    version: int = 1
    base_dir: Path
    installed: list[InstalledVocabulary] = []


def load_manifest(path: Path = DEFAULT_MANIFEST) -> VocabularyManifest:
    """Load manifest from disk, or return an empty manifest if missing."""
    if not path.exists():
        from babel.config import DEFAULT_VOCAB_DIR

        return VocabularyManifest(base_dir=DEFAULT_VOCAB_DIR)
    data = json.loads(path.read_text(encoding="utf-8"))
    return VocabularyManifest.model_validate(data)


def save_manifest(manifest: VocabularyManifest, path: Path = DEFAULT_MANIFEST) -> None:
    """Persist manifest to disk as JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        manifest.model_dump_json(indent=2),
        encoding="utf-8",
    )


def register_vocabulary(entry: InstalledVocabulary, path: Path = DEFAULT_MANIFEST) -> None:
    """Add or update a vocabulary entry in the manifest and save."""
    manifest = load_manifest(path)
    # Replace any existing entry with the same vocabulary_id
    manifest.installed = [v for v in manifest.installed if v.vocabulary_id != entry.vocabulary_id]
    manifest.installed.append(entry)
    save_manifest(manifest, path)
