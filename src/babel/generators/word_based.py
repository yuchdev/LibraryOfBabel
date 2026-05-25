import math

from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.generators.constants import SHARED_PUNCTUATION, TOKEN_SLOTS_PER_BOOK
from babel.generators.metadata import ModelMetadata
from babel.rendering.page_renderer import render_tokens
from babel.utils.hashing import deterministic_index


class WordBasedGenerator(LibraryGenerator):
    """
    Stage 1 Lexical Reduction Model from the article chain.

    Theoretical basis:
      - Stage 1 "Lexical Reduction Model"
    Formula:
      - (W + P)^N, with N = TOKEN_SLOTS_PER_BOOK and P = 4 shared punctuation tokens
    Data requirements:
      - words.txt vocabulary
      - shared punctuation `. ? , !`
    Implementation level:
      - canonical
    Example:
      - uv run library-of-babel metrics --mode word-based
    Tests:
      - tests/test_word_based.py
      - tests/test_determinism.py
    """

    mode_id = "word-based"
    metadata = ModelMetadata(
        mode_id=mode_id,
        stage_number=1,
        display_name="Stage 1: Lexical Reduction Model",
        article_model_name="Lexical Reduction Model",
        formula="(W + P)^N",
        implementation_level="canonical",
        required_data=["words.txt"],
    )

    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        """(W + P)^N"""
        if not self.words:
            return float("-inf")
        total_vocab = len(self.words) + len(SHARED_PUNCTUATION)
        return TOKEN_SLOTS_PER_BOOK * math.log10(total_vocab)

    def generate_token(self, seed: str, position: int) -> str:
        if not self.words:
            raise ValueError("word-based requires non-empty words vocabulary")
        vocab = self.words + SHARED_PUNCTUATION
        idx = deterministic_index(seed, self.mode_id, position, len(vocab))
        return vocab[idx]

    def generate_page(self, config: BookConfig, page_index: int) -> GeneratedPage:
        tokens_per_page = config.tokens_per_page
        page_start = page_index * tokens_per_page
        tokens = [
            self.generate_token(config.seed, page_start + i)
            for i in range(tokens_per_page)
        ]
        text = render_tokens(tokens, set(config.punctuation))
        return GeneratedPage(
            book_config=config,
            page_index=page_index,
            tokens=tokens,
            text=text,
        )
