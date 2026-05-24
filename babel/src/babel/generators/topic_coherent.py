import math
from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.rendering.page_renderer import render_tokens
from babel.utils.hashing import deterministic_index, deterministic_uint64

class TopicCoherentGenerator(LibraryGenerator):
    mode_id = "topic-coherent"
    display_name = "Topic-Coherent Library"

    def _get_book_vocab(self, seed: str) -> list[str]:
        # Pick a subset of words for this book seed.
        h = deterministic_uint64(seed, "topic_selection", 0)
        # Each book is restricted to ~1% of the vocabulary
        topic_size = max(100, len(self.words) // 100)
        start_idx = h % len(self.words)
        
        subset = []
        for i in range(topic_size):
            subset.append(self.words[(start_idx + i) % len(self.words)])
        return subset + self.punctuation

    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        """W * (T + P)^N"""
        topic_size = max(100, len(self.words) // 100)
        p = len(self.punctuation)
        n = pages * tokens_per_page
        w = len(self.words)
        
        return math.log10(w) + n * math.log10(topic_size + p)

    def generate_token(self, seed: str, position: int) -> str:
        vocab = self._get_book_vocab(seed)
        idx = deterministic_index(seed, self.mode_id, position, len(vocab))
        return vocab[idx]

    def generate_page(self, config: BookConfig, page_index: int) -> GeneratedPage:
        tokens_per_page = config.tokens_per_page
        page_start = page_index * tokens_per_page
        vocab = self._get_book_vocab(config.seed)
        
        tokens = [
            vocab[deterministic_index(config.seed, self.mode_id, page_start + i, len(vocab))]
            for i in range(tokens_per_page)
        ]
        text = render_tokens(tokens, set(config.punctuation))
        return GeneratedPage(
            book_config=config,
            page_index=page_index,
            tokens=tokens,
            text=text,
        )
