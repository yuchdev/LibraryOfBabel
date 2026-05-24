from pathlib import Path

from pydantic import BaseModel

from babel_poc.constants import DEFAULT_PUNCTUATION


class AppConfig(BaseModel):
    vocabulary_path: Path = Path("data/vocabulary/english.txt")
    pages: int = 410
    tokens_per_page: int = 320
    punctuation: list[str] = DEFAULT_PUNCTUATION
