from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.generators.constants import SHARED_PUNCTUATION, TOKEN_SLOTS_PER_BOOK
from babel.generators.metadata import ModelMetadata
from babel.mathlib.combinatorics import log10_no_adjacent_punct
from babel.rendering.page_renderer import render_tokens
from babel.utils.hashing import deterministic_index


class PunctuationConstrainedGenerator(LibraryGenerator):
    """Stage 2 punctuation adjacency constraint using log-space combinatorics."""

    mode_id = "punctuation-constrained"
    metadata = ModelMetadata(
        mode_id=mode_id,
        stage_number=2,
        display_name="Stage 2: Syntactic Reduction Model (Punctuation Constraint)",
        article_model_name="Syntactic Reduction Model (Punctuation Constraint)",
        formula="Σ binom(N-k+1,k) P^k W^(N-k)",
        implementation_level="canonical",
        required_data=["words.txt"],
    )

    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        n = TOKEN_SLOTS_PER_BOOK
        w = len(self.words)
        p = len(SHARED_PUNCTUATION)
        return log10_no_adjacent_punct(n, w, p)

    def generate_token(self, seed: str, position: int) -> str:
        """Generate token ignoring adjacency — for raw use only."""
        if not self.words:
            raise ValueError("punctuation-constrained requires non-empty words vocabulary")
        vocab = self.words + SHARED_PUNCTUATION
        idx = deterministic_index(seed, self.mode_id, position, len(vocab))
        return vocab[idx]

    def _generate_token_constrained(
        self, seed: str, position: int, prev_is_punct: bool
    ) -> str:
        """Generate token respecting no-adjacent-punctuation rule."""
        punct_set = set(SHARED_PUNCTUATION)
        vocab = self.words + SHARED_PUNCTUATION
        candidate_idx = deterministic_index(seed, self.mode_id, position, len(vocab))
        candidate = vocab[candidate_idx]
        if prev_is_punct and candidate in punct_set:
            word_idx = deterministic_index(
                seed, f"{self.mode_id}_word", position, len(self.words)
            )
            return self.words[word_idx]
        return candidate

    def _prev_is_punctuation(self, seed: str, position: int, punct_set: set[str]) -> bool:
        if position <= 0:
            return False
        prev_is_punct = False
        for idx in range(position):
            token = self._generate_token_constrained(seed, idx, prev_is_punct)
            prev_is_punct = token in punct_set
        return prev_is_punct

    def generate_page(self, config: BookConfig, page_index: int) -> GeneratedPage:
        tokens_per_page = config.tokens_per_page
        page_start = page_index * tokens_per_page
        punct_set = set(config.punctuation)
        prev_is_punct = self._prev_is_punctuation(config.seed, page_start, punct_set)

        tokens: list[str] = []
        for i in range(tokens_per_page):
            token = self._generate_token_constrained(
                config.seed, page_start + i, prev_is_punct
            )
            tokens.append(token)
            prev_is_punct = token in punct_set

        text = render_tokens(tokens, punct_set)
        return GeneratedPage(
            book_config=config,
            page_index=page_index,
            tokens=tokens,
            text=text,
        )
