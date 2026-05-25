from __future__ import annotations

import math

from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.generators.constants import SHARED_PUNCTUATION, TOKEN_SLOTS_PER_BOOK
from babel.generators.metadata import ModelMetadata
from babel.rendering.page_renderer import render_tokens
from babel.utils.hashing import deterministic_index, deterministic_uint64

TOPIC_WORDSETS: dict[str, list[str]] = {
    "cosmology": ["galaxy", "cosmos", "orbit", "star", "planet", "void", "light", "eclipse"],
    "mathematics": ["proof", "axiom", "number", "infinity", "vector", "theorem", "logic", "set"],
    "grief": ["memory", "absence", "loss", "echo", "mourning", "silence", "tear", "night"],
    "theology": ["grace", "soul", "prayer", "altar", "faith", "mystery", "angel", "covenant"],
    "medieval_warfare": [
        "siege",
        "blade",
        "castle",
        "banner",
        "knight",
        "shield",
        "kingdom",
        "fortress",
    ],
}


class TopicCoherentGenerator(LibraryGenerator):
    """Stage 6 lightweight topic-constrained vocabulary model."""

    mode_id = "topic-coherent"
    metadata = ModelMetadata(
        mode_id=mode_id,
        stage_number=6,
        display_name="Stage 6: Topic-Coherent Manifold Approximation",
        article_model_name="Topic-Coherent Manifold / Topic-Constrained Vocabulary Model",
        formula="Σ_topic (|V_topic| + P)^N",
        implementation_level="lightweight",
        required_data=["words.txt"],
        limitations=["Uses explicit local topic wordsets rather than learned embedding manifolds."],
    )

    def _topic_vocabularies(self) -> dict[str, list[str]]:
        vocab: dict[str, list[str]] = {}
        for topic, fallback in TOPIC_WORDSETS.items():
            filtered = [word for word in self.words if word in set(fallback)]
            vocab[topic] = filtered if filtered else list(fallback)
        return vocab

    def _select_topic(self, seed: str) -> str:
        topics = sorted(self._topic_vocabularies().keys())
        idx = deterministic_uint64(seed, "topic_selection", 0) % len(topics)
        return topics[idx]

    def _get_book_vocab(self, seed: str) -> list[str]:
        topic = self._select_topic(seed)
        return self._topic_vocabularies()[topic] + SHARED_PUNCTUATION

    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        topic_vocab = self._topic_vocabularies()
        if not topic_vocab:
            return float("-inf")
        from babel.mathlib.logmath import log10_sum_exp

        log_terms = [
            TOKEN_SLOTS_PER_BOOK * math.log10(len(topic_words) + len(SHARED_PUNCTUATION))
            for topic_words in topic_vocab.values()
        ]
        return log10_sum_exp(log_terms)

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
        text = render_tokens(tokens, set(SHARED_PUNCTUATION))
        return GeneratedPage(
            book_config=config,
            page_index=page_index,
            tokens=tokens,
            text=text,
        )
