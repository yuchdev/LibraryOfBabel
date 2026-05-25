from __future__ import annotations

import math

from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.generators.constants import SHARED_PUNCTUATION, TOKEN_SLOTS_PER_BOOK
from babel.generators.metadata import ModelMetadata
from babel.rendering.page_renderer import render_tokens
from babel.utils.hashing import deterministic_index


class SemanticConstrainedGenerator(LibraryGenerator):
    """Stage 5 lightweight semantic adjacency graph with deterministic transitions."""

    mode_id = "semantic-constrained"
    NEIGHBOR_OFFSET_A = 7
    NEIGHBOR_HASH_MULTIPLIER = 31
    NEIGHBOR_HASH_OFFSET = 17
    metadata = ModelMetadata(
        mode_id=mode_id,
        stage_number=5,
        display_name="Stage 5: Markovian Semantic Adjacency Constraint",
        article_model_name="Markovian Semantic Adjacency Constraint",
        formula="≈ λ_max^N",
        implementation_level="lightweight",
        required_data=["words.txt"],
        limitations=[
            "Uses deterministic lightweight local graph edges, not full WordNet relations."
        ],
    )

    def __init__(self, words: list[str], punctuation: list[str]) -> None:
        if not words:
            raise ValueError("semantic-constrained requires non-empty words vocabulary")
        super().__init__(words, punctuation)
        self.nodes = self.words + SHARED_PUNCTUATION
        self.node_to_index = {token: i for i, token in enumerate(self.nodes)}
        self.adjacency = self._build_adjacency()
        self.lambda_max = self._estimate_lambda_max()

    def _build_adjacency(self) -> dict[str, list[str]]:
        adjacency: dict[str, list[str]] = {}
        w_len = len(self.words)

        for idx, token in enumerate(self.words):
            neighbors = {
                self.words[(idx + 1) % w_len],
                self.words[(idx + self.NEIGHBOR_OFFSET_A) % w_len],
                self.words[
                    (idx * self.NEIGHBOR_HASH_MULTIPLIER + self.NEIGHBOR_HASH_OFFSET) % w_len
                ],
                SHARED_PUNCTUATION[idx % len(SHARED_PUNCTUATION)],
            }
            adjacency[token] = sorted(neighbors)

        for idx, punct in enumerate(SHARED_PUNCTUATION):
            adjacency[punct] = [
                self.words[idx % w_len],
                self.words[(idx * 13 + 3) % w_len],
            ]

        return adjacency

    def _estimate_lambda_max(self, iterations: int = 20) -> float:
        size = len(self.nodes)
        vector = [1.0 / size] * size
        estimate = 1.0
        for _ in range(iterations):
            next_vector = [0.0] * size
            for src_idx, src in enumerate(self.nodes):
                for dst in self.adjacency[src]:
                    next_vector[self.node_to_index[dst]] += vector[src_idx]
            norm = sum(next_vector)
            if norm <= 0:
                return 1.0
            estimate = norm
            vector = [value / norm for value in next_vector]
        return estimate

    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        if self.lambda_max <= 0:
            return float("-inf")
        return TOKEN_SLOTS_PER_BOOK * math.log10(self.lambda_max)

    def generate_token(self, seed: str, position: int) -> str:
        if position == 0:
            idx = deterministic_index(seed, self.mode_id, 0, len(self.nodes))
            return self.nodes[idx]
        prev = self._token_at_position(seed, position - 1)
        choices = self.adjacency[prev]
        idx = deterministic_index(seed, self.mode_id, position, len(choices))
        return choices[idx]

    def _token_at_position(self, seed: str, position: int) -> str:
        token = ""
        for idx in range(position + 1):
            if idx == 0:
                token = self.nodes[deterministic_index(seed, self.mode_id, 0, len(self.nodes))]
            else:
                choices = self.adjacency[token]
                token = choices[deterministic_index(seed, self.mode_id, idx, len(choices))]
        return token

    def generate_page(self, config: BookConfig, page_index: int) -> GeneratedPage:
        tokens_per_page = config.tokens_per_page
        page_start = page_index * tokens_per_page

        prev = self._token_at_position(config.seed, page_start - 1) if page_start > 0 else ""
        tokens: list[str] = []
        for i in range(tokens_per_page):
            position = page_start + i
            if position == 0:
                token = self.nodes[
                    deterministic_index(config.seed, self.mode_id, 0, len(self.nodes))
                ]
            else:
                choices = self.adjacency[prev]
                token = choices[
                    deterministic_index(config.seed, self.mode_id, position, len(choices))
                ]
            tokens.append(token)
            prev = token

        text = render_tokens(tokens, set(SHARED_PUNCTUATION))
        return GeneratedPage(
            book_config=config,
            page_index=page_index,
            tokens=tokens,
            text=text,
        )
