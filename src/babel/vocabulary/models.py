from pathlib import Path

from pydantic import BaseModel


class VocabularyInfo(BaseModel):
    """
    Lightweight vocabulary stats model used by CLI reporting (`vocab-info`).

    Purpose:
      - summarize loaded vocabulary path and normalization state
    Inputs:
      - computed from a resolved local vocabulary file (`words.txt` style)
    Example:
      - emitted in `babel.cli.cmd_vocab_info`
    Failure modes:
      - upstream loading/normalization failures prevent this model from being created
    Stage relation:
      - used by all implemented stages that depend on local vocabulary files
    """

    vocabulary_id: str
    path: Path
    word_count: int
    punctuation_count: int
    normalized: bool
    lowercase: bool
