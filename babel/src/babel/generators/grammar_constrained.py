import math
from typing import Optional

from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.rendering.page_renderer import render_tokens
from babel.utils.hashing import deterministic_index

BUILTIN_POS_VOCAB: dict[str, list[str]] = {
    "DET": ["the", "a", "an", "this", "that", "some", "every", "each"],
    "ADJ": ["dark", "old", "vast", "silent", "ancient", "strange", "bright", "deep"],
    "NOUN": ["river", "house", "mirror", "memory", "library", "book", "dream", "shadow"],
    "VERB": ["contains", "reflects", "holds", "reveals", "hides", "carries", "echoes", "fills"],
    "PUNCT": [".", "?", "!"],
}

DEFAULT_TEMPLATE = ["DET", "ADJ", "NOUN", "VERB", "DET", "NOUN", "PUNCT"]


class GrammarConstrainedGenerator(LibraryGenerator):
    mode_id = "grammar-constrained"
    display_name = "Grammar-Constrained Library"

    def __init__(
        self,
        words: list[str],
        punctuation: list[str],
        template: Optional[list[str]] = None,
        pos_vocab: dict[str, Optional[list[str]]] = None,
    ) -> None:
        super().__init__(words, punctuation)
        self.template = template or DEFAULT_TEMPLATE
        self.pos_vocab = pos_vocab or BUILTIN_POS_VOCAB

    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        """Product of category sizes per sentence position ^ number of repetitions."""
        total_tokens = pages * tokens_per_page
        template_len = len(self.template)
        n_repetitions = total_tokens // template_len
        log10 = 0.0
        for pos in self.template:
            size = len(self.pos_vocab.get(pos, []))
            if size <= 0:
                return float("-inf")
            log10 += math.log10(size)
        return n_repetitions * log10

    def generate_token(self, seed: str, position: int) -> str:
        template_len = len(self.template)
        pos_in_template = position % template_len
        pos_tag = self.template[pos_in_template]
        choices = self.pos_vocab.get(pos_tag, ["?"])
        idx = deterministic_index(seed, f"{self.mode_id}_{pos_tag}", position, len(choices))
        return choices[idx]

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
