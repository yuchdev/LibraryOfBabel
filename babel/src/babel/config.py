from pathlib import Path

from pydantic import BaseModel

from babel.constants import DEFAULT_PUNCTUATION

# Default local data directory layout
DEFAULT_DATA_DIR = Path.home() / ".local" / "share" / "library-of-babel"
DEFAULT_VOCAB_DIR = DEFAULT_DATA_DIR / "vocabulary"
DEFAULT_CACHE_DIR = DEFAULT_DATA_DIR / "cache"
DEFAULT_MANIFEST = DEFAULT_DATA_DIR / "vocabulary_manifest.json"


class AppConfig(BaseModel):
    vocabulary_path: Path = Path("data/vocabulary/english.txt")
    pages: int = 410
    tokens_per_page: int = 320
    punctuation: list[str] = DEFAULT_PUNCTUATION
