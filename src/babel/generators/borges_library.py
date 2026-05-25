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
    """Stage 0 normalized English character baseline with Borges geometry."""

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
