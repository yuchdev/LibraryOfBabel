import math
from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.rendering.page_renderer import render_tokens
from babel.utils.hashing import deterministic_index, deterministic_uint64

class SemanticConstrainedGenerator(LibraryGenerator):
    mode_id = "semantic-constrained"
    display_name = "Semantic-Constrained Library"

    def __init__(self, words: list[str], punctuation: list[str]) -> None:
        super().__init__(words, punctuation)
        self.num_clusters = 64
        self.clusters: list[list[str]] = [[] for _ in range(self.num_clusters)]
        for w in self.words:
            # Deterministically assign word to a cluster
            h = deterministic_uint64(w, "semantic_cluster_assignment", 0)
            self.clusters[h % self.num_clusters].append(w)
        
        # Ensure no empty clusters to avoid division by zero
        for i in range(self.num_clusters):
            if not self.clusters[i]:
                self.clusters[i] = [self.words[0]]

    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        """
        Approximate size: W * (W/K + P)^(N-1)
        where W is vocab size, K is num clusters, P is punctuation size, N is total tokens.
        """
        n = pages * tokens_per_page
        if n <= 0: return 0.0
        
        w = len(self.words)
        p = len(self.punctuation)
        avg_cluster_size = w / self.num_clusters
        
        log10_first = math.log10(w + p)
        log10_others = (n - 1) * math.log10(avg_cluster_size + p)
        return log10_first + log10_others

    def generate_token(self, seed: str, position: int) -> str:
        """Fallback for independent token generation (ignores semantic links)."""
        vocab = self.words + self.punctuation
        idx = deterministic_index(seed, self.mode_id, position, len(vocab))
        return vocab[idx]

    def _get_next_token(self, seed: str, position: int, prev_token: str) -> str:
        if position == 0 or not prev_token:
            vocab = self.words + self.punctuation
            idx = deterministic_index(seed, self.mode_id, position, len(vocab))
            return vocab[idx]
        
        # Hash prev_token to pick NEXT cluster
        h = deterministic_uint64(prev_token, "semantic_next_cluster", 0)
        # A word can be followed by words in (h % num_clusters) OR ((h+1) % num_clusters)
        # to allow some more variety and connectivity.
        c1 = h % self.num_clusters
        c2 = (h + 1) % self.num_clusters
        
        allowed_vocab = self.clusters[c1] + self.clusters[c2] + self.punctuation
        idx = deterministic_index(seed, self.mode_id, position, len(allowed_vocab))
        return allowed_vocab[idx]

    def generate_page(self, config: BookConfig, page_index: int) -> GeneratedPage:
        tokens_per_page = config.tokens_per_page
        page_start = page_index * tokens_per_page
        
        # To generate a page, we need the token just before it to maintain continuity.
        # This is expensive if we go from the very beginning of the book.
        # For simplicity in this application, we'll start each page independently (prev_token=None for start of page)
        # OR we can generate previous tokens within the page.
        
        tokens: list[str] = []
        prev_token = ""
        # If we wanted full book continuity, we'd need to generate all tokens from 0 to page_start.
        # Let's do it for the current page.
        for i in range(tokens_per_page):
            token = self._get_next_token(config.seed, page_start + i, prev_token)
            tokens.append(token)
            prev_token = token
            
        text = render_tokens(tokens, set(config.punctuation))
        return GeneratedPage(
            book_config=config,
            page_index=page_index,
            tokens=tokens,
            text=text,
        )
