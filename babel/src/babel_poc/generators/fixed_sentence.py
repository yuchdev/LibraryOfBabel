import math

from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.rendering.page_renderer import render_tokens
from babel.utils.hashing import deterministic_index

WORDS_PER_SENTENCE = 15
SENTENCE_END_PUNCTUATION = [".", "?", "!"]


class FixedSentenceGenerator(LibraryGenerator):
    mode_id = "fixed-sentence"
    display_name = "Fixed Sentence"

    def __init__(
        self,
        words: list[str],
        punctuation: list[str],
        words_per_sentence: int = WORDS_PER_SENTENCE,
        sentence_end_punctuation: list[str] | None = None,
    ) -> None:
        super().__init__(words, punctuation)
        self.words_per_sentence = words_per_sentence
        self.sentence_end_punctuation = (
            sentence_end_punctuation or SENTENCE_END_PUNCTUATION
        )

    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        """W^(S * words_per_sentence) * P^S"""
        total_tokens = pages * tokens_per_page
        sentence_len = self.words_per_sentence + 1
        s = total_tokens // sentence_len
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
        sentence_len = self.words_per_sentence + 1
        pos_in_sentence = position % sentence_len
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
