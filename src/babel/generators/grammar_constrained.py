import math
from typing import Optional

from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.generators.constants import SHARED_PUNCTUATION, TOKEN_SLOTS_PER_BOOK
from babel.generators.metadata import ModelMetadata
from babel.rendering.page_renderer import render_tokens
from babel.utils.hashing import deterministic_index

BUILTIN_POS_VOCAB: dict[str, list[str]] = {
    "DET": ["the", "a", "an", "this", "that", "some", "every", "each"],
    "ADJ": ["dark", "old", "vast", "silent", "ancient", "strange", "bright", "deep"],
    "NOUN": ["river", "house", "mirror", "memory", "library", "book", "dream", "shadow"],
    "VERB": ["contains", "reflects", "holds", "reveals", "hides", "carries", "echoes", "fills"],
    "PUNCT": SHARED_PUNCTUATION,
}

DEFAULT_TEMPLATE = ["DET", "ADJ", "NOUN", "VERB", "DET", "NOUN", "PUNCT"]


class GrammarConstrainedGenerator(LibraryGenerator):
    """
    Stage 4 Categorical Grammar Constraint generator.

    Theoretical basis:
      - Stage 4 "Categorical Context-Free Grammar Constraint"
    Formula:
      - (D·A·N·V·D·N·P)^R using default template
      - R = floor(N / len(template))
    Data requirements:
      - optional POS files (WordNet style): nouns.txt, verbs.txt, adjectives.txt
      - deterministic built-in fallback POS lists
      - shared punctuation `. ? , !` for PUNCT category
    Implementation level:
      - lightweight (canonical template with local fallback vocab)
    Example:
      - uv run library-of-babel page --mode grammar-constrained --seed test --page 0
    Tests:
      - tests/generators/test_grammar_constrained.py
      - tests/vocabulary/test_vocab_loading.py
      - tests/test_determinism.py
    """

    mode_id = "grammar-constrained"
    metadata = ModelMetadata(
        mode_id=mode_id,
        stage_number=4,
        display_name="Stage 4: Categorical Grammar Constraint",
        article_model_name="Categorical Grammar Constraint",
        formula="(D·A·N·V·D·N·P)^R",
        implementation_level="lightweight",
        required_data=["wordnet nouns.txt/verbs.txt/adjectives.txt (optional)", "words.txt"],
        limitations=["Uses built-in fallback POS lists when POS vocab files are unavailable."],
    )

    def __init__(
        self,
        words: list[str],
        punctuation: list[str],
        template: Optional[list[str]] = None,
        pos_vocab: Optional[dict[str, list[str]]] = None,
    ) -> None:
        super().__init__(words, punctuation)
        self.template = template or DEFAULT_TEMPLATE
        if pos_vocab:
            merged = {**BUILTIN_POS_VOCAB, **pos_vocab}
            merged["PUNCT"] = list(SHARED_PUNCTUATION)
            self.pos_vocab = merged
        else:
            self.pos_vocab = {**BUILTIN_POS_VOCAB}

    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        """Product of category sizes per sentence position ^ number of repetitions."""
        template_len = len(self.template)
        n_repetitions = TOKEN_SLOTS_PER_BOOK // template_len
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
        choices = self.pos_vocab.get(pos_tag, [])
        if not choices:
            raise ValueError(f"grammar-constrained category {pos_tag} has no tokens")
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
