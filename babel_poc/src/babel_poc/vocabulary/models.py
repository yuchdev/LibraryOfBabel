from pathlib import Path

from pydantic import BaseModel


class VocabularyInfo(BaseModel):
    vocabulary_id: str
    path: Path
    word_count: int
    punctuation_count: int
    normalized: bool
    lowercase: bool
