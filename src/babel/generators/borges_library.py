import math

from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.generators.constants import (
    CHARS_PER_BOOK,
    ENGLISH_CHARACTER_ALPHABET,
    ENGLISH_CHARACTER_ALPHABET_SIZE,
)
from babel.generators.metadata import ModelMetadata
from babel.utils.hashing import deterministic_index


class BorgesLibraryGenerator(LibraryGenerator):
    """
    Stage 0 generator for the article's English-Language Borges Baseline.

    Theoretical basis:
      - docs/article/md.github/Semantic_Models_of_Library_of_Babel.github.md
      - Stage 0 "English-Language Borges Baseline"
    Formula:
      - 31^1,312,000
      - log10 size = CHARS_PER_BOOK * log10(31)
    Data requirements:
      - none (character-level model; vocabulary files are not used)
    Implementation level:
      - canonical
    Example:
      - uv run library-of-babel page --mode borges-library --seed test --page 0
    Tests:
      - tests/generators/test_borges_library.py
      - tests/test_determinism.py
    """

    mode_id = "borges-library"
    metadata = ModelMetadata(
        mode_id=mode_id,
        stage_number=0,
        display_name="Stage 0: English-Language Borges Baseline",
        article_model_name="English-Language Borges Baseline",
        formula="31^1,312,000",
        implementation_level="canonical",
        required_data=[],
        theoretical_basis="Character-level normalized English baseline for all later stages.",
    )

    def __init__(self, words: list[str], punctuation: list[str]) -> None:
        super().__init__(words, punctuation)
        self.alphabet = list(ENGLISH_CHARACTER_ALPHABET)

    def log10_size(self, pages: int = 410, tokens_per_page: int = 3200) -> float:
        """31^1,312,000."""
        return CHARS_PER_BOOK * math.log10(ENGLISH_CHARACTER_ALPHABET_SIZE)

    def generate_token(self, seed: str, position: int) -> str:
        idx = deterministic_index(seed, self.mode_id, position, len(self.alphabet))
        return self.alphabet[idx]

    def generate_page(self, config: BookConfig, page_index: int) -> GeneratedPage:
        # Default Borges page: 40 lines * 80 chars = 3200 chars
        chars_per_page = config.tokens_per_page
        page_start = page_index * chars_per_page
        tokens = [
            self.generate_token(config.seed, page_start + i)
            for i in range(chars_per_page)
        ]
        # Text is just joining characters for Borges.
        text = "".join(tokens)
        return GeneratedPage(
            book_config=config,
            page_index=page_index,
            tokens=tokens,
            text=text,
        )
