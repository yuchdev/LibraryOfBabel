"""Known vocabulary source registry."""
from typing import Optional

from pydantic import BaseModel, Field


class VocabularySource(BaseModel):
    """
    Registry record for a vocabulary source used by runtime/setup commands.

    Purpose:
      - declares source identity, expected files, optional download URL, and stage suitability
    Expected input files:
      - source-specific files listed in `expected_files` (for example `words.txt`,
        and for WordNet-style sources also POS files)
    Example:
      - `KNOWN_VOCABULARY_SOURCES["wordnet"]`
    Failure modes:
      - unknown source IDs are rejected by installer functions
      - sources without `download_url` cannot be auto-installed
    Stage relation:
      - Stage 1–3 lexical vocab sources
      - Stage 4 POS-aware grammar data
      - Stage 5 semantic-friendly source metadata
    """

    source_id: str
    display_name: str
    homepage_url: str
    download_url: Optional[str] = None
    license_name: Optional[str] = None
    local_subdir: str
    expected_files: list[str]
    notes: str
    suitable_stages: list[str] = Field(default_factory=list)


KNOWN_VOCABULARY_SOURCES: dict[str, VocabularySource] = {
    "scowl": VocabularySource(
        source_id="scowl",
        display_name="SCOWL / English Speller Database",
        homepage_url="https://github.com/en-wl/wordlist",
        download_url=None,
        license_name="MIT / SCOWL license (see homepage)",
        local_subdir="scowl",
        expected_files=["words.txt", "metadata.json"],
        notes=(
            "Large spelling-oriented English wordlist. "
            "Download requires building from source or using a pre-built export. "
            "See homepage for details."
        ),
        suitable_stages=["stage-1", "stage-2", "stage-3"],
    ),
    "wordnet": VocabularySource(
        source_id="wordnet",
        display_name="Open English WordNet",
        homepage_url="https://github.com/globalwordnet/english-wordnet",
        download_url=None,
        license_name="CC BY 4.0",
        local_subdir="wordnet",
        expected_files=[
            "words.txt", "nouns.txt", "verbs.txt", "adjectives.txt", "adverbs.txt", "metadata.json"
        ],
        notes=(
            "POS-aware semantic English wordnet. "
            "Best for POS-aware and semantic generation modes."
        ),
        suitable_stages=["stage-4", "stage-5"],
    ),
    "wordfreq_25k": VocabularySource(
        source_id="wordfreq_25k",
        display_name="wordfreq English Top 25 000",
        homepage_url="https://github.com/aparrish/wordfreq-en-25000",
        download_url=(
            "https://raw.githubusercontent.com/aparrish/wordfreq-en-25000/refs/heads/main/wordfreq-en-25000-log.json"
        ),
        license_name="CC BY 4.0 / wordfreq license",
        local_subdir="wordfreq",
        expected_files=["english_top_25000.json", "words.txt", "metadata.json"],
        notes=(
            "25 000 English words with frequency data exported from wordfreq. "
            "Best for frequency-weighted vocabulary."
        ),
        suitable_stages=["stage-1", "stage-2", "stage-3", "stage-6-demo"],
    ),
    "subtlex_us": VocabularySource(
        source_id="subtlex_us",
        display_name="SUBTLEX-US",
        homepage_url="https://osf.io/djpqz/overview",
        download_url=None,
        license_name="See SUBTLEX-US homepage (research use)",
        local_subdir="subtlex_us",
        expected_files=["words.txt", "frequencies.csv", "metadata.json"],
        notes=(
            "American English word frequencies from film subtitles. "
            "Best for common spoken-like English vocabulary."
        ),
        suitable_stages=["stage-1", "stage-2", "stage-3"],
    ),
}
