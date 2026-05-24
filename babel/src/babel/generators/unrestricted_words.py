import math

from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.rendering.page_renderer import render_tokens
from babel.utils.hashing import deterministic_index


class UnrestrictedWordsGenerator(LibraryGenerator):
    mode_id = "unrestricted-words"
    display_name = "Unrestricted Word-Token"

    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        """(W + P)^N"""
        total_vocab = len(self.words) + len(self.punctuation)
        n = pages * tokens_per_page
        return n * math.log10(total_vocab)

    def generate_token(self, seed: str, position: int) -> str:
        vocab = self.words + self.punctuation
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
