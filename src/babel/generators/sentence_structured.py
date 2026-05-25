import math
from typing import Optional

from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.generators.constants import (
    SENTENCE_BLOCK_SIZE,
    SENTENCE_BLOCKS_PER_BOOK,
    SHARED_PUNCTUATION,
    WORDS_PER_SENTENCE_BLOCK,
)
from babel.generators.metadata import ModelMetadata
from babel.rendering.page_renderer import render_tokens
from babel.utils.hashing import deterministic_index

WORDS_PER_SENTENCE = WORDS_PER_SENTENCE_BLOCK
SENTENCE_END_PUNCTUATION = SHARED_PUNCTUATION


class SentenceStructuredGenerator(LibraryGenerator):
    """Stage 3 fixed 16-slot sentence block: 15 words followed by one punctuation token."""

    mode_id = "sentence-structured"
    metadata = ModelMetadata(
        mode_id=mode_id,
        stage_number=3,
        display_name="Stage 3: Sentence-Structured Uniformity Constraint",
        article_model_name="Sentence-Structured Uniformity Constraint",
        formula="W^(15S) P^S, S=floor(N/16)",
        implementation_level="canonical",
        required_data=["words.txt"],
    )

    def __init__(
        self,
        words: list[str],
        punctuation: list[str],
        words_per_sentence: int = WORDS_PER_SENTENCE,
        sentence_end_punctuation: Optional[list[str]] = None,
    ) -> None:
        super().__init__(words, punctuation)
        self.words_per_sentence = words_per_sentence
        self.sentence_end_punctuation = (
            sentence_end_punctuation or list(SENTENCE_END_PUNCTUATION)
        )
        if self.sentence_end_punctuation != SHARED_PUNCTUATION:
            raise ValueError(
                f"sentence-structured requires shared punctuation {SHARED_PUNCTUATION}"
            )

    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        """W^(S * words_per_sentence) * P^S"""
        s = SENTENCE_BLOCKS_PER_BOOK
        w = len(self.words)
        p = len(self.sentence_end_punctuation)
        if w == 0 or p == 0:
            return float("-inf")
        return s * self.words_per_sentence * math.log10(w) + s * math.log10(p)

    def generate_token(self, seed: str, position: int) -> str:
        """
        Position within a sentence determines whether word or end punct.
        position is global token index (0-based across full book).
        """
        pos_in_sentence = position % SENTENCE_BLOCK_SIZE
        if pos_in_sentence == self.words_per_sentence:
            p = self.sentence_end_punctuation
            idx = deterministic_index(seed, f"{self.mode_id}_punct", position, len(p))
            return p[idx]
        idx = deterministic_index(seed, f"{self.mode_id}_word", position, len(self.words))
        return self.words[idx]

    def generate_page(self, config: BookConfig, page_index: int) -> GeneratedPage:
        tokens_per_page = config.tokens_per_page
        page_start = page_index * tokens_per_page
        tokens = [
            self.generate_token(config.seed, page_start + i)
            for i in range(tokens_per_page)
        ]
        punct_set = set(config.punctuation)
        text = render_tokens(tokens, punct_set)
        return GeneratedPage(
            book_config=config,
            page_index=page_index,
            tokens=tokens,
            text=text,
        )
